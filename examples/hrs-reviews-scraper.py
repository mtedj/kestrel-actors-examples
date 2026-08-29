from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/hrs-reviews-scraper").call(run_input={
    "hotelIds": ["10520", "162"],
    "reviewsSort": "lowest_rated",
    "maxRating": 7,
    "maxReviewsPerHotel": 50,
    "proxyConfiguration": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["hotel_name"], row["rating"], row["traveller_type"], (row["negatives"] or "")[:80])
