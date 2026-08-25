const state = {
  dataset: "demoA",
  scenario: "schedule",
  dueWeight: 70,
  maintenanceWeight: 60,
  activeStep: 0,
  runCount: 0
};

const datasetProfiles = {
  demoA: { quality: 86, due: 91, load: 78, templates: 4, label: "离散制造样例 A" },
  demoB: { quality: 82, due: 87, load: 73, templates: 5, label: "维护窗口敏感样例 B" },
  demoC: { quality: 79, due: 84, load: 82, templates: 3, label: "交期压力样例 C" }
};

const readinessBase = [
  ["订单数据", "订单号、交期、数量、优先级", "ok"],
  ["产品与 BOM", "产品、物料、用量关系", "ok"],
  ["工艺路线", "工序顺序、工作中心映射", "ok"],
  ["资源日历", "班制、停机、维护窗口", "warn"],
  ["库存齐套", "库存、在途、缺料风险", "warn"],
  ["目标与规则", "交期、负载、维护避让", "ok"]
];

const businessNodes = [
  { id: "订单", sub: "交期 / 优先级", x: 36, y: 36, tone: "blue" },
  { id: "产品", sub: "型号 / 批量", x: 270, y: 36, tone: "blue" },
  { id: "BOM", sub: "物料 / 用量", x: 504, y: 36, tone: "amber" },
  { id: "工艺", sub: "工序路线", x: 270, y: 176, tone: "green" },
  { id: "资源", sub: "设备 / 工作中心", x: 504, y: 176, tone: "green" },
  { id: "日历", sub: "班制 / 维护", x: 270, y: 316, tone: "purple" },
  { id: "库存", sub: "齐套 / 短缺", x: 504, y: 316, tone: "purple" }
];

const businessEdges = [
  { path: "M 180 78 H 270", label: "需求对象", x: 225, y: 66 },
  { path: "M 414 78 H 504", label: "物料结构", x: 459, y: 66 },
  { path: "M 342 120 V 176", label: "制造路线", x: 385, y: 150 },
  { path: "M 414 218 H 504", label: "能力适配", x: 459, y: 206 },
  { path: "M 342 316 V 260", label: "可用时段", x: 385, y: 290 },
  { path: "M 648 358 H 668 V 78 H 648", label: "齐套约束", x: 630, y: 289 }
];

const timelineData = [
  { row: "WC-01", blocks: [[5, 22, "O-102", "blue"], [28, 20, "O-108", "green"], [56, 16, "维护", "maint"]] },
  { row: "WC-02", blocks: [[10, 20, "O-103", "amber"], [36, 30, "O-112", "blue"]] },
  { row: "WC-03", blocks: [[0, 18, "O-101", "purple"], [24, 24, "O-107", "green"], [58, 24, "O-118", "blue"]] },
  { row: "WC-04", blocks: [[14, 18, "O-105", "blue"], [44, 28, "O-120", "amber"]] }
];

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function profile() {
  const base = datasetProfiles[state.dataset];
  const scenarioBoost = state.scenario === "schedule" ? 2 : state.scenario === "capacity" ? -1 : -3;
  const dueTension = Math.round((state.dueWeight - 60) / 6);
  const maintenanceBoost = Math.round((state.maintenanceWeight - 50) / 8);
  return {
    quality: clamp(base.quality + (state.runCount > 0 ? 2 : 0), 72, 96),
    due: clamp(base.due + scenarioBoost + dueTension - Math.max(0, maintenanceBoost - 2), 68, 98),
    load: clamp(base.load - dueTension + maintenanceBoost, 58, 92),
    templates: base.templates + (state.runCount > 0 ? 1 : 0)
  };
}

function renderKpis() {
  const p = profile();
  document.getElementById("qualityScore").textContent = p.quality + "%";
  document.getElementById("dueScore").textContent = p.due + "%";
  document.getElementById("loadScore").textContent = p.load + "%";
  document.getElementById("templateScore").textContent = p.templates;
}

