curl -X POST "https://api.apify.com/v2/acts/kestrel~google-play-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"appIds": ["com.whatsapp"], "languages": ["en"], "countries": ["us"], "maxReviewsPerApp": 50}'
