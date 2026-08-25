export type ScenarioKey = 'scheduling' | 'capacity' | 'material' | 'maintenance'

export type DatasetKey = 'discreteA' | 'maintenanceB' | 'dueC'

export interface DatasetProfile {
  key: DatasetKey
  name: string
  industry: string
  description: string
  dataQuality: number
  dueRate: number
  loadPeak: number
  templateCount: number
  risk: string
}

export interface ApsObject {
  key: string
  name: string
  category: string
  readiness: 'ready' | 'review' | 'risk'
  count: number
  fields: string
  note: string
}

export interface WorkOrder {
  id: string
  resource: string
  item: string
  start: string
  end: string
  type: 'normal' | 'urgent' | 'maintenance' | 'waiting'
  progress: number
}

export interface ScenarioProfile {
  key: ScenarioKey
  name: string
  objective: string
  description: string
  emphasis: string[]
}

export const datasets: DatasetProfile[] = [
  {
    key: 'discreteA',
    name: '离散制造样例 A',
    industry: '装备部件 / 多工序装配',
    description: '订单、BOM、工艺路线、资源日历基本闭合，适合展示端到端排程验证。',
    dataQuality: 88,
    dueRate: 91,
    loadPeak: 76,
    templateCount: 4,
    risk: '资源峰值集中在 WC-03，需要复核班制与换型窗口。',
  },
  {
    key: 'maintenanceB',
    name: '维护窗口敏感样例 B',
    industry: '设备密集型加工',
    description: '维护计划与工作日历影响明显，适合展示边界控制和维护避让。',
    dataQuality: 83,
    dueRate: 87,
    loadPeak: 81,
    templateCount: 5,
    risk: '维护窗口占用关键设备，局部订单存在跨班组等待。',
  },
  {
    key: 'dueC',
    name: '交期压力样例 C',
    industry: '小批量多品种',
    description: '订单交期紧、优先级差异大，适合展示目标系统与多方案对比。',
    dataQuality: 79,
    dueRate: 82,
    loadPeak: 85,
    templateCount: 3,
    risk: '交期压力会把资源推向高负载，需要平衡延期与稳定性。',
  },
]

export const scenarios: ScenarioProfile[] = [
  {
    key: 'scheduling',
    name: '车间作业排程',
    objective: '在资源、工艺、日历和维护边界内形成可复核排程。',
    description: '关注工序顺序、设备占用、换型、等待与交期满足。',
    emphasis: ['有限产能', '工序依赖', '设备日历', '瓶颈解释'],
  },
  {
    key: 'capacity',
    name: '产能负载分析',
    objective: '识别瓶颈资源、峰值负载和班制调整空间。',
    description: '关注工作中心负载、能力缺口、订单释放节奏与异常峰值。',
    emphasis: ['负载曲线', '瓶颈资源', '班制窗口', '释放节奏'],
  },
  {
    key: 'material',
    name: '齐套与交期复核',
    objective: '把物料短缺、库存和在途信息纳入交期承诺复核。',
    description: '关注 BOM、库存、在途、短缺和订单优先级。',
    emphasis: ['BOM 关系', '库存齐套', '短缺风险', '交期承诺'],
  },
  {
    key: 'maintenance',
    name: '维护计划影响分析',
    objective: '把设备维护、停机和生产节奏放入同一决策边界。',
    description: '关注维护窗口、资源不可用、替代资源和计划稳定性。',
    emphasis: ['维护窗口', '资源可用性', '计划稳定', '边界控制'],
  },
]

