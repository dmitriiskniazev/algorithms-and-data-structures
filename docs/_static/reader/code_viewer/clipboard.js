export async function copySource(button, text) {
  let copied = false;
  try {
    await navigator.clipboard.writeText(text);
    copied = true;
  } catch {
    const area = document.createElement("textarea");
    area.value = text;
    area.className = "sr-only";
    document.body.append(area);
    area.select();
    try {
      copied = document.execCommand("copy");
    } catch {
    } finally {
      area.remove();
      button.focus();
    }
  }
  const label = button.textContent;
  button.textContent = copied ? "Скопировано" : "Не удалось скопировать";
  button.setAttribute("aria-live", "polite");
  setTimeout(() => {
    button.textContent = label;
    button.removeAttribute("aria-live");
  }, 1800);
}
