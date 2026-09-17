# 对象关系与计算规则

[English](Interface-Relationships.md) · [学习指南](Interface-Guide-zh-CN.md) · [字段参考](Interface-Fields-zh-CN.md)

字段表回答“填在哪里”，本页回答“记录之间如何连接、哪些数量可以比较”。准备数据时，先用业务编码确定对象，再把引用转换为目标表的记录ID。

## 1. 需求与制造关系

| 关系 | 当前字段 | 如何检查 |
|---|---|---|
| 一个订单包含多条明细 | `order_item.information → order_info.id` | 每条明细归属一个有效订单；同一制品可按交期拆行 |
| 多条需求可以指向同一制品 | `order_item.product → product.id` | 不把订单行ID填成制品ID |
| 制品引用各维属性记录 | `product.property_i → property_i.id` | 外键、文字标签和数值属性分别填写 |
| 一个制品可以有多条候选路线 | `process_route.product → product.id` | 路线是加工选择，不能把每条候选路线都当成额外需求 |
| 一条路线包含多道工序 | `process.route → process_route.id` | 路线内`operation_number`区分工序，`seqno`表达先后 |
| 工序可以适配多个资源 | `process_adaptor.process/workcenter` | 每条记录是一种工序与资源组合，参数随组合确定 |
| 工序关联多种物料 | `ingredient.process/material` | 单耗基准明确；每种物料都有可追溯的供给 |

相同`seqno`表示相关工序之间没有先后依赖，不必强行改成唯一值。需要确认的另一个问题是，它们能否同时得到资源与物料。

## 2. 时间与资源关系

| 引用来源 | 指向 | 业务问题 |
|---|---|---|
| `order_item.delivery_time` | `time_unit.id` | 需求在哪个时间单元到期 |
| `capacity.time_unit` | `time_unit.id` | 这段资源能力属于哪个时期 |
| `kitting_information.time_unit` | `time_unit.id` | 物料何时具备使用条件 |
| `inventory_limit.time_unit` | `time_unit.id` | 到哪个时点检查累计入库界限 |
| `planning_result.time_unit` | `time_unit.id` | 工序产出落在哪个时期 |
| `capacity.workcenter` | `workcenter.id` | 占用比例属于哪个资源 |
| `workcenter.parent_id` | `workcenter.id` | 资源归属哪个组织节点 |
| `shared_resource.binding/to` | 两个`workcenter.id` | 哪个共享资源供哪个目标资源使用 |

父子资源结构应能追溯到根节点，避免自引用和循环。共享关系也要排除错误的自绑定。一个共享资源可以服务多个目标，一个目标也可以依赖多个共享资源。

日历完整性取决于运行的时间范围与资源范围。某个资源缺少某期记录时，应先确认是“未配置”还是有明确的默认策略，不能自行假定全天可用。

## 3. 物料、库存与结果关系

`kitting_information.material`引用物料。`inventory_limit.product`引用制品，两者的库存语义需要分开：前者用于工序物料的就绪条件，后者用于制品累计生产入库限制。

`planning_result.process`可沿工序、路线追到制品；`workcenter`指定实际资源。结果中的资源和工序除了各自存在，还应构成该场景允许的适配组合。选择了候选路线后，交付量按照实际采用的制造路径归集。

当前数据库允许部分关联字段为空，这是存储能力。具体教学任务或运行能力仍可要求它们必填，例如本教程的结果复核需要明确工序与资源。

## 4. 同名字段的不同含义

| 字段 | 所在对象 | 正确解释 |
|---|---|---|
| `binding` | `material` | 物料选型依赖分组 |
| `binding` | `process_adaptor` | 共同加工分组 |
| `binding` | `inventory_limit` | 共用库存分组 |
| `binding` | `shared_resource` | 共享资源工作中心ID，属于外键 |
| `priority` | 订单、路线、适配、BOM | 各自对象的优先关系；排序方向按对应配置确认 |
| `number` | 订单明细 | 需求数量 |
| `number` | 工序BOM | 按已声明基准计的物料需求量 |
| `number` | 齐套信息 | 按已声明增量或累计口径记录的就绪量 |
| `number` | 计划结果 | 工序产出数量 |

相同整数分组值不表示跨表属于同一组。例如物料`binding=1`与库存`binding=1`没有自动关联。

## 5. 数量与时间核算

以下计算以单资源离散加工、无报废、无切换损失为前提。增加OEE、并行加工、共同产出或库存共用时，应明确相应转换。

| 问题 | 计算 | 例子 |
|---|---|---|
| 正常时期可用时间 | `scale × (1 − used)` | 28800秒×0.75=21600秒 |
| 加工次数 | 产出量÷单次出件数 | 80÷4=20次 |
| 纯加工时间 | 次数×单次加工时间 | 20×600秒=200分钟 |
| 整批配置 | 批量÷单次出件数为整数 | 20÷4=5次/批 |
| 物料消耗 | 工序产出×每件单耗 | 80件装配×2件紧固件=160件 |
| 累计供应 | 期初可用量+后续已生效增量 | 80+40=120件 |
| 期末库存 | 期初+累计入库−累计出库 | 20+120−120=20件 |

单件通过冲压和装配各一次，两道工序都记录80件时，成品为80件；两道工序的160件合计只能描述工序产出记录总量。

## 6. 三种检查要分别完成

**结构检查**：表、字段、类型、主键、外键完整。

**业务检查**：单位、关联方向、时间范围、批量、供给和库存口径成立。

**运行检查**：本次能力配置实际采用了哪些资源、物料和顺序限制，输出能否逐项复核。

配套校验器针对贯穿案例执行前两类检查中的明确规则；完整场景仍需按所用能力补充检查。可从[典型配置模式](Interface-Configurations-zh-CN.md)选择接近自己业务的模式，再按[贯穿案例](Interface-Walkthrough-zh-CN.md)完成一次核对。
