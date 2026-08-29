from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/airbnb-occupancy-scraper").call(run_input={
    "locationQueries": ["Lisbon, Portugal"], "maxListingsPerQuery": 50, "months": 3, "currency": "EUR",
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "occupancy"]
by_month = {}
for r in rows:
    by_month.setdefault(r["month"], []).append(r["occupancy_pct"])
for month, pcts in sorted(by_month.items()):
    print(month, round(sum(pcts) / len(pcts), 1), "% occupied across", len(pcts), "listings")
