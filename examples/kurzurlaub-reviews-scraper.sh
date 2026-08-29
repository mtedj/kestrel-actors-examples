curl -X POST "https://api.apify.com/v2/acts/kestrel~kurzurlaub-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["15699"], "maxReviewsPerHotel": 50}'
