from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/zoover-reviews-scraper").call(run_input={
    "startUrls": ["https://www.zoover.nl/a/91488/esperos-blue-village-spa"],
    "maxReviewsPerAccommodation": 0,
    "maxRating": 6,
})

for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["score"], row["review_date"], row["title"])
