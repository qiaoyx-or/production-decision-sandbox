# Production Decision Sandbox Web

独立的 React/Vite 界面示例，用于了解生产决策页面的组织方式。产品主页位于仓库根目录，本目录不参与 GitHub Pages 静态主页的构建。

## 示例内容

- 切换演示数据集与场景；
- 调整交期权重、维护避让参数，观察前端图表变化；
- 查看业务对象表、能力编排图、资源负荷和排程时间轴；
- 对照不同示意方案的指标。

数据来自 `src/data.ts`，运行步骤由前端模拟。图表变化用于说明交互方式，不是 DecisioWorks 的实际求解结果。需要执行基线与重算时，请使用[本地工作台](../../resources/LOCAL_WORKBENCH.md)。

## 本地开发

准备 Node.js 和 npm，在仓库根目录执行：

```bash
cd apps/web
npm ci
npm run dev -- --host 127.0.0.1 --port 5178
```

访问终端显示的本地地址。构建检查使用 `npm run build`；修改本示例无需重新生成根目录的静态主页。
