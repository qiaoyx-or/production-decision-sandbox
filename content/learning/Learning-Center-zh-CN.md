# DecisioWorks 学习中心

[English](Learning-Center.md)

从一个生产问题开始，学会表达数据、配置条件、比较方案，并把结果交给合适的人作出决定。

DecisioWorks提供生产决策基础能力，学习中心帮助企业、开发者和伙伴理解并应用这些能力。八个专题、24讲包含案例阅读、配置解释、练习和参考解析。

## 选择学习路径

需要从制造语义一直学到字段配置和可复算案例，可进入[标准化数据接口语义详解](Interface-Guide-zh-CN.md)。专题包含总纲、18表105字段、关系与配置参考、九课练习及完整下载包。

| 你的任务 | 建议顺序 |
|---|---|
| 定义问题与评估方案 | A → D → H |
| 接入数据与配置条件 | B → C → D |
| 组织计划协同 | C → E → H |
| 开发应用与Agent | B → C → F → G |
| 组织伙伴或企业学习 | A → F → D → H |

这些是按任务安排的阅读顺序。每个专题另有“阅读准备与学习成果”，列出需要补读的课程和应形成的记录；可以按问题跳转，不必从头逐页读完。

## 怎样使用案例

课程结合教学算例与真实运行案例：算例给出假设和计算过程，冲压与注塑案例保留v1.4.0运行的日期、配置及结果。阅读时先理解条件，再查看差异与解释。

| 学习方式 | 需要的材料 | 可以完成什么 |
|---|---|---|
| 阅读与手算 | 正文、案例表格、工作表 | 字段解释、单位换算、指标复算与比较结论，无需安装软件 |
| 场景讨论 | 本文教学情境或已确认的业务资料 | 规则说明、任务释放判断、角色分工；缺失条件列为待确认 |
| 运行与开发 | 数据副本、完整配方、匹配依赖和有效授权；开发练习另需测试环境 | 数据接入、基线求解、调整后重算及扩展测试，以实际输出为准 |

