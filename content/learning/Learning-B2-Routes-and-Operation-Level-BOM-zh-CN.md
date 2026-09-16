# B2 工艺路线与工序级BOM：物料在哪一步发生作用

[English](Learning-B2-Routes-and-Operation-Level-BOM.md) · [学习中心](Learning-Center-zh-CN.md)

## 一张制品BOM还需要制造顺序
物料清单（BOM）说明制造所需物料，工序级BOM进一步说明在哪一步消耗。教学制品P经过切割、装配两步。每件在切割工序消耗一份坯料，在装配工序消耗两个紧固件。计划10件P时，需要知道20个紧固件用于装配；这会影响何时能够进入该工序。

| 业务对象 | 教学内容 | 对应关系 |
|---|---|---|
| 制品 | P | product |
| 路线 | R-P | process_route.product连接P |
| 工序 | 切割10、装配20 | process.route、process.seqno |
| 资源 | 切割机WC-C、装配台WC-A | process_adaptor连接工序和工作中心 |
| 物料 | 坯料M-1、紧固件M-2 | ingredient连接工序与material |

编号10、20只表示工序顺序。本例假设每执行一次工序产出一件；若实际工序一次产出多件，应分别说明每次加工的产出数量和物料消耗单位。

## 物料进入工序，时间才有含义
若10份坯料今天可用、20个紧固件明天可用，业务上可能允许今天完成切割、明天装配。是否允许这种中间库存、工序拆分和跨时段安排，还要由选用的模型及已启用约束确认。工序级表达提供了检查这些问题所需的位置。

把所有物料只绑定到制品终点，可能掩盖早期工序的物料限制；把全部物料都要求在第一步到齐，也可能过早阻止可开展的工序。正确位置取决于实际消耗点。

## 在数据中逐步复核
1. 确认P的路线与候选路线范围。
2. 检查各工序的顺序、输出与可执行工作中心。
3. 把每条ingredient记录追到具体工序和物料。
4. 核对单耗所依据的数量口径，包括工序次数或产出单位。
5. 将物料可用量映射到相同时间轴，检查是否满足对应工序需求。

本课假设一件成品各经过一次工序、无损耗与副产物，因此10件需10份坯料、20个紧固件。多出件、损耗或联产品场景应先确认所选模型能否表达，再按每次加工的产出数量和物料消耗重新计算；出件率在这里指每次加工的产出数量，不是良品率。

## 改动应该落在哪里
将紧固件单耗从2改为3，教学总需求变为30个。应修改经业务确认的工序物料关系，检查现有可用量，再重算。单纯提高交期权重不会生成缺少的10个紧固件。

修改路线或替代资源时，检查受影响对象，不只看图是否连通。另一条路线可能改变物料、生产率和加工时长，不能只替换工作中心名称。

## 练习与参考解析
为制品P增加一道表面处理，并规定每件耗0.2升处理液。画出路线、资源和物料关系，计算10件在无损耗假设下需要2升处理液。

成果应说明处理液在哪一步消耗、单位是什么、何时可用，以及新工序具备哪些可选资源。这里只完成结构和人工核算；实际计划结果来自启用相应约束后的运行。

## 延伸阅读

[标准化数据接口](https://github.com/qiaoyx-or/decisioworks/wiki/Standardized-Data-Interface-zh-CN) · [数据对象与字段](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Object-and-Field-Reference-zh-CN) · [数据准备与验证](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Readiness-and-Validation-zh-CN) · [ERP与MES数据映射](https://github.com/qiaoyx-or/decisioworks/wiki/ERP-MES-Data-Mapping-Guide-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md)

[专题 B](Learning-Topic-B-Manufacturing-Data-zh-CN.md) · [上一篇: 从业务表格到可计算对象](Learning-B1-Business-Tables-to-Computable-Objects-zh-CN.md) · [下一篇: 让产能、班制、维护与齐套使用同一时间坐标](Learning-B3-Align-Time-Capacity-and-Materials-zh-CN.md)
