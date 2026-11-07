# HRS Reviews Scraper - Hotel Reviews, Guest Reviews, Ratings

Every commented guest rating of any hotel on HRS (hrs.com), Europe's business-travel booking platform — **hrs hotel reviews** and **hrs ratings** as clean rows: the 0-10 score with twelve category votes, what the guest liked and disliked, the hotel's replies, traveller type and age group, stay dates, nights and the language of the comment — plus one free row per property with its averages by traveller type and by category. Give the **HRS reviews scraper** hotel URLs or hotel ids and it returns the **hotel guest reviews** as a dataset you can export to CSV, Excel or JSON, feed to n8n or Make, or hand to an AI agent over MCP. No login, no browser, no HRS API key.

Last verified working: 2026-08-29.

Pay per review row delivered. Filtered reviews, unknown hotels, hotel rows and status rows are free.

## HRS 酒店评论、商务旅客评价与分类评分：中文调用与语言设置

读取酒店评论、优缺点、酒店回复及分类评分。可按旅客类型与原文语言筛选。

languages=["de"] 只保留德语原文；language="zh_cn" 仅设置酒店页面标签语言。两个字段用途不同，不会把评论自动翻译成中文。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.hrs.com/en/hotel/10520"
  ],
  "maxReviewsPerHotel": 1,
  "reviewsSort": "most_recent",
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": [
      "RESIDENTIAL"
    ]
  },
  "languages": [
    "de"
  ],
  "language": "de",
  "sessions": 1
}
```

Deutsch: HRS Hotelbewertungen und Geschäftsreise-Bewertungen; languages=["de"] filtert deutsche Originaltexte.

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## HRS scraper for AI agents: which input answers which request?

Use this actor when the request names HRS, hrs.com or hrs.de and wants guest reviews, ratings, the twelve category scores, the hotel's replies or a property's averages for hotels you can identify by URL or hotel id. Do not use it to find hotels by city or name (there is no search: take the id from an hrs.com URL first), for prices, availability or room offers, for score-only ratings without a comment (HRS does not expose those individually), or for translated text (comments stay in the guest's language, mostly German, then English).

| user request | input JSON |
|---|---|
| every review of one HRS hotel | `{"startUrls": ["https://www.hrs.com/en/hotel/10520"], "maxReviewsPerHotel": 0}` |
| the 30 newest reviews of hotels 10520 and 162 | `{"hotelIds": ["10520", "162"], "reviewsSort": "most_recent", "maxReviewsPerHotel": 30}` |
| negative reviews, complaints, what guests disliked | `{"hotelIds": ["10520"], "maxRating": 7, "reviewsSort": "lowest_rated"}` |
| what business travellers say | `{"hotelIds": ["10520"], "travellerTypes": ["BUSINESS"]}` |
| German comments only | `{"hotelIds": ["10520"], "languages": ["de"]}` |
| compare ten competitors on breakfast, beds or price-performance | `{"hotelIds": ["10520", "162", "22991"], "maxReviewsPerHotel": 1}` then read `avg_by_category` on the free `hotel` rows |
| cheapest daily poll over a known list | `{"hotelIds": ["10520", "162"], "reviewsSort": "most_recent", "maxReviewsPerHotel": 20, "includeHotelRow": false}` |
| HRS Hotelbewertungen, Gästebewertungen, Bewertungen einer Geschäftsreise | the same inputs; every Bewertung is delivered in the language the guest wrote it in, with `language` on the row |

Every row carries `type`. A `review` row (billed, $0.004) has `review_id`, `hotel_id`, `hotel_name`, `rating` (0-10) and `rating_5`, `positives`, `negatives`, `text`, `hotel_reply`, `traveller_type`, `age_group`, `language`, `arrival_date`, `departure_date`, `nights`, `review_date`, `reviewer_name`, `votes` (the twelve category scores) and `url`. A `hotel` row (free, one per hotel while `includeHotelRow` is true) has `stars`, `address`, `city`, `rating`, `rating_count`, `comment_count`, `recommendation_pct`, `ratings_by_traveller_type` and `avg_by_category`. A `status` row (free, one per input) says `status` `ok`, `no_reviews`, `not_found` or `error`, with `reviews` delivered, `filtered` (removed by a filter, never billed), `total` (HRS's rating count) and `comments` (commented ratings available). An input the actor cannot act on (a URL from another site, an id that is not a number, an empty list) ends the run with no rows and the reason on the run card, nothing charged; a source that blocks every hotel fails the run loudly.

### HRS Bewertungen auf Deutsch

HRS ist das Hotelportal für die Geschäftsreise, und die meisten Gästebewertungen sind auf Deutsch geschrieben. Der Scraper liefert jede kommentierte Bewertung einer HRS-Hotelseite als Zeile: Note 0-10, zwölf Kategoriebewertungen, positive und negative Kommentare getrennt, Antwort des Hotels, Reisendentyp und Aufenthaltsdaten. Hotelbewertungen werden nicht übersetzt; `languages: ["de"]` behält nur deutsche Kommentare, `maxRating: 7` nur die schlechten.

## What does the HRS reviews scraper do?

HRS shows a hotel's ratings in a dialog that loads them from a JSON endpoint. This scraper calls that endpoint the way the page does and turns the answer into rows, one per commented rating, with the property's aggregate on the side. Unlike a general **hotel review scraper** that reads whatever the page renders, it gets HRS's own structured record: the guest's positive and negative comments as separate fields, the hotel's separate replies to each, the twelve votes behind the score, the booking's traveller type (business, private, young couple, mature couple, family, group, conference) and age group, and the check-in and check-out dates.

What that gives you that other **hrs hotel reviews** sources do not:

- **Twelve category votes per rating** — reception friendliness, staff service, ambiance, room configuration, tidiness, sanitary facilities, room size, breakfast, restaurant, price-performance, wellness and bed quality — so you can rank a competitor set on the dimension you care about instead of the headline score.
- **Positives and negatives kept apart**, and the hotel's replies to each kept apart too, which is what a reputation team actually reads.
- **Traveller type on every row** and the property's averages per traveller type, so **business travel hotel reviews** can be separated from leisure stays before you compute anything.
- **Filters that run before billing**: complaints only (`maxRating`), one traveller type, one language, only rows with text. You pay for the rows you keep.

## HRS reviews by hotel, by URL or by id

**HRS reviews by hotel id** or by URL: paste hotel page URLs (`https://www.hrs.com/en/hotel/10520`; any language prefix works) or the numeric ids (`10520`, the number after `/hotel/`). A URL and its id are the same hotel and are harvested once. HRS's endpoint takes up to twenty ids per request, so **bulk hotel reviews** for a portfolio of 200 hotels are ten requests plus one page per hotel for the names — a run that finishes in about a minute. That is also how **hrs competitor reviews** work: put the competitor set's ids in one run and compare the hotel rows.

