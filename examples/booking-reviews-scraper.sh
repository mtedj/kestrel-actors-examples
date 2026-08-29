curl -X POST "https://api.apify.com/v2/acts/kestrel~booking-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["536251"], "maxReviewsPerHotel": 25, "languages": ["en"]}'
