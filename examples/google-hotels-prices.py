from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/google-hotels-prices").call(run_input={
    "queries": ["hotels in Lisbon"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "adults": 2, "currency": "USD", "maxHotels": 40})
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
hotels = [r for r in rows if r["type"] == "hotel"]; offers = [r for r in rows if r["type"] == "offer"]
cheapest = min((h for h in hotels if h["nightly"]), key=lambda h: h["nightly"])
print(cheapest["name"], cheapest["nightly_display"], cheapest["total_display"])
