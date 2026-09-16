# H1 复核一份计划：从运行状态到业务结论

[English](Learning-H1-Review-a-Plan.md) · [学习中心](Learning-Center-zh-CN.md)

## 看见结果表之后，还需要作出判断
一张完整表格可能是历史输入，也可能是新运行输出；一个成功状态可能只表示接口处理完成。采用计划前，应把状态、条件、结果与业务承诺放在一起检查。

下面按运行、条件、业务结果和采用决定组织复核。使用时，将清单项目对应到当前页面或接口中的具体字段。

## 按五层检查
| 层次 | 检查内容 | 需要证据 |
|---|---|---|
| 运行身份 | 本次数据、配置、版本和请求 | 运行记录及关联标识 |
| 状态 | 可用候选、选中方案、停止原因 | 状态与错误信息 |
| 可行条件 | 约束启用、软硬处理、例外 | 配置和约束检查 |
| 业务结果 | 数量、交期、负荷、切换 | 指标单位及明细 |
| 采用决定 | 是否可执行，谁确认措施 | 决策与待办记录 |

DecisioCore的analysis提供结果解释，audit和执行记录帮助追溯动作。它们需要与业务事实相互核对，而不是用一个总体分值取代全部检查。

## 同时看总体和细节
教学观察：总体利用率仅60%，但某瓶颈在T-2超载。总体数字不能否定局部问题。按工作中心与时间单元查看负荷，再追到任务及物料限制。比较粒度应与约束粒度一致。

需求全部完成也未必全部准时。分别检查数量满足、完成时点和承诺交期。若界面把带权目标显示为实际时间，先恢复指标定义与单位，不能据此安排现场。

## 正确处理没有方案的情况
| 现象 | 应如何说明 |
|---|---|
| 输入检查失败 | 哪项数据不满足要求，需要补什么 |
| 授权或组件不可用 | 环境未满足运行条件 |
| 时间耗尽且无候选 | 在本次时间上限内未找到可用方案 |
| 已证明不可行 | 在所设数据和约束下不可行 |
| 有候选但检查未通过 | 暂不能按有效结果采用 |

未成功的运行保留本次状态和错误；需要参考历史方案时，另列其运行标识与日期。这样可以同时追查失败原因和保留可供业务参考的旧计划。

## 做一次结果确认
记录可采用的部分、需要修改的条件和责任人。涉及加班、延期或物料替代时，明确确认状态。重算后保留与原计划的差异，检查新增措施是否真正解决原问题以及是否带来新的代价。

## 练习与参考解析
从已有冲压或注塑案例摘取五项可确认事实，再列三项记录尚不足以证明的结论。例如有120条结果不能证明对应120张订单，数量满足也不能证明准时交付。

合格成果能把“观察、解释、决定”分开，并能指出每个事实的来源。

## 延伸阅读

[人工复核与可信运行](https://github.com/qiaoyx-or/decisioworks/wiki/Trusted-Operation-and-Human-Review-zh-CN) · [运行状态与限制](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference-zh-CN) · [Web驾驶舱指南](https://github.com/qiaoyx-or/decisioworks/wiki/Web-Cockpit-Guide-zh-CN) · [价值验证与应用框架](https://github.com/qiaoyx-or/decisioworks/wiki/Value-Validation-and-Adoption-Framework-zh-CN)

配套工作表：[工作表：基线与调整方案比较](Worksheet-Plan-Comparison-zh-CN.md) · [工作表：复盘与持续改进记录](Worksheet-Review-and-Change-Record-zh-CN.md)

[专题 H](Learning-Topic-H-Build-Everyday-Decision-Capability-zh-CN.md) · [上一篇: 为AI Agent写一份可检查的任务说明](Learning-G3-Write-an-Agent-Task-zh-CN.md) · [下一篇: 从小范围验证走向持续运行](Learning-H2-Move-to-Continued-Operation-zh-CN.md)
