# F2 把场景经验沉淀为数据资产与行业模板

[English](Learning-F2-Preserve-Data-Assets-and-Templates.md) · [学习中心](Learning-Center-zh-CN.md)

## 一次接入可以留下什么
企业把订单、工艺、产能和物料整理清楚后，已经形成可复核的业务描述。即使下一步尚在比较实施方案，这些内容也能帮助团队统一口径、发现缺项并减少重复整理。价值需要通过实际复用体现，而不只按数据库大小衡量。

教学情境中，一个车间完成了标准数据接入，准备将方法用于另一个车间。本课的任务是制作能被其他人读懂的模板说明。

## 数据资产包含定义与检查
| 资产 | 应保留的内容 | 复用时检查 |
|---|---|---|
| 对象与字段定义 | 制品、工序、资源、单位 | 同名字段是否同义 |
| 关系映射 | 来源系统到标准对象 | 引用的制品、工序和资源是否存在且对应正确 |
| 业务规则 | 对象、来源、范围、有效期 | 是否仍适合新场景 |
| 能力编排配方（recipe） | 动作、数据源、目标及参数 | 所用能力、版本及运行条件 |
| 检查样例 | 正常输入和错误输入 | 是否发现预期问题 |
| 解释记录 | 结果口径与取舍理由 | 是否能重现判断 |

数据模板与客户数据分开管理。可分享的行业模板可以保留字段、关系、构造样例和检查方法，使用实际企业数据前确认使用范围。

## 从一个车间迁移到另一个
先比较资源、路线、每次加工的产出数量（出件率）、批量、班制和物料关系。相同的接口能降低格式重建，但新车间可能具有不同的工艺或规则，需要重新确认。

例如车间甲按“件”记录需求，车间乙按“箱”下单。模板复用的是对象定义与转换检查，不能把甲的每箱数量直接带到乙。数据资产的作用，是使这个差异容易被发现和定位。

## 建立轻量版本记录
记录数据模板版本、来源说明、字段变更、关联配方和结果检查。修改工艺单耗后，说明受影响制品和下游检查范围。对数据版本建立一致标识，避免同名data.db指向不同业务事实而无人察觉。

DecisioWorks 的标准数据接口提供共同结构，DecisioCore的数据检查、配方和分析记录帮助应用围绕结构积累经验。行业伙伴可以把经过确认的映射与规则组织为模板，再按新场景的工艺、单位和规则进行确认。

## 练习与参考解析
为一个已接入样例制作两页材料：一页说明对象与单位，另一页说明复用前必须检查的五项条件。再提供一条错误样例，例如无法解析的制品引用，并写出期望检查结果。

成果的价值在于其他人能正确使用和检查。只有一份没有解释的数据库文件，难以说明哪些含义稳定、哪些参数可以改变。

## 延伸阅读

[设计原则与差异化](https://github.com/qiaoyx-or/decisioworks/wiki/Design-Principles-and-Differentiation-zh-CN) · [架构总览](https://github.com/qiaoyx-or/decisioworks/wiki/Architecture-Overview-zh-CN) · [生产决策数据资产](https://github.com/qiaoyx-or/decisioworks/wiki/Production-Decision-Data-Assets-zh-CN) · [生态协作](https://github.com/qiaoyx-or/decisioworks/wiki/Ecosystem-Overview-zh-CN) · [伙伴接入](https://github.com/qiaoyx-or/decisioworks/wiki/Partner-Onboarding-and-Integration-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md) · [工作表：复盘与持续改进记录](Worksheet-Review-and-Change-Record-zh-CN.md)

[专题 F](Learning-Topic-F-Open-Collaboration-and-Evolution-zh-CN.md) · [上一篇: 业务变化时，应该调整哪一层](Learning-F1-Place-Changes-in-the-Right-Layer-zh-CN.md) · [下一篇: 企业、咨询与软件伙伴怎样分工](Learning-F3-Define-Ecosystem-Responsibilities-zh-CN.md)
