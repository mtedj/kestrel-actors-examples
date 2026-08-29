from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/agoda-prices-scraper").call(run_input={
    "locationQueries": ["Lisbon"],
    "checkIn": "30 days", "nights": 2, "adults": 2, "currency": "EUR",
    "sortBy": "price_low", "maxHotelsPerQuery": 50, "freeCancellationOnly": True,
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "hotel"]
for r in rows[:5]:
    print(r["rank"], r["hotel_name"], r["price_nightly"], r["currency"], r["cancellation"])
