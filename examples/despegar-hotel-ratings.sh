curl -X POST "https://api.apify.com/v2/acts/kestrel~despegar-hotel-ratings/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"hotelIds":["265543"],"country":"us","includeComments":true}'
