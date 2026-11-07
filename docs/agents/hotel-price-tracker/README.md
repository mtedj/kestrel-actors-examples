# Hotel Price Tracker — Google Hotels Price History & Alerts

Hotel price tracker built on Google Hotels prices: for every property and check-in date in a window you choose, one row with the lowest rate across every booking site Google lists — Booking.com, Expedia, Agoda, Trip.com, the property's own site — the source that has it, its booking link, the official-site rate next to it, and the date's rank within the window. Put it on a daily schedule with relative dates and it becomes hotel price tracking with a history you own; set `maxPrice` and it becomes a hotel price alert that only delivers (and only bills) the dates under your target. It is the Google Hotels price tracker Google's own "track prices" button does not give you: your threshold, every source, every date, as rows. No API key, no login, no browser.

**You pay only for delivered rate rows.** Dates over `maxPrice`, dates with no rate, names that do not resolve, duplicates and status rows cost nothing.

Last verified working: 2026-08-29.

## 酒店价格监控、价格追踪与降价筛选：中文调用与语言设置

按日期扫描酒店价格并找出可见的低价日期。连续定时运行并保存结果，才能形成价格历史；maxPrice 是筛选器。

country 是搜索者市场，language 影响可用的名称翻译，currency 控制币种。示例 language="zh-CN"；不会自动发送降价通知。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "hotels": [
    "https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE"
  ],
  "checkIn": "30 days",
  "days": 1,
  "nights": 1,
  "currency": "USD",
  "language": "zh-CN",
  "sessions": 1
}
```

Hotelpreise verfolgen / seguimiento de precios：调度与历史保存由工作流完成。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Hotel price tracker for AI agents: which input answers which request?

Use it when the user names one or more hotels and wants their price over a range of check-in dates, on a schedule, or only when the price falls under a target: "track the Hyatt in Lisbon", "which night next month is cheapest", "tell me when it drops under 180", "a price calendar for these three hotels". Do not use it for a city search ("hotels in Lisbon" — that is the [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)), for every booking site's rate as its own row or the parity math (the [Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)), for reviews, for flights, or for more than 6 adults or one room.

| The user asks for | Input |
|---|---|
| Track a hotel's price for the next week | `{"hotelNames": ["Hyatt Regency Lisbon"], "checkIn": "tomorrow", "days": 7}` |
| Which day next month is cheapest, a price calendar | `{"hotelNames": ["Hyatt Regency Lisbon"], "checkIn": "2026-11-01", "days": 30, "nights": 1}` then the row with `cheapest_in_window: true` |
| Alert me when it drops under 180 a night | add `"maxPrice": 180, "currency": "EUR"` and schedule the run; rows appear only for dates at or under 180 |
| Track prices daily without editing the input | `"checkIn": "30 days"` (relative) and an Apify schedule; every run appends rows with a new `fetched_at` = hotel price history |
| The same hotels every day, no name lookup | pass the `entity_id` values of a first run in `hotels` |
| A 2-night stay for a family | `"nights": 2, "adults": 2, "childrenAges": [5, 9]` |
| Prices as a UK booker sees them, in pounds | `"country": "gb", "currency": "GBP"` |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `days` × hotels bounds the rows ($0.004 each) |

`days` decides the bill: one `rate` row per hotel and check-in date, so 2 hotels × `days: 30` is at most 60 rows ($0.24). Dates with no rate, dates over `maxPrice`, names that match nothing, duplicates and status rows are never billed.

Rows come in two types. `rate`: `hotel_name`, `entity_id`, `check_in`, `check_out`, `nights`, `price` (lowest nightly rate that day across every booking site Google lists), `total`, `source` (who has it), `official` (true when the cheapest source is the hotel's own site), `source_url` (booking link), `official_price` (the hotel's own rate that day, null when Google lists no official site), `free_cancellation`, `n_sources`, `rank_in_window`, `cheapest_in_window`, `currency`, `fetched_at`; `stars`, `rating`, `reviews` are filled for hotels given by name, null for hotels given by URL. `status`: one per hotel with `days`, `rates`, `filtered`, `no_rates`, `errors`, `cheapest`, `cheapest_date` and a `status` of `ok`, `no_rates`, `not_found`, `duplicate`, `unpaid` or `error`, never charged. An empty result is a `status` row that says why (every date over `maxPrice`, a name that matched nothing, a sold-out hotel), not a failed run. The actor returns rows, not history: history is the same input on a schedule, one `fetched_at` per run.

In other languages: Hotelpreise verfolgen, Preisalarm (DE); precios de hoteles, alerta de precio (ES); prix d'hôtel, alerte prix (FR); preços de hotéis (PT).

## What does the hotel price tracker return?

One `rate` row per property and check-in date. Ask for a property and `days: 30` and you get thirty rows — a price calendar for the month, each row the best rate that day:

- `price` — the lowest nightly rate any source shows for that check-in date and length of stay, and `total`, the stay total at that source. `price_display` keeps Google's formatting.
- `source` — who has it (an OTA or the property's official site), `official` (true when the cheapest source is the property itself), and `source_url`, the booking link with your dates filled in.
- `official_price` — the property's own rate that day when Google lists an official site, so a row shows at a glance whether direct or an OTA wins. `free_cancellation` when Google says the cheapest rate is refundable; `n_sources`, how many sources priced the stay.
- `rank_in_window` and `cheapest_in_window` — the dates of each property's window ranked by price (1 = the cheapest date to stay; an earlier date wins a tie).
- Identity and stay: `hotel_name`, `entity_id`, `hotel_url`, `check_in`, `check_out`, `nights`, `adults`, `children`, `currency`, `fetched_at`; for name lookups also `hotel_id`, `stars`, `rating` and `reviews`.

One `status` row per property (never charged) says what happened: `days` searched, `rates` delivered, `filtered` by `maxPrice`, `no_rates`, `errors`, the `cheapest` rate and `cheapest_date` seen even when the filter dropped them, and a `status` of `ok`, `no_rates`, `not_found`, `duplicate`, `unpaid` or `error` with the first `error` message.

## Hotel price tracking on a schedule

Rates for a stay move every day until check-in, and the only way to know whether today is a good day to book is to have seen yesterday. The tracker is built for that loop:

- **Relative dates.** `"checkIn": "30 days"` means "the stay 30 days from whenever this run starts", forever. A schedule set once never goes stale and never needs its dates edited.
- **A window per run.** `days: 14` prices the same length of stay on fourteen consecutive check-in dates — one row each — so a single run covers the whole span you are flexible over.
- **History you own.** Every run appends dated rows to the same dataset. Export to Sheets, BigQuery or a warehouse and `price` by `fetched_at` for one `check_in` is hotel price history for that stay — the curve Google shows for a handful of properties, for any property, in your currency, with the source attached.
- **Alerts on your terms.** `maxPrice: 180` delivers only dates whose lowest nightly rate is at or under 180. A run that returns nothing means nothing is under your target yet — and cost nothing. Wire the dataset to a Slack, email or Telegram step and that is a hotel price drop alert with the booking link in the message.

The same run works the other way round: a revenue manager tracking their own property and a comp set gets one row per property and date with the market's lowest rate and whether it is direct, which is hotel price monitoring without a rate shopper licence. For the full per-source comparison and the parity math, use the [Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity).

## Google Hotels price tracker vs Google's own "track prices"

Google Hotels added price tracking for signed-in users in 2026. It is useful and it is not this:

| | Google's tracker | This actor |
|---|---|---|
| Threshold | Google decides what counts as a drop | `maxPrice` in your currency |
| Dates | one stay | up to 60 consecutive check-in dates per run |
| Sources | the price Google chooses to show | the lowest across every source, with the source named and the official rate alongside |
| History | a chart you can look at | dated rows you can query, join and chart |
| Delivery | email from Google | any channel: Sheets, Slack, Telegram, a webhook, your own code |
| Properties | one at a time | a list, by URL, token or name |

The data is the same public comparison any traveller sees — this actor reads it through Apify's proxies and returns it as JSON instead of a notification.

## Cheapest date to stay: reading the window

`rank_in_window` answers the question most people actually have — *when* is this property cheapest — without a spreadsheet:

- Filter `cheapest_in_window: true` and you have one row per property: its best date in the window, the rate, the source and the link.
- Sort by `rank_in_window` and the shape of the month appears: weekends up, mid-week down, the conference week that spikes everything.
- Combine with `maxPrice` and the ranks are still computed over the whole window before the filter runs, so a delivered row's rank tells you where it sits among the dates you did not see.

The `status` row keeps the cheapest rate and date even when `maxPrice` dropped every row, so an alert run that delivered nothing still tells you how far off the target the market is.

## Input

| Field | Meaning |
|---|---|
| `hotels` | Google Hotels URLs (`…/travel/hotels/entity/ChkI…`) or bare entity tokens. Exact: one offers call per property and date, no search, nothing unrelated billed. |
| `hotelNames` | Property names. One place search each; kept only when the listing's name matches most of your words (at least two). Add the city to a generic name. |
| `checkIn` | The first check-in date of the window: `YYYY-MM-DD`, or relative for schedules: `"30 days"`, `"6 weeks"`, `"+30d"`, `today`, `tomorrow`. Past dates are rejected before anything is fetched. |
| `days` | How many consecutive check-in dates to price, 1–60 (7 = a week, 30 = a month-long price calendar). |
| `nights` | Length of stay for every date, 1–30. Check-out = check-in + nights. |
| `adults`, `childrenAges` | Occupancy per room; rates scale with it exactly as on Google. |
| `currency`, `language`, `country` | One currency for every price; Google UI language (`hl`); market (`gl`) — the booker's country, which decides which booking sites Google lists. Keep one market across a history. |
| `maxPrice` | 0 = every date. N = only dates whose lowest nightly rate is at or under N (the alert). Dropped dates are never billed. |
| `proxyConfiguration` | Apify datacenter proxies work; keep the default. |
| `sessions`, `perIp` | Parallel proxy sessions and requests per second per IP (defaults 4 and 0.5). |

### Example: one property, a month of check-in dates, one night

```json
{
  "hotels": ["https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE"],
  "checkIn": "tomorrow",
  "days": 30,
  "nights": 1,
  "currency": "USD"
}
```

### Example: a price drop alert for a trip you have not booked

```json
{
  "hotelNames": ["Hyatt Regency Lisbon", "Altis Grand Hotel Lisbon"],
  "checkIn": "2026-10-09",
  "days": 3,
  "nights": 2,
  "adults": 2,
  "currency": "EUR",
  "country": "pt",
  "maxPrice": 220
}
```

Run it every morning: the dataset stays empty until one of the six stays dips under 220 EUR a night, then carries the date, the source and the booking link.

### Example: your property and comp set, two weeks out, daily

```json
{
  "hotels": ["ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE"],
  "checkIn": "14 days",
  "days": 7,
  "nights": 1,
  "currency": "USD",
  "country": "us"
}
```

## Output

`rate` row (the Console's **Price history** and **Cheapest dates** views show the same rows as tables; the dataset schema documents every field):

```json
{ "type": "rate", "query": "https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "hotel_name": "Brown's | Avenue Hotel", "entity_id": "ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "hotel_id": null, "hotel_url": "https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "stars": null, "rating": null, "reviews": null,
  "check_in": "2026-10-08", "check_out": "2026-10-09", "nights": 1, "adults": 2, "children": 0, "currency": "USD",
  "price": 337.96, "price_display": "$338", "total": 337.96, "source": "Super.com", "official": false, "source_url": "https://www.super.com/…", "free_cancellation": false,
  "official_price": 420.03, "n_sources": 5, "cheapest_in_window": true, "rank_in_window": 1,
  "fetched_at": "2026-08-29T06:30:12+00:00" }
