from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/aliexpress-reviews-scraper").call(run_input={
    "productUrls": ["https://www.aliexpress.com/item/1005006255429323.html"],
    "maxReviewsPerProduct": 500,
    "reviewsFilter": "with_photos",
    "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["buyer_country"], row["sku_info"], row["text"])
