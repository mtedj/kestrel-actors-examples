from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/tripadvisor-reviews-scraper").call(run_input={
    "locationIds": ["4509998"],
    "languages": ["en", "fr"],
    "maxRating": 3,
    "requireText": True,
    "maxReviewsPerHotel": 500,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["language"], row["rating"], row["review_date"], row["title"], "-", (row["response"] or "")[:40])
