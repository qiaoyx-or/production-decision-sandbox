# G1 读懂并修改一份能力编排配方

[English](Learning-G1-Read-and-Modify-a-Recipe.md) · [学习中心](Learning-Center-zh-CN.md)

## 用配方说明怎样运行一个场景
能力编排配方（recipe）记录使用哪些能力、按什么顺序运行、输入哪些配置以及期望得到什么。它连接业务意图与标准动作，便于页面、脚本或Agent使用相同过程。

本课以v1.4.0的production_planning.yaml为阅读对象。真实求解需要匹配的运行组件、依赖与有效授权；文件中的参数也应处于当前允许范围内。

## 按五个部分阅读
| 部分 | 本例中要找什么 |
|---|---|
| register | 数据采集与生产能力的注册函数 |
| pipeline | 数据采集、约束解析、生成、选择、评估和结果输出 |
| context.inputs | 数据源、引擎类型与planning配置 |
| expected_outputs | 最佳方案、分析与目标统计量检查 |
| safety | 数据库写入关闭，结果采用独立文件 |

原始数据路径在data_acquisition和production中均有指定时，修改数据源应核对两处一致。文件相对路径按项目的配方加载规则解析。

## 配置片段怎样读
下面摘录配方中的约束与目标配置。执行时使用完整的`production_planning.yaml`，保留数据来源、注册和动作顺序等部分。

```yaml
planning:
  constraints:
    enable_capacity_cons: true
    capacity_soft: true
    enable_demand_cons: true
    demand_cons_mode: 3
    enable_kitting_cons: true
    enable_inventory_cons: false
    CSP: false
  objective:
    job_bias: -0.001
    waittime: 1.0
```

capacity_soft说明产能采用软条件；enable_kitting_cons决定是否启用齐套约束。配置字段以所用版本的配方与接口定义为准。具体枚举如demand_cons_mode应结合当前说明和解析器理解，不能只根据数字猜测。

该配方还通过`initial_objective_overrides`将初始`waittime`设为0，再用`objective_candidate_bridge`把交期或完工期相关意图映射到累计等待时间目标。这里的“桥接”是把业务目标对应到模型能计算的指标。因此，应沿初始配置、目标调整和最终审计查看实际采用的值；`objective`段本身不足以说明运行过程中的全部目标设置。

## 一次修改的过程
复制配方，记录版本和数据来源。只改变一个支持的目标参数，保持其他条件。若研究waittime，先标出初始覆盖值和目标桥接分别在哪一步改变它，再选择当前接口支持的调整位置。运行后以实际生效配置核对修改；若目标值被后续覆盖，应先修正比较设计。通过现有配方加载与执行入口运行，检查实际动作历史、选中方案、production_analysis及错误记录。需要结果文件时使用公开支持的独立输出参数。

`expected_outputs`列出预期输出，运行后应逐项核对状态和结果；如需自动检查，可将其写成测试断言。需要保存JSON结果时，显式设置配方支持的独立输出位置；没有配置时，检查输出动作是否跳过，并在运行记录中注明。

## 练习与参考解析
用不同颜色标出数据来源、业务条件、目标和计算资源与时间上限，写出你打算修改的一项及检查依据。结果应说明加载成功、能力注册成功、动作实际执行和输出成立是不同检查点。

阅读和运行配方可使用相应的脚本入口；使用演示页面时，按页面提供的动作和参数操作。设计有分支或依赖关系的流程时，再查阅DecisioCore执行模块的相应接口。

## 延伸阅读

[标准动作与编排](https://github.com/qiaoyx-or/decisioworks/wiki/Standard-Actions-and-Orchestration-zh-CN) · [动作、配方与执行参考](https://github.com/qiaoyx-or/decisioworks/wiki/Actions-Recipes-and-Execution-Reference-zh-CN) · [开发指南](https://github.com/qiaoyx-or/decisioworks/wiki/Developer-Guide-Index-zh-CN) · [运行状态与限制](https://github.com/qiaoyx-or/decisioworks/wiki/Runtime-Status-Errors-and-Limits-Reference-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md) · [工作表：现场规则记录与检查](Worksheet-Operational-Rule-zh-CN.md)

[专题 G](Learning-Topic-G-Actions-Extensions-and-Agents-zh-CN.md) · [上一篇: 企业、咨询与软件伙伴怎样分工](Learning-F3-Define-Ecosystem-Responsibilities-zh-CN.md) · [下一篇: 扩展一项能力，保持调用方式清楚](Learning-G2-Extend-a-Capability-zh-CN.md)
