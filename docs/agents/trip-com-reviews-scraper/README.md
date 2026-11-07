# Trip.com Reviews Scraper — Ctrip Hotel Guest Reviews & Ratings

A **trip.com reviews scraper** that returns every guest review a hotel has, as structured rows: **trip.com ratings** on both the 0–10 and 5-star scales, the rating word, the four sub-scores (location, cleanliness, service, amenities), the review text in the language it was written in, posting and check-in dates, room type, traveler type, reviewer name and country, photos, and the hotel's public reply. Because Trip.com is Ctrip's international brand, the same rows are **ctrip reviews** — the Chinese-language corpus that no other OTA carries — alongside the Expedia-group reviews Trip.com aggregates. It turns **trip.com hotel reviews** into **hotel review data** you can query: a **hotel review scraper** built for bulk work, not one page at a time.

Give it Trip.com hotel URLs or numeric hotel ids. No login, no **trip.com api** key, no browser, no client-side token. It bills per review row, and three controls cut what you pay for *before* you are billed.

Last verified working: 2026-08-29.

## 携程与 Trip.com 酒店点评、评论与评分：中文调用与语言设置

按酒店 URL 或 ID 读取酒店住客评论、分项评分、入住信息和酒店回复。

只保留中文原文使用 languages=["Chinese"]；locale="zh-HK" 只影响来源标签，不翻译正文。languages=[] 表示所有语言。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.trip.com/hotels/lisbon-hotel-detail-2561632/valverde-hotel/"
  ],
  "maxReviewsPerHotel": 1,
  "reviewsSort": "most_recent",
  "languages": [
    "Chinese"
  ],
  "locale": "zh-HK",
  "sessions": 1
}
```

Trip.com 評價 / Ctrip reviews：用 languages 选择评论原文语言。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Trip.com reviews scraper for AI agents: which input answers which request?

**Use it** for hotel guest reviews of named Trip.com hotels by URL or numeric id — the same rows are the Ctrip (携程) reviews, since Trip.com is Ctrip's international brand; `source` says whether a review came from Trip.com, Ctrip, Expedia or Hotels.com. **Do not use it** with a hotel name (not accepted: find the hotel on trip.com and pass its URL or id), to search a city for hotels, for a date or traveller-type filter (none: for "only since my last run" schedule `most_recent` with a small cap and dedupe on `review_id`), or for translations (text is delivered as written, tagged with `language`; `languages` keeps only the languages you name).

| user request | input JSON |
|---|---|
| the latest 50 reviews of a hotel | `{"startUrls": ["https://www.trip.com/hotels/lisbon-hotel-detail-2561632/valverde-hotel/"], "maxReviewsPerHotel": 50}` |
| every review the hotel has | `{"hotelIds": ["2561632"], "maxReviewsPerHotel": 0}` |
| English and Chinese reviews only | `{"hotelIds": ["2561632"], "languages": ["English", "Chinese"], "maxReviewsPerHotel": 0}` |
| the Chinese (Ctrip) reviews only | `{"hotelIds": ["2561632"], "languages": ["Chinese"]}` |
| negative reviews / complaints only | `{"hotelIds": ["2561632"], "reviewsSort": "lowest_rated", "maxRating": 6, "maxReviewsPerHotel": 200}` |
| the 50 worst reviews | `{"hotelIds": ["2561632"], "reviewsSort": "lowest_rated", "maxReviewsPerHotel": 50}` |
| the hotel's rating, sub-scores and review count, no review text | `{"hotelIds": ["2561632"], "maxReviewsPerHotel": 1}` — the free `hotel` row carries them; one review is billed |
| Japanese labels | `{"hotelIds": ["2561632"], "locale": "ja-JP", "maxReviewsPerHotel": 100}` |
| daily complaints feed across a comp set | `{"hotelIds": ["2561632", "100632153"], "reviewsSort": "lowest_rated", "maxRating": 6, "maxReviewsPerHotel": 100}` on a schedule; dedupe on `review_id` |

**One `review` row** = `review_id`, `rating` (0–10), `rating_5`, `rating_text`, `rating_location`, `rating_facility`, `rating_service`, `rating_room` (Trip.com's four sub-scores), `text`, `language`, `recommend`, `review_date`, `check_in`, `room_type`, `travel_type`, `reviewer_name`, `reviewer_country`, `reviewer_country_code`, `reviewer_reviews`, `reviewer_level`, `helpful_votes`, `images`, `source`, `response`, `response_date`, `hotel_id`, `hotel_name`. Billed at $0.004; nothing else is.

**Status contract**: one free `status` row per input target with `status` = `ok`, `no_reviews` or `error` (an id Trip.com does not know, a URL whose page carries no id, or a hotel refused after every retry — a refusal looks like an empty answer, so it is reported as an error rather than as "no reviews"); `reviews` delivered, `filtered` (removed by `maxRating`/`requireText`), `pages` read, Trip.com's `total`, `duplicates`. A run whose only problem is the input (wrong site, empty list, bad range, unknown language name) ends green with the reason on the run card and nothing charged; a blocked or throttled source fails loudly. If every hotel errors, the run fails with the first error.

## What does the Trip.com reviews scraper do?

You give it hotels. It gives you their **trip.com hotel reviews** as rows you can sort, filter and export.

- **`review` rows** — `review_id`, `rating` (0–10, Trip.com's scale), `rating_5` (the same score out of five), `rating_text` ("Outstanding", "Amazing", "Good"…), `rating_location`, `rating_facility`, `rating_service`, `rating_room`, `text`, `language`, `recommend`, `review_date`, `check_in`, `room_type`, `room_id`, `travel_type`, `travel_type_id`, `reviewer_name`, `reviewer_country`, `reviewer_country_code`, `reviewer_reviews`, `reviewer_level`, `helpful_votes`, `images`, `source`, `source_code`, `response`, `response_date`, `hotel_id`, `hotel_name`, `url`, `locale`, `fetched_at`.
- **`hotel` rows** — free context per property: `hotel_id`, `hotel_name`, `stars`, `address`, `city`, `country`, the overall `rating` with its `rating_text` and the four sub-scores, `review_count`, the `languages` and `travel_types` its reviews come in (name, count and Trip.com's id for each), `reviews_fetched` and the `url`.
- **`status` rows** — free: per input `target`, the `hotel_id` and `hotel_name`, a `status` of `ok`, `no_reviews` or `error`, how many `reviews` were delivered, how many were `filtered`, how many `pages` were read, Trip.com's `total`, a `duplicates` flag, the `error` if any, and `fetched_at`.

Reviews come back **in the language they were written in**, with the language tagged. One Lisbon boutique hotel returned nine languages in a single run, and roughly a quarter of its corpus was Chinese — reviews that exist nowhere else.

## Trip.com reviews by hotel, by URL or by id

- **`startUrls`** — Trip.com hotel pages such as `https://www.trip.com/hotels/lisbon-hotel-detail-2561632/valverde-hotel/`. The numeric id sits in the URL after `hotel-detail-`, so no page has to be loaded to find it; any country subdomain (`us.`, `uk.`, `www.`) works.
- **`hotelIds`** — the numeric id directly, e.g. `2561632`, which is what an earlier run's `hotel_id` gives you. This is the **trip.com reviews by hotel id** path, and the fastest one.

