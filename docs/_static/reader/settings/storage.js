export function readStored(key) {
  try { return localStorage.getItem(`algorithms.${key}`); } catch { return null; }
}
export function writeStored(key, value) {
  try { localStorage.setItem(`algorithms.${key}`, value); return true; } catch { return false; }
}
export function loadPreferences() {
  try { return JSON.parse(readStored("preferences") || "{}"); } catch { return {}; }
}
export function savePreferences(value) { return writeStored("preferences", JSON.stringify(value)); }
