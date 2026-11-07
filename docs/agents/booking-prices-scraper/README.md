# Booking.com Scraper — Hotel Prices & Availability by Date

This **Booking.com scraper** is a **hotel price scraper** for exact dates, guests and rooms: it returns **Booking.com hotel prices** for every property in a destination, or for a list of hotels by URL, name or id, each as one clean row with the stay total in your currency, the nightly price, the taxes and fees Booking leaves out, free-cancellation and breakfast flags, stars, review score, location and the cheapest room. It reads the same call Booking.com's own search results page makes, so there is no browser, no login and no Booking.com API key — a way to scrape Booking.com without API access — and you pay per priced property, never for sold-out ones.

Last verified working: 2026-10-17.

## Booking.com 酒店价格、房态与可订日期：中文调用与语言设置

按目的地或酒店查询入住日期、房价、税费及可订状态。includeRooms 开启后会增加房型报价行；只需要酒店价格时关闭。

locale 设置标签语言，currency 单独控制币种；两者不是同一个概念。示例 locale="fr-FR"。使用一致日期、人数及币种比较价格。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "maxHotelsPerQuery": 1,
  "checkIn": "30 days",
  "nights": 1,
  "adults": 2,
  "currency": "USD",
  "sortBy": "price",
  "locale": "fr-FR",
  "includeRooms": false,
  "sessions": 1,
  "hotelIds": [
    "536251"
  ]
}
```

Prix hôtel / precios de hoteles / Hotelpreise：报价按入住条件查询。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Booking.com scraper for AI agents: which input answers which request?

**Use it when** the request is a Booking.com price or availability for specific dates: every hotel in a destination, a named hotel, a comp set re-priced daily, "hotels under X a night", "is it sold out", or every room and rate one hotel offers. **Do not use it for** guest reviews (Booking.com Reviews Scraper), prices on other booking sites or rate parity (Google Hotels Prices Scraper, Hotel Rate Parity Checker), member-only Genius rates, or making a booking. One run prices ONE stay (`checkIn` + `nights`); for a price calendar run it once per check-in date or use the Hotel Price Tracker.

| User request | Input JSON |
|---|---|
| "Hotel prices in Lisbon for 20–22 November, 2 adults, in euros" | `{"locationQueries": ["Lisbon"], "checkIn": "2026-11-20", "nights": 2, "adults": 2, "currency": "EUR"}` |
| "The 50 cheapest hotels in Lisbon next weekend" | `{"locationQueries": ["Lisbon"], "checkIn": "2026-11-21", "nights": 2, "sortBy": "price", "maxHotelsPerQuery": 50}` |
| "4-star hotels in the Algarve under 150 GBP a night for a family of four" | `{"locationQueries": ["Algarve"], "checkIn": "2026-12-20", "nights": 7, "adults": 2, "childrenAges": ["5", "9"], "currency": "GBP", "minStars": 4, "maxPrice": 150}` |
| "What does Memmo Alfama cost on 20 November?" | `{"hotelNames": ["Memmo Alfama Lisbon"], "checkIn": "2026-11-20"}` |
| "Every room and rate hotel 536251 offers that night" | `{"hotelIds": ["536251"], "checkIn": "2026-11-20", "includeRooms": true}` |
| "Track my comp set every morning at a 30-day lead time" | `{"hotelIds": ["536251", "2251985", "1471925"], "checkIn": "30 days", "nights": 1}` on an Apify schedule |
| "Is hotel X available on these dates?" | the named-hotel input above: a row with `sold_out: true` (and Booking's `alternative_check_in` / `alternative_check_out`) means no |
| "Prices in German, in euros" | add `"currency": "EUR", "locale": "de-DE"` — `locale` changes labels, `currency` changes prices |

**Output row** — one `hotel` row per property: `name`, `hotel_id`, `url`, `property_type`, `stars`, `review_score`, `review_count`, `price_total`, `price_nightly`, `currency`, `price_display`, `taxes_included`, `taxes_fees_excluded`, `price_hotel_currency_total`, `free_cancellation`, `no_prepayment`, `breakfast_included`, `meal_plan`, `room_name`, `rooms_listed`, `sold_out`, `address`, `latitude`, `longitude`, `distance_from_center`, `check_in`, `check_out`, `nights`, `adults`, `children`, `rooms`, `rank`, `query`. With `includeRooms: true`, one `room` row per room and rate combination (`room_name`, `occupancy`, `meal_plan`, `price_total`, `price_nightly`, `free_cancellation_until`, `only_x_left`).

**Status and empty results** — every destination and every named hotel also writes one free `status` row: `status` is `ok`, `no_results`, `not_found`, `duplicate` or `error`, with `hotels`, `priced`, `unpriced`, `filtered`, `duplicates`, `rooms`, `pages` and Booking's `total`. A sold-out property is a free `hotel` row with `sold_out: true`; a place or name Booking cannot match is a `status` row with `error` or `not_found` and no hotel rows; a run whose only problem is the input (no `checkIn`, a past date, a non-Booking URL, no target at all) ends green with the reason on the run card and charges nothing. `checkIn` has no default: a run without it is such an input problem.

## What does the Booking.com scraper do?

Give it a stay — check-in, nights, adults, children's ages, rooms, currency — and either destinations ("Lisbon", "Algarve", "Times Square", "Portugal") or properties. It returns:

- **One `hotel` row per property**: the lowest stay total Booking.com shows for that party, the nightly rate derived from it, the hotel-currency total, what is excluded (taxes and fees) and Booking's own wording for it, free cancellation, no-prepayment and breakfast flags, stars, the 1-10 review score and count, address, coordinates, neighbourhood and distance from the centre, the room behind the headline price, whether the property is sold out and the alternative dates Booking suggests.
- **Optional `room` rows** (`includeRooms`): every room and rate combination Booking matched to the stay, with its own price, occupancy, meal plan, free-cancellation deadline and "only 2 left" message.
- **One `status` row per target**: how many properties were delivered, priced, filtered and duplicated, how many pages were read and Booking's total for the destination.

Destinations are resolved through Booking's own autocomplete, so a city, region, district, landmark, airport or country all work, and sorting uses Booking's own orders (price, review score, stars, distance) so a **hotel price scraper** run is repeatable day after day.

## Booking.com hotel prices for a destination, a comp set or a portfolio

Three ways to address what you want priced, mixed freely in one run:

- **Destinations** (`locationQueries`) — a place name, paged up to `maxHotelsPerQuery` properties in the order `sortBy` gives. "Lisbon" with `sortBy: price` and 100 properties is one request; a 1,000-property market scan is ten.
- **Hotel URLs** (`startUrls`) — Booking.com property pages. A URL carries no id, so it is resolved through autocomplete first.
- **Hotel names or ids** (`hotelNames`, `hotelIds`) — the id is what an earlier run's `hotel_id` column holds, and it is the fastest way to re-price a comp set every morning.

A property that turns up twice (in two destinations, or as a URL and its id) is delivered and billed once; the second sighting is counted in `duplicates`.

## Hotel price monitoring that never goes stale

`checkIn` accepts relative dates — `"30 days"`, `"6 weeks"`, `"tomorrow"` — so a scheduled run always prices the same lead time. Run it daily with `sortBy: price` and you get a **booking.com prices by date** history for a market; run it with a comp set of ids and you have a **hotel rate scraper** doing your **hotel rate shopping** every morning, with **booking.com availability** (sold-out state and alternative dates) in the same rows. Because every row carries `check_in`, `nights`, `adults`, `rooms` and `currency`, rows from different days line up in one table without any post-processing.

The `maxPrice` input keeps only properties whose nightly rate is at or under a figure, and `minStars` is passed to Booking itself as its star filter. Both run **before billing**: a "4-star hotels under 150 EUR in Lisbon" run delivers and bills only the rows that qualify, and a quiet day costs nothing.

## Input

| field | what it does |
|---|---|
| `locationQueries` | Destinations as typed into Booking's search box. Each is one search for the stay. |
| `maxHotelsPerQuery` | Properties to take per destination (1-1000, default 50), in `sortBy` order. Booking pages 100 at a time. |
| `startUrls` | Booking.com property pages, priced one by one. |
| `hotelNames` | Property names; the first autocomplete match is priced — check `hotel_name` in the status row. |
| `hotelIds` | Booking's numeric ids (`hotel_id` from an earlier run). |
| `checkIn` | Required, no default. `YYYY-MM-DD` or relative (`"30 days"`). Check-out is `checkIn` + `nights`. |
| `nights` | Length of stay, 1-30. |
| `adults` | Adults across all rooms (1-30). |
| `childrenAges` | One age per child, 0-17. Booking needs ages to match family rooms. |
| `rooms` | Rooms needed (1-30). |
| `currency` | ISO code for every price. The hotel's own currency is kept alongside. |
| `sortBy` | Booking's orders: `popularity`, `price`, `price_desc`, `review_score`, `review_score_and_price`, `stars`, `stars_asc`, `stars_and_price`, `distance`, `homes_first`. |
| `minStars` | 0 = all; 1-5 = Booking's star filter, applied before fetching. |
| `maxPrice` | 0 = all; N = keep properties whose nightly rate is ≤ N in `currency`. Filtered rows are never billed. |
| `includeRooms` | Also deliver `room` rows for every priced property. |
| `locale` | Booking locale for labels and number formats (`en-US`, `de-DE`, …). |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. |
| `proxyConfiguration` | Apify Proxy, RESIDENTIAL group — required (see the honest notes). |

### Example: the cheapest 100 places in Lisbon for a weekend

```json
{
  "locationQueries": ["Lisbon"],
  "maxHotelsPerQuery": 100,
  "checkIn": "6 weeks",
  "nights": 2,
  "adults": 2,
  "currency": "EUR",
  "sortBy": "price"
}
```

One request, 100 rows, 100 × $0.004 = $0.40.

### Example: a daily rate shop for a comp set

```json
{
  "hotelIds": ["536251", "2251985", "1471925"],
  "checkIn": "30 days",
  "nights": 1,
  "adults": 2,
  "currency": "USD",
  "includeRooms": true
}
```

Three `hotel` rows and every room and rate each property offers for that night, every morning, at the same 30-day lead time.

### Example: family rooms under a budget with Booking's 4-star filter

```json
{
  "locationQueries": ["Algarve"],
  "maxHotelsPerQuery": 200,
  "checkIn": "2026-10-10",
  "nights": 7,
  "adults": 2,
  "childrenAges": [5, 9],
  "rooms": 1,
  "currency": "GBP",
  "sortBy": "review_score",
  "minStars": 4,
  "maxPrice": 180
}
```

Booking applies the star filter; the actor applies the price cap; you are billed for the rows that pass both.

## Output

Every row has `type`: `hotel`, `room` or `status`. Hotel rows always carry every column below (null where Booking shows nothing), so a CSV export is rectangular.

```json
{
  "type": "hotel",
  "hotel_id": "536251",
  "name": "Memmo Alfama - Design Hotels",
  "url": "https://www.booking.com/hotel/pt/memmo-alfama.html",
  "property_type": "hotel",
  "stars": 4,
  "review_score": 9.3,
  "review_count": 894,
  "city": "Lisboa",
  "country_code": "pt",
  "display_location": "Santa Maria Maior, Lisbon",
  "distance_from_center": "0.8 km from downtown",
  "check_in": "2026-09-28",
  "check_out": "2026-09-29",
  "nights": 1,
  "adults": 2,
  "currency": "EUR",
  "price_total": 415.09,
  "price_nightly": 415.09,
  "price_display": "€ 415.09",
  "hotel_currency": "EUR",
  "taxes_included": true,
  "free_cancellation": true,
  "breakfast_included": true,
  "room_name": "Superior Double Room with Terrace",
  "rooms_listed": 3,
  "sold_out": false,
  "rank": 1,
  "query": "Memmo Alfama Lisbon"
}
```

Key columns:

- `price_total` / `price_nightly` / `currency` — the lowest total Booking shows for the whole stay and party, and that total divided by nights. `price_display` is Booking's own formatted string.
- `taxes_included`, `taxes_fees_excluded`, `charges_note` — whether Booking lists excluded charges, how much they are, and its wording ("+US$9 taxes and fees").
- `price_hotel_currency_total` / `hotel_currency` — the same total in the property's own currency, so conversions are yours to make.
- `stars`, `review_score`, `review_count`, `property_type`, `address`, `latitude`, `longitude`, `display_location`, `distance_from_center`, `transport`.
- `free_cancellation`, `no_prepayment`, `meal_plan`, `breakfast_included`, `room_name`, `rooms_listed`.
- `sold_out`, `sold_out_message`, `alternative_check_in`, `alternative_check_out` — a property with no price for the dates is delivered free with these filled in.
- `sponsored`, `newly_opened`, `sustainable`, `host_type`, `image`, `rank`, `query`.

`room` rows: `room_id`, `room_name`, `occupancy`, `meal_plan`, `price_total`, `price_nightly`, `currency`, `price_original` in the hotel currency, `free_cancellation_until`, `only_x_left`, `has_crib`, `third_party`.

`status` rows: `target`, `kind` (destination or hotel), `dest_type`, `dest_id`, `hotel_id`, `hotel_name`, `status` (`ok`, `no_results`, `not_found`, `duplicate`, `error`), `hotels`, `priced`, `unpriced`, `filtered`, `duplicates`, `rooms`, `pages`, `total`, `error`.

## How much does it cost?

$0.004 per priced `hotel` row and $0.002 per `room` row, plus nothing else: sold-out and unpriced properties, status rows, filtered rows and refused runs are free. Pricing 100 Lisbon properties is $0.40; a daily comp set of 10 hotels with room rates (say 60 rooms) is $0.16 a day. Apify's platform usage for a 100-property search is well under a cent.

## Booking.com scraper in Python, JavaScript, curl, n8n, Make or an AI agent

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/booking-prices-scraper").call(run_input={
    "locationQueries": ["Lisbon"], "maxHotelsPerQuery": 50,
    "checkIn": "30 days", "nights": 1, "adults": 2, "currency": "EUR", "sortBy": "price",
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "hotel" and r["price_total"] is not None]
for r in rows[:10]:
    print(r["rank"], r["name"], r["stars"], r["review_score"], r["price_nightly"], r["currency"], r["room_name"])
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/booking-prices-scraper').call({
    hotelIds: ['536251', '2251985'], checkIn: '30 days', nights: 1, adults: 2, currency: 'USD', includeRooms: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const hotels = items.filter(r => r.type === 'hotel');
console.log(hotels.map(h => [h.name, h.price_nightly, h.free_cancellation]));
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~booking-prices-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"locationQueries": ["Algarve"], "maxHotelsPerQuery": 30, "checkIn": "6 weeks", "nights": 3, "adults": 2, "currency": "GBP", "sortBy": "review_score", "minStars": 4}'
```

