import json
import os

from intelligence.risk_engine import calculate_risk


AIS_CACHE_FILE = "data/ais_cache.json"



def load_vessels():

    if not os.path.exists(AIS_CACHE_FILE):
        return []


    with open(
        AIS_CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)




def analyze_maritime():

    vessels = load_vessels()


    print()
    print("=" * 50)
    print("تشغيل محرك تحليل المخاطر البحرية")
    print("=" * 50)

    print("السفن الداخلة للتحليل:", len(vessels))


    report = calculate_risk(vessels)


    return report
