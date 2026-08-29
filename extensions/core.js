export const ACTIONS = [
  {id:'data_acquisition', title:'读取业务数据', input:'标准数据源', output:'业务对象', required:true},
  {id:'constraint_parsing', title:'解析结构约束', input:'业务对象', output:'约束集合', required:true},
  {id:'solution_generation', title:'生成计划方案', input:'业务对象与约束', output:'候选方案', required:true},
  {id:'solution_selection', title:'选择计划方案', input:'候选方案', output:'选定方案', required:true},
  {id:'solution_evaluation', title:'分析与复核', input:'选定方案', output:'分析指标', required:false},
  {id:'execution_dispatch', title:'生成结果记录', input:'选定方案', output:'计划结果', required:false}
];
export function validatePipeline(pipeline) {
  const errors = [];
  if (!Array.isArray(pipeline)) return ['动作列表格式错误'];
  const ids = ACTIONS.map(a=>a.id);
  if (new Set(pipeline).size !== pipeline.length) errors.push('动作重复或存在循环');
  if (pipeline.some(p=>!ids.includes(p))) errors.push('包含未登记动作');
  if (ACTIONS.some(a=>a.required && !pipeline.includes(a.id))) errors.push('缺少必需动作');
  if (pipeline.some((p,i)=>i && ids.indexOf(p)<ids.indexOf(pipeline[i-1]))) errors.push('动作依赖顺序不成立');
  return errors;
}
export function validateConfig(config, policy) {
  const errors = [];
  if (!config || typeof config!=='object' || Array.isArray(config)) return ['参数格式错误'];
  const controls = policy.controls;
  for (const key of Object.keys(config)) if (!(key in controls)) errors.push(`未知参数 ${key}`);
  for (const [key,c] of Object.entries(controls)) {
    const v = config[key];
    if (key==='objective') {
      if (!v || typeof v!=='object' || Array.isArray(v)) {errors.push('目标权重格式错误'); continue;}
      for (const [name,value] of Object.entries(v)) {
        if (!c.keys.includes(name) || !Number.isFinite(value)) errors.push(`目标项 ${name} 不可用`);
      }
    } else if (!Number.isInteger(v) || (c.supported ? v<c.min||v>c.max : v!==(c.fixed??c.default))) {
      errors.push(`${c.label} 超出范围或不可修改`);
    }
  }
  return errors;
}
export function configuredRecipe(item, config, pipeline) {
  const errors=[...validatePipeline(pipeline),...validateConfig(config,item.policy)];
  if(errors.length) throw new Error(errors.join('；'));
  const r=structuredClone(item.recipe);
  r.pipeline=[...pipeline];
  const production=r.context.inputs.production;
  const branch=production.engine_type==='workshop'?production.planning:production.scheduling;
  branch.solver={...branch.solver,time_limit:config.solver_time_limit,threads:config.solver_threads};
  branch.iterations=config.iterations;
  branch.objective={...branch.objective,...config.objective};
  if(production.engine_type==='circular_sequence') {
    branch.sequence_length=config.sequence_length; branch.cycle_count=config.cycle_count;
  }
  r.context.inputs.data_acquisition.read_only=true;
  r.safety={write_database:false};
  return r;
}
export function taskFiles(item, config, pipeline, intent) {
  const recipe=configuredRecipe(item,config,pipeline);
  return {
    'AGENT_TASK.md':`# ${item.title}\n\n## 任务\n${intent}\n\n数据范围：${item.source}\n\n使用已授权的 DecisioWorks 环境，以 recipe.json 完成数据检查、受控运行和结果复核。所有改动先生成差异清单并由使用者确认。数据、配置或环境不足时停止并报告，记录真实错误，不补造求解结果。\n`,
    'context.json':JSON.stringify({schema:'sandbox.agent.v1',dataset:item.id,data_sha256:item.data_sha256,recipe:'recipe.json',config},null,2),
    'acceptance.md':'# 验收条件\n\n- 核对数据版本与 SHA-256。\n- 记录字段与引用关系诊断，不以诊断通过代替求解成功。\n- 保留实际动作、参数、耗时、求解状态和结果。\n- 基线与重算使用同一份输入；解释参数与结果的差异。\n- 对无解、授权失败、超时如实报告。\n- 原始数据保持只读；结果与计划须人工复核后用于执行。\n',
    'allowed-actions.json':JSON.stringify({allowed_paths:[item.source],allowed_actions:pipeline,access:'read-only',write_scope:'user-approved output directory',requires_approval:['change data','change recipe','start solve'],prohibited:['read private keys','upload customer data','bypass license','execute arbitrary script nodes','read protected kernel source']},null,2),
    'recipe.json':JSON.stringify(recipe,null,2)
  };
}
export function flatten(value, prefix='') {
  if(value===null || typeof value!=='object') return [[prefix,value]];
  return Object.entries(value).flatMap(([k,v])=>flatten(v,prefix?`${prefix}.${k}`:k));
}
export function escapeHTML(value) {return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
export function download(name, content, type='application/json') {
  const url=URL.createObjectURL(new Blob([content],{type}));
  const a=document.createElement('a'); a.href=url;a.download=name; a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
// Deterministic, uncompressed ZIP keeps task bundles dependency-free and inspectable.
export function zip(files) {
  const enc=new TextEncoder(), parts=[], central=[];let offset=0;
  const crc=bytes=>{let x=0xffffffff;for(const b of bytes){x^=b;for(let i=0;i<8;i++) x=(x>>>1)^((x&1)?0xedb88320:0);}return (x^0xffffffff)>>>0;};
  for(const [name,content] of Object.entries(files)) {
    const n=enc.encode(name), b=enc.encode(content), c=crc(b), h=new Uint8Array(30+n.length),v=new DataView(h.buffer);
    v.setUint32(0,0x04034b50,true);v.setUint16(4,20,true);v.setUint16(6,0x800,true);v.setUint32(14,c,true);v.setUint32(18,b.length,true);v.setUint32(22,b.length,true);v.setUint16(26,n.length,true);h.set(n,30);
    const d=new Uint8Array(46+n.length),w=new DataView(d.buffer);w.setUint32(0,0x02014b50,true);w.setUint16(4,20,true);w.setUint16(6,20,true);w.setUint16(8,0x800,true);w.setUint32(16,c,true);w.setUint32(20,b.length,true);w.setUint32(24,b.length,true);w.setUint16(28,n.length,true);w.setUint32(42,offset,true);d.set(n,46);
    parts.push(h,b);central.push(d);offset+=h.length+b.length;
  }
  const size=central.reduce((a,b)=>a+b.length,0),e=new Uint8Array(22),v=new DataView(e.buffer);
  v.setUint32(0,0x06054b50,true);v.setUint16(8,central.length,true);v.setUint16(10,central.length,true);v.setUint32(12,size,true);v.setUint32(16,offset,true);
  return new Blob([...parts,...central,e],{type:'application/zip'});
}