function renderReadiness() {
  const list = document.getElementById("readinessList");
  const rows = readinessBase.map((item, index) => {
    let status = item[2];
    if (state.dataset === "demoC" && index === 4) status = "risk";
    if (state.dataset === "demoB" && index === 3) status = "risk";
    const score = status === "ok" ? "已闭合" : status === "warn" ? "需复核" : "高优先级";
    return '<div class="readiness-item ' + status + '"><i class="check-dot"></i><div><strong>' + item[0] + '</strong><span>' + item[1] + '</span></div><em>' + score + '</em></div>';
  });
  list.innerHTML = rows.join("");
}

function renderBusinessMap() {
  const map = document.getElementById("businessMap");
  const edges = businessEdges.map(edge => [
    '<path class="business-edge" d="', edge.path, '" marker-end="url(#business-arrow)"></path>',
    '<g class="edge-label" transform="translate(', edge.x, ' ', edge.y, ')">',
    '<rect x="-38" y="-12" width="76" height="24" rx="12"></rect>',
    '<text text-anchor="middle" dominant-baseline="central">', edge.label, '</text>',
    '</g>'
  ].join("")).join("");
  const nodes = businessNodes.map(node => [
    '<g class="business-node ', node.tone, '" transform="translate(', node.x, ' ', node.y, ')">',
    '<rect width="144" height="84" rx="18"></rect>',
    '<text class="node-title" x="18" y="31">', node.id, '</text>',
    '<text class="node-subtitle" x="18" y="58">', node.sub, '</text>',
    '</g>'
  ].join("")).join("");

  map.innerHTML = [
    '<svg class="business-map-svg" viewBox="0 0 684 436" role="img" aria-labelledby="businessMapTitle businessMapDesc">',
    '<title id="businessMapTitle">制造业务对象关系图</title>',
    '<desc id="businessMapDesc">订单关联产品，产品连接物料结构和制造路线；工艺适配生产资源，资源受日历约束，物料结构受库存齐套约束。</desc>',
    '<defs><marker id="business-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 Z"></path></marker></defs>',
    '<g class="business-edges">', edges, '</g>',
    '<g class="business-nodes">', nodes, '</g>',
    '</svg>'
  ].join("");
}

function renderControlBars() {
  const bars = [
    ["交期优先", state.dueWeight, "客户承诺、订单优先级、延期风险"],
    ["维护避让", state.maintenanceWeight, "设备保养、停机窗口、资源可用性"],
    ["负载均衡", clamp(100 - Math.abs(state.dueWeight - 62), 35, 88), "瓶颈设备、班制负载、峰值控制"],
    ["人工复核规则", clamp(58 + state.runCount * 8, 58, 82), "保留现场判断、责任分工和异常处置"],
  ];
  document.getElementById("controlBars").innerHTML = bars.map(b => '<div class="control-bar"><strong>' + b[0] + '<span>' + b[1] + '%</span></strong><div class="bar-track"><div class="bar-fill" style="width:' + b[1] + '%"></div></div><small>' + b[2] + '</small></div>').join("");
}

function renderTimeline() {
  const offset = state.runCount % 2 === 0 ? 0 : 4;
  document.getElementById("timeline").innerHTML = timelineData.map(row => {
    const blocks = row.blocks.map(block => '<span class="time-block ' + block[3] + '" style="left:' + clamp(block[0] + offset, 0, 84) + '%;width:' + block[1] + '%">' + block[2] + '</span>').join("");
    return '<div class="timeline-row"><b>' + row.row + '</b><div class="time-lane">' + blocks + '</div></div>';
  }).join("");
}