```

`status` row (never charged):

```json
{ "type": "status", "query": "Brown's Avenue Hotel Lisbon", "hotel_name": "Brown's | Avenue Hotel", "entity_id": "ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "check_in": "2026-10-08", "days": 7, "rates": 7, "filtered": 0, "no_rates": 0, "errors": 0, "cheapest": 337.96, "cheapest_date": "2026-10-08", "status": "ok", "error": null, "fetched_at": "2026-08-29T06:30:12+00:00" }
```

A run also writes a `SUMMARY` record to its key-value store: rate rows delivered, dates filtered, dates with no rate, names not found, duplicates, errors, the cheapest rate and date across the run, charged events and RPC stats.

## How is the lowest rate chosen?

For each property and check-in date the actor makes one offers call — the same request the Google Hotels page makes when it lists every booking site's rate for a stay — and takes each source's lowest rate for your occupancy. The row's `price` is the minimum of those; when the official site ties with an OTA the official site is reported, so `official: true` means booking direct is at least as cheap as anywhere else. `total` is the stay total at that source (nightly × nights when the source only shows a nightly rate). `official_price` is the official site's own lowest rate that day whatever the cheapest source was, and `n_sources` counts the sources that priced the stay at all. Whether the displayed rate includes taxes follows the country of the proxy IP the request leaves from (pre-tax plus mandatory fees from a US IP, all-in from most other countries), not `country`; rows are consistent within one proxy setup.

## How much does it cost?

Pay per event: one `rate` event per delivered row, at the price on this page's pricing tab. Two properties over thirty check-in dates is sixty rows — cents. A daily alert run with `maxPrice` bills only the dates under the target, which most days is none. Dates with no rate, names that do not resolve, a property listed twice, rows the spending limit refused and `status` rows are free, and a property and date is billed once per run. Apify's platform usage is a fraction of a cent per run: one search per name, one offers call per property and date.

Compared with the parent [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices), which bills one row per source, a rate row is one event for the whole comparison on that date — the cheap way to track hotel prices over many dates.

## Hotel price history, hotel price data and what to do with it

- **Best time to book a hotel**: run the same window daily from 60 days out and the `price` column by `fetched_at` shows when the rate for a given `check_in` bottomed. That is the curve behind every "book N days ahead" rule, measured for your property instead of averaged over the industry.
- **Hotel price comparison across a set**: one run with several properties gives a like-for-like table for the same dates, occupancy, currency and market — the `cheapest` view is the shortlist.
- **Hotel rate monitoring for owners** — a hotel rate tracker for your own property: the `official` flag over time is the simplest parity signal there is; when it flips to false, open the [Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity) row for that date to see who undercut you and by how much.
- **Hotel price calendar for a booking tool or a newsletter**: `days: 60` with `rank_in_window` is a ready-made "cheapest dates" widget.

Every row is flat JSON, so the dataset drops straight into a sheet, a BI tool or a notebook. To scrape hotel prices from Google Hotels at scale for many places rather than named properties, the parent scraper's place search is the tool; this one is deliberately exact, so nothing you did not name is ever billed.

## How to use it from Python, JavaScript, curl, n8n, Make or an AI agent

Run it from the Apify Console with the form, or programmatically. Replace `<TOKEN>` with your Apify API token.

Python — the cheapest date per property:

```python
from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/hotel-price-tracker").call(run_input={
    "hotelNames": ["Hyatt Regency Lisbon", "Altis Grand Hotel Lisbon"], "checkIn": "30 days", "days": 14, "nights": 2, "currency": "EUR", "country": "pt"})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "rate" and r["cheapest_in_window"]]
