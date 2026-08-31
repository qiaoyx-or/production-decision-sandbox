[English](Architecture-Overview) | **简体中文**

> 适用于 DecisioWorks v1.4.0

# 总体架构

DecisioWorks 以 `Scene × Business × Model × Solver` 为顶层逻辑，并形成四个相互协作的项目层次。项目层次说明“谁负责什么”，运行链路说明“一次决策怎样流动”，两者不能简单理解为同一条单向流水线。

1. **DataSets**：保存行业场景和标准数据接口实例，回答业务如何被准确表达。
2. **GOCK**：承担模型构建与优化，回答计划如何在明确约束和目标下形成。
3. **DecisioCore**：连接数据、目标、规则、模型、结果与反馈，回答计划如何进入决策。
4. **Web Cockpit**：展示输入、配置、过程、输出与证据，回答能力如何被看见和操作。

文档、工具、容器、测试与发行治理横向支撑这些层次。各层可以独立演进，通过稳定接口、分析结果和反馈信号保持联动。

## 项目层次与运行顺序的区别

DataSets、GOCK、DecisioCore 和 Web Cockpit 是职责层次，不表示程序按该列表顺序依次运行。一次典型运行更接近：

```text
DataSets
   ↓ 业务对象与结构约束
DecisioCore：数据校验、目标与规则、标准动作
   ↓ 模型配置与受控参数
GOCK：模型构建与优化
   ↓ 计划结果与运行状态
DecisioCore：分析、解释、偏差与反馈
   ↓
Web Cockpit / API / 下一轮计划
```

DecisioCore 在求解前后都承担职责：求解前组织模型输入，求解后把计划结果拆解为业务指标、对象明细和下一轮决策依据。

## 为什么采用分层架构

生产场景持续变化，但变化发生的位置不同：字段与关系属于数据层，管理偏好属于目标层，现场经验属于规则控制，流程变化属于能力编排，模型升级属于求解层。分层使每类变化回到相应位置处理，并通过稳定接口保持联动。

## 顶层逻辑：Scene × Business × Model × Solver

- **Scene** 确定行业场景、数据范围与业务边界；
- **Business** 表达订单、工艺、产能、物料、目标和规则；
- **Model** 将业务事实转化为可求解结构；
- **Solver** 在受控参数与授权范围内执行计算。

四个项目层次按照各自职责共同承接这条逻辑。DataSets 提供场景和数据模板，DecisioCore 组织生产决策链，GOCK 提供模型与优化能力，Web 负责展示、操作和验证。

下一步：[组件职责](Component-Responsibilities-zh-CN) · [标准动作与能力编排](Standard-Actions-and-Orchestration-zh-CN)
