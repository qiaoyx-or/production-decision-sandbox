# G3 为AI Agent写一份可检查的任务说明

[English](Learning-G3-Write-an-Agent-Task.md) · [学习中心](Learning-Center-zh-CN.md)

## 把意图变成明确任务
“帮我优化排程”没有说明数据、允许动作或判断依据。一个可检查的Agent任务应指出使用哪份样例、允许修改什么、需要哪些结果，以及何时交给人确认。

本课使用注塑标准样例，把任务分为两步：先准备只调整`color`权重的配置差异和检查清单；经过确认后，再由具备运行条件的执行环境完成比较。第一步的配置建议与第二步的运行结果分别保存。

## 一份任务说明示例
| 项目 | 内容 |
|---|---|
| 任务 | 在相同数据和约束下比较一个color权重变更 |
| 输入 | 已确认版本的production_scheduling能力编排配方（recipe）及字段说明 |
| 可修改 | color目标权重，值由任务发起人指定 |
| 保持不变 | capacity权重、工作中心、40×3结构、约束、数据 |
| 资源限制 | 从所用运行环境读取允许范围 |
| 第一阶段输出 | 配置差异与执行前检查，不附未运行的结果 |
| 第二阶段输出 | 实际运行状态、结果对照及解释 |
| 人工确认 | 配置提交运行前，以及建议进入业务执行前 |

授权文件由实际执行环境管理，任务包只需包含配置准备所需的信息。使用外部Agent服务时，先确认可分享的数据范围。

## 给Agent明确的检查问题
要求它回答：color映射哪个业务属性；capacity在该配方中是什么意思；哪些输出能证明本次真正运行；不同权重下怎样比较指标；没有可用方案时怎样描述。

这些问题促使Agent依据结构化输入，而不是凭通用排程知识填空。若它把capacity理解成设备产能，先修正解释与配置，再继续运行。

## 区分三类输出
| 类型 | 标识与复核 |
|---|---|
| 配置建议 | 尚未执行，检查参数和差异 |
| 执行请求 | 记录接收方、输入版本及计算资源与时间上限 |
| 运行结果 | 包含实际状态、动作与结果证据 |

复核运行结果时，先匹配本次请求与运行标识，再检查候选方案、选中方案和指标来源。结果说明应能从实际记录追到相应的配置和输出。

使用支持任务包导出的工作台时，可将任务说明、上下文、预期结果与允许动作一并交给所选Agent。随后由使用者或已配置的集成程序发起调用，并检查返回内容；任务包导出本身只完成信息准备。

## 可直接改写的任务文本
下面是给Agent的自然语言任务示例，不是可直接执行的接口请求。方括号中的内容由任务发起人填写；缺少值时，先补充信息。

```text
任务：准备一次只改变color目标权重的注塑排程比较，暂不启动求解。
输入：数据版本[填写]；production_scheduling配方版本[填写]；
      字段说明[提供]；当前运行环境允许的参数范围[提供]。
修改：color从[基线值]改为[目标值]。
保持：数据、约束、capacity权重、工作中心、序列长度、
      循环次数、线程数和时间上限均与基线一致。
先检查：本样例color对应property_1；
        capacity目标关联容器容量property_3，不是设备产能。
提交：基线与建议配置差异、参数检查、缺失信息和待确认项。
遇到未知字段、超限参数或需要改动固定项时，暂停并说明原因。
配置经确认后，由已具备运行条件的执行端分别运行基线和调整方案；
只有拿到实际记录后，再报告状态、序列、两类切换和目标统计量。
```

阅读检查时，若建议配置同时改变了capacity权重，应退回修改；若目标color值尚未填写，应列为待确认；若所有检查通过，可将配置交给运行负责人。这三种状态都与“已获得改善结果”不同。

## 练习与参考解析
编写一份任务说明，并设计两个拒绝条件：请求超出允许参数范围；Agent尝试修改未授权的数据或字段。另写一条正常验收：仅指定权重变化，其他固定项一致。

最终提交任务、配置差异、检查表及状态说明。Agent帮助组织工作，企业人员仍通过明确证据判断配置与方案能否采用。

## 延伸阅读

[标准动作与编排](https://github.com/qiaoyx-or/decisioworks/wiki/Standard-Actions-and-Orchestration-zh-CN) · [动作、配方与执行参考](https://github.com/qiaoyx-or/decisioworks/wiki/Actions-Recipes-and-Execution-Reference-zh-CN) · [开发指南](https://github.com/qiaoyx-or/decisioworks/wiki/Developer-Guide-Index-zh-CN) · [运行状态与限制](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md) · [工作表：现场规则记录与检查](Worksheet-Operational-Rule-zh-CN.md)

[专题 G](Learning-Topic-G-Actions-Extensions-and-Agents-zh-CN.md) · [上一篇: 扩展一项能力，保持调用方式清楚](Learning-G2-Extend-a-Capability-zh-CN.md) · [下一篇: 复核一份计划：从运行状态到业务结论](Learning-H1-Review-a-Plan-zh-CN.md)
