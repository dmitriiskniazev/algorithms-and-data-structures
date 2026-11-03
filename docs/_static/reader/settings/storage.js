import { createStorage } from "./store.js";

export const { readStored, writeStored, loadPreferences, savePreferences } = createStorage("algorithms");
