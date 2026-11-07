# Airbnb Occupancy Rate Scraper — Availability & Sampled Rates

Measure Airbnb calendar availability per listing and month, with an optional sampled nightly quote. This **airbnb occupancy rate scraper** returns days available, days blocked or booked, `occupancy_pct`, minimum-stay information, the next available night and a quote for the first bookable stay found in each month. `occupancy_pct` is the share of calendar nights marked unavailable: it cannot identify confirmed bookings. `rate_nightly` is one stay quote divided by its nights, not monthly ADR or realized revenue. Supply a place, search URL or listing IDs to collect **short term rental data** from public calendars. No login, no API key, no browser.

This Airbnb calendar scraper supports vacation rental occupancy research from an Airbnb availability calendar. Its STR occupancy rate counts blocked-or-booked nights; it cannot separate confirmed bookings from host blocks.

Last verified working: 2026-08-29.

## Current price for API callers

The active price is **$0.003 per occupancy row per listing-month**, effective since **2026-10-27**: 1,000 delivered rows cost $3. Set `maxTotalChargeUsd` in Apify run options for a spending cap. Proxy and compute are included in this event price. This documentation correction changes no prices.

中文：当前每条已交付记录为 $0.003，自 2026-10-27 起生效。1,000 条记录费用为 $3，代理与计算费用已包含。请在 Apify 运行选项中设置费用上限。

## Airbnb 入住率估算、房源日历与市场数据：中文调用与语言设置

根据可订日历输出房源每月可订及不可订天数。不可订可能是已预订或房东关闭，不能据此认定真实成交入住率或收入。

