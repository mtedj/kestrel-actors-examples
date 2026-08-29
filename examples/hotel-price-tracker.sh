curl -X POST "https://api.apify.com/v2/acts/kestrel~hotel-price-tracker/run-sync-get-dataset-items?token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotels": ["ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE"], "checkIn": "30 days", "days": 7, "nights": 1, "currency": "USD"}'
