from intelligence.risk_engine import calculate_risk


def analyze_maritime(vessels):

    print()
    print("=" * 50)
    print("تشغيل محرك تحليل المخاطر البحرية")
    print("=" * 50)
    print("السفن الداخلة للتحليل:", len(vessels))

    report = calculate_risk(vessels)

    return report
