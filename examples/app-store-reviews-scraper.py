from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/app-store-reviews-scraper").call(run_input={
    "appIds": ["310633997"], "countries": ["us", "gb", "de"],
    "sort": "most_recent", "maxReviewsPerApp": 100,
})
rows = client.dataset(run["defaultDatasetId"]).list_items().items
reviews = [r for r in rows if r["type"] == "review"]
for r in reviews[:5]:
    print(r["country"], r["rating"], r["title"], "—", (r["text"] or "")[:80])
