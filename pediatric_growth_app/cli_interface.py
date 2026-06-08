"""
Interactive CLI for Pediatric Growth Assessment
儿童生长发育评估工具 - 交互式命令行版本
"""

from growth_assessment import comprehensive_assessment


def get_input(prompt, input_type=float, allow_empty=False):
    """Get validated user input."""
    while True:
        try:
            value = input(prompt).strip()
            if allow_empty and not value:
                return None
            if not value:
                print("❌ 输入不能为空，请重新输入。")
                continue
            return input_type(value)
        except ValueError:
            print(f"❌ 输入无效，请输入{'数字' if input_type == float else '整数'}。")


def get_sex():
    """Get child's sex."""
    while True:
        sex = input("\n请选择性别 (1-男 / 2-女): ").strip()
        if sex in ['1', '男', 'male', 'Male', 'MALE']:
            return 'male'
        elif sex in ['2', '女', 'female', 'Female', 'FEMALE']:
            return 'female'
        else:
            print("❌ 无效选择，请输入 1 或 2。")


def main():
    """Main interactive loop."""
    print("=" * 70)
    print("         儿童生长发育评估工具 (WHO 标准 2006)")
    print("         Pediatric Growth Assessment Tool")
    print("=" * 70)
    print("\n本工具适用于 0-5 岁 (0-60 个月) 儿童")
    print("基于世界卫生组织儿童生长标准")
    
    while True:
        print("\n" + "-" * 70)
        print("请输入儿童信息:")
        
        # Get sex
        sex = get_sex()
        
        # Get age
        age_years = get_input("年龄 - 岁 (整数，0-5): ", int)
        if age_years < 0 or age_years > 5:
            print("⚠️  年龄超出范围，本工具适用于 0-5 岁儿童。")
            continue
        
        age_months = get_input("年龄 - 月 (整数，0-11): ", int)
        if age_months < 0 or age_months > 11:
            print("❌ 月份必须在 0-11 之间。")
            continue
        
        total_months = age_years * 12 + age_months
        if total_months > 60:
            print("⚠️  总月龄超过 60 个月，评估结果可能不准确。")
        
        # Get height
        height_cm = get_input("身高 (cm): ")
        if height_cm < 40 or height_cm > 120:
            print("⚠️  身高值超出常见范围，请确认输入是否正确。")
        
        # Get weight
        weight_kg = get_input("体重 (kg): ")
        if weight_kg < 2 or weight_kg > 30:
            print("⚠️  体重值超出常见范围，请确认输入是否正确。")
        
        # Perform assessment
        print("\n" + "=" * 70)
        print("评估结果:")
        print("=" * 70)
        
        result = comprehensive_assessment(sex, age_years, age_months, height_cm, weight_kg)
        
        # Display child info
        child = result["child_info"]
        sex_cn = "男" if child["sex"] == "male" else "女"
        print(f"\n👶 儿童信息:")
        print(f"   性别：{sex_cn}")
        print(f"   年龄：{child['age']}")
        print(f"   身高：{child['height_cm']} cm")
        print(f"   体重：{child['weight_kg']} kg")
        
        # Display summary
        print(f"\n📊 综合评估:")
        print(result["summary"])
        
        # Display detailed results
        print(f"\n📈 详细数据:")
        
        assessments = result["assessments"]
        
        # Weight-for-age
        wa = assessments["weight_for_age"]
        if "error" not in wa:
            print(f"\n   1️⃣ 体重/年龄 (Weight-for-Age):")
            print(f"      百分位：{wa.get('percentile_range', 'N/A')}")
            print(f"      标准差：{wa.get('sd_range', 'N/A')}")
            if wa.get('z_score_estimate') is not None:
                print(f"      Z 评分：{wa.get('z_score_estimate'):.2f}")
            ref = wa.get('reference_values', {})
            if ref:
                print(f"      参考中位数 (P50): {ref.get('P50', 'N/A')} kg")
        
        # Height-for-age
        ha = assessments["height_for_age"]
        if "error" not in ha:
            print(f"\n   2️⃣ 身高/年龄 (Height-for-Age):")
            print(f"      百分位：{ha.get('percentile_range', 'N/A')}")
            print(f"      标准差：{ha.get('sd_range', 'N/A')}")
            if ha.get('z_score_estimate') is not None:
                print(f"      Z 评分：{ha.get('z_score_estimate'):.2f}")
            ref = ha.get('reference_values', {})
            if ref:
                print(f"      参考中位数 (P50): {ref.get('P50', 'N/A')} cm")
        
        # Weight-for-height
        wh = assessments["weight_for_height"]
        print(f"\n   3️⃣ 体重/身高 (Weight-for-Height):")
        print(f"      百分位：{wh.get('percentile_range', 'N/A')}")
        print(f"      标准差：{wh.get('sd_range', 'N/A')}")
        if wh.get('z_score_estimate') is not None:
            print(f"      Z 评分：{wh.get('z_score_estimate'):.2f}")
        ref = wh.get('reference_values', {})
        if ref:
            print(f"      参考中位数 (P50): {ref.get('P50', 'N/A')} kg")
        
        # Clinical interpretation guide
        print("\n" + "-" * 70)
        print("📖 结果解读参考:")
        print("   • Z 评分在 -2 到 +2 之间：正常范围")
        print("   • Z 评分 < -2：偏低 (需要关注)")
        print("   • Z 评分 > +2：偏高 (需要关注)")
        print("   • Z 评分 < -3 或 > +3：严重偏离 (建议进一步评估)")
        print("-" * 70)
        
        # Continue or exit
        while True:
            choice = input("\n是否继续评估下一个儿童？(y/n): ").strip().lower()
            if choice in ['y', 'yes', '是', '1']:
                break
            elif choice in ['n', 'no', '否', '0']:
                print("\n感谢使用！再见 👋")
                return
            else:
                print("请输入 y 或 n。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断。再见！👋")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        print("请检查输入数据或联系技术支持。")
