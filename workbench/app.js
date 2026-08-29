import {ACTIONS, validatePipeline, validateConfig, configuredRecipe, taskFiles, flatten, escapeHTML as esc, download, zip} from '../extensions/core.js';
import {RULES, TASKS} from '../extensions/rules.js';

const $=id=>document.getElementById(id);
const state={cases:[],local:false,token:'',item:null,config:null,pipeline:[],page:0,outPage:0,busy:false,records:{},tasks:null};
const OBJECTIVES={job_bias:'计划偏差目标权重',waittime:'等待目标权重',color:'颜色切换权重',capacity:'循环容量切换权重'};
const STATUS={running:'运行中',success:'完成',succeeded:'完成',completed:'完成',failed:'失败',error:'失败',skipped:'跳过',ok:'成功'};
const show=(text,error=false)=>{$('notice').className=text?(error?'note error-line':'note'):'';$('notice').textContent=text;};
const currentRecords=()=>state.records[state.item?.id]??{};
const format=v=>v===undefined||v===null?'—':typeof v==='object'?JSON.stringify(v):typeof v==='number'?Number(v.toFixed(6)).toLocaleString('zh-CN',{maximumFractionDigits:6}):String(v);

async function api(path,body){
  const response=await fetch(path,{method:body?'POST':'GET',headers:body?{'Content-Type':'application/json','X-Workbench-Token':state.token}:{},body:body?JSON.stringify(body):undefined});
  const data=await response.json();
  if(!response.ok)throw new Error(data.error||'请求未完成');
  return data;
}
function activate(tab){
  if(!['data','flow','rules','results','agent'].includes(tab))tab='data';
  document.querySelectorAll('[data-tab]').forEach(b=>{const active=b.dataset.tab===tab;b.setAttribute('aria-selected',active);b.tabIndex=active?0:-1;});
  document.querySelectorAll('[role=tabpanel]').forEach(p=>p.hidden=p.id!==tab);
  history.replaceState(null,'',`${location.pathname}${location.search}#${tab}`);
}
document.querySelectorAll('[data-tab]').forEach((button,index,buttons)=>{
  button.onclick=()=>activate(button.dataset.tab);
  button.onkeydown=e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();const next=buttons[(index+(e.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length];next.focus();activate(next.dataset.tab);}};
});
function tableHTML(columns,rows,hints={}){
  if(!columns?.length)return '<div class="empty">暂无结果数据</div>';
  return `<table><thead><tr>${columns.map(c=>`<th tabindex="0" title="${esc(hints[c]||c)}">${esc(c)}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${columns.map((c,i)=>`<td title="${esc(format(Array.isArray(r)?r[i]:r[c]))}">${esc(format(Array.isArray(r)?r[i]:r[c]))}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
}
function inputTable(){
  const name=$('table').value,t=state.item.tables[name],size=Number($('pageSize').value),pages=Math.max(1,Math.ceil(t.count/size));
  state.page=Math.min(state.page,pages-1);
  $('inputTable').innerHTML=tableHTML(t.columns,t.rows.slice(state.page*size,(state.page+1)*size),state.item.field_hints?.[name]);
  $('rowCount').textContent=`${name} · 共 ${t.count} 行`;
  $('pageLabel').textContent=`${state.page+1} / ${pages}`;$('prev').disabled=!state.page;$('next').disabled=state.page+1>=pages;
}
function diagnosis(){
  const d=state.item.diagnosis,checks=d.checks||[],blocked=checks.filter(x=>x.status!=='passed').length;
  $('facts').innerHTML=`<div><strong>${Object.keys(state.item.tables).length}</strong><span>输入数据表</span></div><div><strong>${Object.values(state.item.tables).reduce((n,t)=>n+t.count,0)}</strong><span>完整输入记录</span></div><div><strong>${blocked?'待修正':'检查通过'}</strong><span>${state.local?'当前数据诊断':'发行样例快照诊断'}</span></div>`;
  $('diagnosisScope').textContent=d.scope;
  $('checks').innerHTML=tableHTML(['检查项','状态','对象','记录'],checks.map(c=>({'检查项':c.name,'状态':c.status==='passed'?'通过':'阻断','对象':[c.table,c.field].filter(Boolean).join('.'),'记录':c.detail})));
}
function invalidateTask(){state.tasks=null;$('exportTask').disabled=true;$('taskPreview').textContent='尚未生成任务包';$('taskFiles').replaceChildren();}
function errors(){return [...validatePipeline(state.pipeline),...validateConfig(state.config,state.item.policy)];}
function updateValidation(){
  $('flowErrors').textContent=validatePipeline(state.pipeline).join('；');
  $('configErrors').textContent=validateConfig(state.config,state.item.policy).join('；');
  try{$('recipePreview').textContent=JSON.stringify(configuredRecipe(state.item,state.config,state.pipeline),null,2);}catch(e){$('recipePreview').textContent=e.message;}
  $('baseline').disabled=!state.local||state.busy||errors().length>0||state.item.diagnosis.stage==='blocked';
  $('rerun').disabled=$('baseline').disabled||currentRecords().baseline?.result.status!=='ok';
  $('exportRecipe').disabled=errors().length>0;$('makeTask').disabled=errors().length>0;
}
function renderFlow(){
  $('flowNodes').innerHTML=state.pipeline.map(id=>{const a=ACTIONS.find(a=>a.id===id);return `<div class="node"><strong>${esc(a.title)}</strong><small>${esc(a.input)} → ${esc(a.output)}</small><small>${a.required?'必需动作':'可选动作'}</small></div>`;}).join('');
  $('optionalActions').innerHTML=ACTIONS.filter(a=>!a.required).map(a=>`<div class="check-row"><input type="checkbox" id="action-${a.id}" ${state.pipeline.includes(a.id)?'checked':''}><label for="action-${a.id}">${esc(a.title)}</label></div>`).join('');
  for(const a of ACTIONS.filter(a=>!a.required))$(`action-${a.id}`).onchange=e=>{state.pipeline=ACTIONS.filter(x=>x.required||$(`action-${x.id}`)?.checked).map(x=>x.id);invalidateTask();renderFlow();updateValidation();};
}
function renderConfig(){
  const p=state.item.policy;
  $('profile').textContent=state.local?`当前环境：${p.profile.label}。可调范围以本机运行版本为准。`:'当前为发行样例参数快照；本地连接后按实际授权加载可调范围。';
  $('controls').innerHTML=Object.entries(p.controls).filter(([key])=>key!=='objective').map(([key,c])=>`<label>${esc(c.label)}${c.unit?`（${esc(c.unit)}）`:''}<input aria-label="${esc(c.label)}" data-config="${esc(key)}" type="number" step="1" value="${state.config[key]}" ${c.supported?`min="${c.min}" max="${c.max}"`:'disabled'}><span>${c.supported?`${c.min} 至 ${c.max}`:esc(c.reason||'固定参数')}</span></label>`).join('');
  $('objectives').innerHTML=p.controls.objective.keys.map(key=>`<label>${esc(OBJECTIVES[key]||key)}<input type="number" step="any" data-objective="${esc(key)}" aria-label="${esc(OBJECTIVES[key]||key)}" value="${state.config.objective[key]}" ${p.controls.objective.supported?'':'disabled'}><span>${esc(key)} · 优化权重，非实际产量或时间</span></label>`).join('');
  document.querySelectorAll('[data-config],[data-objective]').forEach(input=>input.oninput=()=>{const value=input.value===''?NaN:Number(input.value);if(input.dataset.config)state.config[input.dataset.config]=value;else state.config.objective[input.dataset.objective]=value;invalidateTask();updateValidation();});
  updateValidation();
}
function renderRules(){
  $('ruleList').innerHTML=RULES.map(rule=>`<article><div class="title-row"><h3>${esc(rule.title)}</h3><span class="badge ${rule.preset?'':'warning'}">${esc(rule.status)}</span></div><p>${esc(rule.problem)}</p><p>${esc(rule.expression)}</p><p class="fields">${esc(rule.owner)} · ${esc(rule.fields)}</p><details><summary>验证要点</summary><p>${esc(rule.check)}</p></details>${rule.preset&&rule.dataset===state.item.id?`<button data-preset="${esc(rule.id)}">应用目标对比参数</button>`:''}</article>`).join('');
  document.querySelectorAll('[data-preset]').forEach(button=>button.onclick=()=>{const rule=RULES.find(r=>r.id===button.dataset.preset);Object.assign(state.config.objective,rule.preset);invalidateTask();renderConfig();activate('flow');show('目标参数已更新；尚未求解。');});
}
function selectCase(id){
  state.item=state.cases.find(c=>c.id===id)||state.cases[0];state.page=0;state.outPage=0;
  state.config=structuredClone(state.item.default_config);state.pipeline=[...state.item.recipe.pipeline];invalidateTask();
  $('dataset').value=state.item.id;$('caseQuestion').textContent=state.item.question;
  $('table').innerHTML=Object.entries(state.item.tables).map(([name,t])=>`<option value="${esc(name)}">${esc(name)} · ${t.count} 行</option>`).join('');
  if(state.item.tables.order_item)$('table').value='order_item';
  $('relations').innerHTML=state.item.relations.map(chain=>`<div class="relation"><strong>${esc(chain.title)}</strong>${chain.nodes.map(n=>`<code>${esc(n)}</code>`).join('<span aria-hidden="true">→</span>')}</div>`).join('');
  inputTable();diagnosis();renderFlow();renderConfig();renderRules();renderResults();
  $('runState').textContent=state.local?(currentRecords().baseline?'已载入当前场景的运行记录。':'当前场景尚未运行。'):'实际求解需使用本地工作台服务。';
  show('');
}
function outputTable(){
  const record=currentRecords()[$('resultVersion').value],p=record?.result.status==='ok'?record.result.planning_result:null;
  const rows=p?.rows||[],pages=Math.max(1,Math.ceil(rows.length/20));state.outPage=Math.min(state.outPage,pages-1);
  $('outputTable').innerHTML=rows.length?tableHTML(p.columns,rows.slice(state.outPage*20,(state.outPage+1)*20)):'<div class="empty">本版本尚无成功求解的计划结果</div>';
  $('outputCount').textContent=`当前返回 ${rows.length} 行${p?.count!==undefined&&p.count!==rows.length?` / 总计 ${p.count} 行`:''}`;
  $('outPage').textContent=`${state.outPage+1} / ${pages}`;$('outPrev').disabled=!state.outPage;$('outNext').disabled=state.outPage+1>=pages;
}
function trace(events){
  $('trace').innerHTML=events?.length?tableHTML(['动作','状态','开始后时间（秒）'],events.map(e=>({'动作':ACTIONS.find(a=>a.id.toUpperCase()===e.action?.toUpperCase())?.title||e.action,'状态':STATUS[e.status]||e.status,'开始后时间（秒）':e.at}))):'<div class="empty">尚无实际动作记录</div>';
}
function renderResults(){
  const records=currentRecords();
  $('runSummary').innerHTML=['baseline','candidate'].map((key,i)=>{const r=records[key]?.result;return `<div><h3>${i?'调整后':'基线'}</h3><p>${r?`${r.status==='ok'?'求解成功':esc(r.error||'求解未完成')}${r.code?` (${esc(r.code)})`:''}`:'等待运行'}</p>${r?`<p class="muted">耗时 ${format(r.elapsed_seconds)} 秒 · 输入${r.source_unchanged===true?'保持不变':r.source_unchanged===false?'发生变化':'未确认'}</p>`:''}</div>`;}).join('');
  const b=records.baseline,c=records.candidate,rows=[];
  if(b){
    const left=new Map(flatten(b.config)),right=new Map(c?flatten(c.config):[]);
    for(const [key,value] of left)rows.push({'项目':`参数 · ${key}`,'基线':format(value),'调整后':c?format(right.get(key)):'—','差异':c&&value!==right.get(key)?'已调整':'—'});
    rows.push({'项目':'标准动作','基线':b.pipeline.join(' → '),'调整后':c?.pipeline.join(' → ')||'—','差异':c&&b.pipeline.join()!==c.pipeline.join()?'已调整':'—'});
    if(b.result.status==='ok'){
      const first=new Map(flatten(b.result.production_analysis||{})),second=new Map(c?.result.status==='ok'?flatten(c.result.production_analysis||{}):[]);
      for(const [key,value] of first){if(typeof value!=='number'||/\.\d+(\.|$)/.test(key))continue;const other=second.get(key);rows.push({'项目':key,'基线':format(value),'调整后':format(other),'差异':typeof other==='number'?format(other-value):'—'});}
    }
  }
  $('comparison').innerHTML=rows.length?`<p class="muted">指标沿用运行版本的字段与单位；加权目标值不等同于实际产量或分钟数。${c&&b.result.data_sha256!==c.result.data_sha256?'输入版本不同，不应直接比较结果。':''}</p><div class="table-wrap result-table">${tableHTML(['项目','基线','调整后','差异'],rows)}</div><details><summary>完整分析与单位信息</summary><pre>${esc(JSON.stringify({baseline:b.result.production_analysis,candidate:c?.result.production_analysis},null,2))}</pre></details>`:'<div class="empty">完成基线与调整后运行后展示真实对比</div>';
  trace((c||b)?.result.action_events);outputTable();$('exportEvidence').disabled=!b&&!c;updateValidation();
}
async function run(kind){
  if(state.busy||!state.local||errors().length)return;
  const id=state.item.id,config=structuredClone(state.config),pipeline=[...state.pipeline];
  if(kind==='candidate'&&currentRecords().baseline?.result.status!=='ok')return;
  if(kind==='baseline'&&currentRecords().baseline&&!confirm('重新运行基线将清除当前场景的基线与调整后对比记录，是否继续？'))return;
  if(kind==='baseline')state.records[id]={};else delete state.records[id].candidate;
  state.busy=true;$('dataset').disabled=true;$('refresh').disabled=true;$('diagnose').disabled=true;renderResults();show('');
  $('runState').innerHTML='<p>实际运行中</p><div class="progress" aria-label="运行进行中"></div>';
  try{
    const queued=await api('/local/run',{dataset:id,pipeline,overrides:config});
    for(;;){
      const job=await api(`/local/jobs/${queued.job}`);trace(job.events);
      if(job.state==='finished'){
        state.records[id][kind]={config,pipeline,recorded_at:new Date().toISOString(),result:job.result};
        $('resultVersion').value=kind;$('runState').textContent=job.result.status==='ok'?'本次实际求解完成。':`本次运行未完成：${job.result.error||'请检查环境与参数'}`;break;
      }
      await new Promise(resolve=>setTimeout(resolve,700));
    }
  }catch(e){show(e.message,true);$('runState').textContent='连接或运行请求未完成，请检查本地服务。';}
  finally{state.busy=false;$('dataset').disabled=false;$('refresh').disabled=false;$('diagnose').disabled=false;renderResults();}
}
async function connect(){
  if(state.busy)return;
  $('refresh').disabled=true;show('');const previous=state.item?.id;state.local=false;
  try{
    let catalog;
    if(location.hostname==='127.0.0.1'){
      try{const environment=await api('/local/state');if(environment.mode==='local'){state.token=environment.token;catalog=await api('/local/catalog');state.local=true;}}catch{show('未连接本地运行服务，当前仅载入公开样例快照。');}
    }
    if(!catalog){const response=await fetch('../extensions/data/cases.json');if(!response.ok)throw new Error('样例资源加载失败');catalog=await response.json();}
    state.cases=catalog.cases;state.records={};$('connection').textContent=state.local?'本机运行环境已连接':'公开样例 · 未连接求解环境';
    $('dataset').innerHTML=state.cases.map(c=>`<option value="${esc(c.id)}">${esc(c.title)}</option>`).join('');
    selectCase(previous||new URLSearchParams(location.search).get('dataset'));
    $('runState').textContent=state.local?'尚未运行。':'实际求解需使用本地工作台服务。';
  }catch(e){show(e.message,true);$('connection').textContent='环境或样例未加载';}
  finally{$('refresh').disabled=false;}
}
$('dataset').onchange=()=>selectCase($('dataset').value);$('refresh').onclick=connect;
$('table').onchange=()=>{state.page=0;inputTable();};$('pageSize').onchange=()=>{state.page=0;inputTable();};
$('prev').onclick=()=>{state.page--;inputTable();};$('next').onclick=()=>{state.page++;inputTable();};
$('outPrev').onclick=()=>{state.outPage--;outputTable();};$('outNext').onclick=()=>{state.outPage++;outputTable();};$('resultVersion').onchange=()=>{state.outPage=0;outputTable();};
$('resetFlow').onclick=()=>{state.config=structuredClone(state.item.default_config);state.pipeline=[...state.item.recipe.pipeline];invalidateTask();renderFlow();renderConfig();};
$('exportRecipe').onclick=()=>download('recipe.json',JSON.stringify(configuredRecipe(state.item,state.config,state.pipeline),null,2));
$('exportDiagnosis').onclick=()=>download(`${state.item.id}-diagnosis.json`,JSON.stringify({mode:state.local?'local':'public-snapshot',...state.item.diagnosis},null,2));
$('diagnose').onclick=async()=>{if(!state.item)return;if(!state.local){show('公开页展示发行样例诊断快照；重新检查需启动本地工作台。');return;}try{$('diagnose').disabled=true;const d=await api('/local/diagnose',{dataset:state.item.id});if(d.status!=='ok')throw new Error(d.error);state.item.diagnosis=d;diagnosis();updateValidation();show(d.stage==='data_checked'?'数据检查通过；实际可行性仍需求解确认。':'数据检查存在阻断项。');}catch(e){show(e.message,true);}finally{$('diagnose').disabled=false;}};
$('baseline').onclick=()=>run('baseline');$('rerun').onclick=()=>run('candidate');
$('exportEvidence').onclick=()=>download(`${state.item.id}-evidence.json`,JSON.stringify({schema:'sandbox.evidence.v1',dataset:state.item.id,mode:'local',diagnosis:state.item.diagnosis,...currentRecords()},null,2));
$('intent').oninput=invalidateTask;
$('makeTask').onclick=()=>{state.tasks=taskFiles(state.item,state.config,state.pipeline,$('intent').value.trim());$('taskFiles').innerHTML=Object.keys(state.tasks).map((n,i)=>`<button data-file="${i}">${esc(n)}</button>`).join(' ');$('taskPreview').textContent=state.tasks['AGENT_TASK.md'];document.querySelectorAll('[data-file]').forEach(b=>b.onclick=()=>$('taskPreview').textContent=Object.values(state.tasks)[Number(b.dataset.file)]);$('exportTask').disabled=false;};
$('exportTask').onclick=()=>{if(state.tasks)download(`${state.item.id}-agent-task.zip`,zip(state.tasks),'application/zip');};
const taskIndex=new URLSearchParams(location.search).get('task');if(taskIndex!==null&&TASKS[Number(taskIndex)])$('intent').value=TASKS[Number(taskIndex)][1];
activate(location.hash.slice(1));connect();
