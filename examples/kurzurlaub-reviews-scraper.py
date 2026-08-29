from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/kurzurlaub-reviews-scraper").call(run_input={
    "hotelIds": ["15699"],
    "maxReviewsPerHotel": 0,
    "maxScore": 4,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["score"], row["review_date"], row["title"], row["category_scores"])
