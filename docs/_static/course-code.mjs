import { copySource } from "./reader/code_viewer/clipboard.js";

const catalog = document.querySelector(".course-catalog");
if (catalog && matchMedia("(max-width: 940px)").matches) catalog.open = false;

for (const listing of document.querySelectorAll("div.highlight")) {
  const source = listing.querySelector("pre");
  if (!source || listing.dataset.sourceReady) continue;
  listing.dataset.sourceReady = "true";
  const details = listing.closest(".source-details");
  let panel = details || listing.closest(".literal-block-wrapper");
  let header = details?.querySelector(":scope > summary") || panel?.querySelector(":scope > .code-block-caption");
  if (!panel) {
    panel = document.createElement("div");
    listing.before(panel);
    panel.append(listing);
  }
  panel.classList.add("source-panel");
  if (!header) {
    header = document.createElement("div");
    const label = document.createElement("span");
    label.className = "source-label";
    label.textContent = listing.closest(".highlight-python") ? "Python" : "Код";
    header.append(label);
    panel.prepend(header);
  }
  header.classList.add("source-header");
  const button = document.createElement("button");
  button.type = "button";
  button.className = "copy-button";
  button.textContent = "Копировать";
  const label = header.querySelector(".caption-text, .source-label")?.textContent.trim() || "код";
  button.setAttribute("aria-label", `Копировать: ${label}`);
  button.addEventListener("click", (event) => {
    if (header.tagName === "SUMMARY") {
      event.preventDefault();
      event.stopPropagation();
    }
    copySource(button, source.textContent);
  });
  header.append(button);
}
