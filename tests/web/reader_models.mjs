import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
// Catalogs are local course assets; model tests never access the network.
globalThis.fetch = async (url) => ({ ok: true, json: async () => JSON.parse(await readFile(fileURLToPath(url), 'utf8')) });
const { selection, align } = await import('../../docs/_static/reader/code_viewer/model.js');
const { normalize } = await import('../../docs/_static/reader/settings/schema.js');
const { importVSCode, parseJSONC } = await import('../../docs/_static/reader/settings/vscode.js');
const sources = [{path:'recursive.py',group:'fibonacci',common:false}, {path:'memoized.py',group:'fibonacci',common:false}, {path:'types.py',group:'shared',common:true}];
assert.equal(selection(sources,'?view=code').first,sources[0]);
assert.equal(selection(sources,'?view=code').second,sources[1]);
assert.equal(selection(sources,'?file=memoized.py&compare=&view=code').second,null);
assert.equal(selection(sources,'?file=missing&compare=recursive.py').first,sources[0]);
assert.equal(selection(sources,'?file=types.py&compare=memoized.py').second,sources[1]);
assert.equal(selection([],'?view=code').first,null);
for (const [a,b] of [['a\nb\nc\n','a\nx\nc\n'],['','x\n'],['x\n',''],['x\nx\n','x\n'],['\t  x\n','x\n']]) {
 const rows=align(a,b), first=a.split('\n'), second=b.split('\n');
 if(a.endsWith('\n')) first.pop(); if(b.endsWith('\n')) second.pop();
 assert.deepEqual(rows.filter(r=>r.first!==null).map(r=>first[r.first]),first);
 assert.deepEqual(rows.filter(r=>r.second!==null).map(r=>second[r.second]),second);
 for(const row of rows) if(row.change==='same') assert.equal(first[row.first],second[row.second]);
}
const value=normalize({size:100,lineHeight:0,theme:'missing',font:'missing',favorites:['github_dark','github_dark','unknown']});
assert.equal(value.size,32); assert.equal(value.lineHeight,1.2); assert.equal(value.theme,'system');
assert.deepEqual(value.favorites,['github_dark']);
assert.deepEqual(parseJSONC('{/* note */"x":"https://example.com",}'),{x:'https://example.com'});
const imported=importVSCode('{"editor.fontSize":16,"editor.fontFamily":"Fira Code","[python]":{"editor.fontSize":20}}',normalize({}));
assert.equal(imported.patch.size,20);assert.equal(imported.patch.font,'fira_code');assert.equal(imported.python,true);
assert.throws(()=>parseJSONC('{/* missing'));
console.log('Reader models: URL/variant selection, lossless line alignment, preference validation and JSONC import passed');
