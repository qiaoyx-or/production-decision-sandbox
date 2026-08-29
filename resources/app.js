import {ACTIONS,escapeHTML as e} from '../extensions/core.js';
import {RULES,TASKS} from '../extensions/rules.js';
const $=id=>document.getElementById(id);
$('actions').innerHTML=ACTIONS.map(a=>`<div class="node"><strong>${e(a.title)}</strong><small>${e(a.input)} → ${e(a.output)}</small></div>`).join('');
function renderRules(){
  const search=$('ruleSearch').value.trim().toLowerCase(),filter=$('ruleFilter').value;
  const list=RULES.filter(r=>(!filter||r.status===filter)&&JSON.stringify(r).toLowerCase().includes(search));
  $('ruleList').innerHTML=list.map(r=>`<article class="item"><span class="badge ${r.preset?'':'warning'}">${e(r.status)}</span><h3>${e(r.title)}</h3><p>${e(r.problem)}</p><details><summary>表达与验证</summary><p>${e(r.expression)}</p><p>${e(r.check)}</p><p class="meta">${e(r.owner)}<br>${e(r.fields)}</p></details>${r.preset?`<a href="../workbench/?dataset=${e(r.dataset)}&rule=${e(r.id)}#rules">在样例中比较 →</a>`:''}</article>`).join('')||'<p class="empty">没有匹配的案例</p>';
}
$('ruleSearch').addEventListener('input',renderRules);$('ruleFilter').addEventListener('change',renderRules);renderRules();
$('agentList').innerHTML=TASKS.map(([title,task],i)=>`<article><h3>${e(title)}</h3><p>${e(task)}</p><a href="../workbench/?task=${i}#agent">生成任务包 →</a></article>`).join('');
fetch('../extensions/data/cases.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
  $('caseList').innerHTML=data.cases.map(c=>`<article class="item"><span class="badge">输入快照 · ${e(c.diagnosis.stage==='data_checked'?'结构关系检查通过':'含待处理项')}</span><h3>${e(c.title)}</h3><p>${e(c.question)}</p><p class="meta">${Object.keys(c.tables).length} 张输入表 · ${Object.values(c.tables).reduce((s,t)=>s+t.count,0).toLocaleString()} 条记录</p><a href="../workbench/?dataset=${e(c.id)}#data">查看数据与流程 →</a></article>`).join('');
}).catch(()=>{$('caseList').innerHTML='<p role="alert">样例快照暂不可用，请检查发布文件。</p>';});
