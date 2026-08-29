# kestrel actors — examples

**Runnable examples for 30 Apify scrapers: hotel and flight prices, guest reviews from every major OTA, Amazon and eBay listings, and app-store reviews.**

Copy-paste calls in **Python, JavaScript and curl** · **verified n8n workflows** · an **agent skill file** for Claude Code and Cursor · **[full documentation](https://mtedj.github.io/kestrel-actors-examples/)** with every input, every output field, a sample row and each actor's honest limits, plus a [comparison of every review scraper](https://mtedj.github.io/kestrel-actors-examples/comparison.html).

Every actor is **pay per delivered row** — filtered rows, empty runs and anything a spending limit refused are free — and takes relative dates (`"30 days"`) so a schedule never goes stale. Run one with the [kestrel](https://apify.com/kestrel) actors on Apify, or read the code to see exactly what each call returns before you spend anything.

### Hotel & flight prices

| actor | what it returns | price per row | docs |
|---|---|---|---|
| [google-hotels-prices](https://apify.com/kestrel/google-hotels-prices) | Price Tracking & Rate Parity | hotel $0.004, offer $0.002 | [docs](https://mtedj.github.io/kestrel-actors-examples/google-hotels.html) |
| [hotel-rate-parity](https://apify.com/kestrel/hotel-rate-parity) | OTA Price Comparison | parity $0.01 | [docs](https://mtedj.github.io/kestrel-actors-examples/hotel-rate-parity.html) |
| [hotel-price-tracker](https://apify.com/kestrel/hotel-price-tracker) | Google Hotels Price History & Alerts | rate $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/hotel-price-tracker.html) |
| [booking-prices-scraper](https://apify.com/kestrel/booking-prices-scraper) | Hotel Prices & Availability by Date | hotel $0.004, room $0.002 | [docs](https://mtedj.github.io/kestrel-actors-examples/booking-prices.html) |
| [agoda-prices-scraper](https://apify.com/kestrel/agoda-prices-scraper) | Hotel Rates & Availability by Date | hotel $0.004, calendar_day $0.002 | [docs](https://mtedj.github.io/kestrel-actors-examples/agoda-prices.html) |
| [airbnb-prices-calendar](https://apify.com/kestrel/airbnb-prices-calendar) | Prices, Availability Calendar & Occupancy | listing $0.005, calendar_month $0.002, review $0.003 | [docs](https://mtedj.github.io/kestrel-actors-examples/airbnb-prices-calendar.html) |
| [airbnb-occupancy-scraper](https://apify.com/kestrel/airbnb-occupancy-scraper) | Calendar Availability & ADR | occupancy $0.002 | [docs](https://mtedj.github.io/kestrel-actors-examples/airbnb-occupancy.html) |
| [google-flights-prices](https://apify.com/kestrel/google-flights-prices) | Airfare Prices & Price Tracking | flight $0.005 | [docs](https://mtedj.github.io/kestrel-actors-examples/google-flights.html) |
| [flight-price-tracker](https://apify.com/kestrel/flight-price-tracker) | Cheapest Day to Fly & Airfare Alerts | fare $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/flight-price-tracker.html) |
### Guest & customer reviews

| actor | what it returns | price per row | docs |
|---|---|---|---|
| [tripadvisor-reviews-scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.005 | [docs](https://mtedj.github.io/kestrel-actors-examples/tripadvisor-reviews.html) |
| [tripadvisor-restaurant-reviews](https://apify.com/kestrel/tripadvisor-restaurant-reviews) | Diner Reviews | review $0.005 | [docs](https://mtedj.github.io/kestrel-actors-examples/tripadvisor-restaurant-reviews.html) |
| [booking-reviews-scraper](https://apify.com/kestrel/booking-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.005 | [docs](https://mtedj.github.io/kestrel-actors-examples/booking-reviews.html) |
| [agoda-reviews-scraper](https://apify.com/kestrel/agoda-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.005 | [docs](https://mtedj.github.io/kestrel-actors-examples/agoda-reviews.html) |
| [airbnb-reviews-scraper](https://apify.com/kestrel/airbnb-reviews-scraper) | Guest Reviews, Ratings & Replies | review $0.005 | [docs](https://mtedj.github.io/kestrel-actors-examples/airbnb-reviews.html) |
| [hrs-reviews-scraper](https://apify.com/kestrel/hrs-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.003 | [docs](https://mtedj.github.io/kestrel-actors-examples/hrs-reviews.html) |
| [trip-com-reviews-scraper](https://apify.com/kestrel/trip-com-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/tripcom-reviews.html) |
| [kurzurlaub-reviews-scraper](https://apify.com/kestrel/kurzurlaub-reviews-scraper) | Hotel- & Gästebewertungen | review $0.003 | [docs](https://mtedj.github.io/kestrel-actors-examples/kurzurlaub-reviews.html) |
| [hostelworld-reviews-scraper](https://apify.com/kestrel/hostelworld-reviews-scraper) | Hostel Guest Reviews | review $0.003 | [docs](https://mtedj.github.io/kestrel-actors-examples/hostelworld-reviews.html) |
| [zoover-reviews-scraper](https://apify.com/kestrel/zoover-reviews-scraper) | Hotel Guest Reviews & Ratings | review $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/zoover-reviews.html) |
| [despegar-hotel-ratings](https://apify.com/kestrel/despegar-hotel-ratings) | Guest Scores & Summary | hotel $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/despegar-ratings.html) |
| [trustpilot-reviews-scraper](https://apify.com/kestrel/trustpilot-reviews-scraper) | Company Reviews & TrustScore | review $0.0007 | [docs](https://mtedj.github.io/kestrel-actors-examples/trustpilot-reviews.html) |
| [indeed-company-reviews](https://apify.com/kestrel/indeed-company-reviews) | Employee Reviews | review $0.002 | [docs](https://mtedj.github.io/kestrel-actors-examples/indeed-reviews.html) |
### Ecommerce

| actor | what it returns | price per row | docs |
|---|---|---|---|
| [amazon-product-scraper](https://apify.com/kestrel/amazon-product-scraper) | Details, Prices & Availability by ASIN | product $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/amazon-product.html) |
| [amazon-search-scraper](https://apify.com/kestrel/amazon-search-scraper) | Best Sellers, Ranks & Prices | product $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/amazon-search.html) |
| [amazon-best-sellers-scraper](https://apify.com/kestrel/amazon-best-sellers-scraper) | Top 100 by Category & BSR | product $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/amazon-best-sellers.html) |
| [amazon-reviews-scraper](https://apify.com/kestrel/amazon-reviews-scraper) | Customer Reviews & Ratings | review $0.005, product $0.003 | [docs](https://mtedj.github.io/kestrel-actors-examples/amazon-reviews.html) |
| [aliexpress-reviews-scraper](https://apify.com/kestrel/aliexpress-reviews-scraper) | Product Feedback & Ratings | review $0.002 | [docs](https://mtedj.github.io/kestrel-actors-examples/aliexpress-reviews.html) |
| [ebay-search-scraper](https://apify.com/kestrel/ebay-search-scraper) | Search, Listings, Prices & Sellers | item $0.003 | [docs](https://mtedj.github.io/kestrel-actors-examples/ebay-search.html) |
### Apps

| actor | what it returns | price per row | docs |
|---|---|---|---|
| [app-store-reviews-scraper](https://apify.com/kestrel/app-store-reviews-scraper) | App Reviews & Ratings | review $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/app-store-reviews.html) |
| [google-play-reviews-scraper](https://apify.com/kestrel/google-play-reviews-scraper) | Android App Reviews & Ratings | review $0.004 | [docs](https://mtedj.github.io/kestrel-actors-examples/google-play-reviews.html) |

## Quickstart

```bash
pip install apify-client        # or: npm i apify-client
export APIFY_TOKEN=...          # console.apify.com/account/integrations
python examples/google-hotels-prices.py
```

`examples/<actor>.py|.js|.sh` is the same call in Python, JavaScript and curl, lifted from each actor's README (which documents every input and output field). `n8n/` holds importable n8n workflows verified end to end — review alerts, cheapest day to fly, Best Sellers rank history, hotel price drops. `skills/` is an agent skill file: drop it into a Claude Code or Cursor project and the agent knows how to call the actor.

## Rate limits, proxies, legality

The actors run on Apify Proxy with paced rotating sessions, so you never see a captcha. They read public pages only, store nothing personal beyond what the page itself shows, and each README carries a legality section — read it before scraping at scale.

**Which sites are readable at all?** The measurements behind these actors are published separately in [scraping-reachability-2026](https://github.com/mtedj/scraping-reachability-2026): which review and travel sites answer an ordinary HTTP client, which need a particular TLS fingerprint, which need a browser, and which are closed — with the request, the block signature and the date for each.
