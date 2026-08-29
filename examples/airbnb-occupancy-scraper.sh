curl -X POST "https://api.apify.com/v2/acts/kestrel~airbnb-occupancy-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"listingIds":["17088279"],"months":2,"currency":"USD"}'
