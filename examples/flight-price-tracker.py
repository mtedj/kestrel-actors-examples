from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/flight-price-tracker").call(run_input={
    "routes": ["LIS-LHR"], "departDate": "30 days", "days": 14, "currency": "EUR",
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "fare":
        print(row["rank_in_window"], row["depart_date"], row["price"], row["airline"], row["stops"])