需要开始操作时，按[快速开始](https://github.com/qiaoyx-or/decisioworks/wiki/Quick-Start-zh-CN)检查环境和运行入口，并以所用发行包说明为准。术语可查阅[术语表](https://github.com/qiaoyx-or/decisioworks/wiki/Glossary-zh-CN)。不具备运行条件时，仍可先完成阅读与讨论，不将拟议配置写成已运行结果。

## 专题与课程

### [A. 从生产问题到可检验的决策](Learning-Topic-A-Problem-and-Validation-zh-CN.md)

把范围、承诺和可调整条件写清楚，再比较不同方案。三讲依次形成场景说明、验证设计和可比较的结果记录。

- [A1 从一个交付问题定义决策任务](Learning-A1-Define-a-Decision-Task-zh-CN.md)
- [A2 先验证：设计一次有用的计划比较](Learning-A2-Design-a-Useful-Planning-Comparison-zh-CN.md)
- [A3 用同一把尺子比较两个方案](Learning-A3-Compare-Plans-on-the-Same-Basis-zh-CN.md)

### [B. 用数据表达制造过程](Learning-Topic-B-Manufacturing-Data-zh-CN.md)

从订单追到制品、工序、资源和物料，再把它们放在共同时间坐标上。完成三讲后，读者可以检查数据的业务含义，而不仅核对表头。

- [B1 从业务表格到可计算对象](Learning-B1-Business-Tables-to-Computable-Objects-zh-CN.md)
- [B2 工艺路线与工序级BOM：物料在哪一步发生作用](Learning-B2-Routes-and-Operation-Level-BOM-zh-CN.md)
- [B3 让产能、班制、维护与齐套使用同一时间坐标](Learning-B3-Align-Time-Capacity-and-Materials-zh-CN.md)

### [C. 让目标、经验与规则参与决策](Learning-Topic-C-Objectives-and-Operational-Rules-zh-CN.md)

把现场的判断拆成事实、约束、偏好与待批准措施，再通过数据、目标和规则接口表达。重点是解释取舍及其实际影响。

- [C1 区分业务事实、约束条件与目标偏好](Learning-C1-Facts-Constraints-and-Preferences-zh-CN.md)
- [C2 交期、库存与切换：让取舍可以讨论](Learning-C2-Explain-Objective-Tradeoffs-zh-CN.md)
- [C3 把现场经验写成可检查的规则](Learning-C3-Turn-Experience-into-Rules-zh-CN.md)

### [D. 从真实样例学会读计划](Learning-Topic-D-Read-Real-Planning-Cases-zh-CN.md)

使用已发表的v1.4.0冲压与注塑运行记录，沿输入、配置、流程、结果和差异阅读。再将方法迁移到具有相似数据属性的场景。

- [D1 冲压计划：把需求、产能与齐套放在一起看](Learning-D1-Read-a-Stamping-Plan-zh-CN.md)
- [D2 注塑排程：解释属性与切换的关系](Learning-D2-Read-Injection-Molding-Changeovers-zh-CN.md)
- [D3 按数据属性选择适用案例](Learning-D3-Select-Cases-by-Data-Characteristics-zh-CN.md)

### [E. 让计划层级协同工作](Learning-Topic-E-Coordinate-Plans-and-Responses-zh-CN.md)

通过释放条件、偏差和信号连接不同计划层级。学习重点是每层负责什么、传递什么，以及调整后怎样确认影响。

- [E1 从主生产计划到任务释放与作业排程](Learning-E1-Master-Plan-to-Work-Release-zh-CN.md)
- [E2 把变化表达为偏差与计划信号](Learning-E2-Deviations-to-Planning-Signals-zh-CN.md)
- [E3 扰动发生后，确定需要调整的范围](Learning-E3-Scope-a-Disruption-Response-zh-CN.md)

### [F. 开放协作与持续演进](Learning-Topic-F-Open-Collaboration-and-Evolution-zh-CN.md)

确定业务变化涉及哪些模块，把实践中形成的数据定义、规则和流程整理为可复用资产。企业、咨询和软件伙伴通过共同接口协作。

- [F1 业务变化时，应该调整哪一层](Learning-F1-Place-Changes-in-the-Right-Layer-zh-CN.md)
- [F2 把场景经验沉淀为数据资产与行业模板](Learning-F2-Preserve-Data-Assets-and-Templates-zh-CN.md)
- [F3 企业、咨询与软件伙伴怎样分工](Learning-F3-Define-Ecosystem-Responsibilities-zh-CN.md)

### [G. 用标准动作连接应用与AI Agent](Learning-Topic-G-Actions-Extensions-and-Agents-zh-CN.md)

阅读配方、选择扩展位置、编写可检查的Agent任务。通过明确输入输出和状态，让自动化与人工操作共享同一套能力。

- [G1 读懂并修改一份能力编排配方](Learning-G1-Read-and-Modify-a-Recipe-zh-CN.md)
- [G2 扩展一项能力，保持调用方式清楚](Learning-G2-Extend-a-Capability-zh-CN.md)
- [G3 为AI Agent写一份可检查的任务说明](Learning-G3-Write-an-Agent-Task-zh-CN.md)

### [H. 把一次练习变成日常能力](Learning-Topic-H-Build-Everyday-Decision-Capability-zh-CN.md)

让每次运行留下可复核的结论，让下一次调整接续已有经验。三讲覆盖结果复核、持续运行和跨角色复盘。

- [H1 复核一份计划：从运行状态到业务结论](Learning-H1-Review-a-Plan-zh-CN.md)
- [H2 从小范围验证走向持续运行](Learning-H2-Move-to-Continued-Operation-zh-CN.md)
- [H3 组织一次跨角色的计划复盘](Learning-H3-Run-a-Cross-Functional-Review-zh-CN.md)


## 工作表

- [工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md)
- [工作表：基线与调整方案比较](Worksheet-Plan-Comparison-zh-CN.md)
- [工作表：现场规则记录与检查](Worksheet-Operational-Rule-zh-CN.md)
- [工作表：复盘与持续改进记录](Worksheet-Review-and-Change-Record-zh-CN.md)

## 完成一次学习

用自己的话说明问题、数据、约束、取舍和结果，再保存对应记录。能让另一位同事复核，并知道下一步由谁处理，就是一次有用的学习成果。
