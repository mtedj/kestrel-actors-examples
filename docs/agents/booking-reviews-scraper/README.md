# Booking.com Reviews Scraper — Hotel Reviews, Guest Reviews

A **booking.com reviews scraper** — a **hotel review scraper** for **booking.com hotel reviews** — that returns every guest review a property has, as structured rows: **booking.com ratings** on the 1–10 scale and out of five, the title, what the guest liked and what they disliked, the language it was written in, posting and stay dates, room, traveller type, reviewer name and country, guest photos and the property's public reply.

Give it Booking.com hotel URLs, hotel names or Booking's numeric ids. No login, no **booking.com api** key, no browser. It never loads a Booking.com page — it calls the same review endpoint Booking's own review list uses — so runs are fast, cheap and steady. It bills per review row, and four controls cut what you pay for *before* you are billed.

Last verified working: 2026-10-19.

## Booking.com 酒店评论、住客评价与酒店回复：中文调用与语言设置

获取酒店评论、满意与不满意内容、入住日期和酒店回复。

languages=["zh"] 只保留来源标记为中文的评论；locale 只影响旅客类型等标签。languages=[] 表示所有原文语言，不会自动翻译。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "maxReviewsPerHotel": 1,
  "reviewsSort": "most_recent",
  "languages": [
    "zh"
  ],
  "sessions": 1,
  "hotelIds": [
    "536251"
  ]
}
```

Avis Booking / opiniones Booking / Hotelbewertungen：用 languages 筛选原文语言。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Booking.com reviews scraper for AI agents: which input answers which request?

**Use it** for hotel guest reviews of named Booking.com properties: hotels, apartments, hostels — anything with a `booking.com/hotel/…` page. **Do not use it** to search a city for hotels (give the properties; the [Booking.com Prices Scraper](https://apify.com/kestrel/booking-prices-scraper) searches destinations), for reviews with a date range or "only since my last run" (there is no date filter: schedule `most_recent` with a small cap and dedupe on `review_id`), or for Booking.com attraction reviews. Reviews are never translated; they come back in the language they were written in, tagged with `language`.

| user request | input JSON |
|---|---|
| the latest 50 reviews of a hotel | `{"startUrls": ["https://www.booking.com/hotel/pt/memmo-alfama.html"], "maxReviewsPerHotel": 50}` |
| reviews of a hotel I only know by name | `{"hotelNames": ["Memmo Alfama Lisbon"], "maxReviewsPerHotel": 100}` |
| every review the hotel has | `{"hotelIds": ["536251"], "maxReviewsPerHotel": 0}` |
| negative reviews / complaints only | `{"hotelNames": ["Memmo Alfama Lisbon"], "maxRating": 6, "maxReviewsPerHotel": 200}` |
| English reviews with written text, for sentiment analysis | `{"hotelIds": ["536251"], "languages": ["en"], "requireText": true, "maxReviewsPerHotel": 0}` |
| what business travellers say about breakfast | `{"hotelIds": ["536251"], "travelerType": "business", "keyword": "breakfast"}` |
| the 50 worst reviews | `{"hotelIds": ["536251"], "reviewsSort": "lowest_rated", "maxReviewsPerHotel": 50}` |
| category ratings (staff, cleanliness, location…) and review count, no review text | `{"hotelIds": ["536251"], "maxReviewsPerHotel": 1}` — the free `hotel` row carries them; one review is billed |
| daily complaints feed across a comp set | `{"hotelIds": ["536251", "123456"], "maxRating": 6, "reviewsSort": "most_recent", "maxReviewsPerHotel": 50}` on a schedule; dedupe on `review_id` |
| only the new reviews since yesterday (daily feed) | `{"startUrls": [...], "sinceDate": "1 day", "reviewsSort": "most_recent"}` on a daily schedule — paging stops at the cut, older reviews are never billed; dedupe on `review_id` across runs |
| reviews from the last 12 months | `{"hotelIds": ["536251"], "sinceDate": "12 months", "maxReviewsPerHotel": 0}` |
| overall score + sub-scores for 50 hotels, no review text | `{"startUrls": [...50 URLs...], "maxReviewsPerHotel": 1}` — the free `hotel` row carries `review_score` (Booking's overall 1-10), `stars`, `review_count` and the seven `score_*` columns; one review per hotel is billed |

**One `review` row** = `review_id`, `rating` (1–10), `rating_5`, `title`, `positives`, `negatives`, `text` (both joined), `language`, `review_date`, `check_in`, `check_out`, `nights`, `room_type`, `traveler_type`, `reviewer_name`, `reviewer_country`, `helpful_votes`, `photos`, `response` (the property's reply), `hotel_id`, `hotel_name`. Billed at $0.005; nothing else is.

**Status contract**: one free `status` row per input target with `status` = `ok`, `no_reviews` (the hotel has no reviews, or an unknown id) or `error` (a URL or name Booking cannot match, with the `error` text); `reviews` delivered, `filtered` (removed by `maxRating`/`requireText`), `pages` read and Booking's `total`. A run whose only problem is the input (wrong site, empty list, bad range) ends green with the reason on the run card and nothing charged; a blocked or throttled source fails loudly. If every target errors, the run fails with the first error.

## What does the Booking.com reviews scraper do?

You give it properties. It gives you their **booking.com hotel reviews** as rows you can sort, filter and export.

- **`review` rows** — `review_id`, `rating` (1–10, Booking's scale), `rating_5` (the same score out of five), `title`, `positives` (what the guest liked), `negatives` (what they disliked), `text` (both joined into one comment), `language`, `review_date`, `check_in`, `check_out`, `nights`, `room_type`, `room_id`, `traveler_type` and `traveler_type_code`, `stay_status`, `reviewer_name`, `reviewer_country`, `reviewer_country_code`, `anonymous`, `helpful_votes`, `photos`, `approved`, `response` (the property's reply), plus `hotel_id`, `hotel_name`, `url`, `locale` and `fetched_at`.
- **`hotel` rows** — free context per property: `hotel_id`, `hotel_name`, `city`, `region`, `country`, `country_code`, `latitude`, `longitude`, Booking's seven category scores (`score_staff`, `score_facilities`, `score_cleanliness`, `score_comfort`, `score_value`, `score_location`, `score_wifi`), `review_count`, the `languages` (code and count), `traveler_types` (type and count) and `seasons` (bucket and count) its reviews come in, `reviews_fetched`, `url` and `locale`.
- **`status` rows** — free: per input `target`, the `hotel_id` and `hotel_name`, a `status` of `ok`, `no_reviews` or `error`, how many `reviews` were delivered, how many were `filtered`, how many `pages` were read, Booking's `total`, a `duplicates` flag, the `error` if any, and `fetched_at`.

**Booking.com guest reviews** come back **in the language they were written in**, tagged with the language. One Lisbon boutique hotel returned 24 languages across 892 reviews.

## Booking.com reviews by hotel, by URL, by name or by id

- **`startUrls`** — property pages such as `https://www.booking.com/hotel/pt/memmo-alfama.html`; any language variant (`.en-gb.html`, `.de.html`) and any query string is fine. Booking's URLs carry no numeric id, so the slug is resolved through Booking's own autocomplete, held to the country in the URL, and the resolved name comes back in every row so you can check the match.
- **`hotelNames`** — names as you would type them into Booking's search box: "Memmo Alfama Lisbon". Add the city for chains. The first property Booking's autocomplete returns is used.
- **`hotelIds`** — Booking's numeric id, e.g. `536251`, which is what an earlier run's `hotel_id` gives you. This is the **booking.com reviews by hotel id** path and the fastest one: no lookup at all. Ids carry no name, so `hotel_name` stays empty unless you also give a URL or name.

