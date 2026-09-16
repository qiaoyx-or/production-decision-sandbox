# G2 扩展一项能力，保持调用方式清楚

[English](Learning-G2-Extend-a-Capability.md) · [学习中心](Learning-Center-zh-CN.md)

## 先决定扩展的对象
希望增加“按订单类别汇总结果”的功能，通常可以在分析层完成；希望改变求解器接受的约束，则涉及约束或模型适配。先确定功能处理的是数据、规则、目标、分析还是引擎，再选择接入位置。

本课的开发练习是新增“结果复核摘要”：接收已有分析结果，形成订单类别汇总。下面先定义这项扩展的输入、输出和检查方法。

## 设计输入输出
| 项目 | 约定 |
|---|---|
| 输入 | 已有结果、订单类别映射、指标定义 |
| 输出 | 各类别汇总、未能匹配的记录、统计口径 |
| 结果保存位置 | 在ctx.derived下使用独立键保存汇总，避免覆盖其他分析 |
| 失败条件 | 缺少必需映射、数量单位无法确认 |
| 跳过条件 | 应用明确未启用可选汇总 |
| 副作用 | 不修改源数据或已选中的方案 |

先检查结果能否关联到订单。如果结果只按制品、工序或时段汇总，而同一制品对应多张订单，就需要补充明确的分配关系；没有该关系时，应保持原有汇总粒度，并报告尚不能归属到订单的记录。字段按实际对象结构读取，未分类订单也单独列出，保证分类合计与总量可核对。

## 使用标准扩展方式
处理器是执行具体业务逻辑的函数，ctx是保存本次输入、中间结果和状态的执行上下文。开发指南提供handler(ctx)或handler(ctx, params)签名，处理器返回DecisionContext或ActionResult。通过CapabilityRegistry把处理器注册到合适的标准动作，执行层记录调用与结果。

能力条目具有版本、优先级和启用状态。默认解析选取启用且优先级最高的实现。因此提高优先级可能替换同一动作的已有实现，而不是自动追加一个步骤。扩展前检查动作语义与选择方式；需要保留原评估时，采用符合工程模式的组合处理或独立调用安排。

## 让注册、目录和能力编排配方（recipe）保持一致
1. 编写轻量注册函数，避免导入时加载业务数据或启动求解。
2. 让处理器输入输出与所选动作一致。
3. 更新能力目录和说明，提供适用范围。
4. 增加最小配方或调用例子。
5. 检查注册、解析、调用、异常与结果。

单例适合线程安全且无请求状态的服务。每次运行的求解对象与客户数据应留在请求上下文，避免不同任务相互污染。

## 设计正常与错误检查
| 输入情形 | 预期 |
|---|---|
| 类别齐全、单位明确 | 类别合计与总量一致 |
| 存在未知类别 | 输出未分类清单或按约定失败 |
| 缺少必需结果 | 结构化失败 |
| 可选功能关闭 | 明确跳过 |
| 两次不同请求 | 各自结果独立 |

上游未提供有效结果时，扩展应返回相应错误或跳过状态；汇总只读取本次运行的数据。授权和输入错误继续使用既有的结构化错误响应。

## 练习与参考解析
提交扩展说明、输入输出表、注册策略和五条检查用例。解释为什么选择该动作，以及怎样确保原有分析仍执行。

通过条件是能力真实被选中、结果符合口径、异常可解释，并且已有用法保持一致。只看到模块能导入，尚不能证明扩展完成。

## 延伸阅读

[标准动作与编排](https://github.com/qiaoyx-or/decisioworks/wiki/Standard-Actions-and-Orchestration-zh-CN) · [动作、配方与执行参考](https://github.com/qiaoyx-or/decisioworks/wiki/Actions-Recipes-and-Execution-Reference-zh-CN) · [开发指南](https://github.com/qiaoyx-or/decisioworks/wiki/Developer-Guide-Index-zh-CN) · [运行状态与限制](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md) · [工作表：现场规则记录与检查](Worksheet-Operational-Rule-zh-CN.md)

[专题 G](Learning-Topic-G-Actions-Extensions-and-Agents-zh-CN.md) · [上一篇: 读懂并修改一份能力编排配方](Learning-G1-Read-and-Modify-a-Recipe-zh-CN.md) · [下一篇: 为AI Agent写一份可检查的任务说明](Learning-G3-Write-an-Agent-Task-zh-CN.md)
