# Kurzurlaub Reviews Scraper - Hotel Reviews, Gästebewertungen

A **kurzurlaub reviews scraper** that returns every guest rating a hotel has on Kurzurlaub.de, as structured rows: the overall score on the site's 1–6 scale (6 is the best), the per-area scores the guest gave for the hotel, rooms, service, food, leisure, location and value, the title, the comment when the guest wrote one, the reviewer's first name and the date. **Hotelbewertungen** and **gästebewertungen** are what the site calls them; this turns **kurzurlaub hotel reviews** into **hotel review data** you can sort, filter and export — a **hotel review scraper** for the German short-break market, built for bulk work rather than one page at a time. If you have been searching for **kurzurlaub bewertungen** as a dataset instead of a web page, this is it.

Give it Kurzurlaub hotel URLs or the site's numeric hotel ids. No login, no API key, no browser, no token. It bills per rating row, and three controls cut what you pay for *before* you are billed.

Last verified working: 2026-08-29.

## Kurzurlaub 德国酒店评价与住客评分：中文调用与语言设置

读取酒店公开评价、1–6 分评分和服务、餐饮等分类分数。保持来源分制，不能直接当作五星制。

来源主要为德语，没有 locale 或翻译输入。中文说明用于帮助调用；评论原文不会自动翻译。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.kurzurlaub.de/hotel/rhein_lahn_taunus/hachenburg/parkhotel-hachenburg.html"
  ],
  "maxReviewsPerHotel": 1,
  "sessions": 1
}
```

Deutsch: Kurzurlaub Hotelbewertungen und Gästebewertungen auslesen; Originaltexte und die Skala von 1 bis 6 bleiben erhalten.

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Kurzurlaub scraper for AI agents: which input answers which request?

Use this actor when the request names Kurzurlaub or kurzurlaub.de and wants guest ratings (Hotelbewertungen, Gästebewertungen), the 1-6 scores, the category scores, titles and comments, or a property's averages for hotels you can identify by URL or id. Do not use it to find hotels by city or name (there is no search: take the URL from kurzurlaub.de first), for prices or availability (the free hotel row carries only the offer price range), for hotel replies (the site publishes none), for translations (everything is in German), or for a sorted "worst first" list (ratings come newest first; filter with `maxScore` instead).

| user request | input JSON |
|---|---|
| every rating of one Kurzurlaub hotel | `{"startUrls": ["https://www.kurzurlaub.de/hotel/rhein_lahn_taunus/hachenburg/parkhotel-hachenburg.html"], "maxReviewsPerHotel": 0}` |
| the 30 newest ratings of hotel 15699 | `{"hotelIds": ["15699"], "maxReviewsPerHotel": 30}` |
| negative reviews, complaints, what guests disliked, across the whole history | `{"hotelIds": ["15699"], "maxScore": 4, "maxReviewsPerHotel": 0}` |
| praise only, quotes for marketing | `{"hotelIds": ["15699"], "minScore": 5.5}` |
| only new reviews since the last run (daily schedule) | `{"hotelIds": ["15699", "5382"], "sinceDate": "2 days"}` |
| compare competitors on rooms, food or value | `{"hotelIds": ["15699", "5382"], "maxReviewsPerHotel": 1}` then read `category_averages` on the free `hotel` rows |
| Kurzurlaub Bewertungen, Hotelbewertungen, Wellness-Hotel Gästebewertungen | the same inputs; every Bewertung is delivered in German with English column names |

Every row carries `type`. A `review` row (billed, $0.004) has `review_id`, `hotel_id`, `hotel_name`, `score` (1-6, 6 is best), `category_scores` (`hotel`, `room`, `service`, `food`, `leisure` = Freizeit- und Wellnessangebote, `location`, `value`), `title`, `text` (null when the guest wrote no comment), `reviewer`, `review_date` and `url`. A `hotel` row (free, one per hotel while `includeHotelRow` is true) has `stars`, `street`, `city`, `region`, `country`, `rating`, `rating_word`, `review_count`, `category_averages` and `price_range`. A `status` row (free, one per input) says `status` `ok`, `no_reviews` or `error` (an unknown id is an error with the reason, free), with `reviews` delivered, `filtered` (removed by a filter, never billed), `pages` read and `total` (the site's rating count). `maxScore` and `minScore` are applied to the newest `maxReviewsPerHotel` ratings fetched, so set the cap to 0 to scan a whole history; `sinceDate` stops paging as soon as the date is passed. An input the actor cannot act on (a URL from another site, an id that is not a number, an empty list) ends the run with no rows and the reason on the run card, nothing charged; a source that blocks every hotel fails the run loudly.

### Kurzurlaub Bewertungen auf Deutsch

Kurzurlaub.de ist das Portal für den Kurzurlaub und das Wellness-Wochenende, und jede Hotelbewertung dort ist auf Deutsch geschrieben. Der Scraper liefert jede Gästebewertung einer Hotelseite als Zeile: Gesamtnote 1-6, Kategoriebewertungen für Zimmer, Service, Gastronomie, Freizeit und Wellness, Lage und Preis-Leistung, Titel, Kommentar und Datum. `maxScore: 4` behält nur die schlechten Bewertungen, `sinceDate: "30 days"` nur die neuen.

## What does the Kurzurlaub reviews scraper do?

You give it hotels. It gives you their **kurzurlaub.de reviews** as rows.

- **`review` rows** — `review_id`, `hotel_id`, `hotel_name`, `url`, `score` (1–6), `category_scores` (an object with the areas the guest rated: `overall`, `hotel`, `room`, `service`, `food`, `leisure`, `location`, `value`), `title`, `text` (the comment, when there is one), `reviewer` (a first name, or `Gast`), `review_date`, `fetched_at`.
- **`hotel` rows** — free context per property: `hotel_id`, `hotel_name`, `url`, `stars`, `street`, `postal_code`, `city`, `region`, `country`, the overall `rating` with its `rating_word` (Exzellent, Sehr gut, Gut…), `review_count`, `category_averages` (the same areas, averaged over every rating), `price_range` of the hotel's current offers, `reviews_fetched` and `fetched_at`.
- **`status` rows** — free: per input `target`, the `hotel_id` and `hotel_name`, a `status` of `ok`, `no_reviews` or `error`, how many `reviews` were delivered, how many were `filtered`, how many `pages` were read, the site's `total`, a `duplicates` flag, the `error` if any, and `fetched_at`.

Ratings arrive newest first, which is the order the site lists them in. Every row of a type carries every column, so a CSV export is rectangular.

## Kurzurlaub reviews by hotel, by URL or by id

- **`startUrls`** — hotel pages such as `https://www.kurzurlaub.de/hotel/rhein_lahn_taunus/hachenburg/parkhotel-hachenburg.html`. The page is read once: it carries the hotel's id, name, star class, address and offer price range.
- **`hotelIds`** — the numeric id directly, e.g. `15699`. It is the `o_id` behind the site's "Alle Bewertungen" button and what an earlier run's `hotel_id` gives you. This is the **kurzurlaub reviews by hotel id** path, and it skips the page read.