HRS returns the whole list of commented ratings in one answer, so there is no paging to worry about and `maxReviewsPerHotel` is a pure cost cap applied after sorting: the 50 most recent, the 20 lowest rated, or everything.

## HRS negative reviews without paying for the happy ones

Set `maxRating` to 7 and only ratings at or below 7 on HRS's 0-10 scale are delivered — and billed. A property with 150 ratings and 85 comments, of which 9 are below 7, delivers 9 rows and bills 9 rows; the other 76 are counted in the status row as `filtered` and cost nothing. Add `reviewsSort: "lowest_rated"` and the worst come first, so a small cap gives you the complaints feed. `travellerTypes: ["BUSINESS"]` narrows it to the guests HRS exists for; `languages: ["de"]` keeps German comments only. Every filter runs before the charge.

## Hotel review data for revenue, ops and analysts

- **Hotel reputation monitoring** for a hotel group: schedule a daily run over your properties with `reviewsSort: "most_recent"` and `maxReviewsPerHotel: 30`, keep the rows whose `review_date` is newer than yesterday's, and route negatives to the people who answer them. `hotel_reply` tells you which ones are already answered.
- **Competitor benchmarking**: the `hotels` view carries each property's `avg_by_category` and `ratings_by_traveller_type`, so ten competitors compare on breakfast, beds or price-performance in one sheet — **hotel review data** that keeps its structure.
- **Corporate travel programmes**: the `traveller_type` and `age_group` fields let a travel manager read what business guests say about the hotels in the programme, separated from leisure noise — **corporate travel hotel feedback** and **guest feedback data** by segment.
- **Sentiment and topic models**: separate positive and negative fields, a language code per row and twelve numeric votes make a labelled training set without any annotation.

