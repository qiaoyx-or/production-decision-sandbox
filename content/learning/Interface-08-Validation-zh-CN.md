# 08 导入、校验并读取业务数据

[English](Interface-08-Validation.md) · [学习指南](Interface-Guide-zh-CN.md) · [语义详解](Interface-Semantics-zh-CN.md)

## 任务：建立一份可解释的数据副本

本课把前七课的基础案例写入独立教学数据库，检查结构与数值，再通过项目数据层读取。共享夹具和备选设备是扩展练习，基础库不默认加入这些额外条件。

## 先完成来源映射

| 来源 | 业务含义 | 目标字段 | 转换 | 检查 |
|---|---|---|---|---|
| 订单O-100的P-1 | 需求制品 | order_item.product | P-1映射到id=1 | 制品存在 |
| 第一日交80件 | 当期交付要求 | delivery_time/number | 时间映射为1，数量80 | 单位为件 |
| 冲压维护2小时 | 八小时窗口内不可用时间 | capacity.used | 2÷8=0.25 | 不重复扣减 |
| 每次4件、10分钟 | 单次加工参数 | productivity/processing_time | 4、600秒 | 批量20可整除 |
| 紧固件首期160个 | 首期就绪量 | kitting_information.number | 160 | 与后续增量分开 |

字段映射除了列名，还应保留转换依据。例如“120”可能是分钟、件数或百分数；仅检查它是数字不够。

## 创建与检查

进入配套`examples`目录，运行：

```bash
python build_example.py --output-dir ./output
python check_example.py ./output/data.db
python test_examples.py
```

创建程序拒绝覆盖已存在的目标数据库。重新练习时指定一个新的输出目录。建表结构来自当前标准模板，不包含客户数据。具体文件与输出见[贯穿案例](Interface-Walkthrough-zh-CN.md)。

检查先核对表、字段类型、主键、可空性和外键声明，再检查每条记录的实际存储值，随后检查引用对象、时间状态、占用比例、批量倍数、OEE范围、组织树、工序编号和库存上下限。即使数据表能打开，缺少外键声明也会使数据库自身漏检非法引用，因此应保留模板定义的关联约束。当前教学模板的数量与批量列采用整数；浮点数必须有限，布尔值只能为0或1，OEE按0至100的百分数检查。类型错误会先返回对象、字段和记录ID，不再继续用错误值做算术检查。文件缺失或数据库损坏时，程序返回错误说明并以非零状态退出。

本练习要求交付需求有交期、产能记录有资源归属、工序适配有工序和工作中心；若填写结果或共享资源记录，其关联对象也必须明确。这些是本练习的业务要求，不改变标准数据库允许为空的字段定义。可空库存界限、未使用的属性槽位、根工作中心的父节点等仍可为空。

输出中的`checks_performed`列出已执行的检查，`checks_skipped`列出因前置错误而未执行的检查，`not_checked`列出本程序不负责的范围。`ok: true`表示本练习已列出的输入检查通过；需求覆盖、完整排程可行性、高级场景规则和模型求解仍须分别验证。反例测试覆盖错误类型、小数批量、越界值、缺失引用和组织树环路。

## 使用项目真实入口

在已安装DecisioWorks依赖的环境中，从项目根目录运行配套脚本：

```bash
python /path/to/examples/load_with_decisioworks.py /path/to/output/data.db
```

脚本使用下列真实入口；`/path/to`替换为文件的实际位置：

```python
import sys
from pathlib import Path

root = Path.cwd()  # 从DecisioWorks项目根目录运行
sys.path.insert(0, str(root / "DecisioCore"))
from data_layer.repository import load_business_data
from data_layer.preprocessing.pipeline import run_preprocessing_pipeline

data = load_business_data("/path/to/output/data.db", source_type="sqlite")
data, report = run_preprocessing_pipeline(data, {
    "enabled": True,
    "handlers": ["validate_batch_productivity_multiple"],
    "failure_policy": "error",
})
print(report)
```

先查看加载后的业务对象和记录数，再选择与该场景匹配的计划模型。配置求解时记录实际启用的产能、工艺、物料、库存、目标和运行参数；缺少配置不能用“表已经齐全”代替。

## 练习与解析

在副本中把`used`改为25，应被比例检查拒绝；把一条交期改成99，应出现引用错误；把批量20改为18、出件率仍为4，应出现倍数错误。每项单独修改并检查，保留原始正确副本。错误定位应指出对象与记录，使修复回到业务来源。

[上一课](Interface-07-Inventory-zh-CN.md) · [下一课：结果与更新](Interface-09-Results-zh-CN.md)
