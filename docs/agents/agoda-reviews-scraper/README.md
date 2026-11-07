# Agoda Reviews Scraper — Hotel Reviews, Guest Reviews & Ratings

An **agoda reviews scraper** that returns every guest review a property has, as structured rows: **agoda ratings** on both the 0–10 and 5-star scales, the rating word, title, review text, **separate positives and negatives**, stay dates and length, room type, reviewer name and country, and the hotel's public reply. It turns **agoda hotel reviews** into **hotel review data** you can query — a **hotel review scraper** built for bulk work rather than one page at a time.

Give it a **hotel name**, an Agoda URL, or a numeric hotel id — a name is resolved through Agoda's own search, so you never have to hunt for an id. No login, no **agoda api** key, no browser. This is a **hotel review scraper** that bills per review row, and two filters cut what you pay for *before* you are billed.

Last verified working: 2026-08-29.

## Agoda 酒店评论、点评与評價：中文调用与语言设置

获取 Agoda 展示的酒店评价，包括其展示的 Booking.com 评论。每条保留评分、正文、来源和可用的酒店回复。

locale="zh-cn" 设置请求语言及来源提供的标签或翻译，不会只保留中文评论。original_text 保留可用原文；没有来源翻译时不保证正文为中文。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.agoda.com/tivoli-avenida-liberdade-lisboa/hotel/lisbon-pt.html"
  ],
  "maxReviewsPerHotel": 1,
  "reviewsSort": "most_recent",
  "locale": "zh-cn",
  "sessions": 1
}
```

Agoda 評價 / รีวิวโรงแรม / 호텔 리뷰：来源可能同时包含不同语言评论。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Agoda reviews scraper for AI agents: which input answers which request?

**Use it** for hotel guest reviews of named Agoda properties — hotels, hostels, apartments — by name, URL or id, including the Booking.com reviews Agoda shows on the same page (`source` says which). **Do not use it** to search a city for hotels (give the properties; the [Agoda Prices Scraper](https://apify.com/kestrel/agoda-prices-scraper) searches destinations), for a language, traveller-type or date filter (none: every language is delivered, tagged with `language`; for "only since my last run" schedule `most_recent` with a small cap and dedupe on `review_id`), or for Agoda's category scores (the free `hotel` row carries id, name and count only). Where Agoda translates a review into your `locale`, `text` is the translation and `original_text` the guest's words; otherwise `text` is as written.

| user request | input JSON |
|---|---|
| the latest 50 reviews of a hotel I know by name | `{"hotelNames": ["Park Hyatt Tokyo"], "maxReviewsPerHotel": 50}` |
| reviews from an Agoda URL | `{"startUrls": ["https://www.agoda.com/tivoli-avenida-liberdade-lisboa/hotel/lisbon-pt.html"], "maxReviewsPerHotel": 100}` |
| every review the property has | `{"hotelIds": ["63820"], "maxReviewsPerHotel": 0}` |
| negative reviews / complaints only | `{"hotelNames": ["Park Hyatt Tokyo"], "reviewsSort": "lowest_rated", "maxRating": 5, "maxReviewsPerHotel": 200}` |
| only reviews with written text, for sentiment analysis | `{"hotelIds": ["63820"], "requireText": true, "maxReviewsPerHotel": 0}` |
| the 50 worst reviews | `{"hotelIds": ["63820"], "reviewsSort": "lowest_rated", "maxReviewsPerHotel": 50}` |
| Japanese labels and Agoda's Japanese translations | `{"hotelIds": ["63820"], "locale": "ja-jp", "maxReviewsPerHotel": 100}` |
| daily complaints feed across a comp set | `{"hotelIds": ["63820", "6988894"], "reviewsSort": "lowest_rated", "maxRating": 5, "maxReviewsPerHotel": 100}` on a schedule; dedupe on `review_id` |

**One `review` row** = `review_id`, `rating` (0–10), `rating_5`, `rating_text`, `title`, `text`, `positives`, `negatives`, `original_title`, `original_text`, `language`, `translated_to`, `review_date`, `check_in`, `check_out`, `stay_length`, `room_type`, `group_type`, `reviewer_name`, `reviewer_country`, `helpful_votes`, `unhelpful_votes`, `images`, `source` (Agoda or Booking.com), `responder`, `response`, `response_date`, `hotel_id`, `hotel_name`. Billed at $0.005; nothing else is.

**Status contract**: one free `status` row per input target with `status` = `ok`, `no_reviews` or `error` (a name or URL Agoda cannot match, or a property that answers with no reviews after every retry — a throttle and an empty property look the same, so it is reported as an error rather than as "no reviews"); `reviews` delivered, `filtered` (removed by `maxRating`/`requireText`), `pages` read, `duplicates`. A run whose only problem is the input (wrong site, empty list, bad range) ends green with the reason on the run card and nothing charged; a blocked or throttled source fails loudly. If every property errors, the run fails with the first error.

## What does the Agoda reviews scraper do?

You give it properties. It gives you their **agoda hotel reviews** as rows you can sort, filter and export.

- **`review` rows** — `rating` (0–10, Agoda's scale), `rating_5` (the same score out of five), `rating_text` ("Exceptional"), `title`, `text`, `positives`, `negatives`, `language`, `review_date`, `check_in`, `check_out`, `stay_month`, `stay_length`, `room_type`, `reviewer_name`, `reviewer_country`, `group_type`, `helpful_votes`, `unhelpful_votes`, `responder`, `response`, `response_date`, `images`, `source` and `provider_id`.
- **`hotel` rows** — free context: the property id, name, URL and how many reviews were taken.
- **`status` rows** — free: per property, what was harvested, how many were filtered, and why anything failed.

Reviews come back tagged with the language they were written in; where Agoda translates one into your `locale`, `text` holds the translation and `original_text` the guest's own words. One Lisbon property returned 18 languages and 57 reviewer countries in a single run.

## Agoda reviews by hotel, by name, or by id

Most tools make you find Agoda's internal id first. This one does not:

- **`hotelNames`** — type the property as you would into Agoda's search box: `Park Hyatt Tokyo`. Resolved through Agoda's own autocomplete to the exact property.
- **`startUrls`** — Agoda property pages. The numeric id is read from the page for you.
- **`hotelIds`** — the numeric id directly, e.g. `63820`, which is what an earlier run's `hotel_id` gives you. This is the **agoda reviews by hotel id** path.

A name, its URL and its id all count as the same property and are harvested once, so mixing inputs never double-bills.

## Agoda negative reviews without paying for the happy ones

Two filters run **before** billing, and together they are the reason a complaints feed is affordable:

- **`maxRating`** keeps only reviews at or below a score on Agoda's 0–10 scale. `5` is "a poor stay".
- **`requireText`** drops the score-only reviews that have no words — a large share of Agoda's corpus.

In a verified run, a property with 324 visible reviews delivered **8 rows** under `maxRating: 5` with `requireText` on. You pay for eight. That is what makes **agoda negative reviews** monitoring across a portfolio practical rather than theoretical.

## Hotel review data for revenue, ops and analysts

- **Hotel reputation monitoring.** Schedule a daily run sorted `most_recent` and every new review arrives with its score and text. Nothing to poll.
- **Agoda competitor reviews.** Point it at the properties you compete with and pull their whole review corpus — what guests praise, what they complain about, which hotels bother to reply.
- **Hotel sentiment analysis.** `positives` and `negatives` arrive as separate fields, which is unusual and far easier to model than free text alone.
- **Operations.** Reviews carry `check_in`, `check_out`, `stay_length` and `room_type`, so a score ties back to the actual stay — you can find the room type that generates complaints.
- **OTA review data** benchmarking: `source` and `provider_id` say which channel a review came from, because Agoda aggregates partner reviews alongside its own.

## Input

| Field | What it does |
| --- | --- |
| `hotelNames` | Property names as typed into Agoda's search box, e.g. `Park Hyatt Tokyo`. Resolved through Agoda's own autocomplete. |
| `startUrls` | Agoda property pages. The numeric hotel id is read from the page for you. |
| `hotelIds` | Agoda's numeric ids, e.g. `63820` — the fastest input. |
| `maxReviewsPerHotel` | `0` = every review the property has (Agoda pages ~200 at a time; large hotels run into the thousands). `N` = the first N. The main cost control. |
| `reviewsSort` | `most_recent`, `highest_rated`, `lowest_rated`, `most_relevant`. |
| `maxRating` | `0` = keep everything. `1`–`10` = keep only reviews at or below that score. Filtered reviews are never charged. |
| `requireText` | Keep only reviews that actually have a written comment. |
| `locale` | Agoda locale for the request (`en-us`, `es-es`, `de-de`…). |
| `includeHotelRow` | Emit the free per-property context row. |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. Required — Agoda throttles datacentre traffic that is not rotated. |

### Example: a scheduled complaints feed by hotel name

```json
{ "hotelNames": ["Park Hyatt Tokyo"], "maxReviewsPerHotel": 0, "reviewsSort": "lowest_rated", "maxRating": 5, "requireText": true }
```

### Example: the full corpus for a competitor set

```json
{ "startUrls": ["https://www.agoda.com/the-central-house-lisbon-baixa/hotel/lisbon-pt.html"], "maxReviewsPerHotel": 0 }
```

### Example: newest reviews only, by id, in Spanish

```json
{ "hotelIds": ["63820"], "maxReviewsPerHotel": 200, "reviewsSort": "most_recent", "locale": "es-es" }
```

## Output

```json
{
  "type": "review", "hotel_id": "63820",
  "hotel_name": "Tivoli Avenida Liberdade", "url": null, "locale": "en-us",
  "review_id": "1059514024", "rating": 10.0, "rating_5": 5.0, "rating_text": "Exceptional",
  "title": "Nice Hotel", "text": "Beautiful hotel in the center!", "positives": null, "negatives": null,
  "original_title": null, "original_text": null, "language": "en", "translated_to": "en",
  "review_date": "2025-12-15T10:54:00+07:00", "review_date_text": "December 15, 2025",
  "check_in": "2025-12-08T00:00:00+07:00", "check_out": "2025-12-14T00:00:00+07:00",
  "stay_month": "December 2025", "stay_length": null, "room_type": null, "group_type": null,
  "reviewer_name": "VARDAN", "reviewer_country": "Mozambique", "reviewer_type": null,
  "helpful_votes": 0, "unhelpful_votes": 0, "images": null,
  "source": "Agoda", "provider_id": "332",
  "responder": "Tivoli Avenida Liberdade", "response": null, "response_date": null
}
```

The free `hotel` row gives you context:

```json
{ "type": "hotel", "hotel_id": "63820", "hotel_name": "Tivoli Avenida Liberdade", "url": null, "reviews_fetched": 108, "locale": "en-us" }
```

`status` rows carry `target`, `hotel_id`, `hotel_name`, `status`, `reviews`, `filtered`, `pages`, `duplicates`, `error` and `fetched_at`, so every run says exactly what it did.

## How much does it cost?

Pay per event, one event per **delivered** review row. Free: `hotel` rows, `status` rows, every review removed by `maxRating` or `requireText`, properties with no reviews, and failed properties. A property is harvested once per run whether you give its name, its URL, its id, or all three.

A mid-size hotel is a few hundred reviews; a busy hostel can be over a thousand — 1,457 from a single property was verified in testing. `maxReviewsPerHotel` and the two filters make that a deliberate choice. Verified runs behind this listing cost $0.0002–$0.0026 each in platform compute. Exact per-row pricing is on this page's pricing tab.

## Agoda reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/agoda-reviews-scraper").call(run_input={
    "hotelNames": ["Park Hyatt Tokyo"], "maxReviewsPerHotel": 0,
    "reviewsSort": "lowest_rated", "maxRating": 5, "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["reviewer_country"], row["text"][:80])
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/agoda-reviews-scraper').call({
    hotelIds: ['63820'], maxReviewsPerHotel: 200, reviewsSort: 'most_recent',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'reviews');
```

