# 完整字段参考

[English](Interface-Fields.md) · [语义详解](Interface-Semantics-zh-CN.md)

本参考列出当前标准SQLite模板的18张表、105个字段。业务意义由语义体系定义，以下类型、可空性和对象默认值说明当前工程表示。对象默认值来自ORM构造器，不代表直接SQL插入时数据库会自动填充；配套SQL显式填写所需字段。允许为空也不等于某个计划场景可以省略必要关系。

单位列中的数量口径需要与场景单位表共同使用。OEE默认100表示百分数，capacity.used则采用0到1比例。具体模型的字段采用情况应随能力配置和运行证据核对。

## capacity

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `time_unit` | INTEGER | 否 | `无` | 外键 | 产能对应时期，引用time_unit.id。 → `time_unit.id` |
| `used` | FLOAT | 否 | `0.0` | 比例 | 已占用或不可用比例[0,1]；正常可用时间为scale×(1−used)。 |
| `workcenter` | INTEGER | 是 | `None` | 外键 | 产能所属资源，引用workcenter.id。 → `workcenter.id` |

## ingredient

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `process` | INTEGER | 否 | `无` | 外键 | 发生物料需求的工序，引用process.id。 → `process.id` |
| `material` | INTEGER | 否 | `无` | 外键 | 所需物料，引用material.id。 → `material.id` |
| `number` | INTEGER | 否 | `0` | 物料单位/产出单位 | 工序配套数量；本课按一件工序产出定义，必须与出件率和供给单位一致。 |
| `priority` | INTEGER | 否 | `0` | 优先级 | 存在替代料时的配套优先级，由相应策略采用。 |

## inventory_limit

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `product` | INTEGER | 否 | `无` | 外键 | 受限制制品，引用product.id。 → `product.id` |
| `time_unit` | INTEGER | 否 | `无` | 外键 | 限制生效时期，引用time_unit.id。 → `time_unit.id` |
| `binding` | INTEGER | 是 | `None` | 组标识 | 同值表示共用库存，单位及容量分配需明确。 |
| `upper_bound_acc` | INTEGER | 是 | `None` | 累计制品数量 | 累计生产入库上限，由期初库存、收支与库容推导；NULL为未配置。 |
| `urgency` | FLOAT | 否 | `0.0` | 约定尺度 | 紧迫性或周转相关值，采用方式由业务策略说明。 |
| `lower_bound_acc` | INTEGER | 是 | `None` | 累计制品数量 | 累计生产入库下限，由安全库存等要求推导；NULL为未配置。 |

## kitting_information

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `time_unit` | INTEGER | 否 | `无` | 外键 | 物料可用时点，引用time_unit.id。 → `time_unit.id` |
| `material` | INTEGER | 否 | `无` | 外键 | 已就绪物料，引用material.id。 → `material.id` |
| `number` | INTEGER | 否 | `0` | 物料单位 | 就绪或可用数量；当前累计输入示例采用首期可用量及后续增量，不混入累计快照。 |

## material

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `code` | VARCHAR | 否 | `''` | 编码 | 物料业务编码。 |
| `name` | VARCHAR | 否 | `''` | 文本 | 物料名称。 |
| `vendor` | VARCHAR | 否 | `''` | 编码或文本 | 供应商信息。 |
| `substitute` | INTEGER | 是 | `None` | 组标识 | 可替换物料采用同一值；无替代关系为NULL。 |
| `binding` | INTEGER | 是 | `None` | 组标识 | 物料依赖或配套选型关系，需有对应解释与策略。 |
| `extend` | INTEGER | 是 | `None` | 扩展约定 | 预留扩展字段，例如供应商优先级；当前为整数，使用前定义含义和取值规则。 |

## order_info

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `description` | VARCHAR | 否 | `''` | 文本 | 订单描述。 |
| `priority` | INTEGER | 否 | `0` | 优先级 | 订单头优先级，排序方向由采用策略说明。 |
| `code` | VARCHAR | 是 | `''` | 编码 | 订单业务编码。 |
| `created_at` | DATETIME | 是 | `None` | 时间戳 | 订单创建时间；保留原始时间，不映射为计划时间单元。 |

## order_item

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `product` | INTEGER | 否 | `无` | 外键 | 需求制品，引用product.id；设计中的production_id按制品语义对应此字段。 → `product.id` |
| `information` | INTEGER | 否 | `无` | 外键 | 所属订单头，引用order_info.id，对应order_information_id。 → `order_info.id` |
| `delivery_time` | INTEGER | 是 | `None` | 外键 | 交付时间单元，引用time_unit.id；有交期需求应给出有效引用。 → `time_unit.id` |
| `number` | INTEGER | 否 | `0` | 制品单位 | 该条交付需求数量；分期需求分别记录，避免重复录入累计值。 |

