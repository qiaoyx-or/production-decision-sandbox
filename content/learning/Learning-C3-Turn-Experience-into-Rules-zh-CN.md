# C3 把现场经验写成可检查的规则

[English](Learning-C3-Turn-Experience-into-Rules.md) · [学习中心](Learning-Center-zh-CN.md)

## 经验需要对象、范围和原因
“这台设备最近不稳定，少排一点”包含有价值的判断，但缺少可执行定义。需要确认不稳定影响哪种制品、哪个时段，减少多少，以及何时重新评估。规则写清楚后，经验才能被复用和讨论。

| 规则记录 | 教学示例 |
|---|---|
| 对象 | 工作中心WC-2，今天第二时段 |
| 依据 | 已确认的设备状态检查 |
| 措施 | 分配额度采用经确认的上限 |
| 有效期 | 本时段，复核后续期或取消 |
| 确认人 | 设备负责人提供事实，计划负责人确认安排 |
| 检查 | 额度输入、实际分配与例外记录 |

这份业务说明用于确认规则含义；接入时再将其转换为所选接口要求的字段。

## marginal_control的作用位置
`marginal_control`（规则控制模块）表达现场规则与控制要求，并生成影响分析。`marginalization_analysis`能力编排配方（recipe）演示了`boundary_control`方法：用对象键标识控制对象，`lower_bound`和`upper_bound`分别表示下限和上限，`variable_indices`指定对应的优化变量索引。

`variable_indices`表示变量位置，而不是生产数量。只有在某个变量确实表示指定对象的产量、单位也为“件”时，给它设置`upper_bound=300`才有“最多300件”的业务含义。接入前先确认对象映射、变量单位及模型支持情况。

## 走完四个检查点
1. **表达**：规则记录能说明来源、对象、有效期和计量口径。
2. **分析**：控制输入被解析，报告与对象一致。
3. **应用**：检查相应能力或模型适配器是否读取规则，并将其加入模型或后续处理。
4. **结果**：结合约束配置、执行记录和对象明细核对规则是否得到应用；仅有某次结果恰好满足限额，还不足以说明限额参与了计算。

该分析配方生成控制分析报告。需要让规则影响求解时，还要通过相应能力将其加入配置：可以形成目标调整建议、显式约束或人工待办。沿着报告、配置和执行记录检查，才能看清规则实际发挥了什么作用。

## 处理冲突与到期
新限额可能与交期要求冲突。保存冲突对象、时段及数量，再讨论替代资源、延期或其他措施。多条规则同时存在时，写清优先关系和批准方式，不通过静默覆盖掩盖冲突。

到期规则应重新确认。短期设备问题解除后，如果限制仍然生效，系统会继续按旧条件工作；这正是规则生命周期需要被管理的原因。

## 练习与参考解析
将“重点客户优先”改写为一份规则记录，再写出它与已冻结任务可能发生的冲突。明确“优先”是提高目标偏好，还是必须满足的资源或时间条件。

成果应包含一条正常检查和一条反例：例如有效期已过后不再应用该限制。若当前接口仅产生建议，结论应写“形成建议并等待确认”，而不是“已完成调整”。

## 延伸阅读

[目标与规则控制](https://github.com/qiaoyx-or/decisioworks/wiki/Objectives-and-Rule-Control-zh-CN) · [受控求解与模型适配](https://github.com/qiaoyx-or/decisioworks/wiki/Controlled-Solving-and-Engine-Adapters-zh-CN) · [人工复核与可信运行](https://github.com/qiaoyx-or/decisioworks/wiki/Trusted-Operation-and-Human-Review-zh-CN)

配套工作表：[工作表：基线与调整方案比较](Worksheet-Plan-Comparison-zh-CN.md) · [工作表：现场规则记录与检查](Worksheet-Operational-Rule-zh-CN.md)

[专题 C](Learning-Topic-C-Objectives-and-Operational-Rules-zh-CN.md) · [上一篇: 交期、库存与切换：让取舍可以讨论](Learning-C2-Explain-Objective-Tradeoffs-zh-CN.md) · [下一篇: 冲压计划：把需求、产能与齐套放在一起看](Learning-D1-Read-a-Stamping-Plan-zh-CN.md)
