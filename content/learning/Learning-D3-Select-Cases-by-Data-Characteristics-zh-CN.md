# D3 按数据属性选择适用案例

[English](Learning-D3-Select-Cases-by-Data-Characteristics.md) · [学习中心](Learning-Center-zh-CN.md)

## 行业名称只提供背景
同属机加行业，一个场景以每日产量分配为主，另一个需要多工序设备排序，还有一个主要处理批量与外协。选择样例时，先看需要作出的决策和已有数据，而不是直接根据“机加”标签选择模型。

选择样例时，可以先按下表整理生产结构，再逐项比较数据和模型是否匹配。

## 制作场景画像
| 维度 | 要记录什么 | 对选择的影响 |
|---|---|---|
| 决策粒度 | 时段数量或精确顺序 | 计划与排程能力不同 |
| 工艺结构 | 固定路线、候选路线、循环序列 | 需要的模型结构 |
| 资源条件 | 单机、并行、共享工装 | 资源约束与关系 |
| 批量 | 固定批量、倍数、多出件 | 数量一致性与整数要求 |
| 切换 | 颜色、规格、模具及方向性 | 属性映射与切换代价定义 |
| 时间 | 班次、维护、交期、冻结范围 | 可用时窗与稳定性 |
| 物料 | 工序消耗、到料、库存 | 上游确认或求解中的物料约束 |

画像可以很短，但应说明证据来自哪个表、字段或业务确认。数据里没有体现共享工装，就不能从行业名称推定共享约束已启用。

## 从相近案例迁移
冲压计划样例适合学习时段需求、产能和齐套联合检查；注塑样例适合学习属性驱动的循环序列。迁移时首先比较这些结构，再替换名称和数据。

| 匹配结果 | 下一步 |
|---|---|
| 结构与约束均匹配 | 使用副本接入，检查单位与规则后运行 |
| 结构匹配，但缺少字段或映射 | 先补数据与说明，再进行链路验证 |
| 需要的规则暂无生效接口 | 明确扩展点与检查方式，先完成小范围适配 |
| 决策结构明显不同 | 重新选择能力或模型，避免套用不合适示例 |

SolverReady说明对应数据与能力组合达到了其报告的检查范围。它不意味着同一数据随意换用另一模型也能求解。

## 做一次对比选择
教学场景X有按日需求、工序级物料和可用产能，当前只需确定每日生产量。场景Y有已释放任务、颜色属性和复用周期，当前需要确定周期中的顺序。X可先参考计划链，Y可先参考循环序列链；若Y还有复杂回流工艺，应继续确认现有模型能否表达。

## 练习与参考解析
先用上文X、Y完成两张画像：X选择按时段数量组织的计划案例，Y选择循环序列案例，并列出各自还需确认的条件。

有数据集时，再选择三个样例各填一张画像，并说明一个最接近的已有案例。列出“可复用内容、需要修改内容、尚待确认条件”。

合格答案以数据关系与决策结构为依据。仅写“都是汽车零部件，因此可复用”不足以支撑选择；能指明相同资源、时间或切换结构，才有可检查的迁移基础。

## 延伸阅读

[冲压计划运行案例](https://github.com/qiaoyx-or/decisioworks/wiki/Stamping-Planning-Case-Walkthrough-zh-CN) · [注塑排程运行案例](https://github.com/qiaoyx-or/decisioworks/wiki/Injection-Molding-Scheduling-Case-Walkthrough-zh-CN) · [端到端场景](https://github.com/qiaoyx-or/decisioworks/wiki/End-to-End-Scenario-Walkthrough-zh-CN) · [场景与问题](https://github.com/qiaoyx-or/decisioworks/wiki/Scenarios-and-Pain-Points-zh-CN)

配套工作表：[工作表：基线与调整方案比较](Worksheet-Plan-Comparison-zh-CN.md)

[专题 D](Learning-Topic-D-Read-Real-Planning-Cases-zh-CN.md) · [上一篇: 注塑排程：解释属性与切换的关系](Learning-D2-Read-Injection-Molding-Changeovers-zh-CN.md) · [下一篇: 从主生产计划到任务释放与作业排程](Learning-E1-Master-Plan-to-Work-Release-zh-CN.md)