**n8n and Make:** an HTTP Request node posting the same JSON to `run-sync-get-dataset-items` returns the rows in one step; keep rows where `type` is `hotel`, compare `price_nightly` with the previous run in a Code node, and alert on drops. The Google Hotels price-drop template in the [kestrel examples repository](https://github.com/mtedj/kestrel-actors-examples) follows exactly that shape.

**MCP and AI agents:** the actor is callable through Apify's MCP server; an agent that needs "the cheapest 4-star hotel in Lisbon next weekend under 200 EUR" can pass `locationQueries`, `checkIn`, `minStars`, `maxPrice` and read the first `hotel` row.

## Is it legal to scrape Booking.com prices?

The actor reads the publicly visible prices and property facts that Booking.com shows every anonymous visitor for the dates and party you specify — no login, no personal data, nothing behind an account. Prices are facts, not copyrighted works. Whether your use complies with Booking's terms and with the laws where you operate is your responsibility; keep the request rate reasonable, do not resell Booking's data as your own, and attribute where you publish comparisons.

## Limits and honest notes

- **Residential proxy required.** Booking's search call answers datacenter addresses with its WAF challenge but serves residential ones without cookies or tokens. The default `proxyConfiguration` is set accordingly; changing it to datacenter makes every search fail.
- **"Top picks" shifts between pages.** Booking's default `popularity` order is personalised and reshuffles, so a long paged run under it can repeat properties (deduplicated, counted in `duplicates`) and miss others. Use `price`, `review_score`, `stars` or `distance` for a complete, repeatable list.
- **Prices are for your party.** The stay total depends on adults, children's ages and rooms; a solo traveller sees different rates than a couple. `price_nightly` is the total divided by nights, not Booking's own per-night figure (which it omits for most searches).
- **Taxes vary by market.** In some countries the total includes taxes; elsewhere Booking lists them as excluded. `taxes_included`, `taxes_fees_excluded` and `charges_note` say which, per row.
- **Sold-out properties** still appear (free) with `sold_out: true` and Booking's alternative dates when it offers them. With `maxPrice` set they are dropped, since they have no price to compare.
- **Room rows** describe the combinations Booking matched to the party, not the property's whole inventory; a room can appear twice with different meal plans or cancellation policies.
- **A destination that names a property** ("Memmo Alfama Lisbon") prices just that property — the status row says `kind: hotel`.
- **Unknown ids** are reported as `not_found`, free. An unplaceable destination is an `error` row; the run continues with the other targets.

## FAQ

### Does it need a Booking.com API key or login?

No. It uses the same GraphQL call Booking's public search results page makes, anonymously, and only needs Apify's residential proxy group.

### Can I get Booking.com hotel prices for exact dates?

Yes — that is the whole point. `checkIn` plus `nights` sets the stay; `adults`, `childrenAges` and `rooms` set the party; `currency` sets the money. Every row carries those values.

### How is this different from a browser-based Booking.com scraper?

It never renders a page. A 100-property search is one request that takes about three seconds, so a market scan costs a few cents of platform time instead of minutes of browser time, and it does not break when Booking changes its page layout.

### Which sort orders are repeatable?

`price`, `price_desc`, `review_score`, `stars`, `stars_asc`, `distance` and their combinations are deterministic. `popularity` is Booking's personalised "top picks" and moves between pages.

### Can I filter by star rating or price before paying?

Yes. `minStars` is sent to Booking as its own filter, so those properties are never fetched; `maxPrice` drops rows above your nightly cap before they are billed.

### Does it return room-level rates?

With `includeRooms: true` you get one `room` row per room and rate combination, billed at $0.002 each. Without it you still get the cheapest room's name on the hotel row.

### What does `taxes_included: false` mean?

Booking lists charges it excludes from the displayed total (city tax, VAT, resort fees). `taxes_fees_excluded` holds their amount in your currency and `charges_note` Booking's wording.

### Why does the same hotel come back at a slightly different price on the next run?

Booking.com prices a stay per session. Two runs seconds apart can differ by a few per cent to a quarter — the site rotates promotional rates, mobile-only deals and currency handling per session, and `price_before_discount` is present on some answers and absent on others. That is the site's behaviour, not a parsing artefact, and every scraper of it sees the same thing.

Three ways to work with it rather than against it:

- Compare **the same field across runs** (`price_total` against `price_total`), never a nightly rate from one run with a stay total from another.
- Give a price-drop alert a threshold — three per cent filters the noise, and the n8n price-drop template ships with exactly that knob.
- For a decision that must be defensible (a rate-parity report, a revenue-management brief), take the **median of a few runs** rather than a single reading, or cross-check the stay against [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices), which reports what Google's own comparison shows for the same dates.

### Can I use it for hotel price comparison across sites?

Yes — pair it with the Google Hotels and rate-parity actors below, which return every booking site's rate for the same stay, and compare the `price_total` columns.

### How do I build a Booking.com price history?

Schedule a run with a relative `checkIn` and a deterministic `sortBy`; each day's rows share the same lead time and columns, so appending them to a sheet or a table is a price history.

### Can I scrape Booking.com without an API?

That is what this does: no Booking.com API, no key, no browser — a plain request through Apify's proxy. If you have been searching for a "Booking.com API" for prices, this is the practical answer: the same data the site shows, as rows.

### What does bulk work cost?

1,000 properties across ten destinations is 1,000 × $0.004 = $4.00, with compute and proxy included; ten requests of 100 rows each.

## Rate shopping and market data with Booking.com hotel data

### Comp-set monitoring

Put the ids of your property and its competitors in `hotelIds`, schedule the run at the same hour daily for a few lead times (7, 14, 30 days), and chart `price_nightly` by `hotel_id` and `check_in`. `free_cancellation` and `breakfast_included` tell you whether a lower rate is really comparable.

### Market scans

`locationQueries` with `sortBy: price` and a high `maxHotelsPerQuery` gives you the whole price ladder of a destination for a stay — the median rate, the share of properties under a budget, how many are sold out — in one request per hundred properties.

### What this does not do

It does not read reviews (that is the Booking.com Reviews Scraper below), it does not book, and it does not see member-only or logged-in Genius rates.

## Related scrapers

Prices are one side of a stay. These read the rest of it, and they share the same pay-per-delivered-row billing and the same scheduling story:

- **[Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper)** — every guest review of a Booking.com property, filtered by language and score before billing.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — every booking site's rate for a stay, one row per source.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — one row per property with every source side by side and the parity math done.
- **[Hotel Price Tracker](https://apify.com/kestrel/hotel-price-tracker)** — the lowest rate per property and check-in date over a window, for daily price history.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda guest reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
