# Production Decision Sandbox

生产决策沙盘系统本地 Web 原型，也是围绕 DecisioWorks 建设的数据诊断、流程编排、规则案例、AI Agent 与教学服务入口。

## 当前版本

- 静态前端，无需安装依赖。
- 展示数据准备、业务关系、能力编排、目标边界、排程时间轴、结果分析与反馈迭代。
- 当前使用演示数据，不连接真实 DecisioWorks / GOCK。
- 后续通过 `decisioworks-adapter` 接入 DecisioWorks 授权调用链路。

## V0.2 规划重点

- 输入数据诊断与 ContractReady / ModelReady / SolverReady 分阶段判断；
- 基于 DecisioWorks 注册能力的可视化流程编排；
- 经验、偏好与规则案例库，其中 `marginal_control` 作为工程标识；
- AI Agent 结构化任务包生成；
- DecisioWorks 分角色教学、练习和真实运行检查点；
- 样例、配方、规则、提示词、教学和证据模板资产中心；
- GitHub Pages 公开主页与本地真实运行环境分离。

详细方案：

- [总体设计](DESIGN.md)
- [V0.2 服务范围补充方案](docs/V0.2_SERVICE_SCOPE.md)
- [GitHub Pages 主页设计](GITHUB_PAGES_DESIGN.md)

## V0.2 模块边界

V0.2 以“外围服务”而非“重型系统”为边界，重点补齐六类能力：

- **可视化流程编排**：把 DecisioWorks 的标准动作和 Recipe 变成可读、可校验、可复用的流程图。
- **输入数据诊断**：判断数据是否达到 ContractReady / ModelReady / SolverReady，而不只是检查字段是否存在。
- **经验、偏好与规则案例**：以 `marginal_control` 等工程标识承接现场经验，使规则有条件、有参数、有证据。
- **AI Agent 任务包**：生成带上下文、允许动作、禁止动作和验收标准的结构化提示词包。
- **DecisioWorks 使用教学**：围绕真实样例形成分角色学习、练习、检查和复盘路径。
- **GitHub Pages 公开主页**：发布公开说明、脱敏样例、教程、模板和下载入口，与本地真实运行严格分离。

## 转化型能力

Sandbox 的 V0.2 不以“功能多”为目标，而以“试点转化”为目标：

- **场景卡**：把客户问题整理成业务问题、所需数据、可验证结果、适用对象和下一步动作。
- **数据资产评分**：把数据诊断结果转成结构完整度、语义清晰度、关系闭合度、约束可用度和运行就绪度。
- **证据包**：沉淀数据版本、配方、参数、结果、分析和人工复核结论。
- **伙伴集成包**：帮助 MES / ERP / WMS 厂商和系统集成商理解如何导出数据、调用能力和嵌入结果。
- **咨询伙伴工作流**：支持咨询伙伴从方案诊断走向数据验证、效果评估和 ROI 判断。
- **AI Agent 模板库**：提供带上下文、允许动作、禁止动作和验收标准的结构化任务模板。
- **公开页转化漏斗**：引导访问者从了解项目进入研究版下载、场景整理、伙伴集成或试点沟通。


## 产品边界

- GitHub Pages 仅发布公开说明、脱敏样例、教程、模板索引和下载入口；
- 客户数据诊断、真实流程运行与方案对比只在本地或客户内网完成；
- 所有真实求解通过 `decisioworks-adapter` 调用 DecisioWorks，不提供 GOCK 内部访问入口；
- AI Agent 提示词不得包含私钥、授权文件、客户原始数据和受保护实现信息。

## 本地运行

```bash
cd /home/qiaoyx/workspace/production-decision-sandbox
python3 -m http.server 5177 --bind 0.0.0.0
```

访问：`http://localhost:5177/`
