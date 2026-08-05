import json
import os
from datetime import datetime, timezone


EVENTS_CACHE = "data/events_cache.json"



def load_previous():

    if not os.path.exists(EVENTS_CACHE):
        return {}

    try:

        with open(
            EVENTS_CACHE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}





def save_current(report):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        EVENTS_CACHE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            ensure_ascii=False,
            indent=2
        )





def detect_events(current_report):


    previous_report = load_previous()


    events = []


    event_time = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M UTC"
    )



    for area, current in current_report.items():


        old = previous_report.get(
            area,
            {}
        )


        current_ships = current.get(
            "ships",
            0
        )


        old_ships = old.get(
            "ships",
            0
        )



        difference = (
            current_ships -
            old_ships
        )



        # سفن جديدة

        if difference >= 5:

            events.append({

                "area": area,

                "type":
                    "زيادة كثافة ملاحية",

                "severity":
                    "MEDIUM",

                "message":
                    f"زيادة {difference} سفن في {area}",

                "time":
                    event_time
            })





        # انخفاض كبير

        if difference <= -5:

            events.append({

                "area": area,

                "type":
                    "انخفاض النشاط الملاحي",

                "severity":
                    "LOW",

                "message":
                    f"انخفاض {abs(difference)} سفن في {area}",

                "time":
                    event_time
            })





        # ناقلة نفط جديدة

        current_tankers = current.get(
            "tankers",
            0
        )

        old_tankers = old.get(
            "tankers",
            0
        )


        if current_tankers > old_tankers:


            events.append({

                "area": area,

                "type":
                    "دخول ناقلة نفط",

                "severity":
                    "HIGH",

                "message":
                    "تم رصد زيادة في ناقلات النفط",

                "time":
                    event_time

            })





        # سفن استراتيجية

        current_strategic = current.get(
            "strategic",
            0
        )


        old_strategic = old.get(
            "strategic",
            0
        )



        if current_strategic > old_strategic:


            events.append({

                "area": area,

                "type":
                    "سفينة استراتيجية",

                "severity":
                    "HIGH",

                "message":
                    "تم رصد سفينة استراتيجية جديدة",

                "time":
                    event_time

            })





    save_current(
        current_report
    )


    return events
