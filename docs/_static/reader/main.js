import { createPreferences } from "./settings/preferences.js";
import * as storage from "./settings/storage.js";
import { createSettingsPanel } from "./settings/panel.js";
import { createCodeViewer } from "./code_viewer/viewer.js";
import { selection } from "./code_viewer/model.js";

function initialize() {
const search = document.querySelector("#topic-search");
if (search) {
  const filter = () => {
    const term = search.value.trim().toLocaleLowerCase("ru");
    let count = 0;
    document.querySelectorAll("#reader-topics li").forEach((item) => {
      const link = item.querySelector("a");
      item.hidden = !link || !link.textContent.toLocaleLowerCase("ru").includes(term);
      if (!item.hidden) count++;
    });
    document.querySelector("#topic-search-status").textContent = count ? `Тем найдено: ${count}` : "Совпадений нет";
  };
  search.addEventListener("input", filter);
  search.addEventListener("keydown", (event) => { if (event.key === "Escape") { search.value = ""; filter(); } });
}

const payload = document.querySelector("#reader-sources");
if (!payload) { createPreferences(() => {}, storage); return; }
const status = document.querySelector("#reader-status");
try {
  const sources = JSON.parse(payload.textContent);
  const material = document.querySelector("#lesson-material");
  const workspace = document.querySelector("#code-workspace");
  document.querySelector(".documentwrapper").classList.add("workspace");
  document.querySelectorAll("div.highlight").forEach((listing) => {
    listing.classList.add("code-window");
    const source = listing.querySelector("pre");
    if (source) source.classList.add("source-code");
  });
  let viewer;
  const preferences = createPreferences(() => viewer?.refresh(), storage);
  function render(focusId) {
    const state = selection(sources, location.search);
    material.hidden = state.view === "code";
    workspace.hidden = state.view !== "code";
    document.body.classList.toggle("code-mode", state.view === "code");
    document.querySelectorAll("[data-reader-view]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.readerView === state.view)));
    document.querySelectorAll(".course-catalog a[href]").forEach((link) => {
      const url = new URL(link.href, location.href);
      if (!/\/(algorithms|data-structures)\//.test(url.pathname)) return;
      if (state.view === "code") url.searchParams.set("view", "code");
      else url.searchParams.delete("view");
      link.href = url.href;
    });
    if (state.view === "code") viewer.render(state);
    if (focusId) document.getElementById(focusId)?.focus();
  }
  function choose(patch, focusId) {
    const url = new URL(location.href);
    for (const [key, value] of Object.entries(patch)) url.searchParams.set(key, value);
    history.replaceState(null, "", url);
    render(focusId);
  }
  viewer = createCodeViewer(workspace, sources, preferences, choose);
  preferences.subscribe(() => { viewer.refresh(); preferences.refresh(); });
  createSettingsPanel(preferences, { inertSelector: ".workspace, .sphinxsidebar" });
  document.querySelectorAll("[data-reader-view]").forEach((button) => button.addEventListener("click", () => {
    const url = new URL(location.href);
    url.searchParams.set("view", button.dataset.readerView);
    history.pushState(null, "", url);
    render();
  }));
  window.addEventListener("popstate", () => render());
  document.querySelector(".reader-topbar").hidden = false;
  render();
  preferences.refresh();
} catch (error) {
  document.querySelector("#lesson-material").hidden = false;
  document.querySelector("#code-workspace").hidden = true;
  document.body.classList.remove("code-mode");
  status.textContent = "Не удалось загрузить переключатели. Материал доступен ниже; обновите страницу для повторной попытки.";
  status.hidden = false;
  console.error(error);
}

}
initialize();