With **curl**, synchronously:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~agoda-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"hotelIds":["63820"],"maxReviewsPerHotel":100}'
```

For **n8n**, **Make** and Zapier, add the actor as a step through Apify's integration and map `rating`, `text` and `review_date` into an alert or a sheet — "new review at or below 5/10" is two nodes. For **AI agents**, the actor is callable over Apify's MCP server. To get **agoda reviews csv**, run it and use the dataset's Export button, or append `?format=csv` to the dataset items API.

## Is it legal to scrape Agoda reviews?

This reads publicly visible property pages through the same JSON endpoint agoda.com's own review widget calls, with no login and no account. Reviews are published deliberately for anyone to read, and *hiQ v. LinkedIn* is the usual reference point for public data in the US.

Two caveats. Reviews contain **personal data** — a display name, a country and someone's words — so under GDPR you are a controller once you store them: have a lawful basis, keep them only as long as you need, and do not republish reviewer identities. This actor exposes no email, phone or full name, and has no input that would produce one. Separately, Agoda's Terms of Service discourage automated access, which makes this a terms question rather than a criminal one, with the risk on whoever operates the run. None of this is legal advice.

## Limits and honest notes

- **Agoda rates 0–10, not 1–5.** `rating` is Agoda's own number; `rating_5` is the same score halved so you can compare against five-star sources. Do not mix them.
- **Many reviews are a score with no words.** That is Agoda, not a parsing gap — `requireText` drops them if you only want written feedback.
- **`positives` and `negatives` are only present when the guest used those fields.** Older reviews often put everything in `text`.
- **A throttled request answers `200` with no reviews at all**, rather than an error. The run detects that and retries on a fresh IP, so a busy property is never reported as having none.
- **`stay_length`, `room_type` and `group_type` are frequently null** — Agoda only shows them for some reviews.
- **HTTP/2 is required** by Agoda's endpoint; over HTTP/1.1 it silently returns nothing. The actor handles this, but it is why a naive script fails.

## FAQ

### Does it need an Agoda API key or login?

No. There is no public **agoda api** for reviews to hold a key for. This calls the same endpoint agoda.com's own review widget uses, with no session and no account.

### Can I download Agoda reviews as CSV or Excel?

Yes. Every run writes an Apify dataset, exportable to CSV, Excel, JSON or XML from the Console or over the API with `?format=csv`. That is the quick path to **download agoda reviews** for one property or a whole competitor set.

### How do I get only Agoda negative reviews?

Set `maxRating` to your ceiling — `5` on Agoda's 0–10 scale is a poor stay — and `reviewsSort` to `lowest_rated`. Add `requireText: true` so you only pay for reviews with actual words. Everything above the ceiling is dropped **before** billing.

### Do I need the hotel id, or can I use the name?

Either. `hotelNames` resolves a plain name through Agoda's own autocomplete: `Park Hyatt Tokyo` became id `910` in testing, and `Tivoli Avenida Liberdade` became `63820`. Use `startUrls` if you already have the page, or `hotelIds` if a previous run gave you the number.

### How many reviews can one property return?

All of them. Agoda pages about 200 at a time and the run follows the pages, de-duplicating as it goes — 1,457 unique reviews from a single property was verified. `maxReviewsPerHotel` bounds it when you want a cheaper run.

### Are reviews translated, and which languages come back?

Every review is tagged in `language` with what the guest wrote in. Where Agoda supplies a translation into your `locale`, `text` is that translation, `translated_to` records the target and `original_text` holds the untranslated body; reviews Agoda does not translate come as written. **Multi language hotel reviews** are the normal case here, not an edge case — one property returned 18 languages.

### Does it include the hotel's replies?

Yes — `responder`, `response` and `response_date` when the property answered publicly. `responder` is also how the run recovers the hotel's name, because Agoda ships its property pages with an empty `<title>`.

### Can I use it as a general hotel review aggregator?

For Agoda's corpus, yes — and note that Agoda itself aggregates some partner reviews, which is why each row carries `source` and `provider_id`. For a true **hotel review aggregator** across several OTAs you would run this alongside scrapers for the other sites and join on the property.

### Can I scrape Agoda reviews without an API?

That is what this is — **agoda reviews without api** access, no key to apply for, no approval process. You call an Apify actor and read rows back.

### What does bulk work cost?

**Bulk hotel reviews** are billed per delivered row, so cost scales with data, not time. The two filters and the per-hotel cap cut it directly, because filtered rows are never charged.

## Review monitoring across a portfolio

Watching one property is a browser tab. Watching thirty is a data problem, and it is the job this was built for.

Schedule one run with every property you care about in `hotelNames` or `hotelIds`, sorted `most_recent`. Each run writes rows stamped with `fetched_at`, so the dataset becomes a time series without any extra work: reviews per property per week, average score by month, response rate over time. **Review monitoring** stops being a person checking pages and becomes a table you can chart.

Two settings make the scheduled version cheap. `maxReviewsPerHotel` bounds each property, and `maxRating` means a daily complaints run pays only for the reviews that need a human. A thirty-property portfolio checked daily for reviews at or below 5/10 is a handful of rows most days.

### Guest feedback data that keeps its structure

The reason this corpus is more useful than a page of text comes down to three fields most tools flatten away.

- **Separate positives and negatives.** When a guest fills Agoda's two boxes, they arrive as `positives` and `negatives` rather than one blob. Sentiment work that would otherwise need a model is a column read. This is the single biggest difference between **guest feedback data** here and elsewhere.
- **Stay context on every row.** `check_in`, `check_out`, `stay_length` and `room_type` mean a complaint is attached to a date and a room, so you can find the week or the room type that generated it.
- **The original language, preserved.** `language` says what the guest wrote in, and `original_text` keeps the untranslated body. You can route by language before spending model tokens, or check a translation you do not trust.

### What this does not do

It does not read private messages, it does not touch booking data, and it does not need or accept a login. Public reviews are the boundary, and there is no input that crosses it. It also does not return room prices — that is a different endpoint and a different product.

### Choosing between sort orders

`most_recent` is the one to schedule: it answers "what changed". `lowest_rated` is the one to run once when you inherit a property and need to know its history of problems — combined with `maxRating` it is the cheapest possible audit. `highest_rated` is useful for marketing copy, and `most_relevant` mirrors what a shopper actually sees on the page, which matters if you are trying to understand why a property converts the way it does.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Negative Reviews for Any Hotel](https://apify.com/kestrel/agoda-reviews-scraper/examples/agoda-negative-reviews)
- [Multi-Language Hotel Reviews from](https://apify.com/kestrel/agoda-reviews-scraper/examples/multi-language-hotel-reviews)
- [Hotel Reputation Monitoring on](https://apify.com/kestrel/agoda-reviews-scraper/examples/hotel-reputation-monitoring-agoda)
- [Download Reviews to CSV](https://apify.com/kestrel/agoda-reviews-scraper/examples/download-agoda-reviews-to-csv)
- [Bulk Hotel Reviews by Hotel ID](https://apify.com/kestrel/agoda-reviews-scraper/examples/bulk-hotel-reviews-by-agoda-hotel-id)
- [Guest Feedback Data with Text Only](https://apify.com/kestrel/agoda-reviews-scraper/examples/guest-feedback-data-with-text-only)
- [Competitor Reviews in Bangkok](https://apify.com/kestrel/agoda-reviews-scraper/examples/agoda-competitor-reviews-in-bangkok)
- [Ratings: Highest Rated Reviews](https://apify.com/kestrel/agoda-reviews-scraper/examples/agoda-ratings-highest-rated-reviews)
- [Hotel Reviews in German (de-de)](https://apify.com/kestrel/agoda-reviews-scraper/examples/agoda-hotel-reviews-in-german)
- [Reviews Without API Access](https://apify.com/kestrel/agoda-reviews-scraper/examples/agoda-reviews-without-api-access)
- [Hotel Review Data by Room Type](https://apify.com/kestrel/agoda-reviews-scraper/examples/hotel-review-data-by-room-type)
- [Reviews by Hotel, Most Relevant](https://apify.com/kestrel/agoda-reviews-scraper/examples/agoda-reviews-by-hotel-most-relevant)

## Related scrapers

Agoda reviews are one channel's opinion. These read the other channels and the prices behind them, with the same row shape and billing model:

- **[Agoda Prices Scraper](https://apify.com/kestrel/agoda-prices-scraper)** — Agoda hotel prices for exact dates: every property in a destination or the hotels you name, cheapest rate with taxes, cancellation terms and a per-date price calendar.
- **[TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper)** — TripAdvisor hotel reviews with six sub-ratings, trip type, photos and the management response, in 30 site languages, no browser.
- **[Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper)** — Booking.com guest reviews with liked/disliked text split, traveller type and the property's reply, filtered by language and keyword before billing.
- **[HRS Reviews Scraper](https://apify.com/kestrel/hrs-reviews-scraper)** — HRS business-travel hotel reviews with twelve category votes, positives and negatives kept apart, the hotel's replies and averages by traveller type.
- **[Kurzurlaub Reviews Scraper](https://apify.com/kestrel/kurzurlaub-reviews-scraper)** — German short-break hotel ratings (Hotelbewertungen) with per-area scores, by URL or id, complaints filtered before billing.
- **[Trip.com Reviews Scraper](https://apify.com/kestrel/trip-com-reviews-scraper)** — Trip.com and Ctrip hotel reviews with four sub-scores, the Chinese-language corpus no other OTA carries, and the hotel's replies.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site’s rate for a stay.
- **[Google Flights Scraper](https://apify.com/kestrel/google-flights-prices)** — airfare for a route and date, with a cheapest-day sweep.
- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — Airbnb prices, availability calendars and occupancy.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing, with translations.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
