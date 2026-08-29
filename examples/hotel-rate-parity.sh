curl -X POST "https://api.apify.com/v2/acts/kestrel~hotel-rate-parity/run-sync-get-dataset-items?token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotels": ["ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE"], "checkIn": "30 days", "nights": 1, "currency": "USD"}'
