# H2 从小范围验证走向持续运行

[English](Learning-H2-Move-to-Continued-Operation.md) · [学习中心](Learning-Center-zh-CN.md)

## 一次成功运行之后，问题发生了变化
样例运行回答“这组数据和配置能否形成结果”。日常运行还需要回答：数据何时更新、谁确认目标、输入异常如何处理、结果交给谁，以及环境变化怎样检查。把这些事项落实，才能把一次练习接入企业的工作节奏。

## 建立持续运行清单
| 事项 | 需要确定 |
|---|---|
| 数据更新 | 来源、频率、截止时点与完整性检查 |
| 配置管理 | 目标、规则、能力编排配方（recipe）版本及修改权限 |
| 执行环境 | 运行组件、依赖、授权与资源限制 |
| 结果确认 | 复核角色、时点和采用条件 |
| 异常处理 | 失败通知、人工接续和重新运行条件 |
| 记录保存 | 输入版本、配置差异、状态与结论 |

DecisioWorks提供数据、执行、分析和联动能力；应用与团队把它们接入自身更新和确认流程。版本升级、模型变化和新增规则需要通过代表性样例检查，确保原有用法仍然清楚。

## 按证据扩大范围
先选一个决策对象和有限周期，完成数据、结果与业务确认；再增加订单规模、资源范围或规则种类。每次扩展记录新增条件，避免同时改变太多因素后无法定位问题。

| 检查结果 | 下一步选择 |
|---|---|
| 数据、模型与业务判断一致 | 评估扩大到相近范围 |
| 可运行但目标解释不足 | 补指标与复核，不急于扩张 |
| 关键数据或资源关系缺失 | 先完善表达 |
| 当前能力不适合问题结构 | 重新选择模型或设计适配 |

## 让变化有可追溯记录
教学例子：企业新增夜班。更新日历或产能数据后，同时确认人员、维护安排和物料供应。若夜班产能已生成，别在应用层再次按班次数乘总量。保存变更前后输入和运行结果，比较新增班次真正承担了哪些任务。

持续运行的目标是适应变化，而不是保持一组永远不变的参数。保留有效的基础定义、更新已改变的事实，并使重要取舍获得确认。

## 练习与参考解析
为每周一次的计划运行设计一个流程：数据截止、数据检查、运行、复核、采用、记录。再加入一个异常分支：物料数据晚到。

可行答案应明确继续等待、采用经确认的数据版本或转交人工判断的条件，并将未知物料量与已确认可用量区分开。成果是一页可由同事执行的运行清单。

## 学习与应用之间的连续性
场景说明、检查表、配方和结果记录可以沿用到日常工作。每次复盘补充一个已确认的事实或检查，让工具包的基础能力与企业自己的经验共同积累。

## 延伸阅读

[人工复核与可信运行](https://github.com/qiaoyx-or/decisioworks/wiki/Trusted-Operation-and-Human-Review-zh-CN) · [运行状态与限制](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference-zh-CN) · [Web驾驶舱指南](https://github.com/qiaoyx-or/decisioworks/wiki/Web-Cockpit-Guide-zh-CN) · [价值验证与应用框架](https://github.com/qiaoyx-or/decisioworks/wiki/Value-Validation-and-Adoption-Framework-zh-CN)

配套工作表：[工作表：基线与调整方案比较](Worksheet-Plan-Comparison-zh-CN.md) · [工作表：复盘与持续改进记录](Worksheet-Review-and-Change-Record-zh-CN.md)

[专题 H](Learning-Topic-H-Build-Everyday-Decision-Capability-zh-CN.md) · [上一篇: 复核一份计划：从运行状态到业务结论](Learning-H1-Review-a-Plan-zh-CN.md) · [下一篇: 组织一次跨角色的计划复盘](Learning-H3-Run-a-Cross-Functional-Review-zh-CN.md)
