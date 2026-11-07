# Agoda Prices Scraper — Hotel Rates & Availability by Date

**Agoda prices scraper** for real stays: give a destination or a list of hotels, a check-in date, nights and guests, and get every property's cheapest rate as clean rows — **agoda hotel prices** per night and for the whole stay, with and without taxes, the cancellation term, rooms left, stars, guest score and coordinates. It reads the same search answer agoda.com's own results page reads, so the numbers match what a traveller sees — a hotel rate scraper that returns Agoda's structured data rather than a rendered page. Use it as an **agoda scraper** for market research, as a **hotel price comparison** feed next to the Google Hotels and Booking.com actors below, or as the **agoda api** you were looking for: no key, no browser, pay per priced hotel.

Last verified working: 2026-08-29.

## Agoda 酒店价格、房态与最低价日期：中文调用与语言设置

按城市或酒店查询房价、含税总价、可订状态及来源显示的剩余房间。calendarDays 可扫描日期；剩余房间是来源显示值，不是酒店全部库存。

locale="zh-cn" 设置酒店名称、地区等标签语言；currency 单独控制货币。价格比较必须使用相同日期、人数和币种。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "locationQueries": [
    "Lisbon"
  ],
  "checkIn": "30 days",
  "nights": 1,
  "adults": 2,
  "maxHotelsPerQuery": 1,
  "sortBy": "price_low",
  "currency": "USD",
  "calendarDays": 1,
  "locale": "zh-cn",
  "sessions": 1
}
```

ราคาโรงแรม / 호텔 가격 / Agoda 价格：区域标签与币种分别设置。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Agoda scraper for AI agents: which input answers which request?

**Use it when** the request is an Agoda price or availability for specific dates: every hotel in a city, a named hotel, a comp set re-priced daily, "hotels under X a night", "when is this hotel cheapest" (the price calendar), or how much of a city is sold out. **Do not use it for** guest reviews (Agoda Reviews Scraper), prices on other booking sites or rate parity (Google Hotels Prices Scraper, Hotel Rate Parity Checker), room-by-room rate grids (the row carries the cheapest room only), member or app-only discounts, or making a booking.

| User request | Input JSON |
|---|---|
| "Hotel prices in Bangkok for 20–22 November, 2 adults, in baht" | `{"locationQueries": ["Bangkok"], "checkIn": "2026-11-20", "nights": 2, "adults": 2, "currency": "THB"}` |
| "The 20 cheapest hotels in Lisbon next month" | `{"locationQueries": ["Lisbon"], "checkIn": "30 days", "sortBy": "price_low", "maxHotelsPerQuery": 20}` |
| "4-star hotels in Bali under 100 USD with free cancellation, rated 8+" | `{"locationQueries": ["Bali"], "checkIn": "2026-12-10", "nights": 3, "minStars": 4, "maxPrice": 100, "freeCancellationOnly": true, "minReviewScore": 8}` |
| "What does the Tivoli Avenida Liberdade cost on 20 November?" | `{"hotelNames": ["Tivoli Avenida Liberdade Lisbon"], "checkIn": "2026-11-20"}` |
| "When is hotel 63820 cheapest in the next two months?" | `{"hotelIds": ["63820"], "checkIn": "tomorrow", "calendarDays": 60}` — read the `calendar` rows, `cheapest_in_window: true` |
| "Track my comp set every morning at a 30-day lead time" | `{"hotelIds": ["63820", "6988894"], "checkIn": "30 days", "nights": 1}` on an Apify schedule |
| "How much of Bangkok is sold out this weekend?" | `{"locationQueries": ["Bangkok"], "checkIn": "2026-11-21", "nights": 2, "maxHotelsPerQuery": 0, "includeSoldOut": true}` — count `sold_out: true` rows (free) against priced ones |
| "Hotel names in Japanese, prices in yen" | add `"locale": "ja-jp", "currency": "JPY"` — `locale` changes names and labels, `currency` changes prices |

**Output row** — one `hotel` row per property: `hotel_name`, `hotel_id`, `url`, `property_type`, `stars`, `review_score`, `review_count`, `agoda_score`, `price_nightly`, `price_nightly_with_taxes`, `price_total`, `price_total_with_taxes`, `crossed_out_price`, `currency`, `available_rooms`, `cancellation`, `free_cancellation`, `free_cancellation_until`, `breakfast_included`, `sold_out`, `city`, `area`, `country`, `latitude`, `longitude`, `check_in`, `check_out`, `nights`, `adults`, `children`, `rooms`, `rank`, `sort`, `query`. With `calendarDays`, one `calendar` row per priced check-in date (`check_in`, `price_nightly`, `price_total`, `trend`, `rank_in_window`, `cheapest_in_window`).

**Status and empty results** — every destination and every named hotel also writes one free `status` row: `status` is `ok`, `no_results`, `not_found`, `sold_out`, `duplicate` or `error`, with `hotels`, `sold_out_hotels`, `filtered`, `pages`, `calendar_days` and `duplicates`. A property Agoda cannot price for the stay is not a hotel row unless `includeSoldOut` is true (then a free row with `sold_out: true`); a place or name Agoda cannot match is a `status` row with `error` or `not_found` and no hotel rows; a run whose only problem is the input (a past date, a non-Agoda URL, no target at all) ends green with the reason on the run card and charges nothing. With no `checkIn` the stay starts 30 days after the run.

## What the Agoda prices scraper returns

One `hotel` row per property Agoda prices for your stay:

- **Price** — `price_nightly` (per room per night, before taxes — Agoda's default display price), `price_nightly_with_taxes`, `price_total` and `price_total_with_taxes` for the whole booking, `crossed_out_price` when a discount is shown, the `currency` you asked for.
- **Terms** — `cancellation` (FreeCancellation, NonRefundable, SpecialConditions), `free_cancellation`, `free_cancellation_until`, `breakfast_included`, the raw `benefit_ids`, `available_rooms` at that rate, `supplier_id`, `payment_model`.
- **Property** — `hotel_id`, `hotel_name`, `url`, `property_type`, `stars`, `review_score` and `review_count` across every source Agoda aggregates, `agoda_score` and `agoda_review_count` from Agoda's own reviews, `city`, `city_id`, `area`, `country`, `country_code`, `latitude`, `longitude`.
- **Stay** — `check_in`, `check_out`, `nights`, `adults`, `children`, `rooms`, plus `rank` (position in the destination's results under `sort`), `mode`, `query`, `locale`, `price_source` and `fetched_at`.

Named properties can add a **price calendar**: one `calendar` row per check-in date with a live price, with `price_nightly`, `price_total`, Agoda's `trend` word where it has one (Low, Normal, High; null on most dates), `rank_in_window` and `cheapest_in_window`. Every input also writes a free `status` row (`target`, `mode`, `status`, `hotels`, `sold_out_hotels`, `filtered`, `pages`, `calendar_days`, `duplicates`, `error`).

## Why this Agoda scraper instead of the page

Agoda's results page loads prices asynchronously and re-polls its search until every property is priced — a browser-based scraper waits, scrolls and still misses the last poll. This actor calls the search endpoint with the synchronous flag Agoda's own client eventually sets, so **one request returns 45 priced properties** with the fields above already structured. Named hotels use Agoda's single "extra property" slot: one 3 KB answer per hotel, no page read. Two facts that matter for your data:

1. **Sold-out is not a price.** A property Agoda lists but cannot price for your stay comes back with `sold_out: true` and every price empty. Those rows are free and hidden unless you ask for them, so a price list stays a price list.
2. **A throttle is never a "no results".** When Agoda refuses a session the actor rotates the proxy session and retries; if every attempt is refused the input is reported as an `error`, not as an empty destination. An unknown destination id fails in one call with Agoda's own message.

## Agoda hotel prices by destination

Put a city, area or country in `locationQueries` — or Agoda's numeric city id, or a search URL copied from agoda.com — and set the stay:

```json
{
  "locationQueries": ["Lisbon", "Bangkok"],
  "checkIn": "30 days",
  "nights": 2,
  "adults": 2,
  "currency": "USD",
  "sortBy": "price_low",
  "maxHotelsPerQuery": 100
}
```

Each destination is resolved through Agoda's own autocomplete (the best match wins; put the country in the text for ambiguous names), then paged 45 properties at a time in `sortBy` order until `maxHotelsPerQuery` priced hotels have been collected. `maxHotelsPerQuery: 0` takes every property Agoda lists for the stay, up to 40 pages (about 1,800 properties) — a capital fills that, so set the cap for anything you schedule. The `rank` column is the position in Agoda's order for that sort, which is also how the cap cuts.

### Which sort orders does the scraper support?

`best_match` (Agoda's ranking, the default), `price_low` (cheapest first — Agoda only sorts price ascending), `guest_rating` (highest review score first) and `secret_deals`. Sort only applies to destination searches; named properties are priced on their own.

## Agoda hotel rates for named hotels

Name the properties with `startUrls` (property pages), `hotelIds` (Agoda's numeric ids, the fastest) or `hotelNames` (resolved through the autocomplete):

```json
{
  "hotelIds": ["6988894", "63820"],
  "hotelNames": ["Tivoli Avenida Liberdade Lisbon"],
  "checkIn": "2026-10-10",
  "nights": 3,
  "adults": 2,
  "rooms": 1,
  "currency": "EUR",
  "calendarDays": 30
}
```

Each property costs one small request. A URL, its id and its name are one property: the run delivers it once and the later inputs report `duplicates: 1`. When a named property has no rate for the stay, its status row says `sold_out`; when Agoda does not know the id, `not_found`.

### What is the price calendar?

With `calendarDays: N` the actor also prices each named property for up to 60 check-in dates from `checkIn`, one live single-property search per date at your nights and adults (the stay's own search is reused for the first date). Agoda's price-trend store only lends the `trend` word (Low, Normal, High) where it has one — since October 2026 it is sparse, so `trend` is null on most dates; the prices themselves are live quotes. Dates with no rate are skipped free.

## Filters that run before billing

- `maxPrice` — keep only hotels whose `price_nightly` is at or under this amount in your currency.
- `minStars` — keep only properties with at least this star rating (unrated properties are dropped when set).
- `minReviewScore` — keep only properties with at least this guest score out of 10.
- `freeCancellationOnly` — keep only hotels whose cheapest rate is free to cancel.

Every filter runs on the actor before the charge call, so a hotel a filter removes is never billed. A daily "anything in Lisbon under 60 with free cancellation" schedule costs nothing on days without a match; the status row still reports how many were `filtered`. `includeSoldOut` writes the unpriced properties too (free), which is useful for occupancy tracking.

## What does one run cost?

Pay per event, only for what is delivered:

| Event | Price | What it is |
|---|---|---|
| `hotel` | $0.004 | One priced property for the stay |
| `calendar_day` | $0.002 | One priced check-in date of a property's calendar |

Sold-out properties, filtered hotels and status rows are free. Every property is billed once per run however many inputs reach it. Examples at list price: 100 hotels in a city, $0.40; a comp set of 20 named hotels every morning, $0.08 a day; the same 20 with a 30-day calendar, roughly $0.08 + 20 × (priced dates × $0.002). Runs use Apify Proxy datacenter sessions, which are included in your Apify plan; the endpoint tolerates about one request per second per IP, and a 45-property page is under 100 KB.

## Input

| Field | What it does |
|---|---|
| `locationQueries` | Destinations: names ("Lisbon"), Agoda city ids ("16364") or agoda.com search URLs. One search each. |
| `startUrls` | Agoda property pages (priced one by one) or search-result URLs (treated as destinations). |
| `hotelIds` | Agoda numeric property ids — the fastest way to price a known list. |
| `hotelNames` | Property names, resolved through Agoda's autocomplete; the best match is priced. |
| `checkIn` | YYYY-MM-DD or relative ("30 days", "6 weeks", "tomorrow") so schedules never go stale. Past dates are refused. |
| `nights` | Length of stay, 1-30. |
| `adults`, `children`, `childAges`, `rooms` | Occupancy the price is quoted for; ages 0-17, one per child. |
| `currency` | ISO code for every price (USD, EUR, GBP, THB, JPY…). |
| `sortBy` | Destination result order: `best_match`, `price_low`, `guest_rating`, `secret_deals`. |
| `maxHotelsPerQuery` | Priced properties per destination, in `sortBy` order; 0 = all, up to 40 pages (about 1,800). The main cost control. |
| `maxPrice` | Keep hotels at or under this nightly price; 0 = no limit. Filters before billing. |
| `minStars` | Keep properties with at least this star rating; 0 = any. |
| `minReviewScore` | Keep properties with at least this guest score (0-10); 0 = any. |
| `freeCancellationOnly` | Keep only free-cancellation rates. |
| `includeSoldOut` | Also write unpriced properties (free rows with `sold_out: true`). |
| `calendarDays` | Named properties only: read the price calendar for this many check-in dates (0-60). |
| `locale` | Agoda locale for names and areas (en-us, de-de, ja-jp…). |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. |
| `proxyConfiguration` | Apify Proxy; datacenter is enough for this endpoint. |

## Output example

```json
{
  "type": "hotel",
  "mode": "destination",
  "query": "Lisbon",
  "locale": "en-us",
  "hotel_id": "13505436",
  "hotel_name": "Help Yourself Hostels - Restelo",
  "url": "https://www.agoda.com/help-yourself-hostels-restelo/hotel/all/lisbon-pt.html",
  "property_type": "Hotel",
  "stars": 2.0,
  "review_score": 6.8,
  "review_count": 120,
  "agoda_score": 6.5,
  "agoda_review_count": 31,
  "city": "Lisbon",
  "city_id": 16364,
  "area": "Belem",
  "country": "Portugal",
  "country_code": "PT",
  "latitude": 38.6997,
  "longitude": -9.2079,
  "check_in": "2026-09-28",
  "check_out": "2026-09-29",
  "nights": 1,
  "adults": 2,
  "children": 0,
  "rooms": 1,
  "currency": "USD",
  "price_nightly": 44.71,
  "price_nightly_with_taxes": 60.67,
  "price_total": 44.71,
  "price_total_with_taxes": 60.67,
  "crossed_out_price": null,
  "available_rooms": 1,
  "cancellation": "FreeCancellation",
  "free_cancellation": true,
  "free_cancellation_until": null,
  "breakfast_included": false,
  "benefit_ids": [6, 95, 230, 231],
  "supplier_id": 332,
  "payment_model": "MerchantCommission",
  "sold_out": false,
  "rank": 46,
  "sort": "price_low",
  "price_source": "search",
  "fetched_at": "2026-08-29T11:20:04+00:00"
}
```

Dataset views: **Hotels** (every priced row in result order), **Cheapest first** (priced hotels by `price_nightly`), **Price calendar** (`calendar` rows with `trend`, `rank_in_window`, `cheapest_in_window`) and **Status** (`target`, `mode`, `status`, `hotels`, `sold_out_hotels`, `filtered`, `pages`, `calendar_days`, `duplicates`, `error`). The run's key-value store carries a `SUMMARY` record with the totals delivered, charged, filtered, sold out and failed, plus HTTP stats.

## How to run the Agoda prices scraper from code

### Python

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/agoda-prices-scraper").call(run_input={
    "locationQueries": ["Lisbon"],
    "checkIn": "30 days", "nights": 2, "adults": 2, "currency": "EUR",
    "sortBy": "price_low", "maxHotelsPerQuery": 50, "freeCancellationOnly": True,
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "hotel"]
for r in rows[:5]:
    print(r["rank"], r["hotel_name"], r["price_nightly"], r["currency"], r["cancellation"])
```

