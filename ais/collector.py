from ais.collector import collect_ais


def main():

    print("=" * 50)
    print("Oil Spill Intelligence V3")
    print("AIS INTELLIGENCE ENGINE")
    print("=" * 50)

    print()
    print("📡 Starting AIS Collector...")

    vessels = collect_ais()

    print()
    print("=" * 50)
    print("AIS SUMMARY")
    print("=" * 50)

    print(f"🚢 AIS Vessels Received: {len(vessels)}")
    print("✅ AIS CACHE UPDATED")

    print("=" * 50)


if __name__ == "__main__":
    main()
