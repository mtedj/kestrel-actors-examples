curl -X POST "https://api.apify.com/v2/acts/kestrel~tripadvisor-restaurant-reviews/run-sync-get-dataset-items?token=$APIFY_TOKEN&format=csv" \
  -H 'Content-Type: application/json' \
  -d '{"locationIds":["2703366"],"maxReviewsPerLocation":50,"languages":["en"]}' \
  -o restaurant-reviews.csv
