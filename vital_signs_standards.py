"""
中国儿童生命体征参考值标准 (0-18 岁)
数据来源参考：《诸福棠实用儿科学》第 9 版 及 中国儿科临床指南
"""

# 心率参考值 (次/分) - 格式：{年龄段: (min, max)}
# 注：睡眠时心率可降低 10-20 次，哭闹时可升高
HEART_RATE_STANDARDS = [
    {"age_min": 0, "age_max": 0.083, "label": "新生儿", "min": 100, "max": 205, "avg": 140},  # 0-1 月
    {"age_min": 0.083, "age_max": 0.5, "label": "1-6 月", "min": 100, "max": 180, "avg": 130},
    {"age_min": 0.5, "age_max": 1.0, "label": "6-12 月", "min": 90, "max": 160, "avg": 120},
    {"age_min": 1.0, "age_max": 3.0, "label": "1-3 岁", "min": 80, "max": 140, "avg": 110},
    {"age_min": 3.0, "age_max": 5.0, "label": "3-5 岁", "min": 75, "max": 130, "avg": 100},
    {"age_min": 5.0, "age_max": 8.0, "label": "5-8 岁", "min": 70, "max": 120, "avg": 95},
    {"age_min": 8.0, "age_max": 12.0, "label": "8-12 岁", "min": 65, "max": 110, "avg": 85},
    {"age_min": 12.0, "age_max": 18.0, "label": "12-18 岁", "min": 60, "max": 100, "avg": 75},
]

# 呼吸频率参考值 (次/分)
RESPIRATORY_RATE_STANDARDS = [
    {"age_min": 0, "age_max": 0.083, "label": "新生儿", "min": 40, "max": 60, "avg": 45},
    {"age_min": 0.083, "age_max": 0.5, "label": "1-6 月", "min": 30, "max": 50, "avg": 40},
    {"age_min": 0.5, "age_max": 1.0, "label": "6-12 月", "min": 25, "max": 40, "avg": 35},
    {"age_min": 1.0, "age_max": 3.0, "label": "1-3 岁", "min": 25, "max": 35, "avg": 30},
    {"age_min": 3.0, "max_age": 5.0, "label": "3-5 岁", "min": 20, "max": 30, "avg": 25}, # 修正字段名
    {"age_min": 5.0, "age_max": 8.0, "label": "5-8 岁", "min": 18, "max": 25, "avg": 22},
    {"age_min": 8.0, "age_max": 12.0, "label": "8-12 岁", "min": 15, "max": 22, "avg": 20},
    {"age_min": 12.0, "age_max": 18.0, "label": "12-18 岁", "min": 12, "max": 20, "avg": 16},
]

# 血压参考值 (mmHg)
# 简化版：提供各年龄段的大致正常范围上限 (P95)
# 精确计算需结合身高百分位，此处提供临床快速筛查用的经验值
BLOOD_PRESSURE_STANDARDS = {
    "male": [
        {"age_min": 0, "age_max": 0.083, "sys_min": 60, "sys_max": 80, "dia_min": 30, "dia_max": 50},
        {"age_min": 0.083, "age_max": 0.5, "sys_min": 70, "sys_max": 90, "dia_min": 40, "dia_max": 60},
        {"age_min": 0.5, "age_max": 1.0, "sys_min": 80, "sys_max": 100, "dia_min": 50, "dia_max": 65},
        {"age_min": 1.0, "age_max": 3.0, "sys_min": 85, "sys_max": 105, "dia_min": 50, "dia_max": 70},
        {"age_min": 3.0, "age_max": 6.0, "sys_min": 90, "sys_max": 110, "dia_min": 55, "dia_max": 75},
        {"age_min": 6.0, "age_max": 10.0, "sys_min": 95, "sys_max": 120, "dia_min": 60, "dia_max": 80},
        {"age_min": 10.0, "age_max": 14.0, "sys_min": 100, "sys_max": 130, "dia_min": 60, "dia_max": 85},
        {"age_min": 14.0, "age_max": 18.0, "sys_min": 110, "sys_max": 140, "dia_min": 65, "dia_max": 90},
    ],
    "female": [
        {"age_min": 0, "age_max": 0.083, "sys_min": 60, "sys_max": 78, "dia_min": 30, "dia_max": 48},
        {"age_min": 0.083, "age_max": 0.5, "sys_min": 70, "sys_max": 88, "dia_min": 40, "dia_max": 58},
        {"age_min": 0.5, "age_max": 1.0, "sys_min": 80, "sys_max": 98, "dia_min": 50, "dia_max": 64},
        {"age_min": 1.0, "age_max": 3.0, "sys_min": 85, "sys_max": 103, "dia_min": 50, "dia_max": 68},
        {"age_min": 3.0, "age_max": 6.0, "sys_min": 90, "sys_max": 108, "dia_min": 55, "dia_max": 73},
        {"age_min": 6.0, "age_max": 10.0, "sys_min": 95, "sys_max": 118, "dia_min": 60, "dia_max": 78},
        {"age_min": 10.0, "age_max": 14.0, "sys_min": 100, "sys_max": 128, "dia_min": 60, "dia_max": 83},
        {"age_min": 14.0, "age_max": 18.0, "sys_min": 105, "sys_max": 135, "dia_min": 65, "dia_max": 88},
    ]
}

