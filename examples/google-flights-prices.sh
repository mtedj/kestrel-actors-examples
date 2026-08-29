curl -X POST "https://api.apify.com/v2/acts/kestrel~google-flights-prices/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"routes":["LIS-LHR"],"departDate":"30 days","maxResultsPerSearch":10}'
