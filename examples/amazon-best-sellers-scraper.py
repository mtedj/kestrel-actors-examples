from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-best-sellers-scraper").call(run_input={
    "categories": ["electronics"], "chart": "bestsellers", "pages": 2,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "product":
        print(row["rank"], row["asin"], row["price"], row["rating"], row["title"])
