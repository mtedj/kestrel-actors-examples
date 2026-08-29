curl -X POST "https://api.apify.com/v2/acts/kestrel~agoda-prices-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{"locationQueries": ["Bangkok"], "checkIn": "45 days", "nights": 1, "adults": 2, "currency": "THB", "maxHotelsPerQuery": 45, "minReviewScore": 8}'
