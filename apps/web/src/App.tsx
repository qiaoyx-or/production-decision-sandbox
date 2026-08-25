import { useEffect, useMemo, useRef, useState } from 'react'
import ReactECharts from 'echarts-for-react'
import { ReactFlow, Background, Controls, MarkerType, MiniMap, type Edge, type Node } from '@xyflow/react'
import { Timeline as VisTimeline } from 'vis-timeline/standalone'
import {
  Alert,
  Badge,
  Button,
  Card,
  Col,
  ConfigProvider,
  Divider,
  Flex,
  Layout,
  List,
  Progress,
  Row,
  Segmented,
  Select,
  Slider,
  Space,
  Statistic,
  Steps,
  Table,
  Tabs,
  Tag,
  Timeline,
  Typography,
  theme,
} from 'antd'
import {
  ApartmentOutlined,
  ApiOutlined,
  BranchesOutlined,
  CheckCircleOutlined,
  ClusterOutlined,
  ControlOutlined,
  DashboardOutlined,
  DatabaseOutlined,
  ExperimentOutlined,
  FieldTimeOutlined,
  PlayCircleOutlined,
  ReloadOutlined,
} from '@ant-design/icons'
import dayjs from 'dayjs'
import './App.css'
import {
  apsObjects,
  dataQualityIssues,
  dataReadinessFunnel,
  datasets,
  fieldMappings,
  openSourceReferences,
  pilotChecklist,
  pilotOutputs,
  resourceLoad,
  scenarioCompare,
  scenarios,
  templateAssets,
  workOrders,
  type ApsObject,
  type DatasetKey,
  type ScenarioKey,
} from './data'

const { Header, Content } = Layout
const { Title, Paragraph, Text } = Typography

const statusMap = {
  ready: { color: 'success', text: '已闭合' },
  review: { color: 'warning', text: '需复核' },
  risk: { color: 'error', text: '高优先级' },
} as const

const scenarioColor: Record<ScenarioKey, string> = {
  scheduling: '#2563eb',
  capacity: '#0f9f80',
  material: '#d97706',
  maintenance: '#6d28d9',
}

