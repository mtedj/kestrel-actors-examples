curl -X POST "https://api.apify.com/v2/acts/kestrel~trustpilot-reviews-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"companyDomains":["www.booking.com"],"maxReviewsPerCompany":40,"sort":"most_recent"}'