A URL and its id count as the same hotel and are harvested once, so mixing inputs never double-bills. Hotel names are not an input: the site has no public search endpoint the actor could resolve them against, and guessing would bill you for the wrong property.

## Hotelbewertungen without paying for the happy ones

Three controls run **before** billing, and together they are the reason a complaints feed is affordable:

- **`maxScore`** keeps only ratings at or below a score. On this scale 6 is the best and a 4 is a middling stay, so `maxScore: 4` is a complaints feed.
- **`minScore`** keeps only ratings at or above a score — the praise feed, or combined with `maxScore` a band.
- **`sinceDate`** keeps only ratings from a date on. Because the site lists ratings newest first, paging stops the moment the date is passed, so older ratings are never fetched, let alone charged. Relative dates (`"30 days"`, `"6 weeks"`, `"3 months"`) keep a schedule from going stale.

Filtered ratings are never charged. A hotel with two hundred ratings and six complaints delivers six rows under `maxScore: 4`. You pay for six. That is what makes **kurzurlaub negative reviews** monitoring across a portfolio practical.

## Hotel review data for revenue, ops and analysts

- **Hotel reputation monitoring.** Schedule a daily run with `sinceDate: "2 days"`; every new rating arrives with its score, area scores and comment, and `review_id` is stable across runs, so deduping is a set lookup.
- **Kurzurlaub competitor reviews.** Point it at the properties you compete with in a region and pull their whole corpus: which areas score low, whether the food or the wellness offer drags the average, what guests title their stays.
- **German hotel reviews at scale.** The site is where German-speaking travellers rate short breaks, spa stays and city trips — **wellness hotel reviews** and **short break hotel reviews** that do not appear on the global OTAs. For a hotel group in the DACH market this is a first-party voice-of-guest source in the guests' own language.
- **Guest feedback data with structure.** Per-area scores let you find *which* area generates the low overall scores before any text model runs; `category_averages` on the hotel row gives you the benchmark to compare each rating against.
- **Bulk hotel reviews for a market study.** Thousands of hotels across a country, one run, one dataset, rows that all look the same.