for r in rows: print(r["hotel_name"], r["check_in"], r["price"], r["currency"], "at", r["source"], "direct" if r["official"] else f'(direct {r["official_price"]})', r["source_url"])
```

JavaScript / Node.js — a price drop alert, straight into a message:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/hotel-price-tracker').call({ hotels: ['ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE'], checkIn: '2026-10-09', days: 3, nights: 2, maxPrice: 300 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const hits = items.filter(r => r.type === 'rate').map(r => `${r.hotel_name} ${r.check_in}: ${r.price} ${r.currency} at ${r.source} ${r.source_url}`);
console.log(hits.join('\n') || 'nothing under target yet');
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~hotel-price-tracker/run-sync-get-dataset-items?token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotels": ["ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE"], "checkIn": "30 days", "days": 7, "nights": 1, "currency": "USD"}'
```

- **n8n, Make, Zapier**: a Schedule trigger, an HTTP Request (or the Apify node) calling `run-sync-get-dataset-items` with the input above, a filter on `type = rate` (with `maxPrice` set, every row is a hit), and a Slack, Telegram, email or Sheets node — four nodes for a Google Hotels price alert, five for a price history sheet.
- **AI agents and MCP**: the actor is available through the Apify MCP server and Apify AI; the README, input schema and flat rows are written so an agent can answer "when is the Hyatt in Lisbon cheapest next month, and is direct cheaper?" from one run.
- **Google Sheets, BigQuery, Airtable**: export the dataset from the run page or through Apify's integrations; rows are flat, so no flattening is needed.

