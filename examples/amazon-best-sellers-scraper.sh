curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-best-sellers-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"categories":["electronics"],"pages":1,"maxResultsPerCategory":20}'