## Input

| Field | What it does |
| --- | --- |
| `startUrls` | Kurzurlaub hotel pages. Read once for the hotel's id, name, stars and address. |
| `hotelIds` | The site's numeric hotel ids, e.g. `15699` — the fastest input. |
| `maxReviewsPerHotel` | `0` = every rating the hotel has (the site pages them 10–20 at a time). `N` = the newest N. The main cost control. |
| `maxScore` | `0` = keep everything. `1`–`6` = keep only ratings at or below that score. Filtered ratings are never charged. |
| `minScore` | `0` = keep everything. `1`–`6` = keep only ratings at or above that score. |
| `sinceDate` | Empty = no date limit. `YYYY-MM-DD` or relative (`"30 days"`, `"3 months"`). Paging stops once the date is passed. |
| `includeHotelRow` | Emit the free per-hotel context row (name, stars, address, scores, rating count, averages, price range). |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. The default datacenter group is enough for the site. |

### Example: a scheduled complaints feed

```json
{
  "startUrls": ["https://www.kurzurlaub.de/hotel/rhein_lahn_taunus/hachenburg/parkhotel-hachenburg.html"],
  "maxReviewsPerHotel": 0,
  "maxScore": 4,
  "sinceDate": "30 days"
}
```

### Example: the full corpus for a competitor set, by id

```json
{
  "hotelIds": ["15699", "5382", "9813"],
  "maxReviewsPerHotel": 0
}
```

### Example: the newest 50 ratings of one hotel, no hotel row

```json
{
  "hotelIds": ["5382"],
  "maxReviewsPerHotel": 50,
  "includeHotelRow": false
}
```

## Output

One dataset, three row types, told apart by `type`. A review row looks like this:

```json
{
  "type": "review",
  "review_id": "0c7efb112a9c5d7d",
  "hotel_id": "5382",
  "hotel_name": "Astralis Hotel Domizil",
  "url": "https://www.kurzurlaub.de/hotel/unterer_neckar/walldorf_neckar/astralis-hotel-domizil-walldorf.html",
  "score": 5.7,
  "category_scores": {"hotel": 6.0, "room": 6.0, "service": 6.0, "food": 5.3, "leisure": 6.0, "location": 5.0},
  "title": "Heidelberg - Ich hab mein Herz verloren... - 2 Tage",
  "text": "Es war alles super 👍",
  "reviewer": "Elke",
  "review_date": "2026-08-24",
  "fetched_at": "2026-08-29T10:20:00+00:00"
}
```

And the hotel row for the same property:

```json
{
  "type": "hotel",
  "hotel_id": "5382",
  "hotel_name": "Astralis Hotel Domizil",
  "url": "https://www.kurzurlaub.de/hotel/unterer_neckar/walldorf_neckar/astralis-hotel-domizil-walldorf.html",
  "stars": 4,
  "street": "Schwetzinger Str. 50",
  "postal_code": "69190",
  "city": "Walldorf",
  "region": "Unterer Neckar",
  "country": "Deutschland",
  "rating": 5.2,
  "rating_word": "Sehr gut",
  "review_count": 289,
  "category_averages": {"hotel": 5.3, "room": 5.2, "service": 5.4, "food": 5.2, "leisure": 4.8, "location": 5.4},
  "price_range": "79,00 EUR - 578,00 EUR",
  "reviews_fetched": 289,
  "fetched_at": "2026-08-29T10:20:00+00:00"
}
```