function renderAnalysis() {
  const p = profile();
  const scenarioText = state.scenario === "schedule" ? "当前排程结果已避开主要维护窗口，建议重点复核 WC-03 的峰值负载。" : state.scenario === "capacity" ? "当前产能分析显示 WC-02 存在阶段性峰值，建议拆分部分订单或调整班制。" : "当前齐套风险集中在关键物料组，建议下一轮补充在途与替代料规则。";
  const items = [
    ["瓶颈定位", "资源峰值负载为 " + p.load + "% ，瓶颈主要来自订单集中释放与维护窗口叠加。"],
    ["交期复核", "交期满足率为 " + p.due + "% ，提高交期权重会改善延期，但可能增加局部资源压力。"],
    ["下一轮建议", scenarioText],
    ["模板沉淀", "本轮可沉淀数据检查、场景配置、能力编排与分析报告模板。"]
  ];
  document.getElementById("analysisStack").innerHTML = items.map(i => '<div class="analysis-item"><strong>' + i[0] + '</strong><p>' + i[1] + '</p></div>').join("");
}

function renderChain() {
  document.querySelectorAll(".chain-node").forEach(node => {
    node.classList.toggle("active", Number(node.dataset.step) <= state.activeStep);
  });
}

function render() {
  document.getElementById("dueWeightText").textContent = state.dueWeight;
  document.getElementById("maintenanceText").textContent = state.maintenanceWeight;
  renderKpis();
  renderReadiness();
  renderBusinessMap();
  renderControlBars();
  renderTimeline();
  renderAnalysis();
  renderChain();
}

let runTimerIds = [];

function clearRunTimers() {
  runTimerIds.forEach(timerId => clearTimeout(timerId));
  runTimerIds = [];
}

function setRunning(running) {
  const button = document.getElementById("runSandbox");
  button.disabled = running;
  button.textContent = running ? "沙盘运行中..." : "运行沙盘验证";
}

function runSandbox() {
  clearRunTimers();
  setRunning(true);
  state.runCount += 1;
  state.activeStep = 0;
  const log = document.getElementById("runLog");
  const steps = ["接入数据", "业务表达", "设置规则", "受控求解", "结果分析", "反馈迭代"];
  log.textContent = "沙盘运行中：" + steps[0] + "...";
  render();
  steps.forEach((step, index) => {
    const timerId = setTimeout(() => {
      state.activeStep = index;
      log.textContent = "沙盘运行中：" + steps.slice(0, index + 1).join(" → ");
      render();
      if (index === steps.length - 1) {
        const dataLabel = datasetProfiles[state.dataset].label;
        const sceneLabel = document.getElementById("scenarioSelect").selectedOptions[0].textContent;
        log.textContent = "运行完成：" + dataLabel + " / " + sceneLabel + " 已形成数据质量、能力编排、排程结果与下一轮建议。";
        runTimerIds = [];
        setRunning(false);
      }
    }, 360 * (index + 1));
    runTimerIds.push(timerId);
  });
}

function resetSandbox() {
  clearRunTimers();
  setRunning(false);
  state.dataset = "demoA";
  state.scenario = "schedule";
  state.dueWeight = 70;
  state.maintenanceWeight = 60;
  state.activeStep = 0;
  state.runCount = 0;
  document.getElementById("datasetSelect").value = state.dataset;
  document.getElementById("scenarioSelect").value = state.scenario;
  document.getElementById("dueWeight").value = state.dueWeight;
  document.getElementById("maintenanceWeight").value = state.maintenanceWeight;
  document.getElementById("runLog").textContent = "等待运行：选择数据集与场景后，点击“运行沙盘验证”。";
  render();
}

document.getElementById("datasetSelect").addEventListener("change", event => { state.dataset = event.target.value; render(); });
document.getElementById("scenarioSelect").addEventListener("change", event => { state.scenario = event.target.value; render(); });
document.getElementById("dueWeight").addEventListener("input", event => { state.dueWeight = Number(event.target.value); render(); });
document.getElementById("maintenanceWeight").addEventListener("input", event => { state.maintenanceWeight = Number(event.target.value); render(); });
document.getElementById("runSandbox").addEventListener("click", runSandbox);
document.getElementById("resetSandbox").addEventListener("click", resetSandbox);

render();
