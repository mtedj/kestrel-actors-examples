# Airbnb Scraper — Prices, Availability Calendar & Listings

An Airbnb scraper for Airbnb prices and availability: search any place or paste Airbnb URLs and get every listing's nightly rate and total for your dates and guests in any currency, its rating, location and badges — then, per listing, up to 24 months of availability calendar with occupancy data, the full listing details with the exact price breakdown, and reviews. Scrape Airbnb data as rows you own — the short term rental data behind market analysis, an Airbnb price tracker, or a rate check on your own listings — without an Airbnb API key, a login or cookies: it reads the same public endpoints the airbnb.com front-end uses. You pay per row you receive; a place Airbnb does not recognise, an empty search and every status row cost nothing.

## Airbnb 房源、价格与可订日历：中文调用与语言设置

按地点、房源 URL 或 ID 获取房价与房源资料。calendarMonths 会增加日历输出；只查询入住报价时设为 0，maxReviewsPerListing 设为 0。

locale 控制来源提供的文本语言，currency 控制币种。示例 locale="fr"。不同市场、日期和人数必须保持一致后再比较；中文说明不表示所有房源原文都是中文。

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
  "checkIn": "30 days",
  "checkOut": "33 days",
  "adults": 2,
  "currency": "EUR",
  "maxListingsPerQuery": 1,
  "calendarMonths": 0,
  "maxReviewsPerListing": 0,
  "locale": "fr",
  "includeDetails": false,
  "sessions": 1
}
```

Precios Airbnb / prix Airbnb / Airbnb Preise：价格按日期、入住人数和币种查询。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## What does this Airbnb scraper do?

A listing has a price only for a stay — dates and guests — and many scrapers quietly return a default figure, or listings from anywhere in the world when the place name is not understood. This one prices exactly the stay you ask for and tells you when it could not:

- **`listing` rows** — for a place search, a pasted search URL or listing ids: total for the stay, base nightly rate and effective per-night price, discounts, rating and review count, bedrooms/beds/baths, coordinates, Guest favorite / Superhost badges, free cancellation, pictures. Searches page through the results up to the site's cap (about 280 per search).
- **`calendar` rows** — one per listing: day-by-day availability for the next 1–24 months (`available`, `available_for_checkin`, `min_nights`…) plus an occupancy summary for the next 30/90/365 nights, the next available date and the typical minimum stay.
- **Listing details** on request: description, amenities, house rules, cancellation policy, category ratings, host, capacity, sleeping arrangement, and the exact price breakdown for the dates — including "not available for these dates" when that is the answer.
- **`review` rows** — newest, highest, lowest or most relevant first, with reviewer, date, text and host reply.
- **`status` rows** — one per place, URL or listing: what Airbnb searched (`resolved_place`), how many rows were priced and charged, `unknown_area`, `no_results` or an error. Never charged.

## Airbnb scraper for AI agents: which input answers which request?

Use it when the user wants Airbnb listings with the price for given dates and guests — a city or area, a pasted search URL, or specific listing ids — once or on a schedule; and, per listing, the availability calendar with occupancy, the details (amenities, house rules, host) or a few reviews. Do not use it for occupancy by month across a market (`kestrel/airbnb-occupancy-scraper` bills one small row per listing and month), for every review of a listing or a rating filter (`kestrel/airbnb-reviews-scraper`), for host contact details (not collected), for hotels on booking sites (`kestrel/google-hotels-prices`), or for more than about 280 listings from one search (the site's cap: split the area).

| The user asks for | Input |
|---|---|
| Prices in a city for dates | `{"locationQueries": ["Lisbon, Portugal"], "checkIn": "2026-11-07", "checkOut": "2026-11-10", "adults": 2}` |
| Entire homes under 200 a night with 2 bedrooms | add `"roomTypes": ["entire_home"], "priceMax": 200, "minBedrooms": 2, "currency": "EUR"` |
| Amenities, house rules, host, cancellation policy, price breakdown | add `"includeDetails": true` (no extra charge) |
| Availability calendar, occupancy, when is it free | add `"calendarMonths": 12` (one event per month per listing) |
| Prices and the latest reviews together | add `"maxReviewsPerListing": 20, "reviewsSort": "most_recent"` |
| These exact listings (portfolio, comp set) | `{"listingIds": ["11562247", "45307024"], "checkIn": "30 days", "checkOut": "33 days"}` — details come free |
| The listings from a search the user built on the site | `{"startUrls": ["https://www.airbnb.com/s/Paris--France/homes?checkin=2026-11-10&checkout=2026-11-14&price_max=200"]}` |
| Track prices weekly without editing the input | `"checkIn": "30 days", "checkOut": "33 days"` and an Apify schedule |
| Listing data without dates (default displayed price) | leave `checkIn` and `checkOut` empty; every listing row is billed |
| Prices in the destination's currency, names in French | `"currency": "EUR", "locale": "fr"` |
| A family with a baby and a dog | `"adults": 2, "children": 1, "infants": 1, "pets": 1` |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `maxListingsPerQuery`, `calendarMonths` and `maxReviewsPerListing` bound the rows |
| The 40 cheapest listings | not a sort: `"priceMax": 80` (nightly, in `currency`), or raise `maxListingsPerQuery` and sort `price_total` at your end — Airbnb returns listings in its own relevance order |
| Superhost only, rating 4.8 or better | no input filter: keep rows with `is_superhost` true and `rating` ≥ 4.8 at your end (every listing row carries both) |
| Friday-to-Sunday every week, no edits | `"checkIn": "28 days", "checkOut": "30 days"` on a weekly Friday schedule — relative dates count from the run day |
| A nightly price for every day of the next 90 days | not available: `calendarMonths` gives availability only (Airbnb's calendar carries no prices); price one-night stays with `listingIds` and dates instead |

Where the bill is decided: `maxListingsPerQuery` (default 40) listing events per place search; `calendarMonths` and `maxReviewsPerListing` default to 0, so nothing beyond listing rows is billed unless asked; `includeDetails` is free. A listing the site cannot price for the dates is delivered with `price_total: null` and is not billed; without dates every listing row is billed at its displayed price.

Rows come in four types. `listing`: `id`, `url`, `name`, `title`, `price_total`, `price_nightly`, `price_nightly_effective`, `price_original`, `price_nights`, `price_breakdown`, `currency`, `rating`, `reviews_count`, `bedrooms`, `beds`, `bathrooms`, `lat`, `lng`, `is_superhost`, `is_guest_favorite`, `free_cancellation`, `pictures`, and with `includeDetails` (or from `listingIds`) also `description`, `amenities`, `house_rules`, `cancellation_policy`, `rating_breakdown`, `host`, `person_capacity`, `sleeping`, `available`, `unavailable_message`. `calendar`: `months`, `days` (one entry per day with `available`, `available_for_checkin`, `available_for_checkout`, `min_nights`, `max_nights`), `occupancy_30`, `occupancy_90`, `occupancy_365`, `next_available`, `min_nights_typical`. `review`: `review_id`, `rating`, `text`, `text_localized`, `language`, `created_at`, `reviewer_name`, `reviewer_location`, `host_reply`, `stay_type`. `status`: one per place, URL or listing id with `status` (`ok`, `unknown_area`, `no_results`, `error`), `resolved_place`, `listings`, `priced`, `calendars`, `reviews`, `error`; never charged. An unknown place or an empty search is a `status` row that says why, not a failed run. Blocked and booked nights look the same in the calendar: `occupancy_*` counts both. The actor returns rows, not conclusions: "cheapest entire homes rated over 4.8" is a filter on `price_nightly_effective` and `rating`.

## Airbnb prices for exact dates — nightly rate, total and discounts

Every listing row carries `price_total` (what Airbnb displays for the stay after discounts), `price_original` (before discounts), `price_nightly` (the base nightly rate from the site's own breakdown) and `price_nightly_effective` (total ÷ nights), in the `currency` you chose, with `price_breakdown` lines such as "3 nights x $171.73", "Early booking discount −$89.73" and "Taxes". Airbnb prices include all fees it shows a logged-out guest for that market; the breakdown tells you which. Without dates you get each listing's default displayed price and `price_nights` as Airbnb chose it. Prices depend on guests exactly as on the site, so set `adults`, `children`, `infants` and `pets`. An Airbnb nightly rate estimate for a market is one search — an Airbnb price calculator without the guesswork: the median `price_nightly_effective` of the rows.

## Airbnb availability calendar and Airbnb occupancy data

`calendarMonths: 12` adds a calendar row per listing: 365 days with availability flags and minimum/maximum nights, and `occupancy_30`, `occupancy_90`, `occupancy_365` (share of nights not available — blocked or booked, the calendar does not tell which), `available_90`, `next_available`, `min_nights_typical`. This is the Airbnb availability API people search for and the company does not offer: an Airbnb calendar API you call with listing ids. Run it on a schedule and save each run's dataset externally to build an availability and price history for a market or a portfolio: the short term rental data API investors and revenue managers otherwise buy as AirDNA-style subscriptions, at a few cents per listing. Airbnb occupancy rate by city, by neighbourhood or by bedroom count is a group-by on the calendar rows.

## Does Airbnb have an API? Airbnb API vs Airbnb scraper vs AirDNA alternative

Airbnb's only API is a closed partner program for property-management systems (listings, bookings, messages) — there is no Airbnb API for prices, availability or occupancy, no API key to request, and "Airbnb API access" for analytics does not exist. What developers actually use is one of two things:

| | Airbnb data vendors (AirDNA, AirROI, Airbtics, Mashvisor, Rabbu) | This Airbnb scraper |
|---|---|---|
| Data | Aggregated, modelled estimates by market; monthly or weekly refresh | Raw rows per listing, dates and guests, fetched when you run it |
| Coverage | Their markets and their listing sample | Any place Airbnb serves, any listing id, any currency and locale |
| Price | Subscription per market or plan | Cents per row; empty searches free |
| Occupancy | Modelled from calendars and reviews | Availability per night from the listing's calendar, with the caveat that blocked nights look booked |
| History | Theirs | Yours: every run appends dated rows |
| Access | Dashboard or paid API | Apify API, scheduler, webhooks, n8n/Make/Zapier, MCP for AI agents |

So as an AirDNA alternative it is not a dashboard: it is the Airbnb data API layer you build a dashboard, a model or a spreadsheet on, free of a per-market subscription. If you searched for "Airbnb scraper Python", "Airbnb scraper free" or "Airbnb scraper Apify": the Python and JavaScript calls below are complete, Apify's free plan covers small runs, and the maintenance — the site rotates its query hashes and formats — is done for you, with a daily canary run and status rows instead of silent zeros.

## Airbnb price tracker and Airbnb price history

Schedule the actor with relative dates (`"checkIn": "30 days"`) and every run prices a stay at the same lead time. Save each run's dataset externally to build an Airbnb price history per listing — `price_total` and `price_nightly_effective` by `fetched_at` — and, with `calendarMonths`, an availability history. Connect a run-finished webhook to n8n, Make or Zapier for an Airbnb price tracker that alerts on drops in a shortlist, on a competitor undercutting you, or on new availability. For a portfolio, put your listing ids in `listingIds` and your competitive set in a second run; each listing is delivered and billed at most once per run, even across overlapping stays or guest counts.

## Airbnb market data: comps, revenue and occupancy for investors

To scrape Airbnb listings for a market — a city, a neighbourhood, a coastline — combine a place search with `calendarMonths`: the listing rows give the price distribution for the dates (use `price_nightly_effective` for like-for-like nightly figures), the calendar rows give occupancy for the next 30, 90 and 365 nights per listing, and `rating`, `reviews_count`, `bedrooms`, `room_type` and coordinates let you segment. Airbnb comps for an underwriting: search the neighbourhood with the same bedrooms and room type, take the median `price_nightly_effective` and `occupancy_90`. A displayed-price × unavailable-nights calculation is a scenario, not observed revenue: blocked nights and sampled stay prices cannot establish bookings or realized earnings. A search is capped at about 280 listings, so cover a large market with price bands or map bounds in pasted URLs; the status rows tell you how many pages each search returned and which place was resolved.

## Airbnb reviews scraper

`maxReviewsPerListing` adds review rows per listing (a reviews scraper without a separate run) — newest first by default, or highest, lowest or most relevant — with the rating, text (and the site's translation when it exists), date, reviewer first name and location, the host's reply and the stay-type tag. `reviews_total` carries the listing's total review count so you know how much you sampled. To scrape Airbnb reviews for one property, give its id in `listingIds` with `maxReviewsPerListing: 200`.

### Search URL context and overlapping searches

A search URL keeps its embedded stay and guest filters. Explicit `checkIn` and `checkOut` inputs override its dates. URL guest values remain authoritative for that search; when absent, its existing URL-parser defaults apply (2 adults, no children, infants or pets). Listing and status dates and optional detail-price requests now use that same effective search context.

A listing is delivered and billed at most once per run, including its calendar/review add-ons, even when overlapping searches request different stays or parties. The first processed occurrence wins; concurrent searches need not finish in input order. Use separate runs to compare the same listing across distinct stays or guest counts, and inspect the emitted stay/guest fields.

### Join a stay quote to an availability calendar

This call asks for five Lisbon listings for one three-night stay, with amenities and two calendar months of availability. It costs at most $0.045 for five priced listings ($0.025) plus ten calendar-month events ($0.020), before the $0.05 run cap. It asks for no reviews.

```json
{
  "actor": "kestrel/airbnb-prices-calendar",
  "input": {
    "locationQueries": ["Lisbon, Portugal"],
    "checkIn": "2026-12-10",
    "checkOut": "2026-12-13",
    "adults": 2,
    "currency": "EUR",
    "maxListingsPerQuery": 5,
    "includeDetails": true,
    "calendarMonths": 2,
    "maxReviewsPerListing": 0
  },
  "callOptions": {"maxTotalChargeUsd": 0.05, "timeout": 180},
  "waitSecs": 30
}
```

This is a `call-actor` envelope; only `input` belongs in the Actor input editor. If it is still running, poll `get-actor-run`, then fetch the default dataset with `get-dataset-items`. Group rows by `type`. Join each `calendar` row to its `listing` row using `id`; a two-month calendar is one dataset row containing `days[]`, but two billing events. Five complete results can therefore be five listing rows, five calendar rows and one free status row. A missing calendar is not zero availability: check `calendar_errors`, returned `months`, and `SUMMARY.limit_hit`.

`listing.price_total` and `price_nightly_effective` describe the quoted stay. Calendar months start in the current month, independently of `checkIn`; daily calendar entries supply availability/stay rules, not nightly prices. Do not spread the stay price across all calendar dates or equate unavailable days with confirmed bookings. `occupancy_*` uses the returned days in its named window; check `nights_30`, `nights_90` or `nights_365` before comparing differently sized calendar samples.

To monitor this same December stay, keep its absolute dates and save each run's dataset with `fetched_at`. Relative dates such as `30 days` / `33 days` produce a moving three-night stay, not the same check-in dates. Availability-based revenue calculations are scenarios, not observed earnings.

## Input

| Field | Meaning |
|---|---|
| `locationQueries` | Places as you would type them on the site: `"Lisbon, Portugal"`, `"Algarve"`, `"Brooklyn, NY"`. Unknown places produce an `unknown_area` status row and cost nothing. |
| `startUrls` | Search URLs (dates, guests, price, room type, bedrooms and map bounds in the URL are honoured) or listing URLs. |
| `listingIds` | Listing ids to price, calendar, detail or review directly. |
| `checkIn`, `checkOut` | `YYYY-MM-DD` or relative to the run date (`"30 days"`, `"6 weeks"`) for schedules. Leave both empty for default prices. |
| `adults`, `children`, `infants`, `pets` | Guests; prices depend on them. |
| `currency`, `locale` | Any ISO currency; site locale for names, descriptions and reviews. |
| `priceMin`, `priceMax`, `roomTypes`, `minBedrooms`, `minBeds`, `minBathrooms` | Search filters (prices per night in `currency`; 0 = no limit). |
| `maxListingsPerQuery` | Distinct listings per place or search URL, up to about 280 (the site's cap; split big areas into neighbourhoods or price bands for more). |
| `includeDetails` | Fetch each listing's page (details + exact breakdown; one extra call per listing). |
| `calendarMonths` | 0–24 months of availability per listing. |
| `maxReviewsPerListing`, `reviewsSort` | Reviews per listing and their order. |
| `proxyConfiguration`, `sessions`, `perIp` | Apify datacenter proxies work; defaults are fine. |

### Example: Airbnb prices for a weekend in Lisbon

```json
{ "locationQueries": ["Lisbon, Portugal"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "adults": 2, "currency": "EUR", "maxListingsPerQuery": 80 }
```

### Example: occupancy and prices for a market, weekly, always 30 days out

```json
{ "locationQueries": ["Algarve, Portugal"], "checkIn": "30 days", "checkOut": "33 days", "adults": 2, "currency": "EUR", "maxListingsPerQuery": 200, "calendarMonths": 6 }
```

### Example: your own listings and competitors — details, 12-month calendar, latest reviews

```json
{ "listingIds": ["11562247", "45307024"], "checkIn": "30 days", "checkOut": "33 days", "includeDetails": true, "calendarMonths": 12, "maxReviewsPerListing": 20, "reviewsSort": "most_recent" }
```

### Example: a pasted search with its own filters

```json
{ "startUrls": ["https://www.airbnb.com/s/Paris--France/homes?checkin=2026-11-10&checkout=2026-11-14&adults=2&price_max=200&room_types%5B%5D=Entire%20home%2Fapt&min_bedrooms=2"], "currency": "USD" }
```

## Output

`listing` row (search; with `includeDetails` the same row also carries `description`, `amenities`, `house_rules`, `cancellation_policy`, `rating_breakdown`, `host`, `person_capacity`, `available`):

```json
{ "type": "listing", "id": "1018680572065141154", "url": "https://www.airbnb.com/rooms/1018680572065141154", "name": "Lisboa Bica Nature Fast Net AC Heating", "title": "Apartment in Lisbon",
  "query": "Lisbon, Portugal", "check_in": "2026-10-03", "check_out": "2026-10-06", "nights": 3, "adults": 2, "children": 0, "infants": 0, "pets": 0, "currency": "USD",
  "price_total": 426.0, "price_total_display": "$426", "price_original": 516.0, "price_nightly": 171.73, "price_nightly_effective": 142.0, "price_nights": 3,
  "price_breakdown": [{ "label": "3 nights x $171.73", "amount": 515.19 }, { "label": "Early booking discount", "amount": -89.73 }, { "label": "Price after discount", "amount": 425.46 }],
  "rating": 4.88, "reviews_count": 156, "bedrooms": 1, "beds": 1, "bathrooms": null, "lat": 38.70975, "lng": -9.14708, "badges": ["Guest favorite"], "is_guest_favorite": true, "is_superhost": false, "free_cancellation": false,
  "pictures": ["https://a0.muscache.com/im/pictures/…"], "details": false, "fetched_at": "2026-08-26T09:10:00+00:00" }
```

`calendar` row:

```json
{ "type": "calendar", "id": "11562247", "name": "Charming studio in Baixa", "months": 12, "first_day": "2026-08-01", "last_day": "2027-07-31",
  "nights_30": 30, "available_30": 6, "occupancy_30": 0.8, "nights_90": 90, "available_90": 47, "occupancy_90": 0.478, "nights_365": 340, "available_365": 137, "occupancy_365": 0.597,
  "next_available": "2026-08-29", "min_nights_typical": 3, "days": [{ "date": "2026-08-29", "available": true, "available_for_checkin": true, "available_for_checkout": true, "min_nights": 3, "max_nights": 1125, "bookable": null, "price": null }], "fetched_at": "…" }
```

`review` row: `{ "type": "review", "id": "11562247", "review_id": "1740402488245156304", "rating": 5, "text": "…", "created_at": "2026-07-29T07:09:04Z", "reviewer_name": "Sarah Sofia", "reviewer_location": "…", "host_reply": null, "language": "en", "reviews_total": 441 }`

`status` row (per place, URL or `listing_id`): `{ "type": "status", "query": "Lisbon, Portugal", "listing_id": null, "status": "ok", "resolved_place": "Lisbon, Portugal", "canonical_url": "/s/Lisbon--Portugal/homes", "pages": 2, "listings": 80, "priced": 80, "duplicates": 0, "calendars": 80, "calendar_months": 480, "reviews": 0, "error": null }`

The Console's **Listings**, **Calendar**, **Reviews** and **Run status** tabs show the same rows as tables; every run's dataset downloads as JSON, CSV or Excel — an Airbnb dataset CSV for exactly the market, dates and listings you chose, instead of a stale Kaggle file.

## How much does it cost?

Pay per row: a `listing` row that carries a price, each `calendar_month` (a 12-month calendar row = 12 events), each `review` row. Listings that could not be priced, unknown places, empty searches and `status` rows are free, and each listing is delivered and billed at most once per run even across overlapping stays or guest counts. Worked examples: 80 Lisbon listings with prices for a weekend = 80 listing events; the same 80 with a 6-month calendar = 80 + 480 calendar-month events; your 10 listings with details, 12-month calendars and 20 reviews each = 10 + 120 + 200 events. Platform compute for those runs is a fraction of a cent. Exact per-event prices are on this page's pricing tab.

## Airbnb scraper in Python, JavaScript, curl, n8n, Make or an AI agent

"Airbnb API python" in practice means calling this actor: one POST with a place or listing ids and a stay, a dataset of typed rows back. The same call from JavaScript, curl or an HTTP node is an Airbnb calendar API when `calendarMonths` is set. The examples are complete; the row schemas are documented above and in the Output tab, so an agent or a script can filter on `price_nightly_effective`, `occupancy_90` or `available` without parsing HTML.

```python
from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/airbnb-prices-calendar").call(run_input={"locationQueries": ["Lisbon, Portugal"], "checkIn": "30 days", "checkOut": "33 days", "adults": 2, "currency": "EUR", "maxListingsPerQuery": 80, "calendarMonths": 3})
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
listings = [r for r in rows if r["type"] == "listing"]; cal = {r["id"]: r for r in rows if r["type"] == "calendar"}
for l in sorted(listings, key=lambda r: r["price_nightly_effective"] or 0)[:10]: print(l["name"], l["price_nightly_effective"], "occupancy 90d", cal.get(l["id"], {}).get("occupancy_90"))
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/airbnb-prices-calendar').call({ listingIds: ['11562247'], checkIn: '30 days', checkOut: '33 days', includeDetails: true, calendarMonths: 12 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter(r => r.type === 'calendar').map(r => [r.id, r.occupancy_90, r.next_available]));
```

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~airbnb-prices-calendar/run-sync-get-dataset-items?token=<TOKEN>" -H "Content-Type: application/json" \
  -d '{"locationQueries": ["Lisbon, Portugal"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "maxListingsPerQuery": 20}'
```

- **n8n, Make, Zapier**: run on a schedule, read the dataset, alert on price drops or occupancy changes.
- **AI agents and MCP**: available through the Apify MCP server and Apify AI; the section "Airbnb scraper for AI agents" above maps each request to its input, and rows are flat and typed so "cheapest entire homes in Lisbon for these dates with a rating over 4.8" is a filter.
- **Google Sheets, BigQuery**: export the dataset from the run or through Apify integrations.

## Is it legal to scrape Airbnb prices?

The rows are public listing data as any logged-out visitor sees it: prices, availability, ratings, amenities, and reviews as published. No login, no personal data beyond what is shown publicly (reviewer first names, host first name); it does not scrape Airbnb host emails or phone numbers. Terms of service and local law vary — check that your use complies, and use the data for your own analysis.

## Limits and honest notes

- A search returns the site's ranking up to its cap (about 280 listings); cover a city with neighbourhood queries, price bands (`priceMin`/`priceMax`) or map bounds in a pasted URL.
- `occupancy_*` counts nights that are not available; blocked nights and booked nights look the same in the calendar.
- Prices are what a logged-out visitor sees in `currency` for the stay and guests given; some markets show all-in prices, others add fees at checkout — the breakdown says which.
- The query hashes change occasionally; the actor refreshes them automatically from the site's bundles, a daily canary run watches it, and failures appear as `status` rows rather than silent zeros.

## FAQ

### Does it need an Airbnb API key, login or cookies?

No. It uses the public key every visitor's browser uses and no session; there is no API key for guests to request.

### Is there a free Airbnb scraper here?

Apify's free plan covers small runs, and the actor never charges for unknown places, unpriced listings or empty searches. The Python and JavaScript examples above are complete.

### Why does a place come back as `unknown_area`?

An unrecognised place is answered with listings from all over the world; the actor detects that (empty canonical URL, listings thousands of km apart), returns a status row and charges nothing. Use the spelling the site suggests, e.g. `"Lisbon, Portugal"`.

### Can I get more than 280 listings for a city?

Yes — run several searches: neighbourhoods, price bands, room types, or pasted search URLs with map bounds. Each listing is billed once per run.

### Is occupancy the same as bookings?

No. It is the share of nights not available; hosts also block nights. Over a market it tracks demand well; for one listing treat it as an upper bound.

### Can I track Airbnb prices and availability over time?

Yes. Schedule the actor and save each run's dated rows (`fetched_at`) externally; each run has a separate dataset. Relative dates observe a moving stay at the same lead time; fixed dates observe the same stay. Calendar summaries report unavailability, including both blocked and booked nights.

### Can I scrape Airbnb host emails or phone numbers?

No, by design: the rows carry the host's public first name, Superhost and verification flags and stats, nothing off-platform.

### Can I download an Airbnb dataset as CSV?

Every run's dataset downloads as JSON, CSV or Excel from the run page or the API — an Airbnb dataset for the market, dates and listings you chose, with calendar days as nested arrays (CSV flattens them per day).

### Can I get Airbnb listing data without dates?

Yes: leave `checkIn`/`checkOut` empty and each listing row carries the default displayed price and `price_nights`; add `includeDetails` for description, amenities and host.

### Which languages and currencies?

Any site locale for text (`locale`) and any ISO currency for prices (`currency`); both are echoed in every row.

Last verified working: 2026-10-05.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Availability Calendar for a Market](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-availability-calendar-data)
- [Comps: Nightly Rate by Bedrooms](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-comps-nightly-rates)
- [Short-Term Rental Data: AirDNA Alternative](https://apify.com/kestrel/airbnb-prices-calendar/examples/short-term-rental-data-airdna-alternative)
- [Occupancy Data by Listing ID](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-occupancy-data-by-listing-id)
- [Nightly Rate by Listing ID](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-nightly-rate-by-listing-id)
- [Listing Data: Amenities and Rules](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-listing-data-amenities-and-rules)
- [Scrape Reviews and Prices Together](https://apify.com/kestrel/airbnb-prices-calendar/examples/scrape-airbnb-reviews-and-prices-together)
- [Price Tracker from a Search URL](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-price-tracker-from-a-search-url)
- [Scrape Listings Over $500 a Night](https://apify.com/kestrel/airbnb-prices-calendar/examples/scrape-airbnb-listings-over-500-a-night)
- [Market Data for Private Rooms](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-market-data-for-private-rooms)
- [Data for 3-Bedroom Family Homes](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-data-for-3-bedroom-family-homes)
- [API Alternative: One Call, JSON Out](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-api-alternative-one-call-json-out)
- [Data API: 28-Night Monthly Rates](https://apify.com/kestrel/airbnb-prices-calendar/examples/airbnb-data-api-28-night-monthly-rates)

## Related scrapers

Prices and availability are one half of a listing's story; reviews are the other. These share the same row shape and billing model:

- **[Airbnb Occupancy Rate Scraper](https://apify.com/kestrel/airbnb-occupancy-scraper)** — one row per listing and month from the same calendar: days free vs blocked or booked, occupancy %, minimum stay and a sampled nightly rate, billed per month instead of per calendar.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site’s rate for a stay.
- **[Google Flights Scraper](https://apify.com/kestrel/google-flights-prices)** — airfare for a route and date, with a cheapest-day sweep.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing, with translations.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
