import { themes, fonts } from "../themes/catalog.js";
export const defaults = Object.freeze({
  theme: "system",
  font: "jetbrains_mono",
  size: 14,
  weight: 400,
  lineHeight: 1.8,
  letterSpacing: 0,
  ligatures: false,
  italic: true,
  indents: "off",
  whitespace: "off",
  trailing: false,
  numbers: true,
  wrap: false,
  syntax: true,
  width: "full",
  diff: true,
  syncScroll: false,
  favorites: [],
});
export const groups = {
  themes: ["theme", "favorites"],
  typography: [
    "font",
    "size",
    "weight",
    "lineHeight",
    "letterSpacing",
    "ligatures",
    "italic",
  ],
  code: ["indents", "whitespace", "trailing", "numbers", "syntax"],
  reading: ["wrap", "width", "diff", "syncScroll"],
};
const choices = {
  theme: ["system", ...themes.map((t) => t.id)],
  font: fonts.map((f) => f.id),
  indents: ["off", "plain", "rainbow"],
  whitespace: ["off", "boundary", "all"],
  width: ["narrow", "normal", "wide", "full"],
};
const ranges = {
  size: [10, 32, 1],
  weight: [300, 700, 100],
  lineHeight: [1.2, 2.6, 0.1],
  letterSpacing: [-0.5, 2, 0.1],
};
export function normalize(input) {
  const result = { ...defaults, favorites: [] };
  if (!input || typeof input !== "object" || Array.isArray(input))
    return result;
  for (const [key, allowed] of Object.entries(choices))
    if (typeof input[key] === "string" && allowed.includes(input[key]))
      result[key] = input[key];
  for (const [key, [min, max, step]] of Object.entries(ranges))
    if (typeof input[key] === "number" && Number.isFinite(input[key]))
      result[key] = Number(
        (
          Math.round(Math.max(min, Math.min(max, input[key])) / step) * step
        ).toFixed(2),
      );
  for (const [key, value] of Object.entries(defaults))
    if (typeof value === "boolean" && typeof input[key] === "boolean")
      result[key] = input[key];
  if (Array.isArray(input.favorites))
    result.favorites = [
      ...new Set(
        input.favorites.filter(
          (id) => typeof id === "string" && themes.some((t) => t.id === id),
        ),
      ),
    ];
  return result;
}
