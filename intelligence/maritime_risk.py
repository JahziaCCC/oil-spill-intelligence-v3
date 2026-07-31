from math import radians, sin, cos, sqrt, atan2


# المناطق الاستراتيجية
CHOKEPOINTS = {

    "مضيق هرمز": {
        "lat_min": 25.5,
        "lat_max": 27.5,
        "lon_min": 55.0,
        "lon_max": 58.0
    },


    "باب المندب": {
        "lat_min": 12.0,
        "lat_max": 13.5,
        "lon_min": 42.0,
        "lon_max": 44.5
    },


    "قناة السويس": {
        "lat_min": 29.5,
        "lat_max": 31.5,
        "lon_min": 31.5,
        "lon_max": 33.0
    }

}



def inside_area(lat, lon, area):

    return (
        area["lat_min"] <= lat <= area["lat_max"]
        and
        area["lon_min"] <= lon <= area["lon_max"]
    )



def calculate_risk(vessels):


    report = {}


    for name, area in CHOKEPOINTS.items():


        ships = []


        for vessel in vessels:


            lat = vessel.get("lat")
            lon = vessel.get("lon")


            if lat is None or lon is None:
                continue


            if inside_area(lat, lon, area):

                ships.append(vessel)



        count = len(ships)



        # حساب المخاطر

        score = 0


        if count >= 10:
            score += 30

        elif count >= 5:
            score += 20

        elif count > 0:
            score += 10



        # وجود ناقلات نفط (مبدئي)
        tankers = 0


        for ship in ships:

            name_ship = ship.get("name","").upper()

            keywords = [
                "TANK",
                "OIL",
                "VLCC",
                "CHEM"
            ]


            if any(k in name_ship for k in keywords):

                tankers += 1



        score += min(tankers * 5, 30)



        if score >= 70:

            level = "مرتفع"

        elif score >= 40:

            level = "متوسط"

        else:

            level = "منخفض"



        report[name] = {

            "ships": count,

            "tankers": tankers,

            "risk_score": score,

            "risk_level": level

        }


    return report