## Is it legal to track hotel prices from Google Hotels?

The actor reads publicly displayed prices — the same figures any visitor sees without logging in — and stores no personal data: rows describe properties, booking sources and rates, not people. Tracking public rates is what every fare-and-rate tracking service does; terms of service and local law still differ by place and purpose, so check that your use complies, keep the data for your own analysis, and do not republish it as Google's.

## Limits and honest notes

- Rates are what Google Hotels displays for the market (`country`) and currency you choose. Whether the displayed rate includes taxes follows the country of the proxy IP (pre-tax plus mandatory fees from a US IP, all-in from most others), not `country`; keep one proxy setup and one market across a history so rows compare like with like.
- A property with nothing bookable on a date (sold out, closed) has no rate that day: the date counts in `no_rates`, no row is delivered, nothing is billed.
- Names are resolved with one Google search and kept only when the listing's name matches most of the words you typed. A name that does not resolve gets a `not_found` status row and is free; reuse the `entity_id` from any row in `hotels` for exact, search-free runs.
- Windows are capped at 60 dates and stays at 30 nights per run; run twice for more.
- Google changes its internal payloads without notice. A daily canary run checks this actor; a failed date is reported in the status row's `errors` and `error` fields rather than delivered as a zero.

## FAQ

### Does it need a Google Hotels API key or a Google account?

