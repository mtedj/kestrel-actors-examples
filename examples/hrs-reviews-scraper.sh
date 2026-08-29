curl -X POST "https://api.apify.com/v2/acts/kestrel~hrs-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["10520"], "maxReviewsPerHotel": 30, "reviewsSort": "most_recent", "proxyConfiguration": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}}'
