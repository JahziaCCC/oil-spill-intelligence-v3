import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    حساب المسافة بين نقطتين بالكيلومتر
    """

    R = 6371

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        *
        math.cos(lat2)
        *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)



# المواقع المرجعية للمضائق
CHOKEPOINT_LOCATIONS = {

    "مضيق هرمز": {
        "lat": 26.56,
        "lon": 56.25
    },

    "باب المندب": {
        "lat": 12.58,
        "lon": 43.33
    },

    "قناة السويس": {
        "lat": 30.45,
        "lon": 32.35
    }

}



def calculate_proximity(vessels):

    results = {}

    for name, point in CHOKEPOINT_LOCATIONS.items():

        nearby = []


        for vessel in vessels:

            lat = vessel.get("lat")
            lon = vessel.get("lon")


            if lat is None or lon is None:
                continue


            distance = haversine_distance(
                lat,
                lon,
                point["lat"],
                point["lon"]
            )


            nearby.append({

                "name": vessel.get("name", "UNKNOWN"),
                "mmsi": vessel.get("mmsi"),
                "lat": lat,
                "lon": lon,
                "speed": vessel.get("speed", 0),
                "heading": vessel.get("heading", 0),
                "distance_km": distance

            })


        # ترتيب الأقرب
        nearby = sorted(
            nearby,
            key=lambda x: x["distance_km"]
        )


        results[name] = nearby[:10]


    return results