A URL and its id count as the same hotel and are harvested once, so mixing inputs never double-bills. Hotel names are not an input: Trip.com does not expose a public autocomplete the way Agoda does, and guessing would bill you for the wrong property.

## Trip.com negative reviews without paying for the happy ones

Three controls run **before** billing, and together they are the reason a complaints feed is affordable:

- **`maxRating`** keeps only reviews at or below a score on Trip.com's 0–10 scale. Trip.com's own words: 6 and below is a poor stay, 8 is "Very good".
- **`requireText`** drops any review that has no words. Trip.com reviews nearly always do; the guard is there for the rest.
- **`languages`** asks Trip.com to filter server-side, so reviews in languages you skip are never fetched at all.

Filtered reviews are never charged. A hotel with a hundred **trip.com ratings** and four complaints delivers four rows under `maxRating: 6`. You pay for four. That is what makes **trip.com negative reviews** monitoring across a portfolio practical.

## Hotel review data for revenue, ops and analysts

- **Hotel reputation monitoring.** Schedule a daily run sorted `most_recent`; every new review arrives with its score, sub-scores and text, and `review_id` is stable, so deduping is trivial.
- **Trip.com competitor reviews.** Point it at the properties you compete with and pull their whole corpus: what guests praise, what they complain about, which hotels bother to reply and how fast.
- **Chinese hotel reviews.** Outbound Chinese travellers review on Ctrip, and Trip.com serves those reviews with the rest. If you want to know what Chinese guests think of a hotel in Lisbon or Bangkok, this is the source — and `languages: ["Chinese"]` isolates it.
- **Hotel sentiment analysis.** Four sub-scores per review (`rating_location`, `rating_facility`, `rating_service`, `rating_room`) plus `travel_type` and `room_type` let you find *which* room and *which* kind of guest generates the low scores, before any text model runs.
- **OTA benchmarking.** `source` says whether a review came from Trip.com, Ctrip, Expedia or Hotels.com, because Trip.com aggregates partner reviews alongside its own.

