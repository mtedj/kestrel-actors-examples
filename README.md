# kestrel actors — examples

Runnable examples for the ten [kestrel](https://apify.com/kestrel) Apify actors: Google Hotels, hotel rate parity, Airbnb prices and reviews, Agoda reviews, Google Flights, a flight price tracker, and Amazon search, Best Sellers and reviews. Every actor is pay-per-event on delivered rows only — filtered rows, empty runs and spending-limit refusals are free — and accepts relative dates (`"30 days"`) so schedules never go stale.

| actor | what it returns | price per row |
|---|---|---|
| [agoda-reviews-scraper](https://apify.com/kestrel/agoda-reviews-scraper) | Agoda Reviews Scraper — Hotel Guest Reviews & Ratings | review $0.005 |
| [airbnb-prices-calendar](https://apify.com/kestrel/airbnb-prices-calendar) | Airbnb Scraper — Prices, Availability Calendar & Occupancy | listing $0.005, calendar_month $0.002, review $0.003 |
| [airbnb-reviews-scraper](https://apify.com/kestrel/airbnb-reviews-scraper) | Airbnb Reviews Scraper — Guest Reviews, Ratings & Replies | review $0.005 |
| [amazon-best-sellers-scraper](https://apify.com/kestrel/amazon-best-sellers-scraper) | Amazon Best Sellers Scraper — Top 100 by Category & BSR | product $0.004 |
| [amazon-reviews-scraper](https://apify.com/kestrel/amazon-reviews-scraper) | Amazon Reviews Scraper — Customer Reviews & Ratings | review $0.005, product $0.003 |
| [amazon-search-scraper](https://apify.com/kestrel/amazon-search-scraper) | Amazon Search Scraper — Best Sellers, Ranks & Prices | product $0.004 |
| [flight-price-tracker](https://apify.com/kestrel/flight-price-tracker) | Flight Price Tracker — Cheapest Day to Fly & Airfare Alerts | fare $0.004 |
| [google-flights-prices](https://apify.com/kestrel/google-flights-prices) | Google Flights Scraper — Airfare Prices & Price Tracking | flight $0.005 |
| [google-hotels-prices](https://apify.com/kestrel/google-hotels-prices) | Google Hotels Prices Scraper — Price Tracking & Rate Parity | hotel $0.004, offer $0.002 |
| [hotel-rate-parity](https://apify.com/kestrel/hotel-rate-parity) | Hotel Rate Parity Checker — OTA Price Comparison | parity $0.01 |

## Quickstart

```bash
pip install apify-client        # or: npm i apify-client
export APIFY_TOKEN=...          # console.apify.com/account/integrations
python examples/google-hotels-prices.py
```

Each `examples/<actor>.py|.js|.sh` is the same call in Python, JavaScript and curl, lifted from the actor's README (which documents every input and output field). `n8n/` holds importable n8n workflows (verified end to end) for review alerts, the cheapest day to fly, Best Sellers rank history and hotel price drops. `skills/` is an agent skill file: drop it into a Claude Code / Cursor project and the agent knows how to call the actor.

## Rate limits, proxies, legality

The actors run on Apify Proxy with paced rotating sessions; you never see a captcha. They read public pages only, store nothing personal beyond what the page shows, and each README carries a legality section — read it before scraping at scale.
