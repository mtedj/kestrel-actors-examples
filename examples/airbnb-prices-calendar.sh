curl -X POST "https://api.apify.com/v2/acts/kestrel~airbnb-prices-calendar/run-sync-get-dataset-items?token=<TOKEN>" -H "Content-Type: application/json" \
  -d '{"locationQueries": ["Lisbon, Portugal"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "maxListingsPerQuery": 20}'