A URL, its name and its id count as the same property and are harvested once, so mixing inputs never double-bills.

## Booking.com negative reviews without paying for the happy ones

Four controls run **before** billing, and together they are the reason a complaints feed is affordable:

- **`maxRating`** keeps only reviews at or below a score on Booking's 1–10 scale. It also changes *how* the property is read: lowest score first, stopping at the first review above the threshold. A property with 892 reviews and 24 of them at 6 or below costs one page, not thirty-six.
- **`requireText`** drops score-only reviews. Booking lets guests leave a score with no words — about four in ten do — and those are worthless for reading and free with this switch on.
- **`languages`**, **`travelerType`** and **`keyword`** are applied by Booking itself, so the reviews you skip are never even fetched.

Filtered reviews are never charged. Neither are hotel rows, status rows, properties with no reviews, or lookups that fail.

## Hotel review data for revenue, ops and analysts

- **Revenue and reputation managers** run the complaints feed daily across a comp set and read only what changed: `maxRating: 6`, `reviewsSort: "most_recent"`, `maxReviewsPerHotel: 50`.
- **Operations** search by topic — `keyword: "breakfast"`, `keyword: "noise"` — and see which room types the complaints cluster in (`room_type` is on every row).
- **Analysts** pull the full corpus for sentiment work: `maxReviewsPerHotel: 0`, `requireText: true`, one language at a time so the model gets clean input.
- **Owners and hosts** read `response` to see which complaints the property answered and which it left hanging.

