"""
Pediatric Growth Assessment Tool
Based on Chinese Growth Standards (首都儿科研究所 0-18 岁)

This module provides functions to assess children's growth parameters
including weight-for-age, height-for-age, and weight-for-height.
"""

import bisect
from chinese_growth_standards import (
    BOYS_WEIGHT_AGE_CN, GIRLS_WEIGHT_AGE_CN,
    BOYS_HEIGHT_AGE_CN, GIRLS_HEIGHT_AGE_CN,
    BOYS_WEIGHT_HEIGHT_CN, GIRLS_WEIGHT_HEIGHT_CN,
    CN_MIN_AGE_MONTHS, CN_MAX_AGE_MONTHS, CN_MIN_HEIGHT_CM, CN_MAX_HEIGHT_CM
)


def calculate_age_in_months(years: int, months: int) -> int:
    """Convert age in years and months to total months."""
    return years * 12 + months


def find_nearest_key(data_dict: dict, target: float) -> tuple:
    """
    Find the nearest key in a dictionary for interpolation.
    Returns (lower_key, upper_key, lower_value, upper_value)
    """
    keys = sorted(data_dict.keys())
    
    if target <= keys[0]:
        return keys[0], keys[0], data_dict[keys[0]], data_dict[keys[0]]
    if target >= keys[-1]:
        return keys[-1], keys[-1], data_dict[keys[-1]], data_dict[keys[-1]]
    
    # Find the position where target would be inserted
    idx = bisect.bisect_right(keys, target)
    lower_key = keys[idx - 1]
    upper_key = keys[idx]
    
    return lower_key, upper_key, data_dict[lower_key], data_dict[upper_key]


def interpolate_value(lower_val: dict, upper_val: dict, fraction: float, metric: str) -> float:
    """Linear interpolation between two values."""
    if lower_val == upper_val:
        return lower_val.get(metric, 0)
    return lower_val.get(metric, 0) + (upper_val.get(metric, 0) - lower_val.get(metric, 0)) * fraction


def get_percentile_and_sd(value: float, reference_data: dict) -> dict:
    """
    Determine the percentile and SD range for a given value.
    Returns detailed assessment information.
    """
    percentiles = ["P3", "P15", "P50", "P85", "P97"]
    sd_values = ["-3SD", "-2SD", "-1SD", "0SD", "+1SD", "+2SD", "+3SD"]
    
    result = {
        "value": value,
        "percentile_range": None,
        "sd_range": None,
        "z_score_estimate": None,
        "assessment": ""
    }
    
    # Get reference values
    p_values = {p: reference_data.get(p, 0) for p in percentiles}
    sd_vals = {sd: reference_data.get(sd, 0) for sd in sd_values}
    
    # Determine percentile range
    if value < p_values["P3"]:
        result["percentile_range"] = "< P3"
    elif value >= p_values["P97"]:
        result["percentile_range"] = "≥ P97"
    else:
        for i in range(len(percentiles) - 1):
            if p_values[percentiles[i]] <= value < p_values[percentiles[i + 1]]:
                result["percentile_range"] = f"P{percentiles[i][1:]} - P{percentiles[i+1][1:]}"
                break
    
    # Determine SD range
    if value < sd_vals["-3SD"]:
        result["sd_range"] = "< -3SD"
    elif value >= sd_vals["+3SD"]:
        result["sd_range"] = "≥ +3SD"
    else:
        sd_pairs = [("-3SD", "-2SD"), ("-2SD", "-1SD"), ("-1SD", "0SD"), 
                    ("0SD", "+1SD"), ("+1SD", "+2SD"), ("+2SD", "+3SD")]
        for lower_sd, upper_sd in sd_pairs:
            if sd_vals[lower_sd] <= value < sd_vals[upper_sd]:
                result["sd_range"] = f"{lower_sd} - {upper_sd}"
                break
    
    # Estimate Z-score using linear interpolation
    if value < sd_vals["0SD"]:
        if value <= sd_vals["-3SD"]:
            result["z_score_estimate"] = -3.0
        else:
            # Find which SD range the value falls into
            sd_ranges = [("-3SD", "-2SD", -3, -2), ("-2SD", "-1SD", -2, -1), ("-1SD", "0SD", -1, 0)]
            for lower_sd_key, upper_sd_key, lower_z, upper_z in sd_ranges:
                if sd_vals[lower_sd_key] <= value < sd_vals[upper_sd_key]:
                    fraction = (value - sd_vals[lower_sd_key]) / (sd_vals[upper_sd_key] - sd_vals[lower_sd_key]) if sd_vals[upper_sd_key] != sd_vals[lower_sd_key] else 0
                    result["z_score_estimate"] = lower_z + fraction
                    break
    else:
        if value >= sd_vals["+3SD"]:
            result["z_score_estimate"] = 3.0
        else:
            sd_ranges = [("0SD", "+1SD", 0, 1), ("+1SD", "+2SD", 1, 2), ("+2SD", "+3SD", 2, 3)]
            for lower_sd_key, upper_sd_key, lower_z, upper_z in sd_ranges:
                if sd_vals[lower_sd_key] <= value < sd_vals[upper_sd_key]:
                    fraction = (value - sd_vals[lower_sd_key]) / (sd_vals[upper_sd_key] - sd_vals[lower_sd_key]) if sd_vals[upper_sd_key] != sd_vals[lower_sd_key] else 0
                    result["z_score_estimate"] = lower_z + fraction
                    break
    
    # Generate assessment
    if result["z_score_estimate"]:
        z = result["z_score_estimate"]
        if z < -3:
            result["assessment"] = "严重偏低 (Severely below normal)"
        elif z < -2:
            result["assessment"] = "偏低 (Below normal)"
        elif z < -1:
            result["assessment"] = "中下 (Low normal)"
        elif z <= 1:
            result["assessment"] = "正常范围 (Normal range)"
        elif z <= 2:
            result["assessment"] = "中上 (High normal)"
        elif z <= 3:
            result["assessment"] = "偏高 (Above normal)"
        else:
            result["assessment"] = "严重偏高 (Severely above normal)"
    
    return result