### JavaScript

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/agoda-prices-scraper').call({
    hotelIds: ['6988894', '63820'], checkIn: '2026-10-10', nights: 3, adults: 2, currency: 'USD', calendarDays: 30,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const cheapest = items.filter(r => r.type === 'calendar' && r.cheapest_in_window);
console.log(cheapest.map(r => [r.hotel_name, r.check_in, r.price_nightly]));
```

### curl

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~agoda-prices-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{"locationQueries": ["Bangkok"], "checkIn": "45 days", "nights": 1, "adults": 2, "currency": "THB", "maxHotelsPerQuery": 45, "minReviewScore": 8}'
```

## Integrations: n8n, Make, MCP and AI agents

- **n8n / Make / Zapier** — call the actor with an HTTP Request node (`run-sync-get-dataset-items`, JSON body as above, a 300 s timeout) on a Schedule; keep `checkIn` relative so the workflow never goes stale. Filter on `type` first, then compare `price_nightly` with yesterday's value in your sheet or database to build a price-drop alert.
- **MCP and AI agents** — the actor is available through Apify's MCP server and to Apify AI, so an agent can ask for "the ten cheapest free-cancellation hotels in Lisbon next month" and receive these rows; the input and output schemas above are what the agent reads.
- **Sheets, BI, webhooks** — every run's dataset exports as JSON, CSV or Excel; add a webhook on run success to push new prices where they need to go.

