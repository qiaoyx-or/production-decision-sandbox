# 贯穿案例：120件支架的输入、核对与调整

[English](Interface-Walkthrough.md) · [学习指南](Interface-Guide-zh-CN.md)

[下载完整练习包（SQL、字段清单、Python脚本、数据库及CSV）](../../assets/data-interface/decisioworks-data-interface-examples.zip)

本案例用冲压、装配两道工序，把时间、需求、路线、资源、物料和库存联系起来。完成后可以得到一个可加载的教学数据库、表格文件和数量核算报告。全程不需要修改自己的业务数据库。

## 1. 业务条件

| 项目 | 条件 |
|---|---|
| 制品 | P-1蓝色支架 |
| 订单 | 第1期80件、第2期40件 |
| 时间 | 两个8小时正常生产期，每期28800秒 |
| 冲压 | 设备11，每次4件，每次600秒，批量20件 |
| 装配 | 设备12，每次1件，每次120秒，批量20件 |
| 维护 | 第1期冲压设备不可用2小时，`used=0.25` |
| BOM | 每件冲压消耗坯料1件，每件装配消耗紧固件2件 |
| 供给 | 第1期坯料80、紧固件160；第2期新增40、80 |
| 成品库存 | 期初20，期末要求20至100，出库80、40 |
| 简化条件 | 无报废、无切换损失，OEE为100，无备选资源 |

两个时期在本例中对应两个生产窗口。接入真实日期时，应另外保留计划起点、班次时间和非工作时段的映射。

## 2. 准备文件

在配套的`examples`目录中使用Python 3.10或以上版本执行以下命令；基础脚本只使用标准库。Windows可使用环境中的`python`，Linux可按环境改为`python3`。

```bash
python build_example.py --output-dir ./my-first-example
python check_example.py ./my-first-example/data.db
python calculate_candidate.py ./my-first-example
python test_examples.py
```

创建程序会生成：

| 文件 | 用途 |
|---|---|
| `data.db` | 18张标准表的教学数据库 |
| 各表同名CSV | 查看、比较输入表；结果表初始只有表头 |
| `manual_candidate.csv` | 四条人工候选工序产出，供手算练习 |
| `scenario.json` | 单位、供给口径、期初库存、独立的各期出库计划`period_issues`及简化条件 |

程序遇到已有`data.db`会停止，请另选目录。也可以先查看随附的[完整示例下载](../../assets/data-interface/decisioworks-data-interface-examples.zip)，再从SQL重建。两份数据的业务内容相同。

## 3. 检查输入

`check_example.py`应返回`ok: true`、18张表、105个字段；其中订单明细2行、工序2行、适配2行、产能4行、BOM2行、齐套4行、库存限制2行。

`planning_result`为0行。人工候选计划独立保存，不会被当作真实求解结果写回输入库。

可以在SQLite查看器中运行以下查询，核对需求通过何种路线进入工序：

```sql
SELECT oi.id AS order_line, p.code AS product_code,
       oi.delivery_time, oi.number AS demand_quantity,
       r.code AS route_code, op.code AS operation_code, op.seqno
FROM order_item oi
JOIN product p ON p.id = oi.product
JOIN process_route r ON r.product = p.id
JOIN process op ON op.route = r.id
ORDER BY oi.id, r.id, op.seqno;
```

查询会返回4行，因为2条需求分别关联2道工序。连接后不要把重复显示的需求数相加当成新需求。

## 4. 读取到DecisioWorks

已有安装及依赖的环境可以从任意目录执行：

```bash
python /path/to/examples/load_with_decisioworks.py /path/to/my-first-example/data.db --project-root /path/to/DecisioWorks
```

把三个路径替换为实际位置。该脚本设置项目导入路径，调用真实的`load_business_data`，随后执行`validate_batch_productivity_multiple`预处理。

本例实际加载结果为：`demand=2`、`process=2`、`capacity=4`、`bom=2`、`kitting=4`、`inventory_limit=2`，预处理状态`ok`。这验证了示例可进入数据层；此步骤没有执行求解。

## 5. 复核人工候选计划

| 资源 | 时期 | 工序 | 产出件数 | 加工次数 | 纯加工分钟 |
|---:|---:|---|---:|---:|---:|
| 11 | 1 | 冲压 | 80 | 20 | 200 |
| 12 | 1 | 装配 | 80 | 80 | 160 |
| 11 | 2 | 冲压 | 40 | 10 | 100 |
| 12 | 2 | 装配 | 40 | 40 | 80 |

冲压第1期可用360分钟，其他资源期均可用480分钟。两期累计消耗坯料120件、紧固件240件，与累计供给一致；各期成品库存都为20件，累计生产分别80、120件。

计算器应返回`aggregate_checks_passed: true`。结果还保留`solver_executed: false`与`full_scheduling_feasibility_proven: false`，因为核算验证的是上述候选的汇总数量关系，未覆盖全部时刻、搬运、切换和任务重叠条件。

`ok`表示输入满足此手算程序的要求；`aggregate_checks_passed`表示候选的资源、物料及库存汇总检查通过。`demand_issue_comparison`逐期列出订单量、假定出库量与差额；`issues_match_due_quantities`只比较这两组数量，不能证明订单分配或准时交付，故`demand_coverage_checked`仍为`false`。缺少配套记录或输入不受支持时，程序返回`ok: false`、定位信息`errors`及非零退出码。

## 6. 维护调整后，为什么要重新检查

另建练习副本：

```bash
python build_example.py --output-dir ./three-hour-maintenance
```

在副本数据库中执行：

```sql
UPDATE capacity SET used=0.375
WHERE workcenter=11 AND time_unit=1;
```

再运行检查与核算。冲压可用时间降为300分钟，200分钟加工仍在汇总能力内。

增加“维护在班初、全部冲压完成后才开始装配、两道工序不重叠”的假设：原条件需要120+200+160=480分钟；维护延长后需要180+200+160=540分钟。由此可见，单设备总量通过，并不等于整个工艺链可在8小时内完成。

下一步应选择具体业务动作，例如允许经确认的转运批次重叠、调整到料与开工时点、调整交付安排，或启用可选时间。将所选条件交给相应排程能力重新运行，再用实际结果复核。

## 7. 把练习迁移到自己的数据

从保留本例对象关系的小改动开始。改变交期或计划期数时，按[第02课](Interface-02-Demand-zh-CN.md)同步出库计划、库存界限、资源日历、供给和人工候选产出；导出的表CSV用于查看，计算以`data.db`为准。每次记录来源、单位、预期变化和检查结果。

此手算脚本适用于单制品`id=1`、一条路线、两道顺序工序、每道工序一个独立资源、OEE100、无准备损失的离散件数练习。每期两道工序产出相等，不带期初在制品；时间单元均为正常生产期。允许按完整步骤增加时期，不自动处理替代路线、共享资源、替代料、共同加工、可选时间或高级批次规则。批次派工、在制品容量、订单分配和详细时间可行性应通过对应模型另行检查。

改变需求不会自动修改`scenario.json`的出库假设或`manual_candidate.csv`的候选产出。先解释差额，再决定改订单、出库安排还是候选方案。迁移到超出上述范围的业务时，继续使用字段和关系检查，并切换到相应DecisioWorks模型与运行配置；不要沿用此手算报告作为完整验收结论。

建议提交给同事共同检查的材料包括：输入表、来源映射、规则配置、运行记录、结果表、前后变化说明。字段查询回到[字段参考](Interface-Fields-zh-CN.md)，业务关系疑问回到[语义详解](Interface-Semantics-zh-CN.md)。
