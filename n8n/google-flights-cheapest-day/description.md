A flight price tracker that finds the cheapest day to fly: every morning it prices a route on Google Flights for each of the next 14 departure days, picks the cheapest day, compares it with yesterday and sends a Telegram digest with the three cheapest dates and a link to the results — a flight price alert without refreshing Google Flights. It calls the [Google Flights Scraper](https://apify.com/kestrel/google-flights-prices) Apify actor through a core HTTP Request node — n8n Cloud or self-hosted.

## Who is this for

Travellers with flexible dates, deal newsletters and travel bloggers.

## How it works

1. **Run daily at 07:00** — Schedule trigger.
2. **Run Google Flights** — HTTP POST to the actor's run-sync endpoint: `routes`, relative `departDate` ("30 days"), `sweepDays: 13` → 14 dates, up to 3 itineraries each.
3. **Find the cheapest day** — Code node reads the free `status` rows (one per date, carrying `cheapest`), takes the minimum per route, attaches the matching `flight` row, compares with the previous run (workflow static data) and builds `message` and `top3`.
4. **Drop ≥ threshold?** — IF; threshold 0 = send daily, 5 = only drops ≥ 5 %.
5. **Send Telegram** — the digest.
6. **Skip today** — NoOp.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in *Run Google Flights*.
2. Edit `routes` (`"LIS-LHR"`) and `departDate`; add `returnDate: "37 days"` for round trips (the return shifts with each swept day).
3. Connect `Telegram Bot` in *Send Telegram* and set your chat id.

## How to customize

- Several routes: `routes: ["LIS-LHR", "LIS-CDG"]` — one message per route.
- `maxStops: "nonstop"`, `seat: "business"`, `currency: "EUR"`, `market: "de"`.
- Swap Telegram for Email, Slack or Discord — `message` is ready to send.

## Cost

$0.005 per itinerary row; status rows are free. 14 dates × up to 3 itineraries = at most 42 rows = $0.21 per route per day; the verification run delivered exactly 42 rows = $0.21. `maxResultsPerSearch: 1` cuts it to $0.07 but may miss the cheapest fare.