## Hotel price comparison and other uses for the data

- **Hotel price comparison across channels** — run the same stay through this actor, the [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices) (every booking site's rate per hotel) and the [Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper)'s sibling data, and see where Agoda undercuts.
- **Rate parity** — join on `hotel_name` with the [Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity) to flag OTAs cheaper than the official site.
- **Agoda price tracker** — schedule a destination search daily with relative dates; `hotel_id` is the stable join key and `fetched_at` the timestamp, so a month of runs is a price history per property — hotel price tracking without a rate-shopping subscription.
- **Cheapest hotels on Agoda** — `sortBy: price_low` with `maxHotelsPerQuery: 20` is a twenty-row answer to "what is the cheapest place to sleep in Bangkok next Friday", refreshed every morning for a few cents.
- **Market snapshots** — `maxHotelsPerQuery: 0` with `includeSoldOut: true` gives the whole inventory for a date: how many properties are priced, at what median, and how many are sold out — an occupancy proxy for a city.
- **Revenue management** — a comp set as `hotelIds` every morning with `calendarDays: 60` shows every competitor's cheapest dates next to your own.

## FAQ

### Are these the prices a guest sees on Agoda?

Yes — for the same stay, currency and occupancy. `price_nightly` is Agoda's default display price (per room per night, before taxes and fees); `price_total_with_taxes` is what the booking would cost. Agoda personalises some discounts for logged-in members and app users; this actor prices as a logged-out visitor, the same view Google and metasearch engines get.

### How many hotels can one run collect?

As many as Agoda lists for the stay: a large city returns one to three thousand properties at 45 per page. `maxHotelsPerQuery` caps that per destination (its default is 45, one page) and `status.pages` tells you how many pages were read. Runs are paced at about one request per second per session; four sessions read roughly 180 properties a second of wall time.

### Can I get room-level rates?

The row carries the cheapest rate Agoda would show on the property card — one room type, one supplier — with its cancellation term, benefits and rooms left. Agoda room prices by room type (the full grid) are not part of this actor; ask on the Issues tab if you need them and say how many properties you price a day.

### Does it work for apartments, hostels and resorts?

Yes: `property_type` tells them apart, and stars are empty for unrated properties. Filters like `minStars` drop unrated ones by design; use `minReviewScore` to rank hostels and apartments instead.

### Why is a property sold out in one run and priced in the next?

Availability is per stay. Change the dates, the number of nights or the occupancy and Agoda's answer changes with it. The Tivoli Avenida Liberdade, for example, has no rate for one specific night but a price calendar full of other dates — that is exactly what `calendarDays` is for.

### Which currencies and locales are supported?

Any ISO currency Agoda quotes in (USD, EUR, GBP, THB, JPY, AUD, SGD…), converted at Agoda's own rate. `locale` changes names and area labels (de-de, ja-jp, th-th…), not the prices.

### What happens when Agoda throttles the run?

The session's IP is rotated and the request retried with back-off; the input is only reported as an `error` when every attempt was refused. Nothing is billed for an errored input, and the run only fails outright when every input failed.

### Is scraping Agoda prices legal?

The actor reads public, logged-out price listings — the same data Agoda publishes to search engines and metasearch partners — and stores no personal data. Using that data for price comparison, market research and revenue management is a normal business use; check Agoda's terms and your local law before republishing prices commercially, respect the site with sensible pacing, and do not use the data to interfere with Agoda's service.

## Related scrapers

Prices are one side of a booking decision. These read the rest of it and share the same pay-per-delivered-row billing:

- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — every guest review of an Agoda property with separate positives and negatives.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site's rate for a stay.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — one row per property with every source side by side and the parity math done.
- **[Hotel Price Tracker](https://apify.com/kestrel/hotel-price-tracker)** — the lowest Google Hotels rate per property and date over a window, for daily schedules.
- **[Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper)** — Booking.com guest reviews by URL, name or id.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
