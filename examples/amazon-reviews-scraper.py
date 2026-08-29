from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-reviews-scraper").call(run_input={
    "asins": ["B0BSHF7WHW"], "minRating": 2, "verifiedOnly": True, "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["country"], row["text"][:80])