The dataset ships with five views: **Overview**, **Ratings** (every review field), **Low scores** (the complaints feed), **Hotels** (`stars`, `city`, `region`, `country`, scores, `review_count`, `price_range`, `reviews_fetched`) and **Run status** (`target`, `status`, `reviews`, `filtered`, `pages`, `total`, `duplicates`, `error`). Export any of them as CSV, Excel, JSON or XML from the Apify console or the API — that is the **kurzurlaub reviews csv** path, and the **download kurzurlaub reviews** path when a spreadsheet is what someone asked for.

## How much does it cost?

**$0.004 per rating row.** Hotel rows, status rows, filtered ratings, hotels with no ratings, unknown ids and failed hotels are free. A 205-rating property costs $0.82 in full; the same property as a daily complaints feed costs a fraction of a cent per day. Compute and proxy usage for the run are included in the event price.

**Bulk hotel reviews** at scale: 3,000 hotels × 100 newest ratings = 300,000 rows = $1,200, delivered in an afternoon with 16 sessions. The pocket's other actor charges about the same per row; the difference is the per-area scores, the date stop and what you never pay for.

## Kurzurlaub reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/kurzurlaub-reviews-scraper").call(run_input={
    "hotelIds": ["15699"],
    "maxReviewsPerHotel": 0,
    "maxScore": 4,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["score"], row["review_date"], row["title"], row["category_scores"])
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/kurzurlaub-reviews-scraper').call({
    startUrls: ['https://www.kurzurlaub.de/hotel/rhein_lahn_taunus/hachenburg/parkhotel-hachenburg.html'],
    maxReviewsPerHotel: 200,
    sinceDate: '90 days',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const ratings = items.filter((r) => r.type === 'review');
console.log(ratings.length, 'ratings; with a comment:', ratings.filter((r) => r.text).length);
```

curl (synchronous, returns the dataset):

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~kurzurlaub-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["15699"], "maxReviewsPerHotel": 50}'
```

