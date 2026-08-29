curl -X POST "https://api.apify.com/v2/acts/kestrel~hostelworld-reviews-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"propertyIds":["15529"],"maxReviewsPerProperty":50,"reviewsSort":"-date"}'
