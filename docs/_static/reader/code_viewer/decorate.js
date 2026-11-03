// Whitespace markers live in attributes/CSS, never in the copyable source text.
export function decorateCode(container = document) {
  const decorate = (code) => {
    if (code.dataset.decorated) return;
    code.dataset.decorated = "true";
    const walker = document.createTreeWalker(code, NodeFilter.SHOW_TEXT),
      nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    const original = code.textContent;
    let offset = 0;
    for (const node of nodes) {
      const fragment = document.createDocumentFragment();
      for (const part of node.data.split(/([ \t]+)/)) {
        if (!part) continue;
        if (/^[ \t]+$/.test(part)) {
          const lineStart = original.lastIndexOf("\n", offset - 1) + 1;
          let lineEnd = original.indexOf("\n", offset);
          if (lineEnd < 0) lineEnd = original.length;
          const span = document.createElement("span");
          span.className = "code-space";
          span.textContent = part;
          span.dataset.leading = String(
            /^[ \t]*$/.test(original.slice(lineStart, offset)),
          );
          span.dataset.trailing = String(
            /^[ \t]*$/.test(original.slice(offset + part.length, lineEnd)),
          );
          let column = 0;
          for (const character of original.slice(lineStart, offset))
            column += character === "\t" ? 4 - (column % 4) : 1;
          const startColumn = column;
          span.dataset.boundary = String(
            span.dataset.leading === "true" ||
              span.dataset.trailing === "true" ||
              part.length > 1 ||
              part.includes("\t"),
          );
          span.dataset.marks = [...part]
            .map((character) => {
              const width = character === "\t" ? 4 - (column % 4) : 1;
              column += width;
              return character === "\t" ? "→" + " ".repeat(width - 1) : "·";
            })
            .join("");
          span.style.backgroundPositionX = `calc(-${startColumn}ch - ${startColumn} * var(--editor-letter-spacing, 0px))`;
          fragment.append(span);
        } else fragment.append(part);
        offset += part.length;
      }
      node.replaceWith(fragment);
    }
  };
  container.querySelectorAll(".source-code").forEach((code) => {
    if (!code.querySelector(".code-row"))
      decorate(code);
  });
  container
    .querySelectorAll(".code-line-content")
    .forEach(decorate);
}