## Input

| Field | What it does |
| --- | --- |
| `startUrls` | Trip.com hotel pages. The numeric id is read from the URL. |
| `hotelIds` | Trip.com's numeric hotel ids, e.g. `2561632` — the fastest input. |
| `maxReviewsPerHotel` | `0` = every review the hotel has (Trip.com pages 100 at a time; large hotels run into the thousands). `N` = the first N. The main cost control. |
| `reviewsSort` | `most_recent`, `highest_rated`, `lowest_rated`, `most_relevant`. |
| `languages` | Empty = every language. Otherwise names (`English`, `Chinese`, `Japanese`, `Korean`, `German`, `French`, `Spanish`…) or Trip.com language ids; filtered by Trip.com itself, so skipped reviews are never fetched or charged. |
| `maxRating` | `0` = keep everything. `1`–`10` = keep only reviews at or below that score. Filtered reviews are never charged. |
| `requireText` | Keep only reviews that have a written comment. |
| `locale` | Trip.com locale for the request (`en-US`, `en-GB`, `ja-JP`, `de-DE`…). Sets the language of Trip.com's labels; reviews always come back as written. |
| `includeHotelRow` | Emit the free per-hotel context row (name, stars, address, scores, review count, languages). |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. The default datacenter group works for Trip.com. |

### Example: a scheduled complaints feed

```json
{
  "startUrls": ["https://www.trip.com/hotels/lisbon-hotel-detail-2561632/valverde-hotel/"],
  "maxReviewsPerHotel": 0,
  "reviewsSort": "most_recent",
  "maxRating": 6,
  "requireText": true
}
```

### Example: the full corpus for a competitor set, English and Chinese only

```json
{
  "hotelIds": ["2561632", "100632153", "3064303"],
  "maxReviewsPerHotel": 0,
  "languages": ["English", "Chinese"],
  "reviewsSort": "most_relevant"
}
```

### Example: the newest 50 by id, Japanese labels

```json
{
  "hotelIds": ["2561632"],
  "maxReviewsPerHotel": 50,
  "reviewsSort": "most_recent",
  "locale": "ja-JP",
  "includeHotelRow": false
}
```

## Output

One dataset, three row types, told apart by `type`. A review row looks like this:

```json
{
  "type": "review",
  "review_id": "2067108455",
  "hotel_id": "2561632",
  "hotel_name": "Hotel Valverde Lisboa - Relais & Chateaux",
  "rating": 9.7,
  "rating_5": 4.85,
  "rating_text": "Amazing",
  "rating_location": 10,
  "rating_facility": 9.5,
  "rating_service": 10,
  "rating_room": 9.5,
  "text": "非常精緻的小型酒店，新裝修的設施很新，床品舒適…",
  "language": "zh",
  "recommend": true,
  "review_date": "2026-08-17T06:13:30",
  "check_in": "2026-08-01",
  "room_type": "Classic Room",
  "travel_type": "Couple",
  "reviewer_name": "Xiaoyufeifeijiejie",
  "reviewer_country": "China",
  "reviewer_country_code": "CN",
  "reviewer_reviews": 10,
  "reviewer_level": "Review Specialist",
  "helpful_votes": 0,
  "images": ["https://ak-d.tripcdn.com/images/…_W_1280_853_R5_Q70.jpg"],
  "source": "ctrip",
  "response": "Dear Guest, Thank you very much for your wonderful review…",
  "response_date": "2026-08-19",
  "url": "https://www.trip.com/hotels/lisbon-hotel-detail-2561632/valverde-hotel/",
  "locale": "en-US",
  "fetched_at": "2026-08-29T04:30:12+00:00"
}
```

