curl -X POST "https://api.apify.com/v2/acts/kestrel~indeed-company-reviews/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&format=csv" \
  -H 'Content-Type: application/json' \
  -d '{"companies":["Google"],"countries":["us"],"maxReviewsPerCompany":100}' \
  -o indeed-reviews.csv
