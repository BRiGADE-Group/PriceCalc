"""
In case you wonder, yes this was vibe coded,
In case you wonder why... I was way too fucking lazy IT IS 4:40 AM BRO DON'T PISS ME OFF :sob:

(I also hope you enjoy my very serious and mature comments. <3)

- 0xSenko
"""
import requests
import time

APPIDS = [line.strip() for line in open("ids.txt") if line.strip()] # STRIP?! WHERE??! IS IT LIKE THE SHOES STORE??
ids: int = 0
for _ in APPIDS:
    ids = ids + 1
print("Loaded {ids} AppIDs.".format(ids=ids))
print(f"Estimated calculation time : {ids * 1.5}s.")

COUNTRIES = [ # If you can't understand this, I'm sincerely quetioning how you end up in my code...
    "ar","au","br","ca","cl","cn","co","cz","de","eg",
    "fr","gb","gr","hu","il","in","id","it","jp","kr",
    "mx","my","nl","no","nz","ph","pl","ro","ru","sa",
    "sg","za","es","se","ch","tw","tr","ua","us","ve","vn"
]

rows = requests.get("https://api.frankfurter.dev/v2/rates?base=USD", timeout=10).json() # Saussage?
fx = {row["quote"]: row["rate"] for row in rows}
print(f"FX : {len(fx)} currencies loaded\n")

country_prices = {} # Scream when it hurts...

for i, cc in enumerate(COUNTRIES):
    url = (
        f"https://store.steampowered.com/api/appdetails"  # STEAM MACHINE POWAHHH (sry I wont do this again I promise...) 
        f"?appids={','.join(map(str, APPIDS))}"
        f"&cc={cc}&filters=price_overview"
    )
    try:
        data = requests.get(url, timeout=15).json()
    except Exception as e:
        print(f"[{i+1:2d}/{len(COUNTRIES)}] {cc} — error: {e}")
        continue

    prices = []
    for appid in APPIDS:
        entry = data.get(str(appid), {})
        if not entry.get("success"): # If it succeds, aka what I will never do in life, 'cause I'm a loser, have a nice day :3
            continue
        d = entry.get("data")
        if not isinstance(d, dict):
            continue
        po = d.get("price_overview")
        if not po:
            continue
        usd = (po["final"] / 100) / fx.get(po["currency"], 1)
        prices.append(usd)
# http://batarong.com/ (Click for a surprise!)
    if prices:
        country_prices[cc] = sum(prices) / len(prices) # Calculates the average (in case you failed math grades ^^)
        print(f"[{i+1:2d}/{len(COUNTRIES)}] {cc} — avg ${country_prices[cc]:.2f} ({len(prices)} games)")

    time.sleep(1.5)  # be nice to Steam <3

print(f"\n{'Rank':<5}{'Country':<10}{'Avg (USD)':<12}")
print("-" * 27)
for rank, (cc, avg) in enumerate(sorted(country_prices.items(), key=lambda x: x[1]), 1):
    print(f"{rank:<5}{cc:<10}${avg:.2f}")

best = sorted(country_prices.items(), key=lambda x: x[1])[0]
print(f"\nCheapest: {best[0]} at ${best[1]:.2f}/game") # ...AHHHHHHHHH!!!