export const apsObjects: ApsObject[] = [
  { key: 'demand', name: 'Demand / 订单需求', category: '需求层', readiness: 'ready', count: 126, fields: '订单号、交期、数量、优先级、客户', note: '参考 frePPLe 的 demand 视角，强调需求驱动计划。' },
  { key: 'item', name: 'Item / 产品物料', category: '物料层', readiness: 'ready', count: 284, fields: '物料编码、类型、批量、提前期', note: '承接 BOM、库存和工艺路线。' },
  { key: 'bom', name: 'BOM / 物料清单', category: '物料层', readiness: 'review', count: 512, fields: '父项、子项、用量、损耗、替代关系', note: '齐套分析和交期复核的关键入口。' },
  { key: 'operation', name: 'Operation / 工序', category: '模型层', readiness: 'ready', count: 178, fields: '工序、顺序、加工时间、准备时间', note: '参考 APS 常见工艺/工序组织方式。' },
  { key: 'resource', name: 'Resource / 资源设备', category: '资源层', readiness: 'ready', count: 42, fields: '工作中心、设备、能力、技能、效率', note: '可表达主资源与副资源。' },
  { key: 'calendar', name: 'Calendar / 班制日历', category: '边界层', readiness: 'review', count: 18, fields: '班次、可用时间、例外日、维护窗口', note: '生产班制和维护计划是 APS 隐藏基础。' },
  { key: 'inventory', name: 'Inventory / 库存齐套', category: '执行层', readiness: 'risk', count: 96, fields: '库存、在途、锁定、短缺、安全库存', note: '当前样例中仍有缺口，适合进入下一轮数据共建。' },
  { key: 'result', name: 'Plan Result / 结果快照', category: '反馈层', readiness: 'ready', count: 6, fields: '计划、排程、负载、延期、瓶颈、异常', note: '沉淀为报告与模板，不只展示甘特图。' },
]

export const workOrders: WorkOrder[] = [
  { id: 'MO-1007', resource: 'WC-01', item: 'A12 轴承座', start: '2026-08-14 08:00', end: '2026-08-14 11:30', type: 'normal', progress: 82 },
  { id: 'MO-1012', resource: 'WC-01', item: 'B07 支架', start: '2026-08-14 13:00', end: '2026-08-14 16:40', type: 'urgent', progress: 64 },
  { id: 'MT-01', resource: 'WC-01', item: '设备维护', start: '2026-08-14 17:00', end: '2026-08-14 19:00', type: 'maintenance', progress: 100 },
  { id: 'MO-1008', resource: 'WC-02', item: 'C21 壳体', start: '2026-08-14 09:00', end: '2026-08-14 14:20', type: 'normal', progress: 76 },
  { id: 'MO-1016', resource: 'WC-02', item: 'A12 轴承座', start: '2026-08-14 15:00', end: '2026-08-14 20:30', type: 'waiting', progress: 38 },
  { id: 'MO-1020', resource: 'WC-03', item: 'D03 箱体', start: '2026-08-14 08:30', end: '2026-08-14 13:10', type: 'urgent', progress: 71 },
  { id: 'MO-1024', resource: 'WC-03', item: 'E19 总成', start: '2026-08-14 13:40', end: '2026-08-14 21:20', type: 'normal', progress: 55 },
  { id: 'MO-1028', resource: 'WC-04', item: 'F06 连接件', start: '2026-08-14 10:00', end: '2026-08-14 15:00', type: 'normal', progress: 68 },
]

export const resourceLoad = [
  { resource: 'WC-01', load: 72, available: 88, risk: 38 },
  { resource: 'WC-02', load: 84, available: 86, risk: 52 },
  { resource: 'WC-03', load: 91, available: 94, risk: 73 },
  { resource: 'WC-04', load: 68, available: 80, risk: 31 },
  { resource: 'WC-05', load: 57, available: 78, risk: 22 },
]

export const scenarioCompare = [
  { name: '当前方案', due: 88, load: 81, stable: 74, shortage: 28 },
  { name: '交期优先', due: 94, load: 90, stable: 66, shortage: 31 },
  { name: '维护避让', due: 86, load: 76, stable: 84, shortage: 24 },
  { name: '均衡方案', due: 91, load: 79, stable: 81, shortage: 25 },
]

export const openSourceReferences = [
  { name: 'frePPLe', value: '借鉴对象模型、数据导入向导、计划任务、ERP 集成与计划员日常工作流。' },
  { name: 'SuperAPS / iSuperAPS', value: '借鉴多工厂、多资源、库存、工作日历、甘特调整等传统 APS 功能清单。' },
  { name: 'OpenMES / ERP 类系统', value: '借鉴工单、产线、设备和生产执行侧面板，但不把沙盘做成 MES。' },
]

