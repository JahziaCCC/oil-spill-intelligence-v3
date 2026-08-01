import json
import os


TREND_FILE = "trend_history.json"


def load_previous():

    if not os.path.exists(TREND_FILE):
        return {}

    try:

        with open(
            TREND_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}


def save_current(report):

    with open(
        TREND_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            ensure_ascii=False,
            indent=4
        )


def analyze_trend(current):

    previous = load_previous()

    result = {}

    for area, data in current.items():

        old = previous.get(area, {})

        old_score = old.get(
            "risk_score",
            0
        )

        new_score = data.get(
            "risk_score",
            0
        )

        diff = new_score - old_score

        if diff > 10:

            trend = "🔺 تصاعد سريع"

        elif diff > 0:

            trend = "🟡 تصاعد"

        elif diff < -10:

            trend = "🔻 انخفاض سريع"

        elif diff < 0:

            trend = "🟢 انخفاض"

        else:

            trend = "⚪ مستقر"

        result[area] = {

            "trend": trend,

            "difference": diff

        }

    save_current(current)

    return result
