from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/trip-com-reviews-scraper").call(run_input={
    "hotelIds": ["2561632"],
    "maxReviewsPerHotel": 0,
    "reviewsSort": "lowest_rated",
    "maxRating": 6,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["language"], row["travel_type"], row["text"][:80])