def assess_weight_for_age(sex: str, age_years: int, age_months: int, weight_kg: float) -> dict:
    """
    Assess weight-for-age based on Chinese standards.
    
    Args:
        sex: 'male' or 'female'
        age_years: Age in years
        age_months: Additional months (0-11)
        weight_kg: Weight in kilograms
    
    Returns:
        Dictionary containing assessment results
    """
    total_months = calculate_age_in_months(age_years, age_months)
    
    if total_months > CN_MAX_AGE_MONTHS:
        return {"error": f"Age exceeds 18 years ({CN_MAX_AGE_MONTHS} months). This tool is designed for children 0-18 years."}
    
    # Select appropriate reference data
    reference_data = BOYS_WEIGHT_AGE_CN if sex.lower() == 'male' else GIRLS_WEIGHT_AGE_CN
    
    # Find nearest age points for interpolation
    lower_month, upper_month, lower_data, upper_data = find_nearest_key(reference_data, total_months)
    
    # Calculate interpolation fraction
    if lower_month == upper_month:
        interpolated_ref = lower_data
    else:
        fraction = (total_months - lower_month) / (upper_month - lower_month)
        interpolated_ref = {}
        for key in lower_data.keys():
            interpolated_ref[key] = interpolate_value(lower_data, upper_data, fraction, key)
    
    # Get assessment
    assessment = get_percentile_and_sd(weight_kg, interpolated_ref)
    
    return {
        "sex": sex,
        "age": f"{age_years} years {age_months} months ({total_months} months)",
        "weight_kg": weight_kg,
        "assessment_type": "Weight-for-Age",
        **assessment,
        "reference_values": interpolated_ref
    }


def assess_height_for_age(sex: str, age_years: int, age_months: int, height_cm: float) -> dict:
    """
    Assess height-for-age based on Chinese standards.
    
    Args:
        sex: 'male' or 'female'
        age_years: Age in years
        age_months: Additional months (0-11)
        height_cm: Height in centimeters
    
    Returns:
        Dictionary containing assessment results
    """
    total_months = calculate_age_in_months(age_years, age_months)
    
    if total_months > CN_MAX_AGE_MONTHS:
        return {"error": f"Age exceeds 18 years ({CN_MAX_AGE_MONTHS} months). This tool is designed for children 0-18 years."}
    
    # Select appropriate reference data
    reference_data = BOYS_HEIGHT_AGE_CN if sex.lower() == 'male' else GIRLS_HEIGHT_AGE_CN
    
    # Find nearest age points for interpolation
    lower_month, upper_month, lower_data, upper_data = find_nearest_key(reference_data, total_months)
    
    # Calculate interpolation fraction
    if lower_month == upper_month:
        interpolated_ref = lower_data
    else:
        fraction = (total_months - lower_month) / (upper_month - lower_month)
        interpolated_ref = {}
        for key in lower_data.keys():
            interpolated_ref[key] = interpolate_value(lower_data, upper_data, fraction, key)
    
    # Get assessment
    assessment = get_percentile_and_sd(height_cm, interpolated_ref)
    
    return {
        "sex": sex,
        "age": f"{age_years} years {age_months} months ({total_months} months)",
        "height_cm": height_cm,
        "assessment_type": "Height-for-Age",
        **assessment,
        "reference_values": interpolated_ref
    }


