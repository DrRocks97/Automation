# 儿童生长发育评估工具
## Pediatric Growth Assessment Tool

基于 WHO 2006 年儿童生长标准的儿童生长发育评估软件。

## 功能特点

- ✅ **体重/年龄评估** (Weight-for-Age)
- ✅ **身高/年龄评估** (Height-for-Age)  
- ✅ **体重/身高评估** (Weight-for-Height)
- ✅ **百分位评估** (P3, P15, P50, P85, P97)
- ✅ **标准差评估** (-3SD 到 +3SD)
- ✅ **Z 评分估算** (Z-score)
- ✅ **临床解读建议**

## 适用人群

0-5 岁 (0-60 个月) 儿童

## 文件结构

```
pediatric_growth_app/
├── who_growth_standards.py    # WHO 生长标准参考数据
├── growth_assessment.py       # 核心评估算法
├── cli_interface.py           # 交互式命令行界面
└── README.md                  # 说明文档
```

## 使用方法

### 方法 1: 交互式命令行

```bash
cd /workspace/pediatric_growth_app
python cli_interface.py
```

按照提示输入:
- 性别 (男/女)
- 年龄 (岁和月)
- 身高 (cm)
- 体重 (kg)

### 方法 2: Python API 调用

```python
from growth_assessment import comprehensive_assessment

# 评估一个 2 岁男孩，身高 87cm，体重 12.5kg
result = comprehensive_assessment(
    sex="male",
    age_years=2,
    age_months=0,
    height_cm=87.0,
    weight_kg=12.5
)

# 查看综合评估摘要
print(result["summary"])

# 查看详细数据
for assessment_type, data in result["assessments"].items():
    print(f"{assessment_type}:")
    print(f"  百分位：{data.get('percentile_range')}")
    print(f"  标准差：{data.get('sd_range')}")
    print(f"  Z 评分：{data.get('z_score_estimate'):.2f}")
```

### 方法 3: 运行测试案例

```bash
cd /workspace/pediatric_growth_app
python growth_assessment.py
```

## 输出指标说明

### 百分位 (Percentile)
- **P3**: 第 3 百分位 (低于 3% 的同龄儿童)
- **P15**: 第 15 百分位
- **P50**: 第 50 百分位 (中位数)
- **P85**: 第 85 百分位
- **P97**: 第 97 百分位 (高于 97% 的同龄儿童)

### 标准差 (Standard Deviation, SD)
- **-3SD**: 低于平均值 3 个标准差
- **-2SD**: 低于平均值 2 个标准差
- **-1SD**: 低于平均值 1 个标准差
- **0SD**: 平均值
- **+1SD**: 高于平均值 1 个标准差
- **+2SD**: 高于平均值 2 个标准差
- **+3SD**: 高于平均值 3 个标准差

### Z 评分 (Z-score)
Z 评分表示测量值与参考人群中位数的标准差距离:
- **正常范围**: -2 到 +2
- **偏低**: < -2
- **偏高**: > +2
- **严重偏低**: < -3
- **严重偏高**: > +3

## 临床意义

| 指标 | Z 评分 < -2 | Z 评分 > +2 |
|------|------------|------------|
| 体重/年龄 | 体重低下 | 超重 |
| 身高/年龄 | 生长迟缓 | 高身材 |
| 体重/身高 | 消瘦 | 超重/肥胖 |

## 数据来源

本工具基于 **WHO Multicentre Growth Reference Study (2006)** 标准数据:
- [WHO Child Growth Standards](https://www.who.int/tools/child-growth-standards)

## 注意事项

⚠️ **重要提示**:
1. 本工具适用于 0-5 岁儿童
2. 评估结果仅供参考，不能替代专业医疗诊断
3. 对于异常结果，建议咨询儿科医生或儿童保健专家
4. 早产儿需要使用矫正年龄进行评估
5. 某些疾病状态可能影响评估结果的准确性

## 技术实现

- **插值算法**: 使用线性插值计算非整数月龄的参考值
- **Z 评分估算**: 基于相邻 SD 值的线性插值
- **数据精度**: 参考数据保留一位小数

## 开发者

为儿科临床医生设计的实用工具

## 许可证

MIT License
