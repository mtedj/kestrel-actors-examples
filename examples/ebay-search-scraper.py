from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/ebay-search-scraper").call(run_input={
    "queries": ["mechanical keyboard"],
    "pages": 2,
    "minPrice": 30,
    "maxPrice": 200,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "item":
        print(row["price"], row["currency"], row["units_sold"], row["title"])
