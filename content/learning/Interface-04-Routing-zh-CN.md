# 04 配置工艺路线与可选资源

[English](Interface-04-Routing.md) · [学习指南](Interface-Guide-zh-CN.md) · [语义详解](Interface-Semantics-zh-CN.md)

## 任务：把制品连接到可执行工序

支架P-1先冲压、再装配。建立路线101，所属制品为1，编码`ROUTE-P1`，优先级0。路线通过`product`引用制品，工序通过`route`引用路线。

| process.id | route | name | code | operation_number | seqno |
|---:|---:|---|---|---:|---:|
| 1001 | 101 | 冲压 | STAMP | 10 | 1 |
| 1002 | 101 | 装配 | ASSEMBLE | 20 | 2 |

编号10、20识别工序，顺序1、2表达先后。两者分开后，调整工序顺序无需改变其业务身份。

## 连接工作中心

基础配置使用以下两条适配记录，时间均为秒：

| id | process | workcenter | productivity | batch_size | processing_time | setup_time |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1001 | 11 | 4 | 20 | 600 | 0 |
| 2 | 1002 | 12 | 1 | 20 | 120 | 0 |

两条记录的`priority=0`、`wip_buffer_size=120`、`OEE=100`、`binding=NULL`。缓存容量的单位在本例中为该工序产出件数；是否形成模型限制须检查相应能力配置。

沿订单追溯时，逐条核对真实外键关系；从制品查找候选路线等步骤属于反向查询：

```text
order_item.product        -> product.id
process_route.product     -> product.id
process.route             -> process_route.id
process_adaptor.process   -> process.id
process_adaptor.workcenter-> workcenter.id
```

每个被引用的标识都应有实际记录。

## 增加备选设备与备选路线

若冲压工序还能在工作中心13执行，新增适配记录，保留`process=1001`，将`workcenter`设为13，并填写该机器真实的出件率和时长。不要复制出一个含义相同的工序来冒充资源选项。

若备选加工方法改变了工序组合，例如采用外协成形后再装配，则建立新的路线及其工序。两种表达的差别是“同一道工序换资源”与“制品换制造路径”。路线选择策略与资源选择策略分别确认，不能因一条路线有多台设备就重复计算产品需求。

## 相同顺序数怎样解释

假设另一项练习中存在两个无先后依赖的检查工序，可给它们不同`operation_number`、相同`seqno`。这仅取消两者之间的先后要求；同一检查员、共用仪器或物料仍可能使它们无法同时进行。该语义与具体模型的并行工序支持应对应核对。

## 检查与练习

检查路线所属制品、路线内工序编号、顺序数、资源引用和每个候选资源的参数。为P-1增加一道表面处理，要求在冲压后、装配前执行：可保留原编号10、20，新增编号15；顺序调整为1、2、3，并为表面处理补充资源与物料记录。只画出新节点而没有配置适配记录，仍然缺少可执行资源。

[上一课](Interface-03-Resources-zh-CN.md) · [下一课：数量与加工时间](Interface-05-Quantity-zh-CN.md)
