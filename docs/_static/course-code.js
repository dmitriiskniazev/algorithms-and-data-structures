// Copy only the rendered source text; captions and controls stay outside pre.
(() => {
    const catalog = document.querySelector(".course-catalog");
    if (catalog && matchMedia("(max-width: 940px)").matches) catalog.open = false;
    if (!navigator.clipboard) return;
    document.querySelectorAll("div.highlight").forEach((listing) => {
        const source = listing.querySelector("pre");
        if (!source) return;
        const button = document.createElement("button");
        button.type = "button";
        button.className = "copy-source";
        button.textContent = "Копировать";
        button.setAttribute("aria-label", "Копировать код");
        button.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(source.textContent);
                button.textContent = "Скопировано";
            } catch {
                button.textContent = "Выделите код для копирования";
            }
        });
        listing.prepend(button);
    });
})();
