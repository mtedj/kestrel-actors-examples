curl -X POST "https://api.apify.com/v2/acts/kestrel~trip-com-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["2561632"], "maxReviewsPerHotel": 50, "reviewsSort": "most_recent"}'
