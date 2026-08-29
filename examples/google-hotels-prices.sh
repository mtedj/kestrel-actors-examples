curl -X POST "https://api.apify.com/v2/acts/kestrel~google-hotels-prices/run-sync-get-dataset-items?token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["hotels in Lisbon"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "maxHotels": 20, "includeOffers": false}'
