curl -X POST "https://api.apify.com/v2/acts/kestrel~tripadvisor-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon.html"], "maxReviewsPerHotel": 50}'