No. There is no public Google Hotels API for reading prices — Google's hotel APIs are feeds for properties *sending* rates to Google. This actor reads the public comparison page through Apify's proxies. No account, no key, no browser on your side.

### How do I get a price drop alert instead of a table?

Set `maxPrice` to your target nightly rate and schedule the run. Rows appear only for dates at or under the target; wire the dataset to an n8n, Make or Zapier step that posts each row to Slack, Telegram or email. Days with nothing under target deliver nothing and cost nothing, and the status row still tells you the cheapest rate seen.

### Can it build hotel price history for a stay?

Yes — that is the scheduled use, and it is Google Hotels price tracking on your terms rather than Google's. Run the same input daily; each run appends rows with a new `fetched_at`. For one `check_in`, `price` over `fetched_at` is the history of that stay's best rate; `source` tells you who had it each day.

### Which dates does a window cover?

`days` consecutive check-in dates starting at `checkIn`, each for `nights` nights. `days: 7` from `"30 days"` prices check-ins 30 to 36 days from the run date. Relative `checkIn` values move with the calendar, so a schedule keeps looking the same distance ahead.

### Does the price include taxes and fees?

It follows what Google Hotels displays for the country the request leaves from — the proxy IP, not `country`: pre-tax plus mandatory fees from a US IP (the default datacenter proxies), all-in from most other countries. Rows are consistent within one proxy setup, so keep comparisons inside it.

### How is this different from the Google Hotels Prices Scraper?

The parent returns one row per booking source per property and stay, and can search places for many properties at once. This actor returns one row per property and date — the lowest rate and where it is — over a window of dates, ranked, with an alert filter. Use the parent when you want every source as its own row; use this one to track hotel prices over time or to find the cheapest date to stay.

### Can I track a competitor set for my own property?

Yes. List your property and the competitors by URL, token or name; every run gives one row per property and date with the market's lowest rate and whether it is direct. For the per-source breakdown and undercut math, pair it with the Hotel Rate Parity Checker on the same properties.

### Is there a free tier?

Every Apify account includes free platform credit, which covers many runs of this actor; the per-row price is on the pricing tab. Runs that deliver nothing — every date over `maxPrice`, unresolved names — have no event charge; compute and proxy are included in the event price.

## Related scrapers

Tracking a stay is one side of a trip. These read the rest of it, and they share the same pay-per-delivered-row billing and the same scheduling story:

- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — the parent: every booking source's rate per property and stay as its own row, plus place search.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — one row per property and stay with every source side by side and the undercut math done.
- **[Flight Price Tracker](https://apify.com/kestrel/flight-price-tracker)** — the same idea for airfare: one row per route and departure day, the cheapest fare, with a `maxPrice` alert.
- **[Google Flights Scraper](https://apify.com/kestrel/google-flights-prices)** — every itinerary for a route, date and cabin.
- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — Airbnb prices, availability calendars and occupancy.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
