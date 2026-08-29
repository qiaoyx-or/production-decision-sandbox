import assert from 'node:assert/strict';
import {readFile,writeFile} from 'node:fs/promises';
import {ACTIONS,validatePipeline,validateConfig,configuredRecipe,taskFiles,zip} from '../extensions/core.js';
const catalog=JSON.parse(await readFile(new URL('../extensions/data/cases.json',import.meta.url),'utf8'));
const order=ACTIONS.map(a=>a.id);
assert.equal(validatePipeline(order).length,0);
for(const bad of [[],[...order,order[0]],[...order].reverse(),['__import__'],null])assert.ok(validatePipeline(bad).length);
for(const c of catalog.cases){
  assert.equal(validateConfig(c.default_config,c.policy).length,0);
  assert.ok(validateConfig({...c.default_config,solver_threads:99999},c.policy).length);
  assert.ok(validateConfig({...c.default_config,max_workers:99},c.policy).length);
  assert.ok(validateConfig({...c.default_config,objective:{bad:1}},c.policy).length);
  const before=JSON.stringify(c),recipe=configuredRecipe(c,c.default_config,order);
  assert.equal(JSON.stringify(c),before);assert.equal(recipe.context.inputs.data_acquisition.read_only,true);
  assert.ok(!JSON.stringify(recipe).includes('/home/'));assert.ok(!('_recipe_path' in recipe));
  for(const t of Object.values(c.tables))assert.equal(t.rows.length,t.count);
  const files=taskFiles(c,c.default_config,order,'Test');
  assert.equal(Object.keys(files).length,5);
  assert.equal(JSON.parse(files['allowed-actions.json']).access,'read-only');
  await writeFile(`/tmp/${c.id}-sandbox-task-test.zip`,new Uint8Array(await zip(files).arrayBuffer()));
}
console.log('PASS pipeline, dependency order, config limits, immutable recipes, full rows, relative paths and task ZIPs');
