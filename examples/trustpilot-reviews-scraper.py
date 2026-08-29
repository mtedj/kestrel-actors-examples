from apify_client import ApifyClient

client = ApifyClient("<YOUR_API_TOKEN>")
run = client.actor("kestrel/trustpilot-reviews-scraper").call(run_input={
    "companyDomains": ["www.booking.com"],
    "maxReviewsPerCompany": 200,
    "sort": "most_recent",
    "languages": "all",
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["review_date"], row["title"])
