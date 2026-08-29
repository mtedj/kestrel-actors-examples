from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-product-scraper").call(run_input={
    "asins": ["B0CHWRXH8B", "B09B8V1LZ3"],
    "domain": "com",
    "inStockOnly": True,
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "product"]
for r in rows:
    print(r["asin"], r["price_display"], r["availability"], r["rating"], r["ratings_count"])
