# E2 把变化表达为偏差与计划信号

[English](Learning-E2-Deviations-to-Planning-Signals.md) · [学习中心](Learning-Center-zh-CN.md)

## 先把变化说清楚
“原料晚到”描述了事件，但计划员还需要知道影响哪些订单、哪道工序、多少数量及哪个时期。变化只有连接业务对象，才便于决定后续行动。

本课的教学时段T1、T2、T3按时间先后排列。教学事件：物料M原定T2可用，确认推迟到T3；工序OP-1在T2需要它。首先检查OP-1的任务数量及可替代条件，再表达计划影响。

## 分清四种记录
| 记录 | 作用 | 本例需要保留 |
|---|---|---|
| 业务变化 | 记录更新的事实 | M的新到料时点及来源 |
| 计划偏差PlanBias | 表达变化相对原计划的影响 | 受影响对象、时段、方向和数量 |
| 计划信号PlanSignal | 将影响传递给后续处理环节 | 接收方、优先级与建议方向 |
| 后续措施 | 执行或等待确认的处理 | 调整释放、目标调整建议、规则或人工协调 |

表中按业务含义说明记录内容；调用接口时，使用所选版本定义的数据类型与字段。

## 沿联动配方观察
`planning_system_linkage`能力编排配方（recipe）先运行生产计划和分析，再执行影响分析动作`impact_analysis`。阅读结果时，先看`production_analysis.planning`中的计划分析，再看`planning_system.linkage_report`联动报告，以及`plan_biases`偏差记录和`plan_signals`计划信号，追踪同一业务变化如何被逐步处理。

`PlanBias`属于运行期间生成的接口数据，与`data.db`中的标准输入表分开管理。需要长期保存时，可写入应用的独立结果记录，并附上来源数据版本和运行标识。

## 信号到动作之间保留判断
一种偏差可能对应多种处理方向：继续观察、降低近期释放量、建议调整目标，或提示采购确认。把建议、审批和实际处理状态分别记录，便于参与者知道下一步由谁完成。

检查时依次查看分析输出、接收方、是否采用及处理结果。目标调整建议被采用后，核对实际配置和重算结果；如果还在等待确认，则保留为待处理建议。

## 合并信息，但保留来源
同一物料延迟可能影响多张订单。汇总可以帮助判断优先级，但仍需保留订单到工序、物料和时段的追溯关系。若后续又收到到料恢复信息，需要辨别更新版本，防止重复计入影响。

## 练习与参考解析
为教学事件列出受影响对象、检查来源、两种可选措施和各自确认人。再写一条“措施尚未执行”的正确说明。

例如：已识别T2工序OP-1的物料风险，建议调整任务释放时间，等待计划负责人确认。执行后，再记录实际释放任务、时间及计划结果，用于评价这项措施的效果。

## 延伸阅读

[计划与排程](https://github.com/qiaoyx-or/decisioworks/wiki/Planning-and-Scheduling-Overview-zh-CN) · [结果与反馈](https://github.com/qiaoyx-or/decisioworks/wiki/Results-Evidence-and-Feedback-zh-CN) · [模块职责](https://github.com/qiaoyx-or/decisioworks/wiki/Component-Responsibilities-zh-CN)

配套工作表：[工作表：现场规则记录与检查](Worksheet-Operational-Rule-zh-CN.md) · [工作表：复盘与持续改进记录](Worksheet-Review-and-Change-Record-zh-CN.md)

[专题 E](Learning-Topic-E-Coordinate-Plans-and-Responses-zh-CN.md) · [上一篇: 从主生产计划到任务释放与作业排程](Learning-E1-Master-Plan-to-Work-Release-zh-CN.md) · [下一篇: 扰动发生后，确定需要调整的范围](Learning-E3-Scope-a-Disruption-Response-zh-CN.md)
