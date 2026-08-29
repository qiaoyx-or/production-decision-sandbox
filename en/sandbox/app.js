const state = {
  dataset: "demoA",
  scenario: "schedule",
  dueWeight: 70,
  maintenanceWeight: 60,
  activeStep: 0,
  runCount: 0
};

const datasetProfiles = {
  demoA: { quality: 86, due: 91, load: 78, templates: 4, label: "Discrete Manufacturing Demo A" },
  demoB: { quality: 82, due: 87, load: 73, templates: 5, label: "Maintenance-Sensitive Demo B" },
  demoC: { quality: 79, due: 84, load: 82, templates: 3, label: "Due-Date Pressure Demo C" }
};

const readinessBase = [
  ["Order Data", "order ID, due date, quantity, priority", "ok"],
  ["Products and BOM", "products, materials, and quantity relationships", "ok"],
  ["Process Routes", "operation sequence and work-center mapping", "ok"],
  ["Resource Calendar", "shifts, downtime, and maintenance windows", "warn"],
  ["Material Availability", "inventory, in-transit supply, and shortage risk", "warn"],
  ["Objectives and Rules", "due dates, load, and maintenance avoidance", "ok"]
];

const businessNodes = [
  { id: "Orders", sub: "due date / priority", x: 36, y: 36, tone: "blue" },
  { id: "Products", sub: "model / batch", x: 270, y: 36, tone: "blue" },
  { id: "BOM", sub: "material / quantity", x: 504, y: 36, tone: "amber" },
  { id: "Process", sub: "operation route", x: 270, y: 176, tone: "green" },
  { id: "Resources", sub: "equipment / work center", x: 504, y: 176, tone: "green" },
  { id: "Calendar", sub: "shift / maintenance", x: 270, y: 316, tone: "purple" },
  { id: "Inventory", sub: "availability / shortage", x: 504, y: 316, tone: "purple" }
];

const businessEdges = [
  { path: "M 180 78 H 270", label: "Demand", x: 225, y: 66 },
  { path: "M 414 78 H 504", label: "Material", x: 459, y: 66 },
  { path: "M 342 120 V 176", label: "Route", x: 385, y: 150 },
  { path: "M 414 218 H 504", label: "Capability", x: 459, y: 206 },
  { path: "M 342 316 V 260", label: "Availability", x: 385, y: 290 },
  { path: "M 648 358 H 668 V 78 H 648", label: "Material Check", x: 630, y: 289 }
];

const timelineData = [
  { row: "WC-01", blocks: [[5, 22, "O-102", "blue"], [28, 20, "O-108", "green"], [56, 16, "Maintenance", "maint"]] },
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
    const score = status === "ok" ? "Ready" : status === "warn" ? "Review" : "High Priority";
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
    '<title id="businessMapTitle">Manufacturing Business Object Relationship Map</title>',
    '<desc id="businessMapDesc">Orders relate to products; products connect material structures and manufacturing routes; processes use production resources constrained by calendars, while material structures are constrained by availability.</desc>',
    '<defs><marker id="business-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L8,4 L0,8 Z"></path></marker></defs>',
    '<g class="business-edges">', edges, '</g>',
    '<g class="business-nodes">', nodes, '</g>',
    '</svg>'
  ].join("");
}

function renderControlBars() {
  const bars = [
    ["Due-Date Priority", state.dueWeight, "customer commitments, order priority, delay risk"],
    ["Maintenance Avoidance", state.maintenanceWeight, "equipment service, downtime windows, resource availability"],
    ["Load Balancing", clamp(100 - Math.abs(state.dueWeight - 62), 35, 88), "bottleneck equipment, shift load, peak control"],
    ["Human Review Rules", clamp(58 + state.runCount * 8, 58, 82), "preserve shop-floor judgment, accountability, and exception handling"],
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
  const scenarioText = state.scenario === "schedule" ? "The current schedule avoids major maintenance windows. Review peak load on WC-03." : state.scenario === "capacity" ? "Capacity analysis shows a temporary peak on WC-02. Consider splitting orders or adjusting shifts." : "Material availability risk is concentrated in key material groups. Add in-transit and substitute-material rules in the next cycle.";
  const items = [
    ["Bottleneck Location", "Peak resource load is " + p.load + "%. The main bottleneck comes from concentrated order release overlapping maintenance windows."],
    ["Due-Date Review", "Due-date fulfillment is " + p.due + "%. Increasing due-date weight may reduce delays but increase local resource pressure."],
    ["Next-Cycle Recommendation", scenarioText],
    ["Template Retention", "This cycle can retain reusable templates for data checks, scenario configuration, capability orchestration, and analysis reports."]
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
  button.textContent = running ? "Sandbox Running..." : "Run Sandbox Validation";
}

function runSandbox() {
  clearRunTimers();
  setRunning(true);
  state.runCount += 1;
  state.activeStep = 0;
  const log = document.getElementById("runLog");
  const steps = ["Connect Data", "Represent Business", "Configure Rules", "Controlled Optimization", "Analyze Results", "Iterate with Feedback"];
  log.textContent = "Sandbox running: " + steps[0] + "...";
  render();
  steps.forEach((step, index) => {
    const timerId = setTimeout(() => {
      state.activeStep = index;
      log.textContent = "Sandbox running: " + steps.slice(0, index + 1).join(" → ");
      render();
      if (index === steps.length - 1) {
        const dataLabel = datasetProfiles[state.dataset].label;
        const sceneLabel = document.getElementById("scenarioSelect").selectedOptions[0].textContent;
        log.textContent = "Run complete: " + dataLabel + " / " + sceneLabel + " produced data-quality checks, capability orchestration, scheduling results, and next-cycle recommendations.";
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
  document.getElementById("runLog").textContent = "Ready: select a dataset and scenario, then click Run Sandbox Validation.";
  render();
}

document.getElementById("datasetSelect").addEventListener("change", event => { state.dataset = event.target.value; render(); });
document.getElementById("scenarioSelect").addEventListener("change", event => { state.scenario = event.target.value; render(); });
document.getElementById("dueWeight").addEventListener("input", event => { state.dueWeight = Number(event.target.value); render(); });
document.getElementById("maintenanceWeight").addEventListener("input", event => { state.maintenanceWeight = Number(event.target.value); render(); });
document.getElementById("runSandbox").addEventListener("click", runSandbox);
document.getElementById("resetSandbox").addEventListener("click", resetSandbox);

render();