def assess_weight_for_height(sex: str, height_cm: float, weight_kg: float) -> dict:
    """
    Assess weight-for-height based on Chinese standards.
    
    Args:
        sex: 'male' or 'female'
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
    
    Returns:
        Dictionary containing assessment results
    """
    if height_cm < CN_MIN_HEIGHT_CM or height_cm > CN_MAX_HEIGHT_CM:
        return {"error": f"Height must be between {CN_MIN_HEIGHT_CM}cm and {CN_MAX_HEIGHT_CM}cm for weight-for-height assessment."}
    
    # Select appropriate reference data
    reference_data = BOYS_WEIGHT_HEIGHT_CN if sex.lower() == 'male' else GIRLS_WEIGHT_HEIGHT_CN
    
    # Find nearest height points for interpolation
    lower_height, upper_height, lower_data, upper_data = find_nearest_key(reference_data, height_cm)
    
    # Calculate interpolation fraction
    if lower_height == upper_height:
        interpolated_ref = lower_data
    else:
        fraction = (height_cm - lower_height) / (upper_height - lower_height)
        interpolated_ref = {}
        for key in lower_data.keys():
            interpolated_ref[key] = interpolate_value(lower_data, upper_data, fraction, key)
    
    # Get assessment
    assessment = get_percentile_and_sd(weight_kg, interpolated_ref)
    
    return {
        "sex": sex,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "assessment_type": "Weight-for-Height",
        **assessment,
        "reference_values": interpolated_ref
    }


def comprehensive_assessment(sex: str, age_years: int, age_months: int, 
                            height_cm: float, weight_kg: float) -> dict:
    """
    Perform comprehensive growth assessment including all three indicators.
    
    Args:
        sex: 'male' or 'female'
        age_years: Age in years
        age_months: Additional months (0-11)
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
    
    Returns:
        Dictionary containing all assessment results
    """
    weight_age = assess_weight_for_age(sex, age_years, age_months, weight_kg)
    height_age = assess_height_for_age(sex, age_years, age_months, height_cm)
    weight_height = assess_weight_for_height(sex, height_cm, weight_kg)
    
    return {
        "child_info": {
            "sex": sex,
            "age": f"{age_years} years {age_months} months",
            "height_cm": height_cm,
            "weight_kg": weight_kg
        },
        "assessments": {
            "weight_for_age": weight_age,
            "height_for_age": height_age,
            "weight_for_height": weight_height
        },
        "summary": generate_summary(weight_age, height_age, weight_height)
    }


def generate_summary(weight_age: dict, height_age: dict, weight_height: dict) -> str:
    """Generate a clinical summary based on all assessments."""
    summary_parts = []
    
    # Weight-for-age assessment
    if "error" not in weight_age:
        wa_assessment = weight_age.get("assessment", "")
        wa_percentile = weight_age.get("percentile_range", "")
        summary_parts.append(f"体重年龄：{wa_assessment} ({wa_percentile})")
    
    # Height-for-age assessment
    if "error" not in height_age:
        ha_assessment = height_age.get("assessment", "")
        ha_percentile = height_age.get("percentile_range", "")
        summary_parts.append(f"身高年龄：{ha_assessment} ({ha_percentile})")
    
    # Weight-for-height assessment
    wh_assessment = weight_height.get("assessment", "")
    wh_percentile = weight_height.get("percentile_range", "")
    summary_parts.append(f"体重身高：{wh_assessment} ({wh_percentile})")
    
    # Overall interpretation
    concerns = []
    if weight_age.get("z_score_estimate", 0) < -2:
        concerns.append("体重低下")
    if height_age.get("z_score_estimate", 0) < -2:
        concerns.append("生长迟缓")
    if weight_height.get("z_score_estimate", 0) < -2:
        concerns.append("消瘦")
    if weight_height.get("z_score_estimate", 0) > 2:
        concerns.append("超重/肥胖风险")
    
    if concerns:
        summary_parts.append(f"\n⚠️  关注指标：{', '.join(concerns)}")
    else:
        summary_parts.append("\n✓ 所有指标均在正常范围内")
    
    return "\n".join(summary_parts)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("儿童生长发育评估工具 (WHO标准)")
    print("=" * 70)
    
    # Test case 1: 2-year-old boy
    print("\n【案例 1】2 岁男孩，身高 87cm，体重 12.5kg")
    result = comprehensive_assessment("male", 2, 0, 87.0, 12.5)
    print(result["summary"])
    
    print("\n详细数据:")
    for assessment_type, data in result["assessments"].items():
        print(f"\n{assessment_type}:")
        print(f"  百分位范围：{data.get('percentile_range', 'N/A')}")
        print(f"  标准差范围：{data.get('sd_range', 'N/A')}")
        print(f"  Z 评分估计：{data.get('z_score_estimate', 'N/A'):.2f}" if data.get('z_score_estimate') else "  Z 评分估计：N/A")
    
    # Test case 2: 1-year-old girl
    print("\n" + "=" * 70)
    print("\n【案例 2】1 岁 6 个月女孩，身高 80cm，体重 10.2kg")
    result2 = comprehensive_assessment("female", 1, 6, 80.0, 10.2)
    print(result2["summary"])
    
    print("\n详细数据:")
    for assessment_type, data in result2["assessments"].items():
        print(f"\n{assessment_type}:")
        print(f"  百分位范围：{data.get('percentile_range', 'N/A')}")
        print(f"  标准差范围：{data.get('sd_range', 'N/A')}")
        if data.get('z_score_estimate'):
            print(f"  Z 评分估计：{data.get('z_score_estimate'):.2f}")
