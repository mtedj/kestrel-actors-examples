from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/indeed-company-reviews").call(run_input={
    "companies": ["Google", "Starbucks"],
    "countries": ["us"],
    "maxReviewsPerCompany": 500,
    "sort": "rating_asc",
    "maxRating": 2,
    "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["job_title"], "|", row["title"])
