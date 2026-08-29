curl -X POST "https://api.apify.com/v2/acts/kestrel~aliexpress-reviews-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"productUrls":["https://www.aliexpress.com/item/1005006255429323.html"],"maxReviewsPerProduct":100}'
