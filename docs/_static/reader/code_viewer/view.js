import { escape } from "../dom.js";
import { displayRows } from "./model.js";
import { copySource } from "./clipboard.js";
import { decorateCode } from "./decorate.js";

const option = (file, selected) => `<option value="${escape(file.path)}" ${file === selected ? "selected" : ""}>${escape(file.group + "." + file.name)}</option>`;
const header = (file, side) => `<header class="pane-header source-header" data-header="${side}"><div><span class="pane-side">${escape(file.name)}</span><span class="pane-path" title="${escape(file.path)}">${escape(file.path)}</span></div><button type="button" class="copy-button" data-copy="${side}" aria-label="Копировать: ${escape(file.path)}">Копировать</button></header>`;
function pane(file, side, rows) {
  return `<div class="pane-source code-window" data-pane="${side}"><pre><code class="source-code">${rows.map((row) => {
    const index = row[side === "before" ? "first" : "second"];
    return `<span class="code-row ${index === null ? "is-gap" : "row-" + row.change}"><span class="code-line-number" aria-hidden="true">${index === null ? "" : index + 1}</span><span class="code-line-content">${index === null ? "" : file.lines[index]}</span></span>`;
  }).join("")}</code></pre></div>`;
}

export function createCodeViewer(container, sources, preferences, choose) {
  let active = null;
  let renderedChanges = null;
  let scrolling = false;
  const query = (selector) => container.querySelector(selector);
  const compact = matchMedia("(max-width: 1100px)");
  function refresh() {
    const comparison = query(".code-comparison");
    if (comparison) {
      if (renderedChanges !== preferences.value.diff) drawSources();
      comparison.dataset.changes = String(preferences.value.diff);
      comparison.dataset.compact = String(compact.matches);
    }
    query("#code-changes")?.setAttribute("aria-pressed", String(preferences.value.diff));
  }
  function drawSources() {
    const columns = query(".code-columns");
    if (!columns || !active?.first) return;
    const scroll = query(".code-scroll");
    const top = scroll.scrollTop;
    const positions = new Map([...container.querySelectorAll(".pane-source")].map((node) => [node.dataset.pane, node.scrollLeft]));
    const rows = displayRows(active.first, active.second, preferences.value.diff);
    columns.innerHTML = pane(active.first, "before", rows.before) + (active.second ? pane(active.second, "after", rows.after) : "");
    container.querySelectorAll(".pane-source").forEach((node) => {
      node.scrollLeft = positions.get(node.dataset.pane) || 0;
      node.addEventListener("scroll", () => {
        if (!preferences.value.syncScroll || scrolling) return;
        scrolling = true;
        container.querySelectorAll(".pane-source").forEach((other) => { if (other !== node) other.scrollLeft = node.scrollLeft; });
        requestAnimationFrame(() => { scrolling = false; });
      });
    });
    scroll.scrollTop = top;
    renderedChanges = preferences.value.diff;
    decorateCode(container);
  }
  compact.addEventListener("change", refresh);
  function render(state) {
    active = state;
    if (!state.first) {
      container.innerHTML = '<p class="pane-empty" role="status">На этой вводной странице нет отдельных исходных файлов. Выберите алгоритм в каталоге тем.</p>';
      return;
    }
    const { first, second } = state;
    renderedChanges = null;
    const groups = [...new Set(sources.map((file) => file.group))];
    container.innerHTML = `<div class="code-toolbar"><label>Реализация / файл<select id="code-file-select">${sources.map((file) => option(file, first)).join("")}</select></label><label>Сравнить с<select id="code-compare-select"><option value="">Без сравнения</option>${sources.filter((file) => file !== first).map((file) => option(file, second)).join("")}</select></label><button type="button" id="code-changes" title="Выравнивать строки и подсвечивать различия" aria-pressed="${preferences.value.diff}">Изменения</button><button type="button" id="copy-code-link" class="copy-button">Ссылка на код</button></div><div class="code-layout"><nav class="file-tree" aria-label="Файлы и варианты реализации">${groups.map((group) => `<section class="file-group"><h2>${escape(group)}</h2><ul>${sources.filter((file) => file.group === group).map((file) => `<li><button type="button" class="file-choice" data-file="${escape(file.path)}" ${file === first ? 'aria-current="page"' : ""}>${escape(file.name)}${file.common ? " · общий" : ""}</button></li>`).join("")}</ul></section>`).join("")}</nav><div class="code-comparison" data-common="${!second}" data-side="before"><div class="mobile-sides" role="group" aria-label="Сторона сравнения"><button type="button" data-code-side="before" aria-pressed="true">${escape(first.name)}</button>${second ? `<button type="button" data-code-side="after" aria-pressed="false">${escape(second.name)}</button>` : ""}</div><div class="pane-headers">${header(first, "before")}${second ? header(second, "after") : ""}</div><div class="code-scroll" tabindex="0" aria-label="Код выбранных реализаций"><div class="code-columns"></div></div></div></div>`;
    query("#code-file-select").addEventListener("change", (event) => choose({ file: event.target.value, compare: "" }, "code-file-select"));
    query("#code-compare-select").addEventListener("change", (event) => choose({ compare: event.target.value }, "code-compare-select"));
    container.querySelectorAll("[data-file]").forEach((button) => button.addEventListener("click", () => choose({ file: button.dataset.file, compare: "" }, "code-file-select")));
    query("#code-changes").addEventListener("click", () => preferences.update({ diff: !preferences.value.diff }));
    query("#copy-code-link").addEventListener("click", (event) => copySource(event.currentTarget, location.href));
    container.querySelectorAll("[data-copy]").forEach((button) => button.addEventListener("click", () => copySource(button, button.dataset.copy === "before" ? active.first.code : active.second.code)));
    container.querySelectorAll("[data-code-side]").forEach((button) => button.addEventListener("click", () => {
      query(".code-comparison").dataset.side = button.dataset.codeSide;
      container.querySelectorAll("[data-code-side]").forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
    }));
    refresh();
  }
  return { render, refresh };
}
