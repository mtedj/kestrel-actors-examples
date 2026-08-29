from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-search-scraper").call(run_input={
    "queries": ["wireless earbuds"], "pages": 2, "skipSponsored": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "product":
        print(row["position"], row["asin"], row["price"], row["rating"])