The dataset ships with five views: **Overview**, **Reviews** (every review field), **Low scores** (the complaints feed), **Hotels** (`stars`, `city`, `country`, scores, `review_count`, `reviews_fetched`) and **Run status** (`target`, `status`, `reviews`, `filtered`, `pages`, `total`, `duplicates`, `error`). Export any of them as CSV, Excel, JSON or XML from the Apify console or the API — that is the **trip.com reviews csv** path, and the **download trip.com reviews** path when a spreadsheet is what someone asked for.

## How much does it cost?

**$0.004 per review row.** Hotel rows, status rows, filtered reviews, hotels with no reviews, unknown ids and failed hotels are free. A 95-review property costs $0.38 in full; the same property as a daily complaints feed costs a fraction of a cent per day. Compute and proxy usage for the run are included in the event price.

**Bulk hotel reviews** at scale: 1,000 hotels × 200 most-recent reviews = 200,000 rows = $800, delivered in an afternoon with 16 sessions. The pocket's leading actor charges the same per review; the difference is what you get per row and what you never pay for.

## Trip.com reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/trip-com-reviews-scraper").call(run_input={
    "hotelIds": ["2561632"],
    "maxReviewsPerHotel": 0,
    "reviewsSort": "lowest_rated",
    "maxRating": 6,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["language"], row["travel_type"], row["text"][:80])
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/trip-com-reviews-scraper').call({
    startUrls: ['https://www.trip.com/hotels/lisbon-hotel-detail-2561632/valverde-hotel/'],
    maxReviewsPerHotel: 200,
    languages: ['English'],
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter((r) => r.type === 'review');
console.log(reviews.length, 'reviews; replied to:', reviews.filter((r) => r.response).length);
```

curl (synchronous, returns the dataset):

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~trip-com-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["2561632"], "maxReviewsPerHotel": 50, "reviewsSort": "most_recent"}'
```