## planning_result

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `workcenter` | INTEGER | 是 | `None` | 外键 | 执行计划任务的workcenter.id。 → `workcenter.id` |
| `time_unit` | INTEGER | 否 | `None` | 外键 | 任务执行时期，引用time_unit.id。 → `time_unit.id` |
| `process` | INTEGER | 是 | `None` | 外键 | 执行的工序，引用process.id；特定空序列槽位可用NULL。 → `process.id` |
| `number` | INTEGER | 否 | `0` | 工序产出数量 | 计划产出，不是加工次数；多工序合计不等于成品交付。 |
| `value_1` | INTEGER | 否 | `0` | 场景约定 | 扩展字段；循环排程可约定为循环序号。 |
| `value_2` | INTEGER | 否 | `0` | 场景约定 | 扩展字段；循环排程可约定为序列位置。 |
| `value_3` | INTEGER | 否 | `0` | 场景约定 | 预留扩展字段，使用前定义含义。 |

## process

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `route` | INTEGER | 否 | `无` | 外键 | 所属工艺路线，引用process_route.id。 → `process_route.id` |
| `name` | VARCHAR | 否 | `''` | 文本 | 工序名称。 |
| `code` | VARCHAR | 是 | `''` | 编码 | 工序业务编码。 |
| `operation_number` | INTEGER | 否 | `1` | 编号 | 路线内工序编号；与执行顺序分开，按路线检查唯一性。 |
| `seqno` | INTEGER | 否 | `1` | 顺序 | 工序顺序数；相同值表示无先后依赖，实际并行仍取决于其他条件。 |

## process_adaptor

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `process` | INTEGER | 是 | `None` | 外键 | 被适配工序，引用process.id。 → `process.id` |
| `workcenter` | INTEGER | 是 | `None` | 外键 | 可执行该工序的资源，引用workcenter.id。 → `workcenter.id` |
| `priority` | INTEGER | 否 | `0` | 优先级 | 该工序选用此资源的优先级。 |
| `wip_buffer_size` | INTEGER | 否 | `0` | 约定数量单位 | 在制品缓存容量；0的具体模型含义及约束采用方式需核对。 |
| `productivity` | INTEGER | 否 | `1` | 件/次 | 当前离散模板为单次加工产出；连续生产设计需明确单位时间产出的转换。 |
| `processing_time` | FLOAT | 否 | `0.0` | 秒/次 | 标准单次加工时长，来源节拍应转换为这一口径。 |
| `setup_time` | FLOAT | 否 | `0.0` | 秒 | 工艺切换时长；是否包含首次准备须在场景中说明。 |
| `batch_size` | INTEGER | 否 | `1` | 制品单位 | 按批加工数量，应为单次出件数量的整数倍。 |
| `OEE` | INTEGER | 否 | `100` | 百分数 | 设备综合效率；当前默认100，实际折减位置由配置说明。 |
| `binding` | INTEGER | 是 | `None` | 组标识 | 同值表示共同加工；NULL或单独组不形成多工序共同加工。 |

## process_route

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `product` | INTEGER | 否 | `无` | 外键 | 路线所属制品，引用product.id；一制品可有多路线。 → `product.id` |
| `name` | VARCHAR | 否 | `''` | 文本 | 工艺路线名称。 |
| `code` | VARCHAR | 否 | `''` | 编码 | 工艺路线业务编码。 |
| `priority` | INTEGER | 否 | `0` | 优先级 | 路线选择优先级，须由路线策略解释。 |
| `description` | VARCHAR | 是 | `''` | 文本 | 加工路线的业务说明。 |

## product

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `name` | VARCHAR | 否 | `''` | 文本 | 制品名称，可为成品、半成品或零部件。 |
| `code` | VARCHAR | 否 | `''` | 编码 | 制品业务编码，与记录id分别管理。 |
| `vin` | VARCHAR | 是 | `''` | 编码 | 所属成品唯一编码；不单独定义装配数量。 |
| `property_1` | INTEGER | 是 | `None` | 外键 | 引用property_1.id；本场景应固定说明其业务维度。 → `property_1.id` |
| `property_2` | INTEGER | 是 | `None` | 外键 | 引用property_2.id；与第一属性构成独立分类维度。 → `property_2.id` |
| `property_3` | INTEGER | 是 | `None` | 外键 | 引用property_3.id；空值表示未关联此维度。 → `property_3.id` |

## property_1

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `name` | VARCHAR | 否 | `''` | 文本 | 属性名称，如型号、配置、颜色；与具体编码及属性值配合解释。 |
| `code` | VARCHAR | 是 | `''` | 编码 | 属性编码；在场景内保持稳定分类与映射。 |
| `value` | FLOAT | 是 | `None` | 按维度 | 属性数值；当前SQLite类型为FLOAT，文字标签保存在名称和编码。 |
| `is_key` | BOOLEAN | 否 | `False` | 布尔 | 关键属性标识，表达需求中区分制品的必要属性；当前加载器据此选取属性字段。 |

