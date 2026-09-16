# F1 业务变化时，应该调整哪一层

[English](Learning-F1-Place-Changes-in-the-Right-Layer.md) · [学习中心](Learning-Center-zh-CN.md)

## 变化本身并不可怕，关键是知道改哪里
新增一种制品，可能只需增加工艺与物料数据；新增一种从未支持的调度结构，则可能需要模型适配。两者都叫“业务变化”，工程工作却不同。分层让团队知道应修改哪些数据或模块，以及需要检查哪些关联功能。

## 用四个部分理解 DecisioWorks
| 部分 | 主要职责 | 典型变化 |
|---|---|---|
| DataSets与标准接口 | 场景数据及制造关系 | 订单、路线、产能、物料清单（BOM）变化 |
| DecisioCore | 数据、目标、规则、编排、分析与联动 | 管理偏好、行业逻辑、反馈方式 |
| GOCK | 模型构建与优化 | 模型或求解能力升级 |
| Web及其他应用 | 展示、操作与业务交互 | 新报表、培训页面、应用流程 |

DecisioCore进一步区分数据接入、目标管理（`objective_system`）、规则控制（`marginal_control`）、模型适配（`engine_adapters`）、结果分析（`analysis`）与计划联动（`planning_system`）。开放参考实现使开发者能够理解这些连接，复用已有方式或实现自己的调用层。

## 对一次变化画影响图
教学变化：客户要求同一组制品按颜色分组展示，同时更重视减少颜色切换。这包含两项独立需求。分组展示由应用处理；切换偏好需要确认数据中存在颜色映射，模型也支持相应的切换指标，再调整目标。改变页面排序不会自动改变求解顺序。

| 变化 | 首先检查 | 修改后需要复查 |
|---|---|---|
| 加工时间更新 | 数据单位及工艺适配 | 负荷、交期及结果 |
| 交期偏好更新 | 目标统计量与方向 | 取舍、明细与审计 |
| 临时资源额度 | 规则对象及模型采用方式 | 约束生效及到期处理 |
| 新结果展示 | 分析字段与单位 | 数值一致性和页面阅读 |
| 新模型能力 | 输入输出适配 | 支持范围、状态和既有调用 |

## 独立演进仍需要协作验证
接口让各模块可以分别改进。新增字段、改变单位或替换模型后，通过检查输入含义、输出结构和既有场景，确认新版本仍能与其他部分配合。演进的实际含义，是利用已有基础持续调整，同时保留能继续工作的部分。

开放参考实现也让伙伴能够看清哪些能力适合复用，哪些需要自行适配。最终应用可采用自己的页面、数据接入或工作流，同时通过明确接口调用所需优化能力。

## 练习与参考解析
把“新增制品、调整交期偏好、增加一个审批页面、换用新的模型能力”分别放到对应层，再写一个跨层影响。

审批页面属于应用，但审批状态若决定任务是否释放，还需连接计划输入。成果应同时标出主责任层和受影响的接口，避免把“分层”理解为彼此完全无关。

## 延伸阅读

[设计原则与差异化](https://github.com/qiaoyx-or/decisioworks/wiki/Design-Principles-and-Differentiation-zh-CN) · [架构总览](https://github.com/qiaoyx-or/decisioworks/wiki/Architecture-Overview-zh-CN) · [生产决策数据资产](https://github.com/qiaoyx-or/decisioworks/wiki/Production-Decision-Data-Assets-zh-CN) · [生态协作](https://github.com/qiaoyx-or/decisioworks/wiki/Ecosystem-Overview-zh-CN) · [伙伴接入](https://github.com/qiaoyx-or/decisioworks/wiki/Partner-Onboarding-and-Integration-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md) · [工作表：复盘与持续改进记录](Worksheet-Review-and-Change-Record-zh-CN.md)

[专题 F](Learning-Topic-F-Open-Collaboration-and-Evolution-zh-CN.md) · [上一篇: 扰动发生后，确定需要调整的范围](Learning-E3-Scope-a-Disruption-Response-zh-CN.md) · [下一篇: 把场景经验沉淀为数据资产与行业模板](Learning-F2-Preserve-Data-Assets-and-Templates-zh-CN.md)
