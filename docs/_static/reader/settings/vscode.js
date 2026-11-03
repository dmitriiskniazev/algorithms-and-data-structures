import { themes, fonts } from "../themes/catalog.js";
import { normalize } from "./schema.js";

export function parseJSONC(text) {
  if (typeof text !== "string" || text.length > 1_000_000)
    throw new Error("Выберите файл настроек размером до 1 МБ.");
  let clean = "",
    quote = false,
    escaped = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i],
      next = text[i + 1];
    if (quote) {
      clean += c;
      if (escaped) escaped = false;
      else if (c === "\\") escaped = true;
      else if (c === '"') quote = false;
      continue;
    }
    if (c === '"') {
      quote = true;
      clean += c;
      continue;
    }
    if (c === "/" && next === "/") {
      while (i < text.length && text[i] !== "\n") i++;
      clean += "\n";
      continue;
    }
    if (c === "/" && next === "*") {
      i += 2;
      let closed = false;
      for (; i < text.length; i++) {
        if (text[i] === "*" && text[i + 1] === "/") {
          i++;
          closed = true;
          break;
        }
        if (text[i] === "\n") clean += "\n";
      }
      if (!closed) throw new Error("Незакрытый комментарий в JSONC.");
      clean += " ";
      continue;
    }
    clean += c;
  }
  let json = "";
  quote = false;
  escaped = false;
  for (let i = 0; i < clean.length; i++) {
    const c = clean[i];
    if (quote) {
      json += c;
      if (escaped) escaped = false;
      else if (c === "\\") escaped = true;
      else if (c === '"') quote = false;
      continue;
    }
    if (c === '"') quote = true;
    if (c === ",") {
      let next = i + 1;
      while (next < clean.length && /\s/.test(clean[next])) next++;
      if (clean[next] === "}" || clean[next] === "]") continue;
    }
    json += c;
  }
  const value = JSON.parse(json.replace(/^\uFEFF/, ""));
  if (!value || typeof value !== "object" || Array.isArray(value))
    throw new Error("Настройки должны быть JSON-объектом.");
  return value;
}
const compact = (text) => text.toLowerCase().replace(/[^a-z0-9]/g, "");
export function importVSCode(text, current) {
  const original = parseJSONC(text);
  const python = original["[python]"];
  const source = {
    ...original,
    ...(python && typeof python === "object" && !Array.isArray(python)
      ? python
      : {}),
  };
  const patch = {},
    rows = [],
    used = new Set();
  function accept(key, target, convert) {
    if (!Object.hasOwn(source, key)) return;
    used.add(key);
    const result = convert(source[key]);
    if (result === undefined) {
      rows.push({
        key,
        status: "skipped",
        message: "Неподдерживаемое значение",
      });
      return;
    }
    patch[target] = result;
    rows.push({ key, target, status: "applied", message: String(result) });
  }
  const number = (value) =>
    typeof value === "number" && Number.isFinite(value) ? value : undefined;
  const bool = (value) => (typeof value === "boolean" ? value : undefined);
  accept("workbench.colorTheme", "theme", (name) => {
    if (typeof name !== "string") return;
    const aliases = {
      onedarkpro: "one_dark",
      defaultdarkmodern: "github_dark",
      defaultlightmodern: "github_light",
      defaultdarkplus: "github_dark",
      defaultlightplus: "github_light",
    };
    return (
      themes.find((t) => compact(t.name) === compact(name))?.id ||
      (Object.hasOwn(aliases, compact(name))
        ? aliases[compact(name)]
        : undefined)
    );
  });
  accept("editor.fontFamily", "font", (name) => {
    if (typeof name !== "string") return;
    for (const part of name.split(",")) {
      const key = compact(part);
      const found = fonts.find((font) =>
        [font.name, font.family, ...(font.aliases || [])].some(
          (alias) => compact(alias) === key,
        ),
      );
      if (found) return found.id;
    }
  });
  accept("editor.fontSize", "size", number);
  accept("editor.fontWeight", "weight", (value) =>
    value === "normal"
      ? 400
      : value === "bold"
        ? 700
        : typeof value === "string" && /^\d+$/.test(value)
          ? Number(value)
          : number(value),
  );
  accept("editor.lineHeight", "lineHeight", (value) => {
    const n = number(value);
    if (n === undefined || n < 0) return;
    if (n === 0) return 1.5;
    return n < 8 ? n : n / normalize({ ...current, ...patch }).size;
  });
  accept("editor.letterSpacing", "letterSpacing", number);
  accept("editor.fontLigatures", "ligatures", bool);
  accept("editor.wordWrap", "wrap", (value) =>
    value === "off"
      ? false
      : ["on", "wordWrapColumn", "bounded"].includes(value)
        ? true
        : undefined,
  );
  accept("editor.lineNumbers", "numbers", (value) =>
    value === "off"
      ? false
      : ["on", "relative", "interval"].includes(value)
        ? true
        : undefined,
  );
  accept("editor.guides.indentation", "indents", (value) =>
    typeof value === "boolean" ? (value ? "plain" : "off") : undefined,
  );
  accept("editor.renderWhitespace", "whitespace", (value) =>
    typeof value === "string" &&
    ["none", "boundary", "all", "trailing"].includes(value)
      ? { none: "off", boundary: "boundary", all: "all", trailing: "off" }[
          value
        ]
      : undefined,
  );
  if (source["editor.renderWhitespace"] === "trailing") patch.trailing = true;
  if (source["window.autoDetectColorScheme"] === true) {
    patch.theme = "system";
    used.add("window.autoDetectColorScheme");
    rows.push({
      key: "window.autoDetectColorScheme",
      status: "applied",
      message: "По оформлению системы; подсветка синтаксиса включена",
    });
  }
  if (Object.hasOwn(patch, "theme")) patch.syntax = true;
  const normalized = normalize({ ...current, ...patch });
  for (const key of Object.keys(patch)) patch[key] = normalized[key];
  for (const row of rows.filter((row) => row.status === "applied")) {
    if (row.target) row.message = String(patch[row.target]);
    if (row.target === "font")
      row.message =
        fonts.find((f) => f.id === patch.font)?.name || String(patch.font);
    if (row.key === "editor.renderWhitespace" && source[row.key] === "trailing")
      row.message =
        "Обычные пробелы скрыты; выделение пробелов в конце строки включено";
    if (row.key === "workbench.colorTheme")
      row.message =
        (themes.find((t) => t.id === patch.theme)?.name || "По системе") +
        "; подсветка синтаксиса включена";
  }
  for (const key of Object.keys(source))
    if (!used.has(key) && !key.startsWith("["))
      rows.push({ key, status: "skipped", message: "Не используется в курсе" });
  return {
    patch,
    rows,
    python: Boolean(
      python && typeof python === "object" && !Array.isArray(python),
    ),
    count: Object.keys(patch).length,
  };
}
