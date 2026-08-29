from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/tripadvisor-restaurant-reviews").call(run_input={
    "locationIds": ["2703366"],
    "locationType": "restaurant",
    "languages": ["en"],
    "maxReviewsPerLocation": 200,
    "maxRating": 3,
    "requireText": True,
})

for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] != "review":
        continue
    subs = row["sub_ratings"] or {}
    print(row["rating"], subs.get("food"), subs.get("service"), row["review_date"], row["title"])