export const dataReadinessFunnel = [
  { stage: '原始业务数据', value: 100, note: '客户 ERP / MES / Excel / 接口导出' },
  { stage: '标准对象映射', value: 86, note: '进入 Demand、Item、BOM、Operation、Resource 等对象' },
  { stage: '业务关系闭合', value: 74, note: '订单、物料、工艺、资源、日历之间形成可计算关系' },
  { stage: '可求解输入', value: 68, note: '具备目标、边界、时间窗口与运行参数' },
  { stage: '可复核结果', value: 61, note: '结果能解释负载、交期、瓶颈、异常与下一轮调整' },
]

export const fieldMappings = [
  { key: 'order-no', source: 'sale_order.order_no', target: 'Demand.code', meaning: '订单唯一标识', status: 'ready', rule: '去重后作为需求主键' },
  { key: 'due-date', source: 'sale_order.due_date', target: 'Demand.due', meaning: '客户承诺交期', status: 'ready', rule: '统一到分钟级时间戳' },
  { key: 'bom-child', source: 'bom_component.material_code', target: 'BOM.component', meaning: '子项物料', status: 'review', rule: '需补充替代料和损耗率' },
  { key: 'route-op', source: 'process_route.operation_seq', target: 'Operation.sequence', meaning: '工序顺序', status: 'ready', rule: '按产品与版本关联' },
  { key: 'work-center', source: 'equipment.work_center', target: 'Resource.group', meaning: '工作中心', status: 'ready', rule: '设备归属到可用资源组' },
  { key: 'calendar-stop', source: 'maintenance.stop_window', target: 'Calendar.exception', meaning: '维护停机窗口', status: 'review', rule: '需确认是否影响全部设备' },
  { key: 'inventory-lock', source: 'stock.lock_qty', target: 'Inventory.reserved', meaning: '锁定库存', status: 'risk', rule: '锁定逻辑不清会影响齐套判断' },
]

export const dataQualityIssues = [
  { key: 'issue-calendar', level: 'review', object: 'Calendar', issue: '班制与维护计划存在交叉窗口', action: '确认维护窗口是否覆盖整台设备或单工装', owner: '客户设备/计划团队' },
  { key: 'issue-inventory', level: 'risk', object: 'Inventory', issue: '锁定库存与可用库存口径不一致', action: '补充库存口径说明，区分可用、锁定、在途', owner: '客户仓储/ERP 团队' },
  { key: 'issue-bom', level: 'review', object: 'BOM', issue: '部分物料存在替代料但未进入结构化字段', action: '建立替代料字段或在场景说明中声明', owner: '客户工艺/物控团队' },
  { key: 'issue-route', level: 'ready', object: 'Operation', issue: '主工艺路线完整，但返工/外协路径需作为扩展场景', action: '首轮试点先冻结主路线，第二轮补充外协边界', owner: '试点双方' },
]

export const pilotChecklist = [
  { title: '数据能否进入', detail: '字段、格式、脱敏、主键和映射关系可以被沙盘识别。' },
  { title: '业务是否闭合', detail: '订单、产品、BOM、工艺、资源、日历、库存之间能形成可计算链路。' },
  { title: '边界是否明确', detail: '目标偏好、维护窗口、资源能力、交期承诺和例外规则有明确口径。' },
  { title: '结果能否复核', detail: '输出不止甘特图，还能解释负载、瓶颈、延期、短缺和下一轮调整。' },
]

export const pilotOutputs = [
  { title: '数据质量报告', status: '已形成', detail: '识别必填字段、业务关系、异常数据和下一轮补充项。' },
  { title: '场景配置快照', status: '已形成', detail: '记录当前数据集、验证场景、目标权重、维护避让和求解边界。' },
  { title: '运行结果快照', status: '演示数据', detail: '形成资源负载、排程时间轴、方案对比和瓶颈说明。' },
  { title: '模板沉淀建议', status: '可沉淀', detail: '沉淀数据准备模板、字段映射模板、场景模板和试点报告模板。' },
]

export const templateAssets = [
  { name: '数据准备模板', value: '客户需要提供的字段、格式、脱敏要求与业务说明。' },
  { name: '字段映射模板', value: '客户字段到 DecisioWorks 标准对象的映射关系。' },
  { name: '场景配置模板', value: '计划范围、资源范围、时间窗口、目标偏好和约束启停。' },
  { name: '能力编排模板', value: '数据校验、业务表达、边界控制、求解调用、结果分析的流程节点。' },
  { name: '试点报告模板', value: '试点结论、数据缺口、结果解释、下一轮建议与责任边界。' },
]

