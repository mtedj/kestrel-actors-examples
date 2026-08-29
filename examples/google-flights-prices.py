from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/google-flights-prices").call(run_input={
    "routes": ["LIS-LHR"], "departDate": "30 days", "sweepDays": 6, "currency": "EUR",
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "flight":
        print(row["depart_date"], row["price"], row["airline"], row["stops"])
