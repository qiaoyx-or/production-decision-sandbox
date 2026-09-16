# B3 让产能、班制、维护与齐套使用同一时间坐标

[English](Learning-B3-Align-Time-Capacity-and-Materials.md) · [学习中心](Learning-Center-zh-CN.md)

## “今天有产能”还不够具体
一个班次可用480分钟，已有任务占用25%，再安排维护30分钟，新任务能使用多少时间？答案取决于480分钟是否已经扣除维护、占用比例的分母，以及维护是否与已有任务重叠。先确认这些定义，再计算可用时间。

以下为人工教学假设：480分钟是未扣维护的班次时间，25%占用按480分钟计算，维护与已占任务不重叠。因此剩余时间为480×(1−0.25)−30=330分钟。这个计算适用于上述三项假设；其他产能定义需要使用相应的换算方法。

## 先对齐四类时间
| 信息 | 应关联的对象 | 检查 |
|---|---|---|
| 订单交期 | order_item.delivery_time | 能否解析到时间单元 |
| 资源可用量 | capacity及日历班制 | 范围、时间尺度与折减含义 |
| 物料可用量 | kitting_information.time_unit | 到料时点与数量单位 |
| 计划结果 | planning_result.time_unit | 与输入使用同一时间坐标 |

time_unit.id是引用标识，offset与scale共同解释时间位置和尺度。连续编号不自动代表一天，也不意味着可以直接换算成分钟。需要查看场景的时间定义。

## 比例、数量和时间分别检查
capacity.used采用0到1的比例语义，25%应为0.25；写成25或120分钟都会改变含义。界面可以显示百分比，但存储、计算与显示必须约定一致。

| 条件 | 正确处理思路 |
|---|---|
| 班制已生成净产能 | 核对维护是否已扣除，避免再次扣减 |
| 并行工位已计入capacity | 检查后续是否重复乘以工位数 |
| 物料明日到达 | 对齐到料时间与使用工序，而非只看总量 |
| 需要分钟结果 | 先确定数据原有单位及换算，再标注分钟 |

## 在 DecisioWorks 中做一次检查
选择样例，读取时间、产能、物料可用量和结果表。先挑一个工作中心与一个时间单元，再追溯相关订单和物料。先看总体余量，再检查具体时段与关键物料，找出被平均值掩盖的局部缺口。

实际修改使用数据副本。只更改一段已经确认的维护安排，核对产能生成规则与数据差异，再运行对应计划能力。查看该时段的负荷、等待与未满足需求，不根据平均利用率直接判断影响。

## 练习与参考解析
在上述330分钟假设下，新增任务需要360分钟。按时间总量计算，缺口为30分钟。应检查是否存在可批准的其他时间或资源，并核对连续加工要求与维护时窗，确保新增时间确实能够用于该任务。

如果480分钟本来已经扣除维护，本题公式就不成立。成果应同时保存计算结果与定义依据，使读者知道在哪些条件下可以复算。

## 延伸阅读

[标准化数据接口](https://github.com/qiaoyx-or/decisioworks/wiki/Standardized-Data-Interface-zh-CN) · [数据对象与字段](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Object-and-Field-Reference-zh-CN) · [数据准备与验证](https://github.com/qiaoyx-or/decisioworks/wiki/Data-Readiness-and-Validation-zh-CN) · [ERP与MES数据映射](https://github.com/qiaoyx-or/decisioworks/wiki/ERP-MES-Data-Mapping-Guide-zh-CN)

配套工作表：[工作表：场景与决策任务](Worksheet-Scenario-Brief-zh-CN.md)

[专题 B](Learning-Topic-B-Manufacturing-Data-zh-CN.md) · [上一篇: 工艺路线与工序级BOM：物料在哪一步发生作用](Learning-B2-Routes-and-Operation-Level-BOM-zh-CN.md) · [下一篇: 区分业务事实、约束条件与目标偏好](Learning-C1-Facts-Constraints-and-Preferences-zh-CN.md)
