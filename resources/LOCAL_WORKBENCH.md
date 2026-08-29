# DecisioWorks 本地工作台

工作台与首页、原沙盘分别位于独立目录。公开站点可以查看标准样例、整理配方和生成 Agent 任务包；运行操作通过本机服务连接已经安装的 DecisioWorks。

## 准备

1. 获取完整的 Production Decision Sandbox 项目。
2. 准备完整的 DecisioWorks 运行目录，包含 `DecisioCore`、`DataSets`、`web_cockpit` 和发行时提供的运行组件。
3. 使用该 DecisioWorks 版本支持的 Python 与依赖环境；按其发行说明完成授权。工作台使用原有授权校验。
4. 首版工作台使用 `production_planning` 和 `production_scheduling` 两个标准样例。运行目录需要包含这两个样例及其场景配方。

## 启动

在 Sandbox 项目根目录执行，将占位路径替换为本机的真实路径：

```bash
/path/to/venv/bin/python workbench/serve.py \
  --runtime /path/to/DecisioWorks \
  --python /path/to/venv/bin/python \
  --port 8892
```

Windows PowerShell：

```powershell
& 'C:\path\venv\Scripts\python.exe' workbench\serve.py `
  --runtime 'D:\path\DecisioWorks' `
  --python 'C:\path\venv\Scripts\python.exe' `
  --port 8892
```

访问 `http://127.0.0.1:8892/workbench/`。端口已被占用时，选择另一个空闲端口。服务仅绑定本机回环地址；退出终端前按 Ctrl+C 停止。

工作台服务本身使用 Python 标准库；运行子进程使用 `--python` 指定的 DecisioWorks 环境。请使用完整运行目录，不把受保护组件临时放入源码工程。

## 完成一次比较

1. 选择冲压计划或注塑排程，查看完整输入表及诊断记录。
2. 在“流程与参数”核对必需动作、可选分析动作、目标权重和参数上限。上限来自所连接的运行版本。
3. 在“运行与对比”执行基线。计划结果只来自本次实际执行，运行前为空。
4. 调整一项目标权重或支持的求解参数，执行“调整后重算”。两次结果分别保留，不覆盖基线。
5. 比较输入 SHA-256、参数、实际动作、求解状态和分析指标，再下载运行证据。

失败结果会保留错误码和诊断编号。未授权、超时或没有可用方案均不会显示为成功。权重和目标总分不是时间或实物量；真实指标的单位以当前 DecisioWorks 的分析输出为准。

## 配方与任务包

能力编排配方（recipe）以 JSON 导出，包含标准动作、输入源和运行参数。四个必需动作按顺序执行，分析与结果记录可选择。首版不提供任意脚本节点、DAG 连线或自定义插件执行。

Agent 任务包包含任务说明、结构化上下文、验收条件、允许动作清单及配方。文件不包含原始数据明细、私钥或授权文件。任务包生成不等于 Agent 已执行。

## 版本与数据安全

- 数据文件以只读方式打开；运行前后核对 SHA-256。
- 工作台不上传数据，不调用外部 AI 服务，也不接收任意 Python 代码。
- 运行记录在服务内存中保留最近 20 次；停止服务后消失。需要保留时主动下载证据。
- 运行证据包含本地结果明细，分享前由使用者确认数据公开范围。
- 标准样例的公开快照与本地数据分别标识。本地运行失败时不使用静态结果替代。
- 当前适配接口依据 DecisioWorks v1.4.0。升级运行目录后需重新执行数据、参数、授权负例及实际求解回归。
