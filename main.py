from ais.collector import collect_ais


print("=" * 50)
print("Oil Spill Intelligence V3")
print("AIS INTELLIGENCE ENGINE")
print("=" * 50)

print("")
print("AIS Collector Starting...")

vessels = collect_ais()

print("")
print("=" * 50)
print("AIS SUMMARY")
print("=" * 50)

print("AIS Vessels Received:", len(vessels))
print("AIS CACHE UPDATED")

print("=" * 50)
