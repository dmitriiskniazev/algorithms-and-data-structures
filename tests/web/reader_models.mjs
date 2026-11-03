import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
// Catalogs are local course assets; model tests never access the network.
globalThis.fetch = async (url) => ({ ok: true, json: async () => JSON.parse(await readFile(fileURLToPath(url), 'utf8')) });
const reader = new URL(process.argv[2] + "/");
const { selection, align, displayRows } = await import(new URL("code_viewer/model.js", reader));
const { normalize } = await import(new URL("settings/schema.js", reader));
const { importVSCode, parseJSONC } = await import(new URL("settings/vscode.js", reader));
const sources = [{path:'recursive.py',group:'fibonacci',common:false}, {path:'memoized.py',group:'fibonacci',common:false}, {path:'types.py',group:'shared',common:true}];
assert.equal(selection(sources,'?view=code').first,sources[0]);
assert.equal(selection(sources,'?view=code').second,sources[1]);
assert.equal(selection(sources,'?file=memoized.py&compare=&view=code').second,null);
assert.equal(selection(sources,'?file=missing&compare=recursive.py').first,sources[0]);
assert.equal(selection(sources,'?file=types.py&compare=memoized.py').second,sources[1]);
assert.equal(selection([],'?view=code').first,null);
for (const [a,b] of [['a\nb\nc\n','a\nx\nc\n'],['','x\n'],['x\n',''],['x\nx\n','x\n'],['\t  x\n','x\n']]) {
 const rows=align(a,b), first=a ? a.split('\n') : [], second=b ? b.split('\n') : [];
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

// Switching changes off preserves each file's own lines, including real blank lines.
const firstFile={code:'def f():\n\n    return 1\n',lines:['def f():','','    return 1']};
const secondFile={code:'def f():\n    x = 1\n    y = 2\n    return x + y\n',lines:['def f():','    x = 1','    y = 2','    return x + y']};
const plain=displayRows(firstFile,secondFile,false);
assert.deepEqual(plain.before.map(row=>row.first),[0,1,2]);
assert.deepEqual(plain.after.map(row=>row.second),[0,1,2,3]);
assert.ok(plain.before.every(row=>row.first!==null));
assert.ok(plain.after.every(row=>row.second!==null));
assert.equal(firstFile.lines[plain.before[1].first],'');
const diff=displayRows(firstFile,secondFile,true);
assert.ok(diff.before.some(row=>row.first===null || row.second===null));
assert.deepEqual(displayRows(firstFile,secondFile,false),plain);
assert.deepEqual(displayRows(firstFile,null,false).after,[]);
assert.deepEqual(displayRows({code:'',lines:[]},null,false).before,[]);
assert.deepEqual(align('',''),[]);
console.log('Unaligned display keeps exact line counts and genuine blank lines; diff alignment can be restored');
