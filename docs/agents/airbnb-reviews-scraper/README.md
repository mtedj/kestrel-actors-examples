# Airbnb Reviews Scraper — Guest Reviews, Ratings & Replies

An **airbnb reviews scraper** that returns every guest review a listing has, as structured rows: **airbnb ratings**, the review exactly as the guest wrote it, Airbnb's translation, the language it was written in, the reviewer, the date, the stay type and the host's public reply. It is a **scrape airbnb reviews** tool for hosts and analysts who want **airbnb review data** in bulk, not one page at a time.

Point it at listing ids, Airbnb URLs, or just a place name — a place harvests **airbnb listing reviews** for every listing it returns. No login, no cookies, no **airbnb review api** key, no browser. You pay per review row, and listings with no reviews cost nothing.

Last verified working: 2026-09-24.

## Airbnb 评论、住客评价与房东回复：中文调用与语言设置

按房源或地点获取住客评论。原文与来源翻译分别保留，适合评论分析和竞品研究。

locale 控制 Airbnb 提供的 text_localized 翻译；text 保留原文，language 表示原文语言。示例 locale="fr"；它不是只保留法语原文的筛选器。

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
  "maxReviewsPerListing": 1,
  "reviewsSort": "most_recent",
  "locale": "fr",
  "sessions": 1
}
```

Avis Airbnb / reseñas Airbnb / Airbnb Bewertungen：原文与翻译应分开分析。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## What does the Airbnb reviews scraper do?

You give it listings. It gives you their **airbnb guest reviews** as rows you can sort, filter and export.

- **`review` rows** — `rating`, `text` (original), `text_localized` (Airbnb's translation into your language), `language`, `created_at`, `date_label`, `reviewer_name`, `reviewer_id`, `reviewer_location`, `reviewer_is_superhost`, `host_reply`, `host_reply_date`, `highlight` and `stay_type`.
- **`listing` rows** — free context per listing: title, URL, how many reviews it has and how many were taken.
- **`status` rows** — free: per listing or place, what was harvested and why anything failed.

Reviews come back **in the language they were written in, with the translation alongside**. A Lisbon listing in testing returned Portuguese, Spanish, German, Korean and English reviews in one run — you keep the original and you do not have to translate it yourself.

## Airbnb reviews scraper for AI agents: which input answers which request?

Use it when the user wants the guest reviews of Airbnb listings as data: every review or the latest N of a listing, the complaints only, the review corpus of a city or a comp set, or a scheduled feed — each with the star rating, the text in its original language and Airbnb's translation, the date, the reviewer and the host's reply. Do not use it for prices or availability (`kestrel/airbnb-prices-calendar`), for occupancy (`kestrel/airbnb-occupancy-scraper`), for host contact details (not collected), for Experiences or Services (stays only), or as a "since a date" filter: there is none — take `most_recent`, stop at `created_at` yourself, and expect every delivered review to be billed.

| The user asks for | Input |
|---|---|
| All reviews of a listing | `{"listingIds": ["11562247"], "maxReviewsPerListing": 0}` |
| The latest 20 reviews of a listing URL | `{"startUrls": ["https://www.airbnb.com/rooms/11562247"], "maxReviewsPerListing": 20}` (`most_recent` is the default order) |
| Negative reviews, complaints only | add `"reviewsSort": "lowest_rated", "minRating": 3` (3 stars and below; the rest are never billed) |
| Reviews of every listing in a city | `{"locationQueries": ["Lisbon, Portugal"], "maxListingsPerQuery": 50, "maxReviewsPerListing": 100}` |
| Reviews of a comp set or portfolio, weekly | `{"listingIds": ["11562247", "45307024"], "maxReviewsPerListing": 20}` on an Apify schedule |
| Reviews translated into Spanish, originals kept | add `"locale": "es"` |
| Listings whose negative reviews got no host reply | run with `"minRating": 3` and keep rows where `host_reply` is null |
| How many reviews each listing has | the free `listing` row's `reviews_total` |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `maxReviewsPerListing` × listings bounds the rows |

The bill is one event per delivered `review` row: by default up to 100 per listing; `minRating` drops reviews before billing (a 441-review listing returned 4 rows under `minRating: 3`).

Rows come in three types. `review`: `id` (the listing), `url`, `name`, `reviews_total`, `review_id`, `rating` (a string, `"1"` to `"5"`), `text`, `text_localized`, `language`, `created_at`, `date_label`, `reviewer_name`, `reviewer_id`, `reviewer_location`, `reviewer_is_superhost`, `host_reply`, `host_reply_date`, `highlight`, `stay_type`, `fetched_at`. `listing` (free, on by default): `reviews_total`, `reviews_fetched`. `status`: one per listing or place with `status` (`ok`, `unknown_area`, `no_results`, `error`), `reviews`, `filtered`, `duplicates`, `error`; never charged. A listing with no reviews, an unknown place or an empty search is a `status` row that says why, not a failed run.

## Scrape Airbnb reviews three ways

Most tools make you find listing ids first. This one does not:

- **`listingIds`** — numeric ids like `11562247`, the fastest input when you already know the listings.
- **`startUrls`** — listing URLs (`/rooms/12345678`) or search URLs (`/s/Lisbon--Portugal/homes`). A search URL harvests every listing it returns.
- **`locationQueries`** — a place typed as you would on Airbnb: `Lisbon, Portugal`, `Algarve`. This is how you get **airbnb reviews for a city** without assembling a list by hand.

Give a place and a listing that sits inside it and they de-duplicate: the listing is harvested once, and you are billed once.

## Airbnb negative reviews without paying for the happy ones

`minRating` is the feature that changes the economics. Set it to 3 and only reviews rated 3 or below are delivered — **and only those are billed**. The five-star reviews are filtered before you pay for them.

In a verified run, a listing with 441 reviews returned **4 rows** under `minRating: 3`. That is $0.02 instead of $2.205 for the same question: what are guests actually complaining about. For **review monitoring** and **guest feedback data** on a portfolio, this is usually the only setting that matters.

## Airbnb review data for hosts, managers and analysts

- **Reputation monitoring.** Schedule a daily run ordered by `most_recent` and every new review lands with its rating and text. Nothing to poll, nothing to diff.
- **Competitor research.** Point a place at it and pull the **airbnb competitor reviews** corpus for a whole market — what guests praise, what they complain about, which hosts bother to reply.
- **Airbnb sentiment analysis.** A rated, dated, multi-language corpus with the original text intact is exactly the shape sentiment and topic models want. `language` lets you split or route by language before you spend tokens on it.
- **Airbnb property management reviews.** Reviews carry `host_reply` and `host_reply_date`, so you can find listings where guests were left unanswered.
- **Airbnb host reviews.** `reviewer_is_superhost` flags reviewers who host themselves, which is a useful signal when you are weighing whose opinion carries weight in a market.
- **Vacation rental reviews** and **short term rental reviews** benchmarking across a market, rather than one listing at a time.

## Input

| Field | What it does |
| --- | --- |
| `listingIds` | Numeric Airbnb listing ids, e.g. `11562247`. |
| `startUrls` | Listing URLs (`/rooms/12345678`) or search URLs (`/s/Lisbon--Portugal/homes`). |
| `locationQueries` | Places as you would type them on Airbnb: `Lisbon, Portugal`, `Algarve`. |
| `maxListingsPerQuery` | How many listings to take from each place before harvesting their reviews. |
| `maxReviewsPerListing` | `0` = every review the listing has (Airbnb pages them 50 at a time). `N` = the first N in your chosen order. The main cost control. |
| `reviewsSort` | `most_recent`, `highest_rated`, `lowest_rated`, `most_relevant`. |
| `minRating` | `0` = keep everything. `1`–`5` = keep only reviews at or below that rating. Filtered reviews are never charged. |
| `locale` | Language for the translations (`en`, `es`, `fr`, `de`…). The original text always comes too. |
| `includeListingRow` | Emit the free per-listing context row. |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. Required — Airbnb blocks datacentre traffic that is not rotated. |

### Example: a scheduled complaints feed across a portfolio

```json
{ "listingIds": ["11562247", "45307024"], "maxReviewsPerListing": 0, "reviewsSort": "lowest_rated", "minRating": 3 }
```

### Example: the review corpus for a whole market

```json
{ "locationQueries": ["Lisbon, Portugal"], "maxListingsPerQuery": 50, "maxReviewsPerListing": 100 }
```

### Example: newest reviews only, from a search you already built

```json
{ "startUrls": ["https://www.airbnb.com/s/Lisbon--Portugal/homes?room_types%5B%5D=Entire%20home%2Fapt"], "maxReviewsPerListing": 20 }
```

## Output

```json
{
  "type": "review", "id": "11562247", "url": "https://www.airbnb.com/rooms/11562247",
  "name": "Charming studio in Baixa", "reviews_total": 441, "locale": "en",
  "review_id": "1752111840493470784", "rating": "5",
  "text": "El departamento es muy lindo. Esta todo muy bien ubicado.",
  "text_localized": "The apartment is very nice. Everything is very well located.",
  "language": "es", "created_at": "2026-08-14T10:53:27Z", "date_label": "1 week ago",
  "reviewer_name": "Luis Armando", "reviewer_id": "313623872",
  "reviewer_location": "Buenos Aires, Argentina", "reviewer_is_superhost": false,
  "host_reply": null, "host_reply_date": null, "highlight": null, "stay_type": null
}
```

The free `listing` row gives you context, and `status` rows tell you what happened:

```json
{ "type": "listing", "id": "11562247", "url": "https://www.airbnb.com/rooms/11562247", "name": "Charming studio in Baixa", "reviews_total": 441, "reviews_fetched": 100, "locale": "en" }
```

`reviews_total` is what Airbnb reports for the listing, so you can always see whether you took all of them. Status rows carry `listing_id`, `query`, `listings`, `reviews`, `filtered`, `duplicates`, `fetched_at` and any `error`. Every row — review, listing and status — carries `fetched_at`, which is what turns repeated runs into a time series.

## How much does it cost?

Pay per event, one event per **delivered** review row. Free: `listing` rows, `status` rows, reviews removed by `minRating`, listings with no reviews, unrecognised places, and failed jobs. A listing is harvested once per run however many inputs point at it.

A listing with 441 reviews is 441 rows if you ask for all of them — `maxReviewsPerListing` and `minRating` are there to make that a deliberate choice. Verified runs behind this listing cost $0.0002–$0.0003 each in platform compute. Exact per-row pricing is on this page's pricing tab.

## Airbnb reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/airbnb-reviews-scraper").call(run_input={
    "listingIds": ["11562247"], "maxReviewsPerListing": 0, "reviewsSort": "lowest_rated", "minRating": 3,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["language"], row["text"][:80])
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/airbnb-reviews-scraper').call({
    locationQueries: ['Lisbon, Portugal'], maxListingsPerQuery: 20, maxReviewsPerListing: 50,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'reviews');
```

