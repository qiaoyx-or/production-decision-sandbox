export const RULES = [
  {id:'planning_wait',title:'等待与交付的取舍',dataset:'production_planning',status:'参数实验',owner:'objective_system',problem:'等待压缩与需求偏差的目标并不总是同向。保留同一份输入，观察权重变化怎样影响计划。',fields:'order_item、capacity、process_adaptor',expression:'保留 job_bias；仅把 waittime 权重由 1 调整为 0.5。',preset:{waittime:.5},check:'对照需求满足、短缺、工作中心负荷和等待，不把加权目标值当成实际时间。'},
  {id:'color_switch',title:'同类制品连续生产',dataset:'production_scheduling',status:'参数实验',owner:'objective_system / engine_adapters',problem:'颜色切换与循环容量条件共同影响排程，单独追求少切换可能改变等待与序列。',fields:'product.property_1、product.property_3、process_adaptor',expression:'沿用样例颜色与容量映射；把 color 权重调整为 0.2。',preset:{color:.2},check:'比较序列、切换统计和约束审计，确认任务数量及资源条件仍成立。'},
  {id:'maintenance',title:'维护窗口与生产班制',status:'接入案例',owner:'data_layer / 结构约束',problem:'设备维护或班制变化会改变特定时间内可用于生产的资源。',fields:'time_unit、workcenter、capacity',expression:'先统一时间坐标，再表达对应工作中心的可用能力与已用比例。具体取值以接口手册及实际班制为准。',check:'检查时间引用、capacity.used 的比例语义和资源负荷；当前工作台保持数据只读。'},
  {id:'freeze',title:'冻结窗口与局部调整',status:'规则案例',owner:'marginal_control / planning_system',problem:'扰动发生后，已承诺或已准备的任务需要保留，其他任务才进入调整范围。',fields:'已确认任务、冻结时间窗、计划偏差量',expression:'先明确不可调整集合与可调整范围，再形成控制候选；由对应能力注册和场景配方承接。',check:'逐任务核对冻结集合、重算范围与计划差异，不能仅比较总目标。'},
  {id:'urgent',title:'紧急任务与既有承诺',status:'规则案例',owner:'marginal_control / objective_system',problem:'紧急订单的优先安排，需要同时呈现对已有交付承诺的影响。',fields:'order_info、order_item、交付优先级、资源窗口',expression:'业务负责人确认优先级与可接受影响后，将偏好形成目标或控制候选。',check:'解释受影响订单、交付偏差与资源冲突；本案例不表示当前配方已配置插单动作。'},
  {id:'shared',title:'共享资源与瓶颈保护',status:'接入案例',owner:'planning_system / marginal_control',problem:'多个工作中心同时争用模具、人员或工装，需要在共同资源范围内协调。',fields:'workcenter、shared_resource、capacity',expression:'表达共享资源及绑定关系，在计划侧确定资源窗口或额度，再交给局部排程。',check:'核对共享资源约束是否被所选模型实际消费，检查局部可行与总体额度的一致性。'},
  {id:'kitting',title:'缺料条件下的任务释放',status:'接入案例',owner:'data_layer / planning_system',problem:'计划需求进入排程前，需要确认材料何时可用以及哪些工序受到影响。',fields:'process、ingredient、material、kitting_information',expression:'通过工序级物料关系表达齐套条件，在计划侧确认可释放任务和后续反馈。',check:'检查物料引用和时间坐标，核对释放范围；当前工作台未增加自定义释放节点。'},
  {id:'feedback',title:'偏差反馈进入下一轮',status:'规则案例',owner:'analysis / planning_system',problem:'运行结果需要转为可解释的偏差，支持下一轮目标、控制与释放决策。',fields:'计划结果、实际反馈、PlanBias、PlanSignal',expression:'分析差异、归属业务对象，再形成目标或规则候选；先复核，后进入后续配方。',check:'当前基线与重算提供配置和结果对比；自动 PlanSignal 路由属于独立扩展，不以手动重算冒充。'}
];
export const TASKS = [
  ['数据接入','核对样例标准数据接口，列出表、字段与引用关系，生成数据问题清单及修复顺序；保持原始数据只读。'],
  ['基线验证','以当前配方完成数据检查和基线求解，记录每个动作、实际参数、求解状态与计划结果，并核对约束。'],
  ['方案对比','以同一份输入，比较基线与当前目标权重的结果差异，解释交付、负荷与切换的变化及取舍。'],
  ['故障排查','根据诊断记录和实际运行错误区分数据、参数、依赖与授权问题，给出可验证的排查步骤，禁止绕过授权。'],
  ['伙伴接入','以当前样例形成数据导出、映射、配方执行、结果回传和人工验收清单，列明使用方及集成方职责。']
];