## property_2

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `name` | VARCHAR | 否 | `''` | 文本 | 属性名称，如型号、配置、颜色；与具体编码及属性值配合解释。 |
| `code` | VARCHAR | 是 | `''` | 编码 | 属性编码；在场景内保持稳定分类与映射。 |
| `value` | FLOAT | 是 | `None` | 按维度 | 属性数值；当前SQLite类型为FLOAT，文字标签保存在名称和编码。 |
| `is_key` | BOOLEAN | 否 | `False` | 布尔 | 关键属性标识，表达需求中区分制品的必要属性；当前加载器据此选取属性字段。 |

## property_3

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `name` | VARCHAR | 否 | `''` | 文本 | 属性名称，如型号、配置、颜色；与具体编码及属性值配合解释。 |
| `code` | VARCHAR | 是 | `''` | 编码 | 属性编码；在场景内保持稳定分类与映射。 |
| `value` | FLOAT | 是 | `None` | 按维度 | 属性数值；当前SQLite类型为FLOAT，文字标签保存在名称和编码。 |
| `is_key` | BOOLEAN | 否 | `False` | 布尔 | 关键属性标识，表达需求中区分制品的必要属性；当前加载器据此选取属性字段。 |

## shared_resource

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `binding` | INTEGER | 是 | `None` | 外键 | 作为共享资源的workcenter.id。 → `workcenter.id` |
| `to` | INTEGER | 是 | `None` | 外键 | 依赖该资源的目标workcenter.id。 → `workcenter.id` |

## time_unit

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `offset` | INTEGER | 否 | `0` | 顺序 | 相对计划起点的顺序偏移；与主键分开。 |
| `scale` | INTEGER | 否 | `8 * 60 * 60` | 秒 | 时间单元长度，小时级为3600，八小时窗口为28800。 |
| `status` | INTEGER | 否 | `1` | 状态 | 1正常、0不可用、-1特殊或可选；可选状态需明确采用方式。 |

## workcenter

| 字段 | 存储类型 | 可空 | 对象默认值 | 单位 | 含义 |
|---|---|---|---|---|---|
| `id` | INTEGER | 否 | `生成主键` | 标识 | 本表记录主键，用于引用。 |
| `name` | VARCHAR | 否 | `''` | 文本 | 工作中心名称，如设备、班组、区域、外协或组织。 |
| `code` | VARCHAR | 是 | `''` | 编码 | 资源业务编码。 |
| `type` | INTEGER | 否 | `0` | 类别 | 叶子节点为0，非叶子节点非0。 |
| `parallelism` | INTEGER | 否 | `1` | 并行单元 | 并行能力数量；与工位数分别建模。 |
| `station_count` | INTEGER | 否 | `1` | 工位 | 工位数量，结合热处理、循环产线等具体结构解释。 |
| `equipping_time` | FLOAT | 否 | `0` | 时间 | 工作中心配置准备时间；本课程按秒，与工序切换时间分别核算。 |
| `parent_id` | INTEGER | 是 | `None` | 外键 | 父工作中心，引用workcenter.id；根节点为空。 → `workcenter.id` |

## 名称对应与扩展

`order_information → order_info`; `order_information_id → information`; `product_id → product`; `time_unit_id → time_unit`（订单交期为`delivery_time`）；`route_id → route`; `process_id → process`; `material_id → material`; `workcenter_id → workcenter`; `parent → parent_id`。

属性机制可扩展到property_n；当前三个属性表是实现选择。decision_node属于工程扩展，不计入上述18张标准表。损耗、良率、审批时间等来源信息，应通过明确的映射或扩展表达，不能擅自改变标准字段的语义。

## 设计示例与当前模板的表示差异

语义说明定义业务含义，当前模板记录实际存储要求。下表列出使用时需注意的差异，不通过改写真实类型或默认值来制造表面一致。

| 字段 | 设计结构示例 | 当前模板 | 使用要求 |
|---|---|---|---|
| `process_adaptor.OEE` | FLOAT，默认100 | INTEGER，默认100 | 小数效率需明确转换与精度，不能静默截断 |
| `process_adaptor.wip_buffer_size` | 默认1 | 默认0 | 明确模型如何解释0，不自行视为无限容量 |
| `property_i.value` | 默认0 | 可空，默认None | 区分未给值与数值0 |
| `property_i.is_key` | 默认NULL | 不可空，默认False | 区分未说明与明确非关键，并检查加载 |
| `product.vin/property_i` | 示例不可空，属性可扩展 | vin与三个属性引用可空 | 未使用维度与实际漏填分别处理 |
| `process_adaptor.process/workcenter`、`capacity.workcenter` | 示例外键不可空 | 可空 | 可执行任务与产能仍需完整资源关系 |
| `planning_result.workcenter/process` | 示例外键不可空 | 可空 | 区分有效作业结果与规定的空序列槽位 |

这不是全部物理类型差异清单。表名、列名和数据库形式可以映射变化，业务语义仍需保持一致。

[关系与规则](Interface-Relationships-zh-CN.md) · [配置模式](Interface-Configurations-zh-CN.md) · [教学数据库](Interface-Walkthrough-zh-CN.md)
