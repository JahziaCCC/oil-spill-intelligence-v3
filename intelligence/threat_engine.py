# intelligence/threat_engine.py

# محرك تحليل التهديدات البحرية الاستراتيجية


def classify_vessel(vessel):

    name = vessel.get(
        "name",
        ""
    ).upper()


    tanker_keywords = [
        "TANK",
        "OIL",
        "PETRO",
        "VLCC",
        "CHEM",
        "LNG",
        "GAS"
    ]


    strategic_keywords = [
        "CONTROL",
        "MILITARY",
        "NAVY",
        "GUARDIAN",
        "SUPPORT",
        "PILOT"
    ]


    if any(
        x in name
        for x in tanker_keywords
    ):
        return "ENERGY"


    if any(
        x in name
        for x in strategic_keywords
    ):
        return "STRATEGIC"


    return "COMMERCIAL"





def analyze_threats(vessels, risk_report):


    print()

    print("=" * 60)
    print("تحليل التهديدات البحرية")
    print("=" * 60)



    threat_report = {}



    for area, data in risk_report.items():


        area_vessels = []


        # استخراج السفن التابعة للموقع

        for vessel in vessels:


            lat = vessel.get(
                "lat"
            )

            lon = vessel.get(
                "lon"
            )


            if lat is None or lon is None:
                continue


            # استخدام بيانات المخاطر الموجودة
            # نربط التحليل بالموقع لاحقاً


        energy = data.get(
            "tankers",
            0
        )


        strategic = data.get(
            "strategic",
            0
        )


        stopped = data.get(
            "stopped",
            0
        )


        ships = data.get(
            "ships",
            0
        )



        threats = []



        if energy > 0:

            threats.append(
                {
                    "type":
                    "ناقلات طاقة",

                    "count":
                    energy
                }
            )



        if strategic > 0:

            threats.append(
                {
                    "type":
                    "سفن استراتيجية",

                    "count":
                    strategic
                }
            )



        if ships > 20 and stopped > 10:

            threats.append(
                {
                    "type":
                    "توقف/ازدحام ملاحي",

                    "count":
                    stopped
                }
            )



        if len(threats) >= 2:

            impact = "HIGH"


        elif len(threats) == 1:

            impact = "MEDIUM"


        else:

            impact = "LOW"




        threat_report[area] = {

            "impact":
            impact,


            "threats":
            threats,


            "recommendation":
            get_recommendation(
                impact
            )

        }



    return threat_report





def get_recommendation(level):


    if level == "HIGH":

        return (
            "رفع مستوى الجاهزية "
            "وتكثيف المتابعة"
        )


    elif level == "MEDIUM":

        return (
            "زيادة التحليل والمراقبة"
        )


    else:

        return (
            "استمرار المراقبة"
        )