## Input

| field | what it does |
|---|---|
| `startUrls` | HRS hotel pages, e.g. `https://www.hrs.com/en/hotel/10520`. Any language prefix (`/de/`, `/fr/`…) works; the number is the hotel id. |
| `hotelIds` | HRS numeric hotel ids, e.g. `10520`. Faster than URLs for long lists; up to 20 ids go into one request. |
| `maxReviewsPerHotel` | `0` = every commented rating the hotel has. `N` = the first N in the chosen order — the cost control. Default 200. |
| `reviewsSort` | `most_recent` (default), `oldest`, `highest_rated`, `lowest_rated`. Applied before the cap. |
| `travellerTypes` | Empty = every guest. Otherwise keep only these HRS types: `BUSINESS`, `PRIVATE`, `YOUNG_COUPLE`, `MATURE_COUPLE`, `FAMILY_SMALL_CHILDREN`, `FAMILY_OLDER_CHILDREN`, `GROUP`, `CONFERENCE`. Filters before billing. |
| `languages` | Empty = every language. Otherwise keep comments in these languages, as codes (`de`, `en`, `fr`, `it`, `es`, `nl`, `pl`, `pt`, `ru`, `zh`, `tr`, `cs`, or `deu`, `eng`…) or names (`German`). Filters before billing. |
| `maxRating` | `0` = keep every review. `1`-`10` = keep only reviews at or below it on HRS's scale (7 is a middling stay, below 6 a bad one). Filters before billing. |
| `requireText` | Keep only rows with a written positive or negative. HRS's list already contains only those, so this rarely changes anything; it guarantees every billed row carries text. |
| `language` | Site language of the hotel page read for the hotel row (`en` default, `de`, `fr`, `it`, `es`, `nl`, `pl`, `pt`, `ru`, `zh_cn`, `tr`, `cs`). Comments keep their author's language. |
| `includeHotelRow` | Default on: one free row per hotel with name, stars, address, overall rating, rating count, recommendation rate and the averages by traveller type and category — and the hotel name on every review row. Off saves one request per hotel but leaves names empty. |
| `sessions` | Proxy sessions (egress IPs) in parallel. Default 4. |
| `perIp` | Requests per second per session. Default 1; HRS answered 10 of 10 at that pace on one residential IP. |
| `proxyConfiguration` | Apify Proxy **RESIDENTIAL** is required: hrs.com and its ratings API answer 403 to datacenter IPs. Traffic is small — one JSON call per 20 hotels, one page per hotel for the hotel row. |

### Example: a scheduled complaints feed

```json
{
  "hotelIds": ["10520", "162"],
  "reviewsSort": "lowest_rated",
  "maxRating": 7,
  "maxReviewsPerHotel": 50,
  "proxyConfiguration": { "useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"] }
}
```

Only ratings at or below 7 come back, worst first, at most 50 per hotel; everything above 7 is counted as filtered and never billed.

### Example: what business travellers say, in German

```json
{
  "startUrls": ["https://www.hrs.com/de/hotel/162"],
  "travellerTypes": ["BUSINESS"],
  "languages": ["de"],
  "language": "de",
  "maxReviewsPerHotel": 0,
  "proxyConfiguration": { "useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"] }
}
```

One traveller type is asked of HRS directly, so nothing else is even downloaded; the language filter then keeps German comments. The hotel row is read from the German page.

### Example: the newest 30 for a portfolio, names off

```json
{
  "hotelIds": ["10520", "162", "22991"],
  "reviewsSort": "most_recent",
  "maxReviewsPerHotel": 30,
  "includeHotelRow": false,
  "proxyConfiguration": { "useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"] }
}
```

One ratings request for all three hotels and no page reads: the cheapest way to poll a list daily when you already know the names.

## Output

Three row types share one dataset; `type` tells them apart. Use the **Reviews**, **Complaints**, **Hotels** and **Status** views in the Apify Console, or filter on `type` in your own code.

**`review`** (billed) — one commented rating:

| field | meaning |
|---|---|
| `review_id` | Stable id of the rating (HRS booking id) |
| `hotel_id`, `hotel_name`, `url` | The property (name from the hotel page; empty when `includeHotelRow` is off) |
| `rating`, `rating_5` | Guest score 0-10, and the same on the 5-star scale |
| `recommends` | Whether the guest recommends the hotel |
| `comfort` | HRS's comfort word for the stay, e.g. `NICE` |
| `positives`, `negatives` | What the guest liked and disliked, as separate fields |
| `text` | Positives and negatives joined, so one field always carries the comment |
| `hotel_reply` | The hotel's replies (to the positive and to the negative), joined |
| `traveller_type` | `BUSINESS`, `PRIVATE`, `YOUNG_COUPLE`, `MATURE_COUPLE`, `FAMILY_SMALL_CHILDREN`, `FAMILY_OLDER_CHILDREN`, `GROUP`, `CONFERENCE` |
| `age_group` | `UP_TO_59` or `OVER_59` |
| `language`, `locale` | ISO 639-2 code of the comment (`deu`, `eng`…) and the two-letter site locale the guest used |
| `reviewer_name` | The guest's display name as HRS shows it |
| `arrival_date`, `departure_date`, `nights` | The stay |
| `review_date` | When the rating was written (ISO 8601, UTC) |
| `votes` | The twelve category votes 0-10: `FRIENDLINESS_OF_RECEPTION`, `SERVICE_OF_HOTEL_EMPLOYEES`, `HOTEL_AMBIANCE`, `ROOM_CONFIGURATION`, `HOTEL_TIDINESS`, `SANITARY_FACILITIES`, `ROOM_SIZE`, `BREAKFAST_SERVICE`, `RESTAURANT_SERVICE`, `PRICE_PERFORMANCE_RATIO`, `WELLNESS_RANKING`, `QUALITY_OF_BEDS` (0 = not rated) |
| `fetched_at` | UTC timestamp of the row |

**`hotel`** (free, with `includeHotelRow`) — one per property: `hotel_id`, `hotel_name`, `url`, `stars`, `address`, `postal_code`, `city`, `rating`, `rating_count` (every rating HRS counts, commented or not), `comment_count` (ratings with a comment — what can be delivered), `recommendation_pct`, `ratings_by_traveller_type` (count, rating and recommendation rate per type), `avg_by_category` (the twelve categories), `avg_by_super_category` (`HOTEL_GENERAL_ASPECTS`, `ROOM`, `STAFF_AND_GASTRONOMY`), `reviews_fetched`, `fetched_at`.