With **curl**, synchronously:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~airbnb-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"listingIds":["11562247"],"maxReviewsPerListing":50}'
```

For **n8n**, **Make** and Zapier, add the actor as a step through Apify's integration and map `rating`, `text` and `created_at` into your alert or sheet — a "new review below 4 stars" notification is two nodes. For **AI agents**, the actor is callable over Apify's MCP server, so an agent can ask for a listing's reviews and read them back directly; the section "Airbnb reviews scraper for AI agents" above maps each request to its input. To get **airbnb reviews csv**, run it and use the dataset's Export button, or append `?format=csv` to the dataset items API.

## Is it legal to scrape Airbnb reviews?

This reads publicly visible listing pages through the same public API the airbnb.com front-end uses, with no login and no account. Reviews are published deliberately for anyone to read, and *hiQ v. LinkedIn* is the usual reference point for scraping public data in the US.

Two caveats worth taking seriously. First, reviews contain **personal data** — a reviewer's first name, their stated location and their words. Under GDPR that makes you a controller when you store them: have a lawful basis, keep them no longer than you need, and do not re-publish reviewer identities. This actor deliberately exposes no email, phone or full name, and there is no input that would make it. Second, Airbnb's Terms of Service discourage automated access, so this is a terms question, and the risk sits with whoever operates the run. None of this is legal advice — if your use is commercial or large, ask a lawyer.

## Limits and honest notes

- **`rating` is a string** as Airbnb returns it (`"5"`), not a number. Cast it if you are aggregating.
- **`reviewer_location` is self-declared** and often blank — treat it as a hint, not a fact.
- **Translations are Airbnb's**, not ours. `text` is always the original; `text_localized` is only present when Airbnb translated it.
- **An unrecognised place is reported, not guessed.** Airbnb answers a nonsense place with listings from all over the world; the run detects that, marks the job `unknown_area` and charges nothing.
- **Airbnb pages reviews 50 at a time.** Deep listings take several requests; `maxReviewsPerListing` bounds it.
- **No host contact details.** Not scraped, not exposed, not an input — by design.

## FAQ

### Does it need an Airbnb API key, login or cookies?

No. There is no public **airbnb review api** to hold a key for. This uses the same public GraphQL endpoint airbnb.com's own front-end calls, with no session, and it refreshes Airbnb's query hashes automatically if they change.

### Can I download Airbnb reviews as CSV or Excel?

Yes. Every run writes an Apify dataset, which exports to CSV, Excel, JSON or XML from the Console, or over the API with `?format=csv`. That is the short path to **download airbnb reviews** for a listing or a market.

### How do I get only Airbnb negative reviews?

Set `minRating` to the ceiling you care about — `2` for one- and two-star, `3` to include mediocre stays — and `reviewsSort` to `lowest_rated`. Reviews above the ceiling are dropped **before** billing, so a complaints feed on a heavily reviewed listing costs cents.

### Can I get reviews for every listing in a city?

Yes, with `locationQueries` plus `maxListingsPerQuery`. Airbnb caps a single search at roughly 280 listings, so for a large city, run several searches with different filters (price bands, room types) and let the de-duplication merge them.

### Are reviews translated?

Each review carries `language` (what it was written in) and `text` (the original). When Airbnb offers a translation into your `locale`, it arrives as `text_localized`. So **airbnb review translation** is available without you calling a translation API, and the source text is never lost.

### Does it include host replies?

Yes — `host_reply` and `host_reply_date` when the host answered publicly. That is how you find listings where negative reviews were left unaddressed.

### How many reviews can one listing return?

All of them. Airbnb pages 50 at a time and the run follows the pages until it has what you asked for; 300 unique reviews from a single listing was verified in testing. `reviews_total` tells you how many exist, so you can check you got the lot.

### Can I scrape Airbnb reviews without an API?

That is exactly what this is — **airbnb reviews without api** access, no key to apply for and no approval process. You call an Apify actor and read rows back.

### What does a run cost for bulk work?

**Bulk airbnb reviews** are billed per delivered row, so cost scales with data rather than with time. Filtering with `minRating` or capping with `maxReviewsPerListing` cuts it directly — those rows are never charged.

### Which languages and locales are supported?

Any locale Airbnb supports for translations — `en`, `es`, `fr`, `de`, `pt`, `it`, `ja`, `ko` and the rest. Set `locale` and `text_localized` follows it. The `language` field is independent: it tells you what the guest actually wrote in.

## Airbnb reviews by listing, by market, or on a schedule

The three input modes exist because three different jobs need different shapes.

**Airbnb reviews by listing** is the host's job. You own five properties, you want every new review the moment it appears, and you want the ones below four stars in front of you. Give `listingIds`, sort `most_recent`, schedule it daily. The `listing` row tells you `reviews_total` so you can see growth without counting rows.

**By market** is the analyst's job. You are pricing a portfolio, judging a city, or building comps. Give `locationQueries` with `maxListingsPerQuery` and you get the review corpus for a market in one run — every listing's reviews, tagged with the listing they came from.

**On a schedule** is where the value compounds. Airbnb shows you reviews; it does not show you *change*. Because every row is stamped with `fetched_at`, a weekly run turns into a dataset that answers questions Airbnb's own interface cannot: which listings are gaining reviews fastest, whose ratings are slipping, which complaints repeat across a market and which are one bad night.

### What this does not do

It does not scrape hosts' contact details, it does not touch private messages, and it does not need or accept an Airbnb login. Reviews are the public record of a stay; that is the boundary, and the actor has no input that crosses it.

### Reviews as a data product

Three things make this corpus more useful than a page of text:

- **The original language is preserved.** Most tools translate and discard. Keeping `text` alongside `text_localized` means you can run language-specific models, or check a translation you do not trust.
- **The rating is separable from the words.** `rating` and `text` are distinct fields, so you can weight them independently — a four-star review with an angry paragraph is a different signal from a four-star review with "fine".
- **Replies are attached.** `host_reply` sits on the same row as the review it answers, so response rate and response tone are one `GROUP BY` away.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Negative Reviews Across a Market](https://apify.com/kestrel/airbnb-reviews-scraper/examples/airbnb-negative-reviews)
- [Sentiment Analysis Dataset (CSV)](https://apify.com/kestrel/airbnb-reviews-scraper/examples/airbnb-reviews-for-sentiment-analysis)
- [Bulk Reviews by Listing ID](https://apify.com/kestrel/airbnb-reviews-scraper/examples/bulk-airbnb-reviews-by-listing-id)
- [Scrape Reviews from a Search URL](https://apify.com/kestrel/airbnb-reviews-scraper/examples/scrape-airbnb-reviews-from-a-search-url)
- [Host Reviews, Highest Rated First](https://apify.com/kestrel/airbnb-reviews-scraper/examples/airbnb-host-reviews-highest-rated-first)
- [Review Translation into Spanish](https://apify.com/kestrel/airbnb-reviews-scraper/examples/airbnb-review-translation-into-spanish)
- [Download Reviews for One Listing](https://apify.com/kestrel/airbnb-reviews-scraper/examples/download-airbnb-reviews-for-one-listing)
- [Review Monitoring for Your Own Listings](https://apify.com/kestrel/airbnb-reviews-scraper/examples/review-monitoring-for-your-own-listings)
- [Reviews for a City, by Listing](https://apify.com/kestrel/airbnb-reviews-scraper/examples/airbnb-reviews-for-a-city-by-listing)
- [Competitor Reviews for a Comp Set](https://apify.com/kestrel/airbnb-reviews-scraper/examples/airbnb-competitor-reviews-for-a-comp-set)

## Related scrapers

Reviews tell you how a stay went; prices and availability tell you what it costs and when it is free. These share the same row shape and billing model:

- **[Trip.com Reviews Scraper](https://apify.com/kestrel/trip-com-reviews-scraper)** — Trip.com (Ctrip) hotel guest reviews by URL or hotel id, filtered by language before billing.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site’s rate for a stay.
- **[Google Flights Scraper](https://apify.com/kestrel/google-flights-prices)** — airfare for a route and date, with a cheapest-day sweep.
- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — Airbnb prices, availability calendars and occupancy.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
