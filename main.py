import asyncio

from ais.collector import collect_ais
from intelligence.maritime_engine import analyze_maritime


print("=" * 50)
print("Oil Spill Intelligence V3")
print("AIS INTELLIGENCE ENGINE")
print("=" * 50)
print()


# جمع بيانات AIS
vessels = asyncio.run(collect_ais())


print()
print("=" * 50)
print("ملخص نظام AIS")
print("=" * 50)
print("عدد السفن المرصودة:", len(vessels))
print("تم تحديث سجل المسارات")
print("عدد السفن المتتبعة:", len(vessels))
print("=" * 50)


# تحليل المخاطر
risk_report = analyze_maritime(vessels)


print()
print("=" * 50)
print("تقرير المخاطر البحرية على المضائق")
print("=" * 50)


for name, data in risk_report.items():

    print()

    print(name)
    print("عدد السفن:", data["ships"])
    print("ناقلات محتملة:", data["tankers"])

    if "moving" in data:
        print("سفن متحركة:", data["moving"])

    if "stopped" in data:
        print("سفن متوقفة:", data["stopped"])

    print("درجة المخاطر:", data["risk_score"])
    print("مستوى المخاطر:", data["risk_level"])

    if "recommendation" in data:
        print("التوصية:", data["recommendation"])


print()
print("=" * 50)
print("اكتمل محرك الذكاء البحري")
print("=" * 50)