locale 控制可用的房源名称语言，currency 控制抽样报价币种。includeRates 开启报价时才有对应价格；不要把日历估算当成已验证营收。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "locationQueries": [
    "Lisbon, Portugal"
  ],
  "maxListingsPerQuery": 1,
  "months": 1,
  "includeRates": false,
  "sessions": 1
}
```

Ocupación / Auslastung：日历不可订天数不是已验证订单。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## What does the airbnb occupancy rate scraper do?

For every listing it reads the availability calendar for the next `months` months (1–12) and turns each month into one **`occupancy`** row:

- **Availability** — `days_total` (the month's days from today onward; past days are never counted, so the current month is partial), `days_available`, `days_unavailable` and `occupancy_pct` = unavailable ÷ total × 100, to one decimal.
- **Bookability** — `checkin_days` (available days a stay may also start on), `nights_min` (the most common minimum stay across the month), `next_available` (the first free night, `null` when the month is full), `first_day` and `last_day`.
- **Rate** — with `includeRates` on (the default), the actor finds the first bookable stay of the month — check-in on the first available check-in day, the listing's minimum nights, capped at seven — and prices it for `adults` guests. The row carries `rate_check_in`, `rate_check_out`, `rate_nights`, `rate_total` and `rate_nightly` (total ÷ nights), plus `rate_status` so a missing number is explained (`no_stay`, `unavailable` when the page refuses the stay for that guest count, `unpriced`, `error`) rather than silently zero.
- **Who the listing is** — `id`, `url`, `name`, `title`, `room_type`, `location`, `lat`, `lng`, `rating`, `reviews_count`, and for search results `property_type`, `bedrooms`, `beds`, `bathrooms`, `is_superhost`, `is_guest_favorite` and the `query` that found it.

Two free row types travel with it: an optional **`listing`** row per listing (`includeListingRow`) for spreadsheets that want one line per property, and a **`status`** row per place, URL or id with counts (`listings`, `months`, `filtered`, `rates`, `duplicates`, `calendar_errors`, `rate_errors`, `detail_errors`) and the `resolved_place` Airbnb actually searched. Neither is ever charged.

## Airbnb occupancy scraper for AI agents: which input answers which request?

Use it when the user wants available versus unavailable nights and a sampled stay quote by month: for a place, search URL, portfolio or comp set. Scheduled runs can track changes in calendar availability and sampled quotes. They do not establish booking pace, booked occupancy, realized ADR or revenue. Do not use it for the price of a specific stay (`kestrel/airbnb-prices-calendar` prices your dates and guests), for a day-by-day calendar (that actor's `calendarMonths`), for reviews (`kestrel/airbnb-reviews-scraper`), for past months (the calendar only looks forward), or to tell booked from blocked nights: the public calendar does not, and `occupancy_pct` counts both.

| The user asks for | Input |
|---|---|
| Calendar unavailability for a city sample, next 6 months | `{"locationQueries": ["Lisbon, Portugal"], "months": 6, "maxListingsPerQuery": 100}` |
| Calendar availability by neighbourhood, bedrooms or room type | query the neighbourhood (`"Alfama, Lisbon"`); group the rows by `bedrooms` or `room_type` |
| Calendar availability and sampled quotes for these listings | `{"listingIds": ["17088279", "34832567"], "months": 3}` |
| Months with at least 80% unavailable nights, blocked or booked | add `"minOccupancyPct": 80` (months below the line are free) |
| Availability only, the cheapest run | add `"includeRates": false` |
| The rate for 4 guests, in euros | `"adults": 4, "currency": "EUR"` |
| Entire homes with 2+ bedrooms from a search the user built on the site | `{"startUrls": ["https://www.airbnb.com/s/Porto--Portugal/homes?room_types[]=Entire home/apt&min_bedrooms=2"], "months": 4}` |
| Calendar-availability history from repeated snapshots | an Apify schedule; compare `days_available` per listing and `month` across `fetched_at` |
| One line per property for a sheet | add `"includeListingRow": true` (free) |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `maxListingsPerQuery` × `months` bounds the rows |

The bill is one event per delivered `occupancy` row: listings × months (40 × 3 = 120 per place by default). `includeRates` is on by default and adds a request per row, not a charge; `minOccupancyPct` drops months before billing.

Rows come in three types. `occupancy`: `id`, `url`, `name`, `room_type`, `bedrooms`, `rating`, `reviews_count`, `lat`, `lng`, `month`, `days_total`, `days_available`, `days_unavailable`, `occupancy_pct`, `checkin_days`, `nights_min`, `next_available`, `rate_status`, `rate_check_in`, `rate_check_out`, `rate_nights`, `rate_total`, `rate_nightly`, `currency`, `fetched_at`. `listing`: optional and free. `status`: one per place, URL or id with `status` (`ok`, `unknown_area`, `no_results`, `error`), `resolved_place`, `listings`, `months`, `filtered`, `rates`, `error`; never charged. An unknown place or an empty search is a `status` row that says why, not a failed run; a month with no bookable stay keeps its availability figures with `rate_status: "no_stay"` and a null rate, never an invented number. For a city summary, `AVG(occupancy_pct)` by `month` describes calendar unavailability among the returned listings. It is neither confirmed booking occupancy nor a guarantee of representative market coverage.

## Airbnb occupancy data: what the calendar can and cannot tell you

The public calendar reports whether each night is available. An unavailable night may be booked by a guest or blocked by the host; this source does not distinguish those states. `occupancy_pct` is calculated as `days_unavailable / days_total * 100`. Treat it as a calendar-unavailability percentage, not verified booked occupancy. The share of host-blocked nights is unknown and may differ across listings, dates and markets. Aggregating more listings does not establish how closely this percentage tracks actual bookings.

Three things follow from that:

- **Future months are availability snapshots.** Repeated runs show how available and unavailable counts change. A change can reflect bookings, cancellations or host blocks; it does not identify booking pace.
- **The current month is partial** on purpose. `days_total` starts today; a row for the 29th of a month has two or three days in it and says so in `days_total` and `first_day`.
- **`nights_min` matters as much as `occupancy_pct`.** A listing that is 40 % available but only in one-night available gaps cannot necessarily accommodate a three-night minimum stay; `checkin_days` and `next_available` are there to make that visible.

## Sampled nightly quotes and the limits of Airbnb ADR comparisons

The actor requests a quote for the first bookable stay it finds in each month: an available check-in day, using the listing's minimum stay capped at seven nights, with every sampled night available. It prices that stay for the requested guest count. `rate_nightly` is the returned stay total divided by its nights. It is a sampled asking price, not ADR calculated from booked nights, not an average of all dates in the month, and not evidence of realized revenue. `rate_total`, `rate_check_in`, `rate_check_out` and `rate_nights` identify the sampled quote; a later run may sample different dates.

It is one extra request per listing and month. Turn `includeRates` off for an availability-only run at roughly half the requests; every row then carries `rate_status: "skipped"` and null rate fields, and the price per row is the same.

## Short term rental data: comps and calendar monitoring

A market run with `months: 6` and `maxListingsPerQuery: 100` can return up to 600 listing-month rows. Search coverage, filters and source failures can reduce that count, and a rate is null when no stay can be quoted. This is a bounded sample of **airbnb market data**:

- **Comps** — filter by `room_type`, `bedrooms` and `rating`, then compare `occupancy_pct` and `rate_nightly` for the listings that look like yours. **Airbnb comps** are a group-by, not a subscription tier.
- **Airbnb occupancy rate by city or neighbourhood** — average `occupancy_pct` by `month` to summarize calendar unavailability in the returned sample, including blocked nights. Neighbourhood queries (`"Alfama, Lisbon"`) resolve through the site; `resolved_place` identifies the search area, not statistical representativeness.
- **Airbnb revenue analysis limits** — multiplying `days_unavailable` by `rate_nightly` does not estimate verified revenue: unavailable nights include host blocks and the quoted rate is not a realized booking rate. Obtain independent booking and revenue records for that calculation.
- **Airbnb investment research** — put comparable listings in `listingIds` and save dated availability snapshots and quotes. Any investment model needs separate assumptions and evidence about bookings, achieved rates and costs.

The rows are per listing and timestamped. They can feed **short term rental analytics**, but they are not equivalent to a vendor's modeled STR occupancy or revenue estimates. Calendar history contains only the snapshots you collect; no past booking ledger is reconstructed.

## AirDNA alternative: evaluate the data contract

If considering this as an **airdna alternative**, compare the outputs your workflow requires. This Actor provides public calendar availability and sampled stay quotes. It does not supply verified bookings, modeled market occupancy, realized ADR or retrospective revenue estimates.

| Output | What this Actor supplies |
| --- | --- |
| Calendar | Available and unavailable night counts; unavailable combines blocked and booked |
| Rate | One stay quote per listing-month, with sampled dates and guest count |
| Coverage | The listings returned by the requested search or supplied IDs, within the configured limits |
| History | Snapshots saved from your own repeated runs |
| Access | Apify API, scheduler, webhooks, n8n, Make, Zapier and MCP |

The **airbnb availability api** and **airbnb calendar api** workflow is useful for a dashboard or spreadsheet that retains these distinctions. It does not replace independent booking records.

## Vacation rental calendar availability on a schedule

Schedule the run and the dataset becomes a time series. Because every row carries `fetched_at`, `month` and the listing `id`, you can compare how July's calendar unavailability for the same 40 listings changes over eight weeks. Two patterns work well:

- **Portfolio watch** — your listings and your competitive set in `listingIds`, `months: 3`, weekly. Alert when a competitor's `rate_nightly` drops under yours or when their `occupancy_pct` for next month passes yours.
- **Market calendar changes** — a place, `maxListingsPerQuery: 50`, `months: 4`, twice a week. Chart `AVG(occupancy_pct)` by `month` over `fetched_at`, and account for changes in which listings the search returned. The slope measures sampled calendar changes, not confirmed booking pace.

`minOccupancyPct` turns a scheduled run into a filter: `minOccupancyPct: 80` delivers only months at or above 80 % — months with at least 80% unavailable nights, whether blocked or booked — and, because the filter runs **before** billing, a run that finds no such month has no event charge; compute is included in the event price. Relative scheduling needs no dates at all: the actor always starts at the current month.

## Input

| Field | What it does |
| --- | --- |
| `locationQueries` | Places to search as you would type them on the site: `"Lisbon, Portugal"`, `"Brooklyn, NY"`. An unrecognised place produces a `status` row with `unknown_area` and costs nothing. |
| `startUrls` | Pasted search URLs (their filters are honoured: room type, price band, bedrooms, map bounds) or listing URLs. |
| `listingIds` | Numeric listing ids — your portfolio or a competitive set. No search needed. |
| `maxListingsPerQuery` | Distinct listings per place or search URL, up to about 280 (the site's cap for one search). The main cost control for a market run. |
| `months` | Calendar months to read per listing, 1–12, starting with the current month. One row per listing and month. |
| `includeRates` | Sample a nightly rate per month (one extra request per listing and month). Default on. |
| `adults` | Guests the sampled stay is priced for; prices depend on the guest count. Default 2. |
| `minOccupancyPct` | `0` = deliver every month. `N` = deliver only months with unavailable nights at or above N%; unavailable includes blocked and booked. Dropped months are not billed. |
| `includeListingRow` | Also emit one free `listing` row per listing. |
| `currency` | Currency for the sampled rates (`USD`, `EUR`, `GBP`, …), echoed on every row. |
| `locale` | Site locale for listing names (`en`, `fr`, `de`, `pt`, …). |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. The defaults work. |
| `proxyConfiguration` | Apify Proxy; datacenter proxies are accepted for these calls. |

### Example: calendar availability and sampled quotes, six months out

```json
{ "locationQueries": ["Lisbon, Portugal"], "maxListingsPerQuery": 100, "months": 6, "currency": "EUR" }
```

### Example: your listings and their competitors, weekly

```json
{ "listingIds": ["17088279", "34832567", "13055012"], "months": 3, "adults": 2, "includeListingRow": true }
```

### Example: neighbourhood months with at least 80% unavailable nights

```json
{ "locationQueries": ["Alfama, Lisbon"], "maxListingsPerQuery": 60, "months": 2, "minOccupancyPct": 80, "includeRates": false }
```

### Example: a pasted search with its own filters

```json
{ "startUrls": ["https://www.airbnb.com/s/Porto--Portugal/homes?room_types%5B%5D=Entire%20home%2Fapt&min_bedrooms=2"], "maxListingsPerQuery": 40, "months": 4 }
```

## Output

One `occupancy` row per listing and month:

```json
{
  "type": "occupancy", "id": "17088279", "url": "https://www.airbnb.com/rooms/17088279",
  "name": "Bairro Alto Refuge", "title": "Apartment in Lisbon", "property_type": "Apartment", "room_type": "Entire home/apt",
  "location": "Lisbon", "lat": 38.71209, "lng": -9.14346, "rating": 4.91, "reviews_count": 374,
  "bedrooms": 1, "beds": 1, "bathrooms": 1, "person_capacity": 4, "is_superhost": false, "is_guest_favorite": true, "query": "Lisbon, Portugal",
  "month": "2026-09", "days_in_month": 30, "days_total": 30, "days_available": 12, "days_unavailable": 18, "occupancy_pct": 60.0,
  "checkin_days": 9, "nights_min": 3, "next_available": "2026-09-08", "first_day": "2026-09-01", "last_day": "2026-09-30",
  "currency": "USD", "rate_status": "ok", "rate_check_in": "2026-09-08", "rate_check_out": "2026-09-11", "rate_nights": 3, "rate_total": 791, "rate_nightly": 263.67,
  "fetched_at": "2026-08-29T08:40:12+00:00"
}
```

A month with no bookable stay keeps its availability figures and explains the missing rate:

```json
{ "month": "2026-10", "days_total": 31, "days_available": 0, "days_unavailable": 31, "occupancy_pct": 100.0, "next_available": null, "rate_status": "no_stay", "rate_nightly": null }
```

And one `status` row per job:

```json
{
  "type": "status", "query": "Lisbon, Portugal", "url": null, "listing_id": null, "status": "ok",
  "resolved_place": "Lisbon, Portugal", "canonical_url": "/s/Lisbon--Portugal/homes", "pages": 1,
  "listings": 3, "months": 6, "filtered": 0, "rates": 5, "duplicates": 0, "calendar_errors": 0, "rate_errors": 0, "detail_errors": 0, "error": null,
  "fetched_at": "2026-08-29T08:40:20+00:00"
}
```

The dataset has four views in the Console — *Overview*, *Occupancy by month*, *Listings* and *Run status* — and exports to CSV, Excel or JSON.

## How much does it cost?

Pay per event, one event per **delivered** `occupancy` row — one per listing and month. Listing rows, status rows, months dropped by `minOccupancyPct`, unknown places and listings whose calendar failed are free, and nothing a spending limit refused is ever delivered.

Some worked sizes at the listed per-row price:

- One listing, 12 months: 12 rows × $0.003 = $0.036.
- A portfolio of 20 with 40 competitors, 3 months: 180 rows × $0.003 = $0.54 per run; four weekly runs cost $2.16 for 720 delivered rows.
- A market of 100 listings, 6 months: 600 rows × $0.003 = $1.80.
- A `minOccupancyPct: 80` run that finds nothing: 0 rows, $0 charged to the caller.

Each listing costs one calendar request plus, with rates on, one request per month. The verified runs behind this listing used $0.0002–$0.004 of platform compute each. Exact per-row pricing is on this page's pricing tab.

## How to use it from Python, JavaScript, curl, n8n, Make or an AI agent

Run it and read the dataset. In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/airbnb-occupancy-scraper").call(run_input={
    "locationQueries": ["Lisbon, Portugal"], "maxListingsPerQuery": 50, "months": 3, "currency": "EUR",
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "occupancy"]
by_month = {}
for r in rows:
    by_month.setdefault(r["month"], []).append(r["occupancy_pct"])
for month, pcts in sorted(by_month.items()):
    print(month, round(sum(pcts) / len(pcts), 1), "% occupied across", len(pcts), "listings")
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/airbnb-occupancy-scraper').call({
    listingIds: ['17088279', '34832567'], months: 3, includeListingRow: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const r of items.filter((i) => i.type === 'occupancy')) console.log(r.name, r.month, r.occupancy_pct, r.rate_nightly, r.currency);
```

