from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/google-play-reviews-scraper").call(run_input={
    "appIds": ["com.whatsapp"],
    "languages": ["en", "de"],
    "countries": ["us", "de"],
    "sort": "most_recent",
    "maxRating": 2,
    "requireText": True,
    "maxReviewsPerApp": 200,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["language"], row["country"], row["rating"], row["review_day"], (row["text"] or "")[:80])
