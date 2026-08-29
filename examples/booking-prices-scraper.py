from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/booking-prices-scraper").call(run_input={
    "locationQueries": ["Lisbon"], "maxHotelsPerQuery": 50,
    "checkIn": "30 days", "nights": 1, "adults": 2, "currency": "EUR", "sortBy": "price",
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "hotel" and r["price_total"] is not None]
for r in rows[:10]:
    print(r["rank"], r["name"], r["stars"], r["review_score"], r["price_nightly"], r["currency"], r["room_name"])