Every row carries `traveler_type`, `reviewer_country`, `check_in` and `nights`, so "what do business travellers from Germany say in winter" is a filter, not a project.

## Input

| field | what it does |
|---|---|
| `startUrls` | Booking.com property URLs, resolved through Booking's autocomplete. |
| `hotelNames` | Property names as typed into Booking's search; the first hotel hit is used. |
| `hotelIds` | Booking's numeric property ids. No lookup; no name. |
| `maxReviewsPerHotel` | 0 = every review (25 per page); N = the first N in the chosen order. The main cost control. Default 200. |
| `reviewsSort` | `most_recent` (default), `oldest`, `highest_rated`, `lowest_rated` or `most_relevant`. |
| `languages` | Language codes to keep (`en`, `de`, `fr`, `es`, `it`, `pt`, `nl`, `ru`, `ja`, `zh`, `ko`, `tr` …), filtered by Booking. Empty = all. |
| `travelerType` | `all` (default), `families`, `couples`, `friends`, `solo` or `business`, filtered by Booking. |
| `keyword` | Only reviews mentioning a word or phrase, searched by Booking. Empty = all. |
| `maxRating` | 0 = all; 1–10 = only reviews at or below it, read lowest first. Filters before billing. |
| `requireText` | Only reviews where the guest wrote something. Filters before billing. |
| `locale` | Site locale for Booking's labels (traveller type, country names), e.g. `en-US`, `de-DE`. Reviews stay in their original language. |
| `includeHotelRow` | Emit the free hotel context row (default on). |
| `sessions` | Parallel proxy sessions (default 4). |
| `perIp` | Requests per second per session (default 1). |
| `proxyConfiguration` | Apify Proxy; the default datacenter group is enough. |

### Example: a scheduled complaints feed

```json
{
  "startUrls": ["https://www.booking.com/hotel/pt/memmo-alfama.html", "https://www.booking.com/hotel/pt/the-lumiares.en-gb.html"],
  "maxReviewsPerHotel": 50,
  "reviewsSort": "most_recent",
  "maxRating": 6,
  "requireText": true
}
```

Run it every morning. Each run reads the properties lowest score first, stops at the first review above 6, and bills only the reviews it delivers.

### Example: the full English corpus for a competitor set

```json
{
  "hotelNames": ["Memmo Alfama Lisbon", "The Lumiares Lisbon", "Hotel Valverde Lisboa"],
  "maxReviewsPerHotel": 0,
  "languages": ["en"],
  "requireText": true
}
```

### Example: what families say about breakfast, by id

```json
{
  "hotelIds": ["536251"],
  "maxReviewsPerHotel": 100,
  "travelerType": "families",
  "keyword": "breakfast",
  "locale": "en-GB"
}
```

## Output

One review row, exactly as delivered:

```json
{
  "type": "review",
  "url": "https://www.booking.com/hotel/pt/memmo-alfama.html",
  "locale": "en-US",
  "review_id": "c90f61915f999a43",
  "rating": 10.0,
  "rating_5": 5.0,
  "title": "Best place to stay in Lisbon!",
  "positives": "Great location and amazing terrace.",
  "negatives": null,
  "text": "Great location and amazing terrace.",
  "language": "en",
  "review_date": "2026-08-28",
  "check_in": "2026-08-24",
  "check_out": "2026-08-27",
  "nights": 3,
  "room_type": "Premium Double or Twin Room",
  "room_id": "53625108",
  "traveler_type": "Couple",
  "traveler_type_code": "COUPLES",
  "stay_status": "stayed",
  "reviewer_name": "Jean",
  "reviewer_country": "Canada",
  "reviewer_country_code": "ca",
  "anonymous": false,
  "helpful_votes": 0,
  "photos": null,
  "approved": true,
  "response": null,
  "hotel_id": "536251",
  "hotel_name": "Memmo Alfama - Design Hotels",
  "fetched_at": "2026-08-29T10:12:04+00:00"
}
```

The free hotel row for the same property carries `review_count: 892`, `score_staff: 9.57`, `score_location: 9.6`, `score_value: 8.8`, `score_wifi: 8.59`, a `languages` list such as `[{"code": "en", "count": 490}, {"code": "de", "count": 139}, …]` and `traveler_types` such as `[{"type": "COUPLES", "count": 590}, …]`.

