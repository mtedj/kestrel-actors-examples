curl -X POST "https://api.apify.com/v2/acts/kestrel~app-store-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{"appIds":["310633997"],"countries":["us"],"sinceDate":"7 days","sort":"most_recent","maxReviewsPerApp":200}'
