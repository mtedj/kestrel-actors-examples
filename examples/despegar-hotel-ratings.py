from apify_client import ApifyClient
client = ApifyClient("<APIFY_TOKEN>")
run = client.actor("kestrel/despegar-hotel-ratings").call(run_input={
    "hotelIds": ["265543", "4382832"], "country": "ar", "minRating": 8})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "hotel":
        print(row["hotel_name"], row["rating"], row["review_count"], row["score_value"])