**n8n / Make / Zapier.** Use the HTTP Request node against the URL above, or the Apify node with the actor id. A Schedule trigger → Apify → filter `type == "review"` → Slack/Sheets is a complete **review monitoring** workflow; keep a set of seen `review_id` values in workflow static data and only the new ones reach the channel. Verified n8n templates for the same pattern on Agoda and Airbnb are in the [kestrel examples repo](https://github.com/mtedj/kestrel-actors-examples) and port in minutes.

**MCP / AI agents.** The actor is available through Apify's MCP server, so a Claude, Cursor or custom agent can call `kurzurlaub-reviews-scraper` with a hotel URL and reason over the rows. Every field is documented in the dataset schema, which is what agents read.

## Is it legal to scrape Kurzurlaub reviews?

The actor reads pages and the ratings fragment the site serves to any visitor without logging in, and it stores what the page shows: the score, the title, the comment, the reviewer's first name (or "Gast") and the date. It does not access accounts, private data or anything behind a login. Ratings are user-generated content, and a first name is personal data under the GDPR — process it lawfully for your purpose (analytics, monitoring, research), store it no longer than you need, and read the site's terms before scraping at scale. This is data collection, not legal advice.

## Limits and honest notes

- Many ratings on the site are a title and scores only. `text` is filled when the guest wrote a comment and `null` when not; the actor does not invent prose. Do not expect every row to carry a paragraph.
- The site gives ratings no id. `review_id` is a stable hash of hotel, date, score, title, reviewer and comment, so the same rating hashes the same on every run; two identical anonymous ratings on the same day would collapse into one row.
- Pages carry 10 to 20 ratings depending on the property. The actor follows the site's own "next" link until it runs out, so it never guesses page counts.
- A page that is not a ratings fragment (an error page, an empty answer) is retried on a fresh IP with backoff, and the hotel is reported as `error` if every attempt fails. It is never reported as `no_reviews`, because a false "no reviews" corrupts your dataset silently while a false error costs one retry.
- An unknown id is reported as an error on its status row, free, without retrying. A hotel page with no ratings block is a hotel with no ratings: `no_reviews`, `total: 0`, free.
- The site is German. Titles, comments, rating words and region names come back in German; the column names and the area keys in `category_scores` are English.
- The star class is the Hotelstars Union rating the site displays; a few properties carry none.

## FAQ

### Does it need a Kurzurlaub API key or login?

No. It loads the same ratings fragment the site's own "Alle Bewertungen" button loads. There is no public API for **kurzurlaub bewertungen**, and this is how to get **kurzurlaub reviews without api** access.

### Can I download Kurzurlaub reviews as CSV or Excel?

Yes. Every run writes an Apify dataset; open the **Ratings** view and export it as CSV, Excel, JSON or XML, or fetch it from the API with `?format=csv`.

### How do I get only Kurzurlaub negative reviews?

Set `maxScore` to `4` (or whatever your threshold is). Only the low ratings are delivered and billed; the site orders ratings newest first, so pair it with `sinceDate` for a rolling feed.

### What does the 1–6 score mean?

The site scores on a six-point scale where **6 is the best** ("Exzellent" starts around 5.5, "Sehr gut" around 5) and 1 is the worst. It is points, not German school grades — do not invert it. `rating_word` on the hotel row is the site's own label for the property's average.

### Do I need the hotel id, or can I use the URL?

Either. A URL is read once for the id and the hotel's details; the id skips that read. The id is also `hotel_id` on every row, so a first run by URL gives you the ids for every run after.

### How many ratings can one hotel return?

All of them — set `maxReviewsPerHotel` to `0`. The actor walks the site's pages, newest first, until the last one and dedupes by `review_id`.

### Are the reviews in German?

Yes, as written: titles, comments and the site's own labels are German. The row structure, the area keys and the status words are English, so the dataset slots into an English pipeline without translation.

### Does it include the hotel's replies?

No — the site does not publish hotel replies on the ratings it lists, so there is nothing to scrape. Trip.com and Agoda do; see the related actors below.

### Can I use it as a general hotel review aggregator?

For the German short-break market, yes. For a true **hotel review aggregator** across OTAs, pair it with the Agoda, Trip.com and Airbnb review scrapers below — the rows share the same shape, so one table holds all four.

### What does bulk work cost?

$0.004 per rating, nothing else from the actor. 10,000 ratings is $40. See the cost section above for the platform-usage note.

### Why does a run report fewer ratings than the site's total?

`total` is what the site states for the property; `reviews` is what you asked for and kept. `maxReviewsPerHotel`, `maxScore`, `minScore` and `sinceDate` all reduce the delivered count, and `filtered` on the status row says how many rows the filters removed.

## Review monitoring across a portfolio

The pattern that works: one run per day, `sinceDate: "2 days"`, `maxReviewsPerHotel: 0`, every property in `hotelIds`. Keep the `review_id` values you have seen; the new rows are the day's ratings. Because filtered rows are free, you can run the same schedule twice — once unfiltered for the record, once with `maxScore: 4` straight into the on-call channel — and pay only for what each delivers.

### Guest feedback data that keeps its structure

**Guest feedback data** loses most of its value when it is flattened to a number and a sentence. Every row here keeps the per-area scores, so "the rooms score fine but the food drags every stay below five" is a filter, not a research project — and `category_averages` on the hotel row is the baseline each rating deviates from. That is the difference between **hotel guest reviews** as anecdotes and as a dataset, and it holds for **german hotel reviews** just as it does for the global platforms.

### What this does not do

It does not write ratings, vote on them, or touch anything behind a login. It does not translate. It does not pull offers or prices beyond the `price_range` the hotel page states — for prices, see the hotel price actors below.

### Scrape Kurzurlaub reviews on a schedule, not by hand

The site's ratings modal is fine for reading one hotel. It is not a way to watch forty. **Scrape kurzurlaub reviews** once a day with the inputs above, and the modal becomes a table with a date column.

## Related scrapers

Kurzurlaub is one window on a hotel's reputation. These read the rest, and they share the same row shape, the same pay-per-delivered-row billing and the same scheduling story:

- **[Zoover Reviews Scraper](https://apify.com/kestrel/zoover-reviews-scraper)** — Dutch and German holiday reviews from Zoover, with per-aspect scores and the owner's reply.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives, by hotel name, URL or id.
- **[Trip.com Reviews Scraper](https://apify.com/kestrel/trip-com-reviews-scraper)** — Trip.com and Ctrip hotel reviews with four sub-scores and the hotel's replies.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site's rate for a stay.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — one row per hotel with every OTA's rate side by side and the parity math done.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
