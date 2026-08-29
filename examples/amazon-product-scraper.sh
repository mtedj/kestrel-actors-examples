curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-product-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"asins": ["B0CHWRXH8B"], "domain": "com"}'
