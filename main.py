import asyncio

from ais.collector import collect_ais


print("=" * 50)
print("Oil Spill Intelligence V3")
print("AIS INTELLIGENCE ENGINE")
print("=" * 50)

print()


async def main():

    vessels = await collect_ais(
        duration=120
    )


    print()

    print("FINAL REPORT")
    print("=" * 50)

    print(
        "AIS Vessels Received:",
        len(vessels)
    )

    print("=" * 50)



if __name__ == "__main__":

    asyncio.run(main())