**n8n / Make / Zapier.** Use the HTTP Request node against the URL above, or the Apify node with the actor id. A Schedule trigger → Apify → filter `type == "review"` → Slack/Sheets is a complete **review monitoring** workflow; keep a set of seen `review_id` values in workflow static data and only the new ones reach the channel. A verified n8n template for the same pattern on Agoda is in the [kestrel examples repo](https://github.com/mtedj/kestrel-actors-examples) and ports in minutes.

**MCP / AI agents.** The actor is available through Apify's MCP server, so a Claude, Cursor or custom agent can call `trip-com-reviews-scraper` with a hotel URL and reason over the rows. Every field is documented in the dataset schema, which is what agents read.

## Is it legal to scrape Trip.com reviews?

The actor reads pages and endpoints Trip.com serves to any visitor without logging in, and it stores what the page shows: the review, its score, the reviewer's public display name and country. It does not access accounts, private data or anything behind a login. Reviews are user-generated content, and reviewer names are personal data under the GDPR and similar laws — process them lawfully for your purpose (analytics, monitoring, research), store them no longer than you need, and read Trip.com's terms before scraping at scale. This is data collection, not legal advice.

## Limits and honest notes

- Trip.com pages 100 reviews per request and reported no throttling at 20 concurrent requests from one IP during testing; the default pace of 1 request/second per session is conservative. Large hotels with several thousand reviews take a minute or two.
- A refused call from Trip.com looks exactly like a hotel with no reviews — a `200 Success` with no review block. The actor detects that shape, retries on a fresh IP with backoff, and reports the hotel as `error` if every attempt is refused. It never reports a throttled hotel as `no_reviews`, because a false "no reviews" corrupts your dataset silently while a false error costs one retry.
- An unknown hotel id is reported as an error on its status row, free, without retrying.
- The hotel row's name, stars and address come from the hotel page (one extra request per hotel). If that page cannot be read, the row still goes out with the scores from the review endpoint and the name blank, and the reviews are unaffected.
- Reviews are delivered as written; the actor does not translate. `language` tells you what each one is in. Trip.com's own translations are not exposed by the endpoint the actor reads.
- Trip.com counts repeated reviews once (`repeatComment`), which is why `total` can be a little above the rows that are actually pageable.

## FAQ

### Does it need a Trip.com API key or login?

No. It calls the same JSON endpoint Trip.com's own review panel uses, with the request head a browser sends. There is no public **trip.com api** for reviews, and this is how to get **trip.com reviews without api** access.

### Can I download Trip.com reviews as CSV or Excel?

Yes. Every run writes an Apify dataset; open the **Reviews** view and export it as CSV, Excel, JSON or XML, or fetch it from the API with `?format=csv`.

### How do I get only Trip.com negative reviews?

Set `maxRating` to `6` (or whatever your threshold is), `reviewsSort` to `lowest_rated`, and optionally `requireText: true`. Only the complaints are delivered and billed.

### Are Ctrip reviews included?

Yes. Trip.com is Ctrip's international brand and the review endpoint serves **ctrip hotel reviews** with `source: "ctrip"`, mostly in Chinese. Use `languages` to keep or drop them.

### Do I need the hotel id, or can I use the URL?

Either. The id is the number after `hotel-detail-` in any Trip.com hotel URL; a URL is resolved without loading the page.

### How many reviews can one hotel return?

All of them — set `maxReviewsPerHotel` to `0`. Trip.com pages 100 at a time; the actor walks the pages until Trip.com runs out and dedupes by `review_id`.

### Are reviews translated, and which languages come back?

Reviews arrive in the language they were written in, tagged in `language`. The hotel row lists every language the property's reviews come in, with counts, so you can decide what to keep. **Multi language hotel reviews** are the norm on Trip.com: expect English, Chinese, Japanese, Korean and the local language together.

### Does it include the hotel's replies?

Yes: `response` and `response_date`, when the hotel replied. Reply rate is a useful management signal in itself.

### Can I use it as a general hotel review aggregator?

For Trip.com and what Trip.com aggregates (Ctrip, Expedia, Hotels.com), yes. For a true **hotel review aggregator** across OTAs, pair it with the Agoda and Airbnb review scrapers below — the rows share the same shape, so one table holds all three.

### Can I scrape Trip.com reviews without an API?

That is what this is. No key, no browser automation, no rate-limit babysitting: the actor handles proxies, pacing and retries.

### What does bulk work cost?

$0.004 per review, nothing else from the actor. 10,000 reviews is $40. See the cost section above for the platform-usage note.

## Review monitoring across a portfolio

The pattern that works: one run per day, `reviewsSort: "most_recent"`, `maxReviewsPerHotel: 50`, every property in `hotelIds`. Keep the `review_id` values you have seen; the new rows are the day's reviews. Because filtered rows are free, you can run the same schedule twice — once unfiltered for the record, once with `maxRating: 6` straight into the on-call channel — and pay only for what each delivers.

### Guest feedback data that keeps its structure

**Guest feedback data** loses most of its value when it is flattened to a star and a paragraph. Every row here keeps the stay context (`check_in`, `room_type`, `travel_type`), the reviewer context (`reviewer_country`, `reviewer_reviews`, `reviewer_level`) and the four sub-scores, so "cleanliness complaints from families in the garden rooms since the renovation" is a filter, not a research project. That is the difference between **hotel guest reviews** as anecdotes and as a dataset.

### What this does not do

It does not write reviews, vote on them, or touch anything behind a login. It does not translate. It does not pull prices or availability — for those, see the hotel price actors below.

### Choosing between sort orders

`most_recent` for monitoring; `lowest_rated` with `maxRating` for complaints; `highest_rated` for marketing copy and what guests love; `most_relevant` (Trip.com's default ordering) when you want the reviews Trip.com itself would show a shopper first.

## Related scrapers

Trip.com is one side of a hotel's reputation. These read the rest, and they share the same row shape, the same pay-per-delivered-row billing and the same scheduling story:

- **[Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper)** — the largest hotel review corpus, by URL, name or id, no browser.
- **[HRS Reviews Scraper](https://apify.com/kestrel/hrs-reviews-scraper)** — HRS (hrs.com) guest ratings by URL or hotel id, twenty hotels per request, filtered by traveller type and language before billing.
- **[Kurzurlaub Reviews Scraper](https://apify.com/kestrel/kurzurlaub-reviews-scraper)** — German short-break hotel ratings (Hotelbewertungen) with per-area scores, by URL or id, complaints filtered before billing.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives, by hotel name, URL or id.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site's rate for a stay, Trip.com included.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — one row per hotel with every OTA's rate side by side and the parity math done.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
