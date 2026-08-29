A flight price tracker that finds the cheapest day to fly: every morning it prices a route on Google Flights for each of the next 14 departure days, picks the cheapest day, compares it with yesterday and sends a Telegram digest with the three cheapest dates and a link to the results. It calls the [Flight Price Tracker](https://apify.com/kestrel/flight-price-tracker) Apify actor through a core HTTP Request node — n8n Cloud or self-hosted.

## Who is this for

Travellers with flexible dates, deal newsletters and travel bloggers.

## How it works

1. **Run daily at 07:00** — Schedule trigger.
2. **Run Google Flights** — HTTP POST to the actor's run-sync endpoint: `routes`, relative `departDate` ("30 days"), `days: 14`. One `fare` row per day = that day's cheapest itinerary.
3. **Find the cheapest day** — Code node takes the lowest `fare` per route, compares it with the previous run (workflow static data) and builds `message` and `top3` (the three cheapest days).
4. **Drop ≥ threshold?** — IF; threshold 0 = send daily, 5 = only drops ≥ 5 %.
5. **Send Telegram** — the digest.
6. **Skip today** — NoOp.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in *Run Google Flights*.
2. Edit `routes` (`"LIS-LHR"`), `departDate` and `days` in *Run Google Flights*.
3. Connect `Telegram Bot` in *Send Telegram* and set your chat id.

## How to customize

- Hard alert: `maxPrice: 300` delivers only days at or under $300; days over the line are dropped before billing, so a quiet day costs and sends nothing.
- Round trips: `tripLengthDays: 7` prices every day as a 7-night trip (price = both legs).
- Several routes (one message each); `maxStops: "nonstop"`, `seat: "business"`, `currency: "EUR"`, `market: "de"`.
- Swap Telegram for Email, Slack or Discord — `message` is ready to send.

## Cost

$0.004 per fare row, one per day; status rows are free. 14 days = 14 × $0.004 = $0.056 per route per day, about $1.70 a month; the verification run delivered exactly 14 rows = $0.056.
