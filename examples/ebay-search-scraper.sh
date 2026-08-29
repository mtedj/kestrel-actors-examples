curl -X POST "https://api.apify.com/v2/acts/kestrel~ebay-search-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'content-type: application/json' \
  -d '{"queries":["vintage pocket watch"],"buyingFormat":"auction","pages":1}'
