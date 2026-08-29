from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/agoda-reviews-scraper").call(run_input={
    "hotelNames": ["Park Hyatt Tokyo"], "maxReviewsPerHotel": 0,
    "reviewsSort": "lowest_rated", "maxRating": 5, "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["reviewer_country"], row["text"][:80])
