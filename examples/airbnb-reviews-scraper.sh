curl -X POST "https://api.apify.com/v2/acts/kestrel~airbnb-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"listingIds":["11562247"],"maxReviewsPerListing":50}'
