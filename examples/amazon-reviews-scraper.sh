curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"asins":["B0BSHF7WHW"],"minRating":2}'