The dataset has five views — Overview, Reviews, Complaints (negatives first), Hotels and Status — and exports to CSV, Excel, JSON or XML from the run page or the API.

## How much does it cost?

You pay per delivered `review` row. Everything else is free: hotel rows, status rows, reviews dropped by `maxRating` or `requireText`, properties with no reviews, and lookups that fail. The number of reviews you asked for is the number you pay for, capped by `maxReviewsPerHotel` and by whatever spending limit you set on the run. A 50-review complaints feed across ten properties is at most 500 review rows a day and usually far fewer, because most properties have few new complaints.

## Booking.com reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/booking-reviews-scraper").call(run_input={
    "startUrls": ["https://www.booking.com/hotel/pt/memmo-alfama.html"],
    "maxReviewsPerHotel": 100,
    "reviewsSort": "most_recent",
})
reviews = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "review"]
for r in reviews[:5]:
    print(r["rating"], r["traveler_type"], r["title"], "|", r["negatives"])
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/booking-reviews-scraper').call({
    hotelNames: ['Memmo Alfama Lisbon'], maxReviewsPerHotel: 0, maxRating: 6, requireText: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const complaints = items.filter(r => r.type === 'review');
console.log(complaints.length, 'complaints;', complaints.filter(r => r.response).length, 'answered by the hotel');
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~booking-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["536251"], "maxReviewsPerHotel": 25, "languages": ["en"]}'
```

**n8n**: an HTTP Request node to the URL above (Header Auth with your token) on a Schedule trigger, then a Code node that keeps `type === 'review'` and drops the `review_id` values you have already seen, then Slack, Google Sheets or email. **Make**: the Apify "Run an Actor" module with the same JSON. **AI agents**: the actor is listed on Apify's MCP server, so a Claude, Cursor or LangChain agent can call it by name — the input and output schemas above are what the agent reads.

## Is it legal to scrape Booking.com reviews?

The actor reads publicly visible guest reviews through the same request Booking's own page makes, with no login and no personal accounts. Reviews are the guests' public words about a business; names appear as Booking shows them (first name or "Anonymous"). Whether you may use the data for your purpose depends on your jurisdiction, on Booking.com's terms and on data-protection law (GDPR in the EU treats reviewer names as personal data) — read them and take advice before scraping at scale or republishing. Use the data for analysis and monitoring; do not repost reviews as your own content.

## Limits and honest notes

- **Score-only reviews are real.** Booking lets guests rate without writing; in a recent sample 11 of 25 reviews had no words. `requireText` drops them before billing.
- **Ids carry no name.** An id resolves to reviews and scores but not to a name — Booking's lookup runs from name to id, not back. Give a URL or a name if you need `hotel_name` filled.
- **Unknown ids look like empty properties.** Booking answers a wrong id with zero reviews, which is reported as `no_reviews` (free). A URL or a name that Booking cannot find is reported as `error` (also free).
- **Filters are Booking's.** Language codes must be the ones Booking uses (the hotel row lists them with counts); a code Booking rejects fails that property with a clear message rather than silently harvesting everything.
- **No room-level or topic filter.** Booking's endpoint accepts language, traveller type and keyword; score and topic filters are applied by this actor after fetching (`maxRating` reads ascending so it rarely over-fetches).
- **Pace.** Booking answered ten calls a second from one IP in testing; the default of one call per second per session is conservative. Each call returns 25 reviews.

## FAQ

### Does it need a Booking.com API key or login?

No. There is no public Booking.com reviews API for reading reviews; the actor uses the request Booking's own review list makes, which needs no key, no cookies and no browser.

### Can I download Booking.com reviews as CSV or Excel?

Yes. Every run writes an Apify dataset; open the Reviews or Complaints view and export **booking.com reviews csv**, Excel, JSON or XML, or fetch the same through the API with `?format=csv`.

### How do I get only Booking.com negative reviews?

Set `maxRating` to 6 (Booking's own wording: 5 is "Poor", 7 is "Good"). The property is read lowest score first and paging stops at the threshold, so you pay only for the complaints. Add `requireText: true` to skip score-only ratings.

### Do I need the hotel id, or can I use the URL?

Either — or the name. URLs and names are resolved through Booking's autocomplete and the matched name comes back in every row; ids skip the lookup. Once you have a `hotel_id` from a run, use it for the fastest repeat runs.

### How many reviews can one hotel return?

All of them. Booking pages reviews 25 at a time and the actor keeps going until the property is exhausted or `maxReviewsPerHotel` is reached. A large city hotel with 15,000 reviews is 600 calls.

### Are reviews translated, and which languages come back?

Reviews come back as written, with `language` set — **multi language hotel reviews** from one property, or **booking.com reviews by language** when you set `languages`. The hotel row lists every language the property's reviews come in, with counts, so you can pick what to fetch with `languages`. Booking's labels (traveller type, country names) follow `locale`.

### Does it include the hotel's replies?

Yes — `response` carries the property's public reply when there is one.

### What is `traveler_type_code`?

Booking's own guest category on the booking behind the review: `COUPLES`, `FAMILIES`, `GROUP_OF_FRIENDS`, `SOLO_TRAVELLERS` or `BUSINESS_TRAVELLERS`. `traveler_type` is the same thing in the site language.

### Can I scrape Booking.com reviews without an API?

That is what this is — **booking.com reviews without api** keys: **scrape booking.com reviews** by URL, name or id, no key, no browser, pay per review.

### Can I use it for hotel sentiment analysis?

Yes. `positives` and `negatives` are already split, `text` joins them for a single column, every row is tagged with `language`, `rating` and `traveler_type`, and `requireText` keeps the corpus clean.

### What does bulk work cost?

Reviews only. A **bulk hotel reviews** pull of one hundred properties at 200 reviews each is at most 20,000 review rows; with `requireText` on it is typically 12,000, because score-only reviews are free.

## Review monitoring across a portfolio

Put every property you manage into `startUrls`, set `reviewsSort: "most_recent"` and `maxReviewsPerHotel: 30`, and schedule the run daily. Keep the `review_id` values you have seen; anything new is a new review (add `"sinceDate": "1 day"` and only reviews published since yesterday are read and billed). Route rows with `rating` at or below 6 to the people who answer complaints, and rows with `response: null` older than three days to the people who should have.

### Guest feedback data that keeps its structure

Because every row carries `room_type`, `traveler_type`, `reviewer_country`, `check_in` and `nights`, a **hotel reputation monitoring** table falls out of a pivot: score by room type, by season, by market. The hotel row's category scores (`score_cleanliness`, `score_value` …) are Booking's own aggregates, refreshed every run — a **hotel review data** feed you can chart without computing anything.

### What this does not do

It does not scrape Booking.com prices, availability or search results, and it does not read Booking.com's HTML pages at all. For **booking.com competitor reviews** it is exactly right; for rates, use the hotel price actors below.

### Choosing between sort orders

`most_recent` for schedules, `lowest_rated` (or `maxRating`) for complaints, `highest_rated` for marketing copy, `most_relevant` for Booking's own pick, `oldest` for a full history pull in chronological order. Sort affects which reviews you get when `maxReviewsPerHotel` caps the run; with 0 it only affects order.

## Related scrapers

Booking.com reviews are one voice of the guest. These read the others, and they share the same row shape, the same pay-per-delivered-row billing and the same scheduling story:

- **[Despegar Hotel Ratings Scraper](https://apify.com/kestrel/despegar-hotel-ratings)** — Latin America's largest OTA: guest score, six category scores and the site's own summary of what guests say, per property.
- **[Zoover Reviews Scraper](https://apify.com/kestrel/zoover-reviews-scraper)** — Dutch and German holiday reviews from Zoover, with per-aspect scores and the owner's reply.
- **[Hostelworld Reviews Scraper](https://apify.com/kestrel/hostelworld-reviews-scraper)** — hostel guest reviews with eight sub-ratings, traveller group and trip type, and the owner's reply.
- **[TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper)** — TripAdvisor hotel reviews with six sub-ratings, trip type, photos and the management response, in 30 site languages, no browser.
- **[Booking.com Scraper — Hotel Prices](https://apify.com/kestrel/booking-prices-scraper)** — Booking.com prices for exact dates and guests, for a whole destination or a hotel list: stay total, nightly rate, taxes, cancellation and breakfast flags, optional room rates.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives and the hotel's reply.
- **[Trip.com Reviews Scraper](https://apify.com/kestrel/trip-com-reviews-scraper)** — Trip.com and Ctrip hotel reviews with four sub-scores and the Chinese-language corpus.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site's rate for a stay, Booking.com included.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — which OTAs undercut a property's direct rate.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
