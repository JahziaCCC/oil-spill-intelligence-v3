# intelligence/trend_engine.py

# محرك اتجاه المخاطر البحرية
# Maritime Risk Trend Engine


import json
import os


HISTORY_FILE = "risk_history.json"



def load_history():

    if not os.path.exists(HISTORY_FILE):

        return {}

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except:

        return {}





def save_history(data):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )






def analyze_trend(report):


    previous = load_history()


    trend_report = {}

    current_snapshot = {}




    for area,data in report.items():


        current_score = data.get(
            "risk_score",
            0
        )


        old_score = previous.get(
            area,
            0
        )



        difference = (
            current_score -
            old_score
        )




        if difference >= 20:

            trend = "🔺 تصاعد سريع"


        elif difference > 0:

            trend = "🔸 ارتفاع"


        elif difference < 0:

            trend = "🔻 انخفاض"


        else:

            trend = "⚪ مستقر"





        trend_report[area] = {


            "trend":

                trend,


            "difference":

                difference,


            "previous_score":

                old_score,


            "current_score":

                current_score

        }




        current_snapshot[area] = current_score





    save_history(
        current_snapshot
    )



    return trend_report
