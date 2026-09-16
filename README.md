# Production Decision Sandbox

DecisioWorks 的产品主页、双语文档与生产决策案例网站。通过输入数据、约束配置、处理过程和结果对比，帮助制造企业、咨询伙伴、软件集成商与开发者理解生产决策工具包的使用方式。

**产品主页：[中文](https://qiaoyx-or.github.io/production-decision-sandbox/) · [English](https://qiaoyx-or.github.io/production-decision-sandbox/en/)**

DecisioWorks 提供可复用的数据接口、目标与规则配置、能力编排、模型求解和结果分析。企业和伙伴可以在这些基础能力上建设自己的场景应用，并随着业务变化持续调整数据、规则与流程。

## 从哪里开始

| 想了解的内容 | 中文 | English |
| --- | --- | --- |
| 产品定位与使用路径 | [从这里开始](https://qiaoyx-or.github.io/production-decision-sandbox/guide/) | [Getting started](https://qiaoyx-or.github.io/production-decision-sandbox/en/guide/) |
| 订单、产能和齐套如何进入计划 | [冲压计划案例](https://qiaoyx-or.github.io/production-decision-sandbox/guide/stamping.html) | [Stamping planning](https://qiaoyx-or.github.io/production-decision-sandbox/en/guide/stamping.html) |
| 产品属性与目标权重怎样影响排程 | [注塑排程案例](https://qiaoyx-or.github.io/production-decision-sandbox/guide/injection-molding.html) | [Injection-molding scheduling](https://qiaoyx-or.github.io/production-decision-sandbox/en/guide/injection-molding.html) |
| 架构、数据接口与运行方法 | [文档中心](https://qiaoyx-or.github.io/production-decision-sandbox/docs/) | [Documentation](https://qiaoyx-or.github.io/production-decision-sandbox/en/docs/) |
| 集成分工与合作路径 | [接入与合作](https://qiaoyx-or.github.io/production-decision-sandbox/guide/partners.html) | [Integration and partnerships](https://qiaoyx-or.github.io/production-decision-sandbox/en/guide/partners.html) |

产品与解决方案白皮书可在主页的[白皮书专区](https://qiaoyx-or.github.io/production-decision-sandbox/#whitepapers)阅读和下载。

## 页面与运行方式

| 入口 | 可以做什么 | 数据与结果来源 |
| --- | --- | --- |
| 产品主页、静态导览、文档中心 | 阅读产品说明、案例、架构图和白皮书 | 已发布资料及标明配置的历史运行记录 |
| 原理沙盘 `sandbox/` | 交互了解数据关系、配置和决策流程 | 浏览器中的示意数据与演示逻辑 |
| 本地工作台 `workbench/` | 查看标准样例、整理配方、生成 Agent 任务包；连接本地服务后运行基线与重算 | 静态模式使用样例快照；本地模式读取所连接的 DecisioWorks 运行环境 |

GitHub Pages 提供静态浏览和前端演示，不接收生产数据或执行在线求解。需要实际运行时，请按照[本地工作台指南](resources/LOCAL_WORKBENCH.md)连接已安装、已授权的 DecisioWorks。

冲压和注塑案例采用标准样例的真实运行记录，并区分 API 结果与独立截图运行。读者可以据此理解方法，再用自己的数据和业务验收条件检查适用性；样例指标不代表客户实施收益。

## 场景准备与伙伴集成

- [伙伴集成指南](resources/PARTNER_INTEGRATION.md)：数据映射、调用方式、结果复核及各方分工。
- [场景与验收记录模板](resources/templates/SCENARIO_AND_ACCEPTANCE.md)：整理业务问题、数据来源、约束、基线与重算结果。
- [完整技术 Wiki](https://github.com/qiaoyx-or/decisioworks/wiki)：查阅更多字段、配置、集成与使用说明。

实际使用范围、源码使用条件和运行资源以所选 DecisioWorks 版本的许可与发行说明为准。分享运行记录或 Agent 任务包前，请确认其中的业务内容适合接收方使用。

## 仓库结构

| 目录 | 内容 |
| --- | --- |
| `index.html`、`en/` | 中英文产品主页及英文页面 |
| `guide/`、`content/guides/` | 静态导览页面及双语 JSON 源内容 |
| `docs/`、`content/docs/` | 文档中心页面及双语 Markdown 源内容 |
| `sandbox/` | 原理沙盘 |
| `workbench/`、`resources/` | 本地工作台、操作指南与集成模板 |
| `assets/`、`downloads/` | 图片与白皮书下载文件 |
| `scripts/` | 静态内容生成与检查脚本 |
| `apps/web/` | 独立的 React 界面示例，参见其 [README](apps/web/README.md) |

## 内容维护与检查

浏览静态网站无需安装依赖。维护内容时，在仓库根目录运行以下命令；文档中心生成需要 Python 3 和 Pandoc，静态导览生成及以下检查使用 Python 标准库。

```bash
python3 scripts/build_docs.py
python3 scripts/build_guides.py
python3 scripts/test_static_site.py
python3 scripts/test_guides.py
python3 scripts/test_public_docs.py
```

先修改 `content/docs/` 或 `content/guides/` 中的源内容，再生成页面，并同时检查中英文版本。只更新本站内容时，直接运行上述生成命令；`--sync-from-wiki` 会用 Wiki 文件覆盖文档源内容，仅在需要重新导入时使用。
