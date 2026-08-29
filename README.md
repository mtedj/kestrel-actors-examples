# kestrel actors — examples

Runnable examples for the [kestrel](https://apify.com/kestrel) Apify actors: hotel and flight prices, guest reviews from every major OTA, Amazon product data, app-store reviews and YouTube transcripts. Every actor is **pay per delivered row** — filtered rows, empty runs and anything a spending limit refused are free — and takes relative dates (`"30 days"`) so a schedule never goes stale.

### Hotels & travel

| actor | what it returns | price per row |
|---|---|---|
| [google-hotels-prices](https://apify.com/kestrel/google-hotels-prices) | Price Tracking & Rate Parity | hotel $0.004, offer $0.002 |
| [hotel-rate-parity](https://apify.com/kestrel/hotel-rate-parity) | OTA Price Comparison | parity $0.01 |
| [hotel-price-tracker](https://apify.com/kestrel/hotel-price-tracker) | Google Hotels Price History & Alerts | rate $0.004 |
| [booking-prices-scraper](https://apify.com/kestrel/booking-prices-scraper) | Hotel Prices & Availability by Date | hotel $0.004, room $0.002 |
| [agoda-prices-scraper](https://apify.com/kestrel/agoda-prices-scraper) | Hotel Rates & Availability by Date | hotel $0.004, calendar_day $0.002 |
| [airbnb-prices-calendar](https://apify.com/kestrel/airbnb-prices-calendar) | Prices, Availability Calendar & Occupancy | listing $0.005, calendar_month $0.002, review $0.003 |
| [airbnb-occupancy-scraper](https://apify.com/kestrel/airbnb-occupancy-scraper) | Calendar Availability & ADR | occupancy $0.002 |
| [google-flights-prices](https://apify.com/kestrel/google-flights-prices) | Airfare Prices & Price Tracking | flight $0.005 |
| [flight-price-tracker](https://apify.com/kestrel/flight-price-tracker) | Cheapest Day to Fly & Airfare Alerts | fare $0.004 |
### Guest & customer reviews

| actor | what it returns | price per row |
|---|---|---|
| [tripadvisor-reviews-scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.005 |
| [booking-reviews-scraper](https://apify.com/kestrel/booking-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.005 |
| [agoda-reviews-scraper](https://apify.com/kestrel/agoda-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.005 |
| [hrs-reviews-scraper](https://apify.com/kestrel/hrs-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.003 |
| [trip-com-reviews-scraper](https://apify.com/kestrel/trip-com-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.004 |
| [kurzurlaub-reviews-scraper](https://apify.com/kestrel/kurzurlaub-reviews-scraper) | Hotel- & Gästebewertungen | review $0.003 |
| [airbnb-reviews-scraper](https://apify.com/kestrel/airbnb-reviews-scraper) | Guest Reviews, Ratings & Replies | review $0.005 |
| [trustpilot-reviews-scraper](https://apify.com/kestrel/trustpilot-reviews-scraper) | Company Reviews & TrustScore | review $0.0007 |
### Ecommerce

| actor | what it returns | price per row |
|---|---|---|
| [amazon-product-scraper](https://apify.com/kestrel/amazon-product-scraper) | Details, Prices & Availability by ASIN | product $0.004 |
| [amazon-search-scraper](https://apify.com/kestrel/amazon-search-scraper) | Best Sellers, Ranks & Prices | product $0.004 |
| [amazon-best-sellers-scraper](https://apify.com/kestrel/amazon-best-sellers-scraper) | Top 100 by Category & BSR | product $0.004 |
| [amazon-reviews-scraper](https://apify.com/kestrel/amazon-reviews-scraper) | Customer Reviews & Ratings | review $0.005, product $0.003 |
### Apps & video

| actor | what it returns | price per row |
|---|---|---|
| [app-store-reviews-scraper](https://apify.com/kestrel/app-store-reviews-scraper) | App Reviews & Ratings | review $0.004 |
| [google-play-reviews-scraper](https://apify.com/kestrel/google-play-reviews-scraper) | Android App Reviews & Ratings | review $0.004 |
### Other

| actor | what it returns | price per row |
|---|---|---|
| [hostelworld-reviews-scraper](https://apify.com/kestrel/hostelworld-reviews-scraper) | Hostel Guest Reviews | review $0.003 |
| [zoover-reviews-scraper](https://apify.com/kestrel/zoover-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.004 |

## Quickstart

```bash
pip install apify-client        # or: npm i apify-client
export APIFY_TOKEN=...          # console.apify.com/account/integrations
python examples/google-hotels-prices.py
```

`examples/<actor>.py|.js|.sh` is the same call in Python, JavaScript and curl, lifted from each actor's README (which documents every input and output field). `n8n/` holds importable n8n workflows verified end to end — review alerts, cheapest day to fly, Best Sellers rank history, hotel price drops. `skills/` is an agent skill file: drop it into a Claude Code or Cursor project and the agent knows how to call the actor.

## Rate limits, proxies, legality

The actors run on Apify Proxy with paced rotating sessions, so you never see a captcha. They read public pages only, store nothing personal beyond what the page itself shows, and each README carries a legality section — read it before scraping at scale.
