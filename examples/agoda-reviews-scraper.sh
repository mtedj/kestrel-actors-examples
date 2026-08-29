curl -X POST "https://api.apify.com/v2/acts/kestrel~agoda-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"hotelIds":["63820"],"maxReviewsPerHotel":100}'
