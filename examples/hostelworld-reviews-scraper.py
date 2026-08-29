from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/hostelworld-reviews-scraper").call(run_input={
    "propertyIds": ["15529"],
    "maxReviewsPerProperty": 200,
    "reviewsSort": "-date",
})
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
reviews = [r for r in rows if r["type"] == "review"]
print(len(reviews), "reviews", sum(r["rating"] for r in reviews) / len(reviews))