def get_vital_signs_reference(age_years, gender='male'):
    """
    获取指定年龄和性别的生命体征参考范围
    :param age_years: 年龄 (岁)，浮点数
    :param gender: 'male' 或 'female'
    :return: 包含心率、呼吸、血压参考值的字典
    """
    result = {
        "heart_rate": None,
        "respiratory_rate": None,
        "blood_pressure": None
    }

    # 查找心率
    for item in HEART_RATE_STANDARDS:
        if item["age_min"] <= age_years < item.get("age_max", 99):
            result["heart_rate"] = {
                "range": f"{item['min']}-{item['max']}",
                "min": item["min"],
                "max": item["max"],
                "label": item["label"]
            }
            break

    # 查找呼吸
    for item in RESPIRATORY_RATE_STANDARDS:
        # 兼容字段名可能的拼写差异
        max_age = item.get("age_max") or item.get("max_age")
        if item["age_min"] <= age_years < max_age:
            result["respiratory_rate"] = {
                "range": f"{item['min']}-{item['max']}",
                "min": item["min"],
                "max": item["max"],
                "label": item.get("label", f"{item['age_min']}-{max_age}岁")
            }
            break

    # 查找血压
    bp_data = BLOOD_PRESSURE_STANDARDS.get(gender, BLOOD_PRESSURE_STANDARDS["male"])
    for item in bp_data:
        if item["age_min"] <= age_years < item["age_max"]:
            result["blood_pressure"] = {
                "sys_range": f"{item['sys_min']}-{item['sys_max']}",
                "dia_range": f"{item['dia_min']}-{item['dia_max']}",
                "sys_max": item["sys_max"],
                "dia_max": item["dia_max"],
            }
            break
            
    return result

def evaluate_vital_signs(age, gender, hr=None, rr=None, sbp=None, dbp=None):
    """
    评估生命体征
    :return: 评估结果字典
    """
    refs = get_vital_signs_reference(age, gender)
    evaluation = {
        "heart_rate": {"status": "normal", "msg": "", "ref": refs["heart_rate"]},
        "respiratory_rate": {"status": "normal", "msg": "", "ref": refs["respiratory_rate"]},
        "blood_pressure": {"status": "normal", "msg": "", "ref": refs["blood_pressure"]}
    }

    # 评估心率
    if hr is not None and refs["heart_rate"]:
        if hr < refs["heart_rate"]["min"]:
            evaluation["heart_rate"]["status"] = "low"
            evaluation["heart_rate"]["msg"] = f"心动过缓 (参考: {refs['heart_rate']['range']})"
        elif hr > refs["heart_rate"]["max"]:
            evaluation["heart_rate"]["status"] = "high"
            evaluation["heart_rate"]["msg"] = f"心动过速 (参考: {refs['heart_rate']['range']})"
        else:
            evaluation["heart_rate"]["msg"] = f"正常 (参考: {refs['heart_rate']['range']})"

    # 评估呼吸
    if rr is not None and refs["respiratory_rate"]:
        if rr < refs["respiratory_rate"]["min"]:
            evaluation["respiratory_rate"]["status"] = "low"
            evaluation["respiratory_rate"]["msg"] = f"呼吸缓慢 (参考: {refs['respiratory_rate']['range']})"
        elif rr > refs["respiratory_rate"]["max"]:
            evaluation["respiratory_rate"]["status"] = "high"
            evaluation["respiratory_rate"]["msg"] = f"呼吸急促 (参考: {refs['respiratory_rate']['range']})"
        else:
            evaluation["respiratory_rate"]["msg"] = f"正常 (参考: {refs['respiratory_rate']['range']})"

    # 评估血压
    if sbp is not None and refs["blood_pressure"]:
        status = "normal"
        msgs = []
        if sbp > refs["blood_pressure"]["sys_max"]:
            status = "high"
            msgs.append(f"收缩压偏高 (> {refs['blood_pressure']['sys_max']})")
        if dbp is not None and dbp > refs["blood_pressure"]["dia_max"]:
            status = "high"
            msgs.append(f"舒张压偏高 (> {refs['blood_pressure']['dia_max']})")
        
        if status == "high":
            evaluation["blood_pressure"]["status"] = "high"
            evaluation["blood_pressure"]["msg"] = "; ".join(msgs)
        else:
            evaluation["blood_pressure"]["msg"] = f"正常 (收缩压参考上限：{refs['blood_pressure']['sys_max']})"

    return evaluation
