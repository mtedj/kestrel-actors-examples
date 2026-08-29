from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/booking-reviews-scraper").call(run_input={
    "startUrls": ["https://www.booking.com/hotel/pt/memmo-alfama.html"],
    "maxReviewsPerHotel": 100,
    "reviewsSort": "most_recent",
})
reviews = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "review"]
for r in reviews[:5]:
    print(r["rating"], r["traveler_type"], r["title"], "|", r["negatives"])
