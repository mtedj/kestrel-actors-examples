curl -X POST "https://api.apify.com/v2/acts/kestrel~flight-price-tracker/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"routes":["LIS-LHR"],"departDate":"30 days","days":7,"maxPrice":150,"currency":"EUR"}'
