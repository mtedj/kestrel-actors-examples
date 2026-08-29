from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/airbnb-reviews-scraper").call(run_input={
    "listingIds": ["11562247"], "maxReviewsPerListing": 0, "reviewsSort": "lowest_rated", "minRating": 3,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["language"], row["text"][:80])
