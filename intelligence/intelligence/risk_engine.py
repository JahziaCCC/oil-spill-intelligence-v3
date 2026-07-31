# intelligence/risk_engine.py

CHOKEPOINTS = {

    "مضيق هرمز": {
        "lat_min": 24,
        "lat_max": 28,
        "lon_min": 54,
        "lon_max": 58
    },

    "باب المندب": {
        "lat_min": 11,
        "lat_max": 14,
        "lon_min": 42,
        "lon_max": 45
    },

    "قناة السويس": {
        "lat_min": 29,
        "lat_max": 32,
        "lon_min": 31,
        "lon_max": 33
    }

}



def inside_zone(vessel, zone):

    lat = vessel.get("lat")
    lon = vessel.get("lon")

    if lat is None or lon is None:
        return False


    return (
        zone["lat_min"] <= lat <= zone["lat_max"]
        and
        zone["lon_min"] <= lon <= zone["lon_max"]
    )





def detect_tanker(vessel):

    name = vessel.get("name","").upper()

    keywords = [
        "TANK",
        "OIL",
        "VLCC",
        "LNG",
        "GAS",
        "CHEM"
    ]

    return any(k in name for k in keywords)





def calculate_risk(vessels):


    report = {}



    for zone_name, zone in CHOKEPOINTS.items():


        ships = []


        for vessel in vessels:

            if inside_zone(vessel, zone):
                ships.append(vessel)



        total = len(ships)



        tankers = 0
        moving = 0
        stopped = 0



        for ship in ships:


            if detect_tanker(ship):
                tankers += 1


            speed = ship.get("speed",0)


            if speed > 1:
                moving += 1
            else:
                stopped += 1




        score = 0


        # كثافة السفن

        if total >= 30:
            score += 40

        elif total >= 10:
            score += 25

        elif total > 0:
            score += 10



        # ناقلات

        score += min(tankers * 10,30)



        # الحركة

        if moving > 20:
            score += 20



        elif moving > 5:
            score += 10



        # التوقفات

        if stopped > 15:
            score += 15




        if score >= 70:

            level = "مرتفع"
            recommendation = "رفع مستوى الجاهزية والمراقبة"

        elif score >= 40:

            level = "متوسط"
            recommendation = "زيادة المتابعة والتحليل"

        else:

            level = "منخفض"
            recommendation = "استمرار المراقبة"




        report[zone_name] = {


            "vessels": total,

            "tankers": tankers,

            "moving": moving,

            "stopped": stopped,

            "risk_score": score,

            "risk_level": level,

            "recommendation": recommendation

        }



    return report
