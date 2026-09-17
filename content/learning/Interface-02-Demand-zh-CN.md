# 02 表达订单、制品与产品属性

[English](Interface-02-Demand.md) · [学习指南](Interface-Guide-zh-CN.md) · [语义详解](Interface-Semantics-zh-CN.md)

## 把一个订单拆成可以计划的需求

客户订购蓝色支架120件，第一天交80件、第二天交40件。要保留一个订单身份，同时让两个交付要求分别进入计划。

先建立制品P-1，当前记录的`id=1`。物理表中的属性外键指向属性记录，不直接保存“蓝色”。

| 表 | id | name | code | value | is_key |
|---|---:|---|---|---:|---:|
| property_1 | 1 | 颜色 | BLUE | 1 | 1 |

| product.id | name | code | vin | property_1 | property_2 | property_3 |
|---:|---|---|---|---:|---|---|
| 1 | 蓝色支架 | P-1 | FIN-P1 | 1 | NULL | NULL |

本场景约定`property_1`表达颜色，名称说明属性维度，编码BLUE标识蓝色，数值1为该颜色的稳定数值表示。`vin`标识所属成品，不推导装配数量。关键属性用来区分需求中的制品；如后续规则引用颜色，还应检查它已被加载。

## 建立订单与两条明细

`order_info`中的订单1使用编码`O-100`、描述“蓝色支架分期交付”、优先级0。创建时间可以保存原始时间戳。

| order_item.id | information | product | delivery_time | number |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 80 |
| 2 | 1 | 1 | 2 | 40 |

`information=1`连接订单头，`product=1`连接制品，`delivery_time`连接第一课的时间单元。需求是80和40两条，而不是每期都填累计的80和120；是否做累计满足检查由后续模型处理。

## 属性怎样进入业务配置

下面是数据采集配置片段，业务名`color`对应本场景的属性位置：

```yaml
context:
  inputs:
    data_acquisition:
      property_mappings:
        color: property_1
```

它是能力编排配方（recipe，将数据、参数和动作组织为运行流程的配置）中的一个片段，不是完整求解配方。换一个场景时，颜色可以位于其他属性表，但业务名称与含义应明确。

## 自检

逐条检查订单、制品、时间和属性引用；核对两条明细合计120件；确认需求是否已经扣除取消与交付数量。物理ID与业务编码的转换应留在来源映射表，不能将字符串`P-1`直接填入整数`product`外键。

同一订单的不同制品需要各自的制品记录。一个属性位置不能同时混装颜色与客户等级。属性维度扩展需要同步配置模板与加载链路，当前三个表不是设计上限。

## 练习与解析

客户将第二天40件改为第三天交付。先增加第三个合法时间单元，再把第二条明细的`delivery_time`改为新ID；数量仍为40。若交期编号不存在，即使总数量正确也不能形成有效输入。

这一步只练习订单与时间的引用。若要继续核算库存、物料和产能，还需要同步以下文件。订单需求、预计出库和候选产出是三个不同对象；本例选择按交期出库，不能将此约定直接套用到所有业务。

| 文件或表 | 三期练习中的修改 |
|---|---|
| `time_unit`、`order_item` | 增加`(id=3, offset=2, scale=28800, status=1)`；明细2交期改为3 |
| `capacity` | 为工作中心11、12分别增加第3期记录，`used=0` |
| `scenario.json` | `period_issues`改为`[80,0,40]`，按`time_unit.offset`顺序；期初库存仍为20 |
| `inventory_limit` | 三期累计生产下限80、80、120，上限160、160、200，对应期末库存20至100 |
| `kitting_information` | 保留第2期到料40、80；第3期新增量为0，不能再填累计供给120、240 |
| `manual_candidate.csv` | 将两条第2期产出40件的记录移到第3期；第2期不生产 |

在`examples`目录创建一个独立、完整的三期副本：

```bash
python build_example.py --third-period --output-dir ./third-period-example
python check_example.py ./third-period-example/data.db
python calculate_candidate.py ./third-period-example
```

生成器使用[三期调整SQL](../../assets/data-interface/examples/third-period.sql)，同时维护JSON、候选CSV及各表CSV；已有数据库不会被覆盖。手动练习时，应把表中各项一起修改。只改导出的CSV不会自动更新`data.db`。

预期三期累计产出为80、80、120，期末库存均为20，`aggregate_checks_passed`及`issues_match_due_quantities`均为`true`。第2期没有候选产出行；第3期冲压和装配分别用100、80分钟。该结果是人工候选核算，不是求解记录。

若只新增时间单元，复算会在`errors`中定位出库计划长度；只补出库计划还会定位缺少的库存限制或产能记录。若只把40件订单改为400件，`demand_issue_comparison`会显示差额`-360`，不能把未改变的库存手算当成需求已满足。

[上一课](Interface-01-Calendar-zh-CN.md) · [下一课：资源](Interface-03-Resources-zh-CN.md)
