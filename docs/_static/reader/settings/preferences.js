import { themes, fonts } from "../themes/catalog.js";
import { defaults, normalize, groups } from "./schema.js";
import { loadPreferences, savePreferences } from "./storage.js";
import { decorateCode } from "../code_viewer/decorate.js";
export function createPreferences(onDisplayChange) {
  let value = normalize(loadPreferences());
  const listeners = new Set(),
    system = matchMedia("(prefers-color-scheme: dark)");
  function apply() {
    const root = document.documentElement;
    const id =
      value.theme === "system"
        ? system.matches
          ? "one_dark"
          : "one_light"
        : value.theme;
    root.dataset.theme = id;
    root.dataset.scheme = themes.find((t) => t.id === id)?.kind || "light";
    root.style.setProperty(
      "--editor-font",
      `"${fonts.find((f) => f.id === value.font).family}", monospace`,
    );
    for (const [key, css, unit] of [
      ["size", "size", "px"],
      ["weight", "weight", ""],
      ["lineHeight", "line-height", ""],
      ["letterSpacing", "letter-spacing", "px"],
    ])
      root.style.setProperty("--editor-" + css, value[key] + unit);
    for (const key of [
      "ligatures",
      "italic",
      "indents",
      "whitespace",
      "trailing",
      "numbers",
      "wrap",
      "syntax",
      "width",
    ])
      root.dataset["code" + key[0].toUpperCase() + key.slice(1)] = String(
        value[key],
      );
  }
  function update(patch) {
    const previous = value;
    value = normalize({ ...value, ...patch });
    apply();
    const saved = savePreferences(value);
    listeners.forEach((listener) => listener(value, saved));
    if (previous.diff !== value.diff) onDisplayChange();
  }
  system.addEventListener("change", () => {
    if (value.theme === "system") apply();
  });
  apply();
  return {
    get value() {
      return value;
    },
    update,
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    reset(group) {
      const keys = group ? groups[group] : Object.keys(defaults);
      update(Object.fromEntries(keys.map((key) => [key, defaults[key]])));
    },
    refresh() {
      decorateCode();
    },
  };
}
