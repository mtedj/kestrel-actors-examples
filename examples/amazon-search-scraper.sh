curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-search-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"queries":["wireless earbuds"],"pages":1,"skipSponsored":true}'
