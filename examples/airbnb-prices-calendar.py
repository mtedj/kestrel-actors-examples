from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/airbnb-prices-calendar").call(run_input={"locationQueries": ["Lisbon, Portugal"], "checkIn": "30 days", "checkOut": "33 days", "adults": 2, "currency": "EUR", "maxListingsPerQuery": 80, "calendarMonths": 3})
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
listings = [r for r in rows if r["type"] == "listing"]; cal = {r["id"]: r for r in rows if r["type"] == "calendar"}
for l in sorted(listings, key=lambda r: r["price_nightly_effective"] or 0)[:10]: print(l["name"], l["price_nightly_effective"], "occupancy 90d", cal.get(l["id"], {}).get("occupancy_90"))
