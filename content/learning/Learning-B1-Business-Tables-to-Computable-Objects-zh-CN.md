# B1 从业务表格到可计算对象

[English](Learning-B1-Business-Tables-to-Computable-Objects.md) · [学习中心](Learning-Center-zh-CN.md)

## 同名字段可能描述不同事情
企业导出的“数量”可能是订单件数、包装箱数或剩余未交量，“日期”可能是接单日、承诺交期或预计到料日。接入数据时，先确定业务定义，再映射字段。企业资源计划系统（ERP）、制造执行系统（MES）、电子表格和人工整理的记录都可以成为来源，计算所需的含义与关系保持一致。

本课使用教学订单O-7：制品P-1，需求120件，承诺在时间单元T-3完成。以下是语义映射示意，标识的实际类型以所用数据模板为准。

| 来源信息 | 标准对象或字段 | 需要确认 |
|---|---|---|
| 制品编号P-1 | product及order_item.product | 明细引用的是有效制品标识 |
| 剩余需求120件 | order_item.number | 已交付部分是否已经扣除 |
| 承诺交期T-3 | order_item.delivery_time | 指向time_unit，含义是允许完成的时点 |
| 制品颜色“蓝” | product属性槽位与业务映射 | 明确哪个槽位代表颜色 |

## 按关系检查，而不只按行检查
从订单明细解析制品，再查制品的工艺路线、工序顺序与可加工工作中心。启用物料条件时，再连接工序物料需求与可用量。某行字段全部非空，并不能弥补无效引用。

检查记录应包含原始值、解释后的值和转换规则。例如12箱、每箱10件，应在确认“箱”的包装规则后转换成120件；若包装系数未知，保留问题并补充资料，而不是假设为1。

## 可计算需要哪些检查
| 检查 | 例子 | 处理方式 |
|---|---|---|
| 标识一致 | 订单引用的制品不存在 | 修复映射或补齐主数据 |
| 单位明确 | 件与箱混用 | 使用有来源的换算规则 |
| 时间一致 | 交期不能对应时间单元 | 检查日历映射 |
| 路径可达 | 工序没有适配工作中心 | 确认真实资源选择 |
| 数量与批量 | 需求不是生产批量的整倍数 | 确认是否允许拆批、余量或超产，再按所选模型检查 |

DecisioCore 的 data_layer 将来源转换为统一业务对象，后续计划和排程复用这些对象。数据结构检查与完整求解检查分阶段进行：`ContractReady`（接口检查就绪）表示通过相应的数据接口检查；`SolverReady`（求解链路就绪）表示通过该报告规定的数据与求解能力衔接检查。阅读状态时同时确认适用场景、版本和检查范围，再按本次运行结果判断具体计划的可行性。

## 做一次小调整
把O-7的来源数量改为“12箱”，包装规则确认每箱10件。标准需求仍为120件，但转换说明发生变化。下一次包装规格改变时，应更新映射和检查，而不是让求解器猜测。

## 练习与参考解析
制作五列表：来源字段、业务含义、标准对象、单位转换、检查方法。挑一个看似容易的字段，请业务人员解释。

如果交期字段实际是预计到料日，即使类型符合日期格式，映射仍然错误。合格成果应保留定义、来源和确认信息，让别人能够独立复核。

## 延伸阅读

[标准化数据接口](https://github.com/qiaoyx-or/decisioworks/wiki/Standardized-Data-Interface-zh-CN) · [数据对象与字段](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Object-and-Field-Reference-zh-CN) · [数据准备与验证](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Readiness-and-Validation-zh-CN) · [ERP与MES数据映射](https://github.com/qiaoyx-or/decisioworks/wiki/ERP-MES-Data-Mapping-Guide-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md)

[专题 B](Learning-Topic-B-Manufacturing-Data-zh-CN.md) · [上一篇: 用同一把尺子比较两个方案](Learning-A3-Compare-Plans-on-the-Same-Basis-zh-CN.md) · [下一篇: 工艺路线与工序级BOM：物料在哪一步发生作用](Learning-B2-Routes-and-Operation-Level-BOM-zh-CN.md)
