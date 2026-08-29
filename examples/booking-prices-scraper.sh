curl -X POST "https://api.apify.com/v2/acts/kestrel~booking-prices-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"locationQueries": ["Algarve"], "maxHotelsPerQuery": 30, "checkIn": "6 weeks", "nights": 3, "adults": 2, "currency": "GBP", "sortBy": "review_score", "minStars": 4}'
