export const themes = await fetch(
  new URL("./catalog.json", import.meta.url),
).then((response) => {
  if (!response.ok) throw new Error("Не удалось загрузить каталог тем");
  return response.json();
});
export const fonts = await fetch(
  new URL("../../fonts/catalog.json", import.meta.url),
).then((response) => {
  if (!response.ok) throw new Error("Не удалось загрузить каталог шрифтов");
  return response.json();
});
