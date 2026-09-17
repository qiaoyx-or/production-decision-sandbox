# 标准化数据接口学习指南

[English](Interface-Guide.md)

[下载完整练习包（SQL、字段清单、Python脚本、数据库及CSV）](../../assets/data-interface/decisioworks-data-interface-examples.zip)

把一个生产场景交给计划模型，需要先说明生产什么、怎样加工、使用哪些资源、物料何时到位，以及不同时间内允许做多少。DecisioWorks 的标准化数据接口把这些问题组织为统一的业务对象和关系。

本专题包含完整的语义说明、按任务组织的九课教程，以及字段、关系、模板与代码参考。初次学习从《语义详解》的体系图开始；准备实际数据时，按相应课程完成配置；查找具体字段时使用字段参考。

## 总纲

[DecisioWorks 标准化数据接口语义详解](Interface-Semantics-zh-CN.md)：完整阅读对象、字段语义、时间和数量规则、关联关系及结果更新方式。

## 按任务学习

| 课程 | 完成后的成果 |
|---|---|
| [01 配置生产时间、班制与维护](Interface-01-Calendar-zh-CN.md) | 一张时间表、资源占用记录及可用时间核算 |
| [02 表达订单、制品与产品属性](Interface-02-Demand-zh-CN.md) | 分期交付的订单明细、制品和属性映射 |
| [03 配置工作中心与共享资源](Interface-03-Resources-zh-CN.md) | 组织关系、共享关系和资源能力记录 |
| [04 配置工艺路线与可选资源](Interface-04-Routing-zh-CN.md) | 有序工序、候选路线及资源适配记录 |
| [05 核算出件率、批量与加工时间](Interface-05-Quantity-zh-CN.md) | 数量换算、批量校验和共同产出核算 |
| [06 配置工序级物料与齐套](Interface-06-Materials-zh-CN.md) | 分工序单耗、分时供给及人工齐套检查 |
| [07 把库存要求转换为累计约束](Interface-07-Inventory-zh-CN.md) | 可追溯到库存收支的累计上下限 |
| [08 导入、校验并读取业务数据](Interface-08-Validation-zh-CN.md) | 字段映射表、独立教学数据库和校验结果 |
| [09 解释结果并准备下一轮计划](Interface-09-Results-zh-CN.md) | 数量、时间、物料复核及更新清单 |

## 查询与实践

- [完整字段参考](Interface-Fields-zh-CN.md)：当前标准模板的18张表、105个字段；明确区分业务定义与存储要求。
- [关系与规则参考](Interface-Relationships-zh-CN.md)：外键、基数关系、数量计算、同名字段区别。
- [典型配置模式](Interface-Configurations-zh-CN.md)：单班、双班、连续生产、维护、共享资源、库存及数量口径。
- [贯穿案例与运行步骤](Interface-Walkthrough-zh-CN.md)：从120件需求到配置校验、人工候选计划和维护调整。

示例中的时间、需求和资源均为教学数据。配套程序创建独立数据库，执行结构校验及人工核算；人工候选表明确标注为手算，求解器运行结果须来自实际执行。这样可以分别学习“数据怎样表达”和“模型怎样采用”。

阅读当前工程配置时，使用与安装版本配套的字段字典和能力说明。语义机制中的可扩展属性不限定为三个维度；本套SQLite模板具体提供三个属性表。
