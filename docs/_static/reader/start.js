// Keep the static lesson readable if a module or catalog cannot be loaded.
import("./main.js").catch((error) => {
  const status = document.querySelector("#reader-status");
  if (status) {
    status.textContent = "Не удалось загрузить настройки и выбор кода. Материал доступен ниже; обновите страницу для повторной попытки.";
    status.hidden = false;
  }
  console.error(error);
});