**`status`** (free) — one per input: `target`, `hotel_id`, `hotel_name`, `status` (`ok`, `no_reviews`, `not_found`, `duplicate`, `error`), `reviews` delivered, `filtered` (dropped by a filter, never billed), `total` (HRS's rating count), `comments` (commented ratings available), `duplicates`, `error`, `fetched_at`.

A review row looks like this:

```json
{
  "type": "review",
  "review_id": "315653282",
  "hotel_id": "10520",
  "hotel_name": "Bilderberg Bellevue Hotel Dresden",
  "url": "https://www.hrs.com/en/hotel/10520",
  "rating": 9.36,
  "rating_5": 4.68,
  "recommends": true,
  "comfort": "NICE",
  "positives": "Tolle Lage direkt an der Elbe und fußnah zu Altstadt",
  "negatives": null,
  "text": "Tolle Lage direkt an der Elbe und fußnah zu Altstadt",
  "hotel_reply": "Das klingt nach einer schönen Zeit in Dresden! Wir freuen uns, dass Sie bei der Gelegenheit mit uns als Ihren Gastgeber geplant haben.",
  "traveller_type": "PRIVATE",
  "age_group": "OVER_59",
  "language": "deu",
  "locale": "de",
  "reviewer_name": "Müller K.",
  "arrival_date": "2025-12-08",
  "departure_date": "2025-12-11",
  "nights": 3,
  "review_date": "2025-12-11T14:28:35Z",
  "votes": { "FRIENDLINESS_OF_RECEPTION": 10, "SERVICE_OF_HOTEL_EMPLOYEES": 10, "HOTEL_AMBIANCE": 9, "ROOM_CONFIGURATION": 10, "HOTEL_TIDINESS": 10, "SANITARY_FACILITIES": 8, "ROOM_SIZE": 10, "BREAKFAST_SERVICE": 9, "RESTAURANT_SERVICE": 0, "PRICE_PERFORMANCE_RATIO": 9, "WELLNESS_RANKING": 8, "QUALITY_OF_BEDS": 10 },
  "fetched_at": "2026-08-29T10:20:11+00:00"
}
```

## How much does it cost?

$0.004 per review row delivered, and nothing else: hotel rows, status rows, unknown hotels and filtered reviews are free, and an empty run costs $0. A busy city hotel has 50-150 commented ratings, so 50-150 delivered reviews cost $0.20-$0.60; a daily complaints feed over 20 properties that surfaces a handful of new low ratings costs a few cents a day. Proxy traffic and compute for the run are included in the event price. Set `maxReviewsPerHotel` and the filters to keep bulk work predictable — the status row tells you how much a hotel would have delivered.

## HRS reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

Python, with the [Apify client](https://docs.apify.com/api/client/python/):

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/hrs-reviews-scraper").call(run_input={
    "hotelIds": ["10520", "162"],
    "reviewsSort": "lowest_rated",
    "maxRating": 7,
    "maxReviewsPerHotel": 50,
    "proxyConfiguration": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["hotel_name"], row["rating"], row["traveller_type"], (row["negatives"] or "")[:80])
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/hrs-reviews-scraper').call({
    startUrls: ['https://www.hrs.com/en/hotel/10520'],
    maxReviewsPerHotel: 100,
    proxyConfiguration: { useApifyProxy: true, apifyProxyGroups: ['RESIDENTIAL'] },
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter(r => r.type === 'review');
console.log(reviews.length, 'reviews;', reviews.filter(r => r.hotel_reply).length, 'answered by the hotel');
```

curl, waiting for the run and getting the rows back in one call:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~hrs-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{"hotelIds": ["10520"], "maxReviewsPerHotel": 30, "reviewsSort": "most_recent", "proxyConfiguration": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}}'
```

**n8n**: an HTTP Request node posting the same JSON to `run-sync-get-dataset-items`, a Code node keeping `type === 'review'` rows newer than the last run, and a Slack or Google Sheets node — the same pattern as the review-alert templates in [github.com/mtedj/kestrel-actors-examples](https://github.com/mtedj/kestrel-actors-examples). **Make**: the Apify app's "Run an actor" module with this actor's id and the input above, then "Get dataset items". **MCP / AI agents**: add the Apify MCP server and ask for "the latest negative HRS reviews of hotel 10520" — the input and output schemas are complete, so an agent fills the fields itself.

## Is it legal to scrape HRS reviews?

The scraper reads the same publicly accessible ratings any visitor sees on a hotel page, through the endpoint that page uses, without logging in or bypassing any access control. Reviews contain personal data in the sense of the GDPR — a display name, a stay date, a text — so you need a lawful basis for what you do with them (a hotel monitoring its own reputation, a researcher aggregating sentiment, a travel manager reviewing programme hotels), you should not republish reviewer names, and you should honour deletion requests. Use the data for analysis, not to rebuild HRS's review pages. This is not legal advice; check the rules that apply to you.

## Limits and honest notes

- **Only commented ratings are delivered.** HRS counts every rating in `rating_count` (a property may show 150) but exposes the text of the ones with a written comment (`comment_count`, say 85). Score-only ratings are in the averages, not in the rows.
- **The whole list comes in one answer.** There is no paging on HRS's side, so a very large property is one big response; `maxReviewsPerHotel` trims it after sorting rather than saving requests.
- **Residential proxy only.** Both hrs.com and its ratings API answer 403 to datacenter IPs; the input defaults to the RESIDENTIAL group. Traffic is small.
- **Hotel names need the page.** The ratings endpoint carries no name or address, so with `includeHotelRow` on the scraper reads one page per hotel (about 400 KB); off, `hotel_name` is empty and the run is one request per 20 hotels.
- **Unknown ids are free.** An id HRS does not know comes back as `status: not_found` and costs nothing; a hotel with ratings but no comments is `no_reviews`.
- **Comments are in the guest's language** — HRS is a German-founded platform, so most rows are **german hotel reviews**, then English; HRS does not translate them and neither does this scraper. `language` tells you which.

## FAQ

### Does it need an HRS API key or login?

No. The ratings endpoint the hotel page calls is public; the scraper sends the same client identifier the site's own JavaScript sends. Nothing is logged in and no session is reused.

### Can I download HRS reviews as CSV or Excel?

Yes — **download HRS reviews** from any run, and get **HRS reviews CSV** files straight from the dataset. Every Apify dataset exports as CSV, Excel, JSON, XML or RSS from the Console or the API. The `votes` object flattens to twelve columns in the Excel export; in CSV it is a JSON string.

### How do I get only HRS negative reviews?

`maxRating: 7` keeps ratings at or below 7; `reviewsSort: "lowest_rated"` puts the worst first; `maxReviewsPerHotel` caps the count. Everything above 7 is filtered before billing.

### What is the difference between rating_count and comment_count?

`rating_count` is every rating HRS has for the property, with or without a comment. `comment_count` is how many carry a written positive or negative — the rows this scraper can deliver. Both are on the hotel row and the status row.

### Do I need the hotel id, or can I use the URL?

Either. The id is the number after `/hotel/` in any hrs.com URL; the scraper reads it from the URL without loading the page. Ids are handier for long lists — twenty go into one request.

### How many reviews can one hotel return?

All of its commented **HRS hotel ratings** — HRS returns the full list in one answer. City business hotels typically have 30-150; the status row's `comments` tells you the count before the cap.

### Are reviews translated, and which languages come back?

They are not translated. Most comments are German or English, with French, Italian, Spanish, Dutch and others; `language` carries the ISO 639-2 code and `languages` filters on it before billing.

### Does it include the hotel's replies?

Yes. HRS lets a hotel answer the positive and the negative separately; both go into `hotel_reply`. Counting rows with a reply is a quick measure of how attentive a property is.

### Can I filter by traveller type?

Yes. `travellerTypes` accepts one or more of HRS's eight types. One type is asked of HRS directly (nothing else is downloaded); several are kept from the full list. The hotel row carries each type's average and recommendation rate.

### Can I scrape HRS reviews without an API?

**HRS reviews without API** access is exactly what this does: no HRS API, no key, no browser — a scheduled Apify run and a dataset. Call it from the Apify API, n8n, Make, MCP or the Console.

### What does bulk work cost?

$0.004 per review delivered. 100 hotels at 60 comments each is 6,000 rows and $24; the same 100 hotels with `maxRating: 6` deliver only the bad stays and cost a fraction of that. Runs that deliver nothing cost $0.

## Review monitoring across a portfolio

**HRS.com reviews** change daily. Schedule the actor on Apify with your hotel ids, `reviewsSort: "most_recent"` and a small `maxReviewsPerHotel`, then keep rows whose `review_date` is newer than the previous run's — the ids are stable, so a `review_id` seen before is the same rating. Route rows with `rating` below your threshold and an empty `hotel_reply` to whoever answers guests; sheet the `hotels` view weekly for the category averages.

### Guest feedback data that keeps its structure

Because positives, negatives, replies, votes and traveller type are separate fields, the dataset drops straight into a BI tool or a language model without parsing. A quarter of review-scraper complaints on Apify are about rows that lose fields between runs; every row here carries every key, empty or not.

### What this does not do

It does not book, does not read prices or availability, does not read HRS's corporate rate programme, and does not scrape guest profiles beyond the display name HRS prints next to a rating.

### Choosing between sort orders

`most_recent` for monitoring, `lowest_rated` for a complaints feed, `highest_rated` for marketing copy, `oldest` for a full history you then keep current with the recent view.

## Related scrapers

Hotel guest reviews live on more than one site. These share the same row discipline, the same pay-per-delivered-row billing and the same scheduling story:

- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives and the hotel's reply.
- **[Trip.com Reviews Scraper](https://apify.com/kestrel/trip-com-reviews-scraper)** — Trip.com and Ctrip hotel reviews with four sub-scores and the Chinese-language corpus.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing, `minRating` billed only for the rows you keep.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — every booking site's rate for a stay side by side, with the parity math.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site's rate for exact dates.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
