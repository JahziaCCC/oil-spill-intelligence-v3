import asyncio
from datetime import datetime

from ais.collector import collect_ais
from intelligence.maritime_engine import analyze_maritime


print("=" * 60)
print("Oil Spill Intelligence V3")
print("Strategic Maritime Intelligence Engine")
print("=" * 60)
print("وقت التشغيل :", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
print()


# ======================================================
# Collect AIS
# ======================================================

vessels = asyncio.run(collect_ais())


print()
print("=" * 60)
print("ملخص بيانات AIS")
print("=" * 60)
print("عدد السفن المستلمة :", len(vessels))
print("تم تحديث قاعدة البيانات")
print("جاهزية النظام : مكتمل")
print("=" * 60)


# ======================================================
# Analyze
# ======================================================

risk_report = analyze_maritime(vessels)


print()
print("=" * 60)
print("تقرير المخاطر البحرية")
print("=" * 60)


highest = ("", 0)
total = 0


for name, data in risk_report.items():

    print()

    print("📍", name)
    print("-" * 40)

    print("عدد السفن           :", data["ships"])
    print("ناقلات النفط        :", data["tankers"])

    if "moving" in data:
        print("السفن المتحركة      :", data["moving"])

    if "stopped" in data:
        print("السفن المتوقفة      :", data["stopped"])

    print("درجة المخاطر        :", data["risk_score"])
    print("مستوى المخاطر       :", data["risk_level"])

    if "recommendation" in data:
        print("التوصية             :", data["recommendation"])

    total += data["ships"]

    if data["risk_score"] > highest[1]:
        highest = (name, data["risk_score"])


print()
print("=" * 60)
print("الملخص التنفيذي")
print("=" * 60)

print("إجمالي السفن داخل المضائق :", total)
print("أعلى منطقة خطورة :", highest[0])
print("درجة الخطورة :", highest[1])

if highest[1] >= 80:
    status = "🚨 حرج"

elif highest[1] >= 60:
    status = "🟠 مرتفع"

elif highest[1] >= 30:
    status = "🟡 متوسط"

else:
    status = "🟢 منخفض"

print("الحالة العامة :", status)

print()
print("=" * 60)
print("اكتمل تشغيل محرك الذكاء البحري")
print("=" * 60)