function App() {
  const [datasetKey, setDatasetKey] = useState<DatasetKey>('discreteA')
  const [scenarioKey, setScenarioKey] = useState<ScenarioKey>('scheduling')
  const [dueWeight, setDueWeight] = useState(70)
  const [maintenanceWeight, setMaintenanceWeight] = useState(62)
  const [runVersion, setRunVersion] = useState(0)
  const [activeStep, setActiveStep] = useState(0)
  const [isRunning, setIsRunning] = useState(false)
  const timelineEl = useRef<HTMLDivElement | null>(null)
  const timelineInstance = useRef<any>(null)

  const selectedDataset = useMemo(
    () => datasets.find((dataset) => dataset.key === datasetKey) ?? datasets[0],
    [datasetKey],
  )

  const selectedScenario = useMemo(
    () => scenarios.find((scenario) => scenario.key === scenarioKey) ?? scenarios[0],
    [scenarioKey],
  )

  const metrics = useMemo(() => {
    const dueDelta = Math.round((dueWeight - 60) / 4)
    const maintenanceDelta = Math.round((maintenanceWeight - 55) / 5)
    const scenarioDelta = scenarioKey === 'scheduling' ? 2 : scenarioKey === 'capacity' ? -1 : scenarioKey === 'material' ? -3 : 0
    const quality = Math.min(97, selectedDataset.dataQuality + (runVersion > 0 ? 3 : 0))
    const due = Math.max(62, Math.min(98, selectedDataset.dueRate + dueDelta + scenarioDelta - Math.max(0, maintenanceDelta - 3)))
    const load = Math.max(52, Math.min(95, selectedDataset.loadPeak - dueDelta + maintenanceDelta))
    const stability = Math.max(50, Math.min(96, 74 + maintenanceDelta * 2 - Math.max(0, dueDelta)))
    return {
      quality,
      due,
      load,
      stability,
      templateCount: selectedDataset.templateCount + (runVersion > 0 ? 1 : 0),
      riskCount: apsObjects.filter((item) => item.readiness !== 'ready').length + (datasetKey === 'dueC' ? 1 : 0),
    }
  }, [datasetKey, dueWeight, maintenanceWeight, runVersion, scenarioKey, selectedDataset])

  const flowNodes = useMemo<Node[]>(() => {
    const nodes = [
      ['data', '数据接入', 'data.db / 字段映射', 0, 80, '#2563eb'],
      ['business', '业务表达', '订单 / BOM / 工艺 / 资源', 240, 80, '#0f9f80'],
      ['boundary', '边界控制', '目标 / 日历 / 维护 / 库存', 510, 80, '#d97706'],
      ['solve', '受控求解', 'DecisioWorks Adapter', 780, 80, '#06b6d4'],
      ['analysis', '结果分析', '交期 / 负载 / 瓶颈 / 异常', 510, 250, '#6d28d9'],
      ['template', '模板沉淀', '数据共建 / 试点报告 / 下一轮', 240, 250, '#dc2626'],
    ] as const

    return nodes.map(([id, label, sub, x, y, color], index) => ({
      id,
      position: { x, y },
      data: {
        label: (
          <div className="flow-node">
            <span style={{ backgroundColor: color }}>{String(index + 1).padStart(2, '0')}</span>
            <strong>{label}</strong>
            <small>{sub}</small>
          </div>
        ),
      },
      style: {
        border: `1px solid ${index <= activeStep ? color : '#dbeafe'}`,
        borderRadius: 18,
        width: 190,
        background: index <= activeStep ? '#ffffff' : '#f8fbff',
        boxShadow: index <= activeStep ? '0 18px 40px rgba(37,99,235,.15)' : 'none',
      },
    }))
  }, [activeStep])

  const flowEdges = useMemo<Edge[]>(
    () => [
      { id: 'e1', source: 'data', target: 'business', markerEnd: { type: MarkerType.ArrowClosed }, animated: activeStep >= 1 },
      { id: 'e2', source: 'business', target: 'boundary', markerEnd: { type: MarkerType.ArrowClosed }, animated: activeStep >= 2 },
      { id: 'e3', source: 'boundary', target: 'solve', markerEnd: { type: MarkerType.ArrowClosed }, animated: activeStep >= 3 },
      { id: 'e4', source: 'solve', target: 'analysis', markerEnd: { type: MarkerType.ArrowClosed }, animated: activeStep >= 4 },
      { id: 'e5', source: 'analysis', target: 'template', markerEnd: { type: MarkerType.ArrowClosed }, animated: activeStep >= 5 },
      { id: 'e6', source: 'template', target: 'business', label: '反馈迭代', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed }, animated: activeStep >= 5 },
    ],
    [activeStep],
  )

  const loadChartOption = useMemo(
    () => ({
      color: ['#2563eb', '#0f9f80', '#d97706'],
      tooltip: { trigger: 'axis' },
      legend: { top: 0, right: 0, data: ['负载', '可用能力', '风险'] },
      grid: { left: 36, right: 16, top: 44, bottom: 34 },
      xAxis: { type: 'category', data: resourceLoad.map((row) => row.resource), axisTick: { show: false } },
      yAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
      series: [
        { name: '负载', type: 'bar', data: resourceLoad.map((row) => Math.min(98, row.load + Math.round((dueWeight - 65) / 5))), barWidth: 18, borderRadius: [6, 6, 0, 0] },
        { name: '可用能力', type: 'line', smooth: true, data: resourceLoad.map((row) => row.available), symbolSize: 8 },
        { name: '风险', type: 'line', smooth: true, data: resourceLoad.map((row) => Math.min(98, row.risk + Math.round((100 - maintenanceWeight) / 8))), lineStyle: { type: 'dashed' } },
      ],
    }),
    [dueWeight, maintenanceWeight],
  )

  const compareOption = useMemo(
    () => ({
      color: ['#2563eb', '#0f9f80', '#d97706', '#6d28d9'],
      tooltip: { trigger: 'axis' },
      legend: { top: 0, right: 0 },
      radar: {
        radius: '62%',
        indicator: [
          { name: '交期', max: 100 },
          { name: '负载', max: 100 },
          { name: '稳定', max: 100 },
          { name: '齐套', max: 100 },
        ],
      },
      series: [
        {
          type: 'radar',
          data: scenarioCompare.map((item) => ({
            name: item.name,
            value: [item.due, item.load, item.stable, 100 - item.shortage],
          })),
        },
      ],
    }),
    [],
  )

  useEffect(() => {
    if (!timelineEl.current) return
    timelineInstance.current?.destroy?.()

    const groups = [
      { id: 'WC-01', content: 'WC-01' },
      { id: 'WC-02', content: 'WC-02' },
      { id: 'WC-03', content: 'WC-03' },
      { id: 'WC-04', content: 'WC-04' },
    ]

    const items = workOrders.map((order) => ({
      id: order.id,
      group: order.resource,
      content: `<b>${order.id}</b><br/><span>${order.item}</span>`,
      start: order.start,
      end: order.end,
      className: `order-${order.type}`,
      title: `${order.item}｜${order.start} - ${order.end}`,
    }))

    timelineInstance.current = new VisTimeline(timelineEl.current, items as any, groups as any, {
      stack: false,
      zoomable: true,
      horizontalScroll: true,
      orientation: 'top',
      margin: { item: 12, axis: 12 },
      start: dayjs('2026-08-14 07:00').toDate(),
      end: dayjs('2026-08-14 22:30').toDate(),
      locale: 'zh-cn',
    } as any)

    return () => timelineInstance.current?.destroy?.()
  }, [datasetKey, runVersion])

  const runSandbox = () => {
    setIsRunning(true)
    setActiveStep(0)
    const steps = [0, 1, 2, 3, 4, 5]
    steps.forEach((step, index) => {
      window.setTimeout(() => {
        setActiveStep(step)
        if (index === steps.length - 1) {
          setRunVersion((value) => value + 1)
          setIsRunning(false)
        }
      }, 420 * (index + 1))
    })
  }

  const resetSandbox = () => {
    setDatasetKey('discreteA')
    setScenarioKey('scheduling')
    setDueWeight(70)
    setMaintenanceWeight(62)
    setActiveStep(0)
    setRunVersion(0)
    setIsRunning(false)
  }



  const dataReadinessOption = useMemo(
    () => ({
      color: ['#2563eb'],
      tooltip: { trigger: 'axis' },
      grid: { left: 36, right: 16, top: 24, bottom: 64 },
      xAxis: {
        type: 'category',
        data: dataReadinessFunnel.map((item) => item.stage),
        axisLabel: { interval: 0, rotate: 24 },
      },
      yAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
      series: [
        {
          name: '闭合度',
          type: 'bar',
          data: dataReadinessFunnel.map((item, index) => Math.max(24, item.value + (metrics.quality - 86) - index * 2)),
          barWidth: 28,
          itemStyle: { borderRadius: [8, 8, 0, 0] },
          label: { show: true, position: 'top', formatter: '{@score}%' },
        },
      ],
      dataset: {
        dimensions: ['stage', 'score'],
        source: dataReadinessFunnel.map((item, index) => ({
          stage: item.stage,
          score: Math.max(24, item.value + (metrics.quality - 86) - index * 2),
        })),
      },
    }),
    [metrics.quality],
  )

  const objectColumns = [
    { title: '对象', dataIndex: 'name', key: 'name', render: (text: string, row: ApsObject) => <Space direction="vertical" size={2}><Text strong>{text}</Text><Text type="secondary">{row.category}</Text></Space> },
    { title: '数量', dataIndex: 'count', key: 'count', width: 92, render: (count: number) => <Text strong>{count}</Text> },
    { title: '关键字段', dataIndex: 'fields', key: 'fields' },
    { title: '状态', dataIndex: 'readiness', key: 'readiness', width: 110, render: (value: ApsObject['readiness']) => <Badge status={statusMap[value].color} text={statusMap[value].text} /> },
    { title: '说明', dataIndex: 'note', key: 'note' },
  ]



  const mappingColumns = [
    { title: '客户字段', dataIndex: 'source', key: 'source' },
    { title: '标准对象', dataIndex: 'target', key: 'target' },
    { title: '业务含义', dataIndex: 'meaning', key: 'meaning' },
    { title: '处理规则', dataIndex: 'rule', key: 'rule' },
    { title: '状态', dataIndex: 'status', key: 'status', width: 110, render: (value: ApsObject['readiness']) => <Badge status={statusMap[value].color} text={statusMap[value].text} /> },
  ]

  const issueColumns = [
    { title: '对象', dataIndex: 'object', key: 'object', width: 120 },
    { title: '问题', dataIndex: 'issue', key: 'issue' },
    { title: '处理建议', dataIndex: 'action', key: 'action' },
    { title: '责任方', dataIndex: 'owner', key: 'owner', width: 150 },
    { title: '状态', dataIndex: 'level', key: 'level', width: 110, render: (value: ApsObject['readiness']) => <Badge status={statusMap[value].color} text={statusMap[value].text} /> },
  ]

  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#2563eb',
          colorSuccess: '#0f9f80',
          colorWarning: '#d97706',
          borderRadius: 18,
          fontFamily: 'Inter, "Segoe UI", "Microsoft YaHei", system-ui, sans-serif',
        },
      }}
    >
      <Layout className="sandbox-layout">
        <Header className="sandbox-header">
          <div className="brand-block">
            <span className="brand-kicker">AI+生产决策 / DecisioWorks</span>
            <Title level={1}>生产决策沙盘工作台</Title>
            <Paragraph>
              不是再做一个重型 APS，而是把数据验证、能力编排、受控求解与结果复核组织成可演化的试点入口。
            </Paragraph>
          </div>
          <div className="header-card">
            <Text type="secondary">当前工作模式</Text>
            <Title level={3}>本地部署 · 试点验证</Title>
            <Tag color="blue">DecisioWorks Adapter</Tag>
            <Tag color="green">GOCK 不暴露</Tag>
          </div>
        </Header>

        <Content className="sandbox-content">
          <Row gutter={[18, 18]}>
            <Col xs={24} xl={6}>
              <Card className="control-card" title="沙盘输入">
                <Space direction="vertical" size="large" className="full-width">
                  <div>
                    <Text strong>数据集</Text>
                    <Select
                      className="control-select"
                      value={datasetKey}
                      onChange={setDatasetKey}
                      options={datasets.map((dataset) => ({ value: dataset.key, label: dataset.name }))}
                    />
                  </div>
                  <div>
                    <Text strong>验证场景</Text>
                    <Select
                      className="control-select"
                      value={scenarioKey}
                      onChange={setScenarioKey}
                      options={scenarios.map((scenario) => ({ value: scenario.key, label: scenario.name }))}
                    />
                  </div>
                  <div>
                    <Flex justify="space-between"><Text strong>交期权重</Text><Text>{dueWeight}%</Text></Flex>
                    <Slider value={dueWeight} min={30} max={95} onChange={setDueWeight} />
                  </div>
                  <div>
                    <Flex justify="space-between"><Text strong>维护避让</Text><Text>{maintenanceWeight}%</Text></Flex>
                    <Slider value={maintenanceWeight} min={20} max={95} onChange={setMaintenanceWeight} />
                  </div>
                  <Space wrap>
                    <Button type="primary" icon={<PlayCircleOutlined />} loading={isRunning} onClick={runSandbox}>
                      运行验证
                    </Button>
                    <Button icon={<ReloadOutlined />} onClick={resetSandbox}>重置</Button>
                  </Space>
                  <Alert
                    type="info"
                    showIcon
                    message="当前为演示数据"
                    description="后续通过 decisioworks-adapter 接入真实 data.db、场景配置与授权求解链路。"
                  />
                </Space>
              </Card>
            </Col>

            <Col xs={24} xl={18}>
              <Row gutter={[18, 18]}>
                <Col xs={24} md={12} xl={6}><Card><Statistic title="数据质量" value={metrics.quality} suffix="%" prefix={<DatabaseOutlined />} /><Progress percent={metrics.quality} strokeColor="#2563eb" /></Card></Col>
                <Col xs={24} md={12} xl={6}><Card><Statistic title="交期满足" value={metrics.due} suffix="%" prefix={<FieldTimeOutlined />} /><Progress percent={metrics.due} strokeColor="#0f9f80" /></Card></Col>
                <Col xs={24} md={12} xl={6}><Card><Statistic title="峰值负载" value={metrics.load} suffix="%" prefix={<DashboardOutlined />} /><Progress percent={metrics.load} strokeColor={metrics.load > 86 ? '#d97706' : '#2563eb'} /></Card></Col>
                <Col xs={24} md={12} xl={6}><Card><Statistic title="模板沉淀" value={metrics.templateCount} prefix={<ClusterOutlined />} /><Progress percent={Math.min(100, metrics.templateCount * 18)} strokeColor="#6d28d9" /></Card></Col>
              </Row>

              <Card className="scenario-card">
                <Flex justify="space-between" align="start" gap={18} wrap="wrap">
                  <div>
                    <Text className="section-kicker">Scenario</Text>
                    <Title level={3}>{selectedScenario.name}</Title>
                    <Paragraph>{selectedScenario.objective}</Paragraph>
                    <Text type="secondary">{selectedDataset.industry}：{selectedDataset.description}</Text>
                  </div>
                  <Segmented
                    value={scenarioKey}
                    onChange={(value) => setScenarioKey(value as ScenarioKey)}
                    options={scenarios.map((scenario) => ({ label: scenario.name, value: scenario.key }))}
                  />
                </Flex>
                <Space wrap className="tag-row">
                  {selectedScenario.emphasis.map((item) => <Tag key={item} color={scenarioColor[scenarioKey]}>{item}</Tag>)}
                  <Tag color="red">风险：{selectedDataset.risk}</Tag>
                </Space>
              </Card>
            </Col>
          </Row>

          <Tabs
            className="main-tabs"
            items={[

              {
                key: 'data',
                label: '数据接入检查',
                children: (
                  <Row gutter={[18, 18]}>
                    <Col xs={24} xl={10}>
                      <Card title={<Space><DatabaseOutlined />数据闭合链路</Space>}>
                        <ReactECharts option={dataReadinessOption} style={{ height: 340 }} />
                        <Alert
                          type="info"
                          showIcon
                          message="数据不是字段对齐，而是业务可计算"
                          description="沙盘先检查字段、对象和关系是否能够进入 DecisioWorks 能力链，再决定是否进入求解验证。"
                        />
                      </Card>
                    </Col>
                    <Col xs={24} xl={14}>
                      <Card title={<Space><ApiOutlined />字段映射样例</Space>} extra={<Tag color="blue">标准化数据接口</Tag>}>
                        <Table
                          rowKey="key"
                          columns={mappingColumns}
                          dataSource={fieldMappings}
                          pagination={false}
                          scroll={{ x: 900 }}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} xl={15}>
                      <Card title={<Space><ExperimentOutlined />数据质量问题清单</Space>}>
                        <Table
                          rowKey="key"
                          columns={issueColumns}
                          dataSource={dataQualityIssues}
                          pagination={false}
                          scroll={{ x: 900 }}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} xl={9}>
                      <Card title={<Space><CheckCircleOutlined />进入试点的判断</Space>}>
                        <List
                          dataSource={pilotChecklist}
                          renderItem={(item, index) => (
                            <List.Item>
                              <List.Item.Meta
                                avatar={<Tag color={index < 2 ? 'blue' : 'green'}>{index + 1}</Tag>}
                                title={<Text strong>{item.title}</Text>}
                                description={item.detail}
                              />
                            </List.Item>
                          )}
                        />
                      </Card>
                    </Col>
                  </Row>
                ),
              },
              {
                key: 'workbench',
                label: '沙盘工作台',
                children: (
                  <Row gutter={[18, 18]}>
                    <Col xs={24} xxl={15}>
                      <Card className="flow-card" title={<Space><BranchesOutlined />能力编排链路</Space>} extra={<Tag color={isRunning ? 'processing' : 'default'}>{isRunning ? '运行中' : '可运行'}</Tag>}>
                        <Steps
                          current={activeStep}
                          size="small"
                          items={['接入数据', '业务表达', '边界控制', '受控求解', '结果分析', '反馈迭代'].map((title) => ({ title }))}
                        />
                        <div className="react-flow-shell">
                          <ReactFlow nodes={flowNodes} edges={flowEdges} fitView nodesDraggable={false} nodesConnectable={false} panOnScroll>
                            <MiniMap pannable zoomable />
                            <Controls />
                            <Background gap={18} color="#dbeafe" />
                          </ReactFlow>
                        </div>
                      </Card>
                    </Col>
                    <Col xs={24} xxl={9}>
                      <Card title={<Space><DashboardOutlined />资源负载与风险</Space>}>
                        <ReactECharts option={loadChartOption} style={{ height: 360 }} />
                      </Card>
                    </Col>
                    <Col xs={24} xxl={15}>
                      <Card title={<Space><FieldTimeOutlined />排程时间轴</Space>} extra={<Text type="secondary">支持缩放与横向滚动</Text>}>
                        <div ref={timelineEl} className="vis-timeline-shell" />
                      </Card>
                    </Col>
                    <Col xs={24} xxl={9}>
                      <Card title={<Space><ExperimentOutlined />方案对比</Space>}>
                        <ReactECharts option={compareOption} style={{ height: 330 }} />
                      </Card>
                    </Col>
                  </Row>
                ),
              },
              {
                key: 'objects',
                label: 'APS 对象模型',
                children: (
                  <Row gutter={[18, 18]}>
                    <Col xs={24} xl={16}>
                      <Card title={<Space><DatabaseOutlined />标准化数据接口对象</Space>}>
                        <Table
                          rowKey="key"
                          columns={objectColumns}
                          dataSource={apsObjects}
                          pagination={false}
                          scroll={{ x: 980 }}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} xl={8}>
                      <Card title={<Space><ApiOutlined />对象关系摘要</Space>}>
                        <Timeline
                          items={[
                            { color: 'blue', children: 'Demand 驱动订单承诺与计划优先级。' },
                            { color: 'green', children: 'Item / BOM / Inventory 承载齐套与供应约束。' },
                            { color: 'orange', children: 'Operation / Resource / Calendar 形成有限产能边界。' },
                            { color: 'purple', children: 'Result / Analysis 回到业务解释与下一轮迭代。' },
                          ]}
                        />
                        <Divider />
                        <Alert
                          type="warning"
                          showIcon
                          message="取舍原则"
                          description="借鉴 frePPLe 等系统的对象与页面组织，但沙盘仍保持验证入口、模板沉淀和生态协作定位，不做重型 APS。"
                        />
                      </Card>
                    </Col>
                  </Row>
                ),
              },

              {
                key: 'report',
                label: '试点输出',
                children: (
                  <Row gutter={[18, 18]}>
                    <Col xs={24} md={8}>
                      <Card className="report-card">
                        <Statistic title="试点成熟度" value={Math.round((metrics.quality + metrics.due + metrics.stability) / 3)} suffix="%" prefix={<ExperimentOutlined />} />
                        <Progress percent={Math.round((metrics.quality + metrics.due + metrics.stability) / 3)} strokeColor="#0f9f80" />
                      </Card>
                    </Col>
                    <Col xs={24} md={8}>
                      <Card className="report-card">
                        <Statistic title="待补数据项" value={metrics.riskCount} prefix={<DatabaseOutlined />} />
                        <Progress percent={Math.min(100, metrics.riskCount * 18)} strokeColor="#d97706" />
                      </Card>
                    </Col>
                    <Col xs={24} md={8}>
                      <Card className="report-card">
                        <Statistic title="可复用资产" value={templateAssets.length} prefix={<ClusterOutlined />} />
                        <Progress percent={Math.min(100, templateAssets.length * 16)} strokeColor="#6d28d9" />
                      </Card>
                    </Col>
                    <Col xs={24} xl={14}>
                      <Card title={<Space><ExperimentOutlined />试点输出物</Space>}>
                        <Timeline
                          items={pilotOutputs.map((item, index) => ({
                            color: index < runVersion + 1 ? 'green' : 'blue',
                            children: (
                              <Space direction="vertical" size={2}>
                                <Space wrap><Text strong>{item.title}</Text><Tag color={index < runVersion + 1 ? 'green' : 'blue'}>{item.status}</Tag></Space>
                                <Text type="secondary">{item.detail}</Text>
                              </Space>
                            ),
                          }))}
                        />
                        <Alert
                          type="success"
                          showIcon
                          message="适合对外表达"
                          description="试点输出强调数据质量、场景边界、运行结果和下一轮建议，而不是承诺一次性交钥匙。"
                        />
                      </Card>
                    </Col>
                    <Col xs={24} xl={10}>
                      <Card title={<Space><ClusterOutlined />模板资产包</Space>}>
                        <List
                          dataSource={templateAssets}
                          renderItem={(item) => (
                            <List.Item>
                              <List.Item.Meta
                                title={<Text strong>{item.name}</Text>}
                                description={item.value}
                              />
                            </List.Item>
                          )}
                        />
                      </Card>
                    </Col>
                    <Col xs={24}>
                      <Card title={<Space><FieldTimeOutlined />从试点到正式接入</Space>}>
                        <Steps
                          current={Math.min(3, runVersion + 1)}
                          items={[
                            { title: '合格数据场景', description: '形成 data.db、映射说明与业务描述' },
                            { title: '沙盘验证', description: '完成数据检查、边界配置、运行与复核' },
                            { title: '伙伴集成', description: 'MES/ERP/咨询伙伴接入模板与接口' },
                            { title: '正式授权', description: '进入 DecisioWorks 授权与本地部署' },
                          ]}
                        />
                      </Card>
                    </Col>
                  </Row>
                ),
              },
              {
                key: 'reference',
                label: '开源 APS 参考',
                children: (
                  <Row gutter={[18, 18]}>
                    <Col xs={24} lg={10}>
                      <Card title={<Space><ApartmentOutlined />参考对象</Space>}>
                        <List
                          dataSource={openSourceReferences}
                          renderItem={(item) => (
                            <List.Item>
                              <List.Item.Meta
                                title={<Text strong>{item.name}</Text>}
                                description={item.value}
                              />
                            </List.Item>
                          )}
                        />
                      </Card>
                    </Col>
                    <Col xs={24} lg={14}>
                      <Card title={<Space><ControlOutlined />沙盘系统吸收什么，不吸收什么</Space>}>
                        <Row gutter={[14, 14]}>
                          <Col xs={24} md={12}>
                            <div className="decision-box accept">
                              <CheckCircleOutlined />
                              <Title level={4}>吸收</Title>
                              <Paragraph>对象模型、数据导入、计划任务、甘特视图、资源负载、异常清单、ERP/MES 集成接口思路。</Paragraph>
                            </div>
                          </Col>
                          <Col xs={24} md={12}>
                            <div className="decision-box reject">
                              <ReloadOutlined />
                              <Title level={4}>不照搬</Title>
                              <Paragraph>不做完整 ERP/MES，不复刻传统 APS 的重实施形态，不暴露 GOCK，不把现场流程固化成唯一答案。</Paragraph>
                            </div>
                          </Col>
                        </Row>
                        <Alert
                          className="bottom-alert"
                          type="success"
                          showIcon
                          message="最终定位"
                          description="沙盘系统是 DecisioWorks 的可视化试点与能力生长界面：先验证数据与场景，再让能力在企业自身和生态伙伴体系中逐步长起来。"
                        />
                      </Card>
                    </Col>
                  </Row>
                ),
              },
            ]}
          />
        </Content>
      </Layout>
    </ConfigProvider>
  )
}

export default App