With **curl**, synchronously, getting the dataset straight back:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~airbnb-occupancy-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"listingIds":["17088279"],"months":2,"currency":"USD"}'
```

For **n8n** and **Make** (and Zapier), a portfolio watch is three steps: a Schedule trigger, an HTTP Request to the `run-sync-get-dataset-items` URL above with the JSON body, and a Google Sheets append (or a Slack message when any row's `occupancy_pct` or `rate_nightly` crosses a line you set). With `minOccupancyPct` set, inspect the `status` rows to distinguish no qualifying unavailable-night percentages from source failures; free status rows may remain in the dataset.

For **AI agents**, the actor is callable over Apify's MCP server, so an agent asked for availability counts and sampled quotes for two-bedroom listings in Alfama can run it and explain that unavailable nights combine blocked and booked dates; the section "Airbnb occupancy scraper for AI agents" above maps each request to its input.

## Is it legal to scrape Airbnb occupancy and availability?

This reads the same public calendar and listing page a logged-out visitor sees, with no login and no account. The rows describe properties, not people: availability, a price and the listing's public attributes. Host names, contact details and guest identities are not collected. Reading public pages that carry no personal data is broadly accepted in the EU and the US (*hiQ v. LinkedIn* is the usual reference for public data), and the actor runs under limited permissions.

That is not the whole story: the site's terms discourage automated access, so this is a terms question rather than a criminal one, and the responsibility for a run sits with whoever runs it. Facts are not copyrightable, but a compiled database can attract *sui generis* protection in the EU — do not resell the raw dataset as a product. If you are unsure how this applies to your use, ask a lawyer; this is not legal advice.

## Limits and honest notes

- **Calendar unavailability is not booked occupancy.** `occupancy_pct` counts both host-blocked and guest-booked nights as unavailable. This source cannot determine their proportions or establish accuracy against actual bookings.
- **The rate is a sampled quote, not realized or monthly ADR.** One stay per month — the first bookable one at the listing's minimum length, capped at seven nights, for `adults` guests. A month with weekend premiums or a stay priced mid-month can differ; run `adults` and `months` to match the stay you care about.
- **A search returns the site's ranking up to its cap** (about 280 listings). Cover a city with neighbourhood queries or a pasted URL with map bounds.
- **A calendar covers twelve months** from the current month; `months` is capped there.
- **Delisted or snoozed listings** return a status row with an error and no charge.
- **The query hashes the site uses change occasionally.** The actor refreshes them from the site's bundles, a daily canary run watches it, and failures appear as `status` rows rather than silent zeros.

## FAQ

### Does it need an Airbnb API key, login or cookies?

No. There is no public **airbnb availability api** for guests, no key to request and no login involved. The actor uses the public key every visitor's browser uses and no session at all.

### Is occupancy the same as bookings?

No — see the section above. The calendar shows availability; a night can be unavailable because a guest booked it or because the host blocked it. `occupancy_pct` counts both. The difference from actual booked occupancy is unknown for both individual listings and markets. Do not treat unavailable nights as revenue.

### How do I get the airbnb occupancy rate by city?

Put the city in `locationQueries`, choose `months` and a bounded `maxListingsPerQuery`, then average `occupancy_pct` by `month` over the returned rows. This summarizes calendar unavailability for the sample; increasing the cap does not guarantee representativeness or reveal actual bookings. For a neighbourhood, query it by name; the `status` row's `resolved_place` confirms what the site searched.

### Where does the nightly rate come from if the calendar has no prices?

From the listing page, priced for a real stay: the first bookable check-in of the month with the listing's minimum nights, for the `adults` you set. `rate_check_in`, `rate_check_out` and `rate_nights` are on the row so you can reproduce the quote; `rate_status` explains any missing number.

### Can I track airbnb booked dates over time?

Not the dates of individual bookings — the calendar only says whether a night is free. What you can track is the *change*: schedule the run and compare `days_available` for the same listing and month across `fetched_at`. Nights that became unavailable may be newly booked or newly blocked; the change does not identify confirmed bookings.

### Can I get airbnb nightly rate history?

Not retroactively — the site does not publish it. You can build it: a scheduled run appends a dated `rate_nightly` per listing and month every time it runs.

### How is this different from the Airbnb Scraper?

The [Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar) prices a specific stay for every listing and can attach a full day-by-day calendar and reviews; it bills per listing, per calendar month and per review. This one skips the stay price, reads the calendar for everyone, folds each month into one occupancy row with a rate sample, and bills only those rows — the cheaper shape for market and portfolio occupancy work. Use both when you want the stay price and the occupancy together.

### Which currencies and languages?

Any ISO currency for the rate sample and any site locale for names. `currency` is echoed on every row so a mixed export never guesses.

### Is there a free tier?

Listing rows, status rows, filtered months, unknown places and failed calendars are always free, and Apify's free plan includes monthly platform credit you can spend on the paid rows.

## Related scrapers

From the same publisher, with the same pay-per-delivered-row billing:

- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — prices for exact dates and guests, day-by-day calendars, listing details and reviews.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of a listing, with a rating filter that bills only the rows you keep.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site's rate for a stay, for the hotel side of the same market.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — one row per hotel with every source side by side.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — hotel reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
