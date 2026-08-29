curl -X POST "https://api.apify.com/v2/acts/kestrel~zoover-reviews-scraper/runs?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"startUrls":["https://www.zoover.nl/a/91488/esperos-blue-village-spa"],"maxReviewsPerAccommodation":0}'

curl "https://api.apify.com/v2/acts/kestrel~zoover-reviews-scraper/runs/last/dataset/items?token=$APIFY_TOKEN&format=csv&clean=1" > zoover-reviews.csv
