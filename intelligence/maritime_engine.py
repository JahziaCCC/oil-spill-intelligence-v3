from intelligence.risk_engine import calculate_risk


def analyze_maritime(vessels):
    """
    Maritime Intelligence Engine
    """

    print()
    print("=" * 60)
    print("تشغيل محرك الذكاء البحري")
    print("=" * 60)
    print(f"عدد السفن الداخلة للتحليل : {len(vessels)}")

    report = calculate_risk(vessels)

    print("تم الانتهاء من تحليل المخاطر.")
    print("=" * 60)

    return report
