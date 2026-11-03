import { $, escape } from "../dom.js";
import { themes, fonts } from "../themes/catalog.js";
import { defaults, groups } from "./schema.js";
import { importVSCode } from "./vscode.js";
import { decorateCode } from "../code_viewer/decorate.js";

const labels = {
  themes: "Темы",
  typography: "Типографика",
  code: "Код",
  reading: "Чтение и сравнение",
  import: "Импорт VS Code",
};
const range = (name, label, min, max, step, unit = "") =>
  `<label for="setting-${name}">${label} <output for="setting-${name}" data-output="${name}"></output><input id="setting-${name}" name="${name}" type="range" min="${min}" max="${max}" step="${step}" data-unit="${unit}"></label>`;
const check = (name, label) =>
  `<label class="setting-check"><input type="checkbox" name="${name}"> ${label}</label>`;
const select = (name, label, options) =>
  `<label>${label}<select name="${name}">${options.map(([id, text]) => `<option value="${id}">${text}</option>`).join("")}</select></label>`;
export function createSettingsPanel(preferences) {
  const panel = $("#settings-panel"),
    opener = $("#settings-toggle");
  let section = "themes",
    preview = null,
    search = "",
    kind = "all",
    onlyFavorites = false;
  panel.innerHTML = `<header class="settings-header"><h2 id="settings-title">Настройки</h2><button id="settings-close" type="button" class="subtle-button" aria-label="Закрыть настройки">Закрыть</button></header>
  <nav class="settings-tabs" aria-label="Разделы настроек">${Object.entries(
    labels,
  )
    .map(
      ([id, label]) =>
        `<button type="button" data-settings-tab="${id}" aria-controls="settings-body">${label}</button>`,
    )
    .join("")}</nav>
  <div id="settings-body"></div><section class="settings-preview" aria-label="Предпросмотр оформления"><p>Предпросмотр</p><div class="code-window"><pre><code class="source-code"><span class="k">def</span> <span class="nf">read</span>(text):
    <span class="c1"># Проверка текста</span>
    message = <span class="s2">"Привет, мир!"</span>
    <span class="k">return</span> message
</code></pre></div></section>
  <footer class="settings-footer"><button type="button" id="settings-reset-section" class="subtle-button">Сбросить раздел</button><button type="button" id="settings-reset-all" class="subtle-button">Сбросить всё</button><p id="settings-status" role="status"></p></footer>`;
  function close() {
    panel.removeAttribute("aria-modal");
    panel.removeAttribute("role");
    document.body.classList.remove("settings-open");
    panel.hidden = true;
    opener.setAttribute("aria-expanded", "false");
    document.querySelectorAll(".workspace, .sphinxsidebar").forEach((node) => { node.inert = false; });
    opener.focus();
  }
  function mobile() {
    return matchMedia("(max-width: 959px)").matches;
  }
  function syncPanelMode() {
    const isMobile = mobile();
    if (isMobile) {
      panel.setAttribute("role", "dialog");
      panel.setAttribute("aria-modal", "true");
      if (!panel.contains(document.activeElement)) $("#settings-close").focus();
    } else {
      panel.removeAttribute("role");
      panel.removeAttribute("aria-modal");
    }
    document.querySelectorAll(".workspace, .sphinxsidebar").forEach((node) => { node.inert = isMobile; });
  }
  function open() {
    panel.hidden = false;
    document.body.classList.add("settings-open");
    opener.setAttribute("aria-expanded", "true");
    syncPanelMode();
    $("#settings-close").focus();
  }
  opener.addEventListener("click", () => (panel.hidden ? open() : close()));
  $("#settings-close").addEventListener("click", close);
  document.addEventListener("keydown", (event) => {
    if (panel.hidden) return;
    if (event.key === "Escape") {
      event.preventDefault();
      close();
      return;
    }
    if (event.key !== "Tab" || !mobile()) return;
    const controls = [
      ...panel.querySelectorAll("button,input,select,textarea,a"),
    ].filter((el) => !el.disabled && !el.hidden && el.getClientRects().length);
    if (event.shiftKey && document.activeElement === controls[0]) {
      event.preventDefault();
      controls.at(-1)?.focus();
    } else if (!event.shiftKey && document.activeElement === controls.at(-1)) {
      event.preventDefault();
      controls[0]?.focus();
    }
  });
  matchMedia("(max-width: 959px)").addEventListener("change", () => {
    if (!panel.hidden) syncPanelMode();
  });
  function fields() {
    const value = preferences.value;
    panel.querySelectorAll("[name]").forEach((el) => {
      if (!Object.hasOwn(defaults, el.name)) return;
      if (el.type === "checkbox") el.checked = value[el.name];
      else el.value = String(value[el.name]);
    });
    panel.querySelectorAll("[data-output]").forEach((output) => {
      const input = panel.querySelector(`[name="${output.dataset.output}"]`);
      output.value = value[output.dataset.output] + (input?.dataset.unit || "");
    });
    const availability = $("#font-availability");
    if (availability) {
      const font = fonts.find((item) => item.id === value.font);
      availability.textContent = font.faces.some(
        (face) => face.style === "italic",
      )
        ? "Шрифт включён в курс с кириллицей; доступны прямое и курсивное начертания."
        : "Шрифт включён в курс с кириллицей; доступно только прямое начертание. Синтетический курсив отключён.";
    }
  }
  function catalog() {
    const focused = document.activeElement;
    const focusKey = focused?.dataset.themeChoice
      ? "themeChoice"
      : focused?.dataset.themeFavorite
        ? "themeFavorite"
        : null;
    const focusId = focusKey ? focused.dataset[focusKey] : null;
    const value = preferences.value;
    const list = themes.filter(
      (t) =>
        (kind === "all" || t.kind === kind) &&
        (!onlyFavorites || value.favorites.includes(t.id)) &&
        t.name.toLocaleLowerCase().includes(search.toLocaleLowerCase()),
    );
    $("#theme-list").innerHTML =
      list
        .map(
          (theme) =>
            `<article class="theme-card" data-theme="${theme.id}"><button type="button" data-theme-choice="${theme.id}" aria-pressed="${value.theme === theme.id}"><span class="theme-swatch"><span>def</span> read(text):</span><strong>${escape(theme.name)}</strong><small>${theme.kind === "light" ? "Светлая" : "Тёмная"}</small></button><button type="button" class="theme-favorite" data-theme-favorite="${theme.id}" aria-label="${value.favorites.includes(theme.id) ? "Убрать из избранного" : "В избранное"}: ${escape(theme.name)}" aria-pressed="${value.favorites.includes(theme.id)}">${value.favorites.includes(theme.id) ? "★" : "☆"}</button></article>`,
        )
        .join("") || "<p>Тем не найдено.</p>";
    if (focusId) {
      const key =
        focusKey === "themeChoice"
          ? "data-theme-choice"
          : "data-theme-favorite";
      const next =
        panel.querySelector(`[${key}="${focusId}"]`) ||
        $("#theme-only-favorites");
      next.focus({ preventScroll: true });
    }
  }
  let fileVersion = 0;
  function render() {
    fileVersion++;
    panel
      .querySelectorAll("[data-settings-tab]")
      .forEach((button) =>
        button.setAttribute(
          "aria-current",
          button.dataset.settingsTab === section ? "page" : "false",
        ),
      );
    $("#settings-reset-section").hidden = section === "import";
    let html = "";
    if (section === "themes")
      html = `${select("theme", "Текущая тема", [["system", "По оформлению системы"], ...themes.map((t) => [t.id, t.name])])}<label>Поиск тем<input type="search" id="theme-search" value="${escape(search)}"></label><div class="theme-filters"><label>Варианты<select id="theme-kind"><option value="all">Все</option><option value="light">Светлые</option><option value="dark">Тёмные</option></select></label><label><input type="checkbox" id="theme-only-favorites"> Избранное</label></div><div id="theme-list" class="theme-list"></div>`;
    if (section === "typography")
      html = `${select(
        "font",
        "Шрифт кода",
        fonts.map((f) => [f.id, f.name]),
      )}<p class="settings-hint" id="font-availability">Все шрифты включены в курс и доступны офлайн. Насыщенность и курсив ограничены начертаниями выбранной гарнитуры.</p>${range("size", "Размер шрифта", 10, 32, 1, " px")}${range("weight", "Насыщенность", 300, 700, 100)}${range("lineHeight", "Межстрочный интервал", 1.2, 2.6, 0.1)}${range("letterSpacing", "Расстояние между символами", -0.5, 2, 0.1, " px")}${check("ligatures", "Лигатуры")}${check("italic", "Курсив подсветки")}`;
    if (section === "code")
      html = `${select("indents", "Направляющие отступов", [
        ["off", "Выключены"],
        ["plain", "Обычные"],
        ["rainbow", "Цветные"],
      ])}${select("whitespace", "Пробелы и табуляции", [
        ["off", "Не показывать"],
        ["boundary", "Кроме одиночных между словами"],
        ["all", "Все"],
      ])}${check("trailing", "Выделять пробелы в конце строки")}${check("numbers", "Номера строк в файлах")}${check("syntax", "Подсветка синтаксиса")}`;
    if (section === "reading")
      html = `${check("wrap", "Перенос длинных строк")}<p class="settings-hint">При переносе номера строк скрываются.</p>${select(
        "width",
        "Ширина разбора",
        [
          ["narrow", "Узкая"],
          ["normal", "Обычная"],
          ["wide", "Широкая"],
          ["full", "Вся доступная ширина"],
        ],
      )}${check("diff", "Показывать изменения по умолчанию")}${check("syncScroll", "Связывать горизонтальную прокрутку парных файлов")}`;
    if (section === "import")
      html = `<p class="settings-hint">Откройте в VS Code «Preferences: Open User Settings (JSON)». Файл обрабатывается на устройстве. Настройки [python] имеют приоритет.</p><label>Выбрать файл<input id="vscode-file" type="file" accept=".json,.jsonc,application/json"></label><label for="vscode-text">Или вставить настройки JSONC</label><textarea id="vscode-text" rows="9" spellcheck="false" placeholder='{ "editor.fontSize": 16 }'></textarea><button type="button" id="vscode-preview">Предпросмотр импорта</button><div id="vscode-report" aria-live="polite"></div><button type="button" id="vscode-apply" hidden>Применить распознанные настройки</button>`;
    $("#settings-body").innerHTML =
      `<h3>${labels[section]}</h3><form id="settings-form">${html}</form>`;
    $("#settings-form").addEventListener("submit", (event) =>
      event.preventDefault(),
    );
    fields();
    if (section === "themes") {
      $("#theme-kind").value = kind;
      $("#theme-only-favorites").checked = onlyFavorites;
      catalog();
    }
    if (section === "import") {
      preview = null;
      $("#vscode-file").addEventListener("change", async (event) => {
        const version = ++fileVersion;
        const textarea = $("#vscode-text");
        preview = null;
        $("#vscode-apply").hidden = true;
        const file = event.target.files[0];
        if (!file) return;
        if (file.size > 1_000_000) {
          $("#vscode-report").textContent = "Выберите файл размером до 1 МБ.";
          return;
        }
        try {
          const text = await file.text();
          if (version !== fileVersion || !textarea.isConnected) return;
          textarea.value = text;
          showImport();
        } catch {
          if (version === fileVersion && textarea.isConnected)
            $("#vscode-report").textContent = "Не удалось прочитать файл.";
        }
      });
      $("#vscode-preview").addEventListener("click", showImport);
      $("#vscode-text").addEventListener("input", () => {
        fileVersion++;
        preview = null;
        $("#vscode-apply").hidden = true;
        $("#vscode-report").textContent =
          "Нажмите «Предпросмотр импорта», чтобы проверить изменённый текст.";
      });
      $("#vscode-apply").addEventListener("click", () => {
        if (preview) {
          preferences.update(preview.patch);
          $("#settings-status").textContent =
            `Применено настроек: ${preview.count}.`;
          preview = null;
          $("#vscode-apply").hidden = true;
        }
      });
    }
  }
  function showImport() {
    try {
      preview = importVSCode($("#vscode-text").value, preferences.value);
      $("#vscode-report").innerHTML =
        `<p>Будет применено параметров: ${preview.count}.${preview.python ? " Учтён раздел [python]." : ""} Неизвестные темы и шрифты сохраняют текущий выбор; известные темы используют адаптированную палитру курса.</p><ul>${preview.rows.map((row) => `<li><code>${escape(row.key)}</code>: ${row.status === "applied" ? "Будет применено" : "Пропущено"} — ${escape(row.message)}</li>`).join("")}</ul>`;
      $("#vscode-apply").hidden = preview.count === 0;
    } catch (error) {
      preview = null;
      $("#vscode-report").textContent = "Ошибка: " + error.message;
      $("#vscode-apply").hidden = true;
    }
  }
  panel.addEventListener("input", (event) => {
    const el = event.target;
    if (el.id === "theme-search") {
      search = el.value;
      catalog();
      return;
    }
    if (el.id === "theme-kind") {
      kind = el.value;
      catalog();
      return;
    }
    if (el.id === "theme-only-favorites") {
      onlyFavorites = el.checked;
      catalog();
      return;
    }
    if (!Object.hasOwn(defaults, el.name)) return;
    const value =
      el.type === "checkbox"
        ? el.checked
        : el.type === "range"
          ? Number(el.value)
          : el.value;
    preferences.update({ [el.name]: value });
  });
  panel.addEventListener("click", (event) => {
    const tab = event.target.closest("[data-settings-tab]");
    if (tab) {
      section = tab.dataset.settingsTab;
      render();
      return;
    }
    const theme = event.target.closest("[data-theme-choice]");
    if (theme) {
      preferences.update({ theme: theme.dataset.themeChoice });
      return;
    }
    const favorite = event.target.closest("[data-theme-favorite]");
    if (favorite) {
      const id = favorite.dataset.themeFavorite,
        old = preferences.value.favorites;
      preferences.update({
        favorites: old.includes(id)
          ? old.filter((t) => t !== id)
          : [...old, id],
      });
    }
  });
  $("#settings-reset-section").addEventListener("click", () =>
    preferences.reset(section),
  );
  $("#settings-reset-all").addEventListener("click", () => preferences.reset());
  preferences.subscribe((value, saved) => {
    fields();
    if (section === "themes") catalog();
    $("#settings-status").textContent = saved
      ? "Сохранено на этом устройстве."
      : "Хранение недоступно: настройки действуют до закрытия страницы.";
  });
  render();
  decorateCode(panel);
}
