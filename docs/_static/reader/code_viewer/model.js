export function selection(sources, search) {
  const query = new URLSearchParams(search);
  const first = sources.find((file) => file.path === query.get("file")) ||
    sources.find((file) => !file.common) || sources[0] || null;
  let second = sources.find((file) => file.path === query.get("compare")) || null;
  if (!query.has("compare") && first)
    second = sources.find((file) => !file.common && file.group === first.group && file.path !== first.path) || null;
  if (second === first) second = null;
  return { view: query.get("view") === "code" ? "code" : "read", first, second };
}

// Equal lines share a row; additions/removals occupy a gap on the other side.
export function align(first, second) {
  const a = first.split("\n"), b = second.split("\n");
  if (first.endsWith("\n")) a.pop();
  if (second.endsWith("\n")) b.pop();
  const dp = Array.from({ length: a.length + 1 }, () => new Uint32Array(b.length + 1));
  for (let i = a.length - 1; i >= 0; i--)
    for (let j = b.length - 1; j >= 0; j--)
      dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  const rows = [];
  let i = 0, j = 0;
  while (i < a.length || j < b.length) {
    if (i < a.length && j < b.length && a[i] === b[j]) rows.push({ first: i++, second: j++, change: "same" });
    else if (i < a.length && (j === b.length || dp[i + 1][j] >= dp[i][j + 1]))
      rows.push({ first: i++, second: null, change: "removed" });
    else rows.push({ first: null, second: j++, change: "added" });
  }
  return rows;
}
