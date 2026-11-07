# Hostelworld Reviews Scraper - Hostel Guest Reviews, Ratings

This **hostelworld reviews scraper** turns any hostel on Hostelworld into structured **hostel guest reviews**: the 0-100 overall score with its seven sub-ratings, the guest's own words, the hostel's public reply, who was travelling and where they came from. Point it at Hostelworld URLs or property ids and it returns every review the site lists, newest first — **hostel reviews** as rows you can filter, chart and diff, not a page you have to read. Because it reads Hostelworld's own public JSON API there is no browser, no login and no key, so **budget travel reviews** arrive at a few hundred rows a second and **review monitoring** on a daily schedule costs cents.

Last verified working: 2026-08-29.

## Hostelworld 青年旅舍评论、住客评价与评分：中文调用与语言设置

按旅舍 URL 或 ID 获取评分、分项评分、评论、群体类型和回复。评分使用 0–100 分制。

没有 locale 或翻译输入；评论按来源原文返回。旅客国籍不等于评论语言，不应把国籍当成语言筛选条件。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.hostelworld.com/hostels/p/15529/home-lisbon-hostel/"
  ],
  "maxReviewsPerProperty": 1,
  "reviewsSort": "-date",
  "sessions": 1
}
```

Avis auberge de jeunesse / opiniones hostales / Hostel Bewertungen：保留 0–100 来源分制。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Hostelworld scraper for AI agents: which input answers which request?

Use this actor when the request names Hostelworld or hostelworld.com and wants hostel guest reviews, the 0-100 score and its seven sub-ratings, the hostel's reply, who was travelling (group type, age band, trip type, nationality) or a property's aggregate for hostels you can identify by URL or property id. Do not use it to find hostels by city or name (there is no search: take the URL from hostelworld.com first), for prices or availability beyond the free hostel row's lowest nightly price, for a language filter (Hostelworld serves one machine-translated English set and ignores a language parameter, so there is none), or for score-only ratings that Hostelworld does not list.

| user request | input JSON |
|---|---|
| every review of one hostel | `{"startUrls": ["https://www.hostelworld.com/hostels/p/15529/home-lisbon-hostel/"], "maxReviewsPerProperty": 0}` |
| the 50 newest reviews of hostels 15529 and 1150 | `{"propertyIds": ["15529", "1150"], "maxReviewsPerProperty": 50}` |
| the 20 worst reviews, complaints, what guests disliked | `{"propertyIds": ["15529"], "reviewsSort": "rating", "maxReviewsPerProperty": 20}` (add `"maxRating": 70` to keep only scores at or below 70) |
| only new reviews since the last run (daily schedule) | `{"propertyIds": ["15529", "1150"], "sinceDate": "2 days"}` |
| what solo female travellers say | `{"propertyIds": ["15529"], "groupTypes": ["FEMALE"], "maxReviewsPerProperty": 0}` |
| praise only, quotes for marketing | `{"propertyIds": ["15529"], "minRating": 90, "reviewsSort": "-rating"}` |
| compare competitors on safety, staff or cleanliness | `{"propertyIds": ["15529", "1150", "3287"], "maxReviewsPerProperty": 1}` then read `sub_ratings` on the free `property` rows |
| opiniones de hostales, avaliações de hostel, Hostel-Bewertungen | the same inputs; the text comes back in English (Hostelworld's own machine translation), `language` and `machine_translated` say so on every row |

Every row carries `type`. A `review` row (billed, $0.004) has `review_id`, `property_id`, `property_name`, `property_url`, `rating` (0-100) and `rating_5`, `sub_ratings` (`value`, `safety`, `location`, `staff`, `atmosphere`, `cleanliness`, `facilities`), `text`, `language`, `machine_translated`, `owner_comment`, `group_type`, `age_group`, `trip_types`, `reviewer_nickname`, `reviewer_country`, `reviewer_country_code`, `reviewer_reviews` and `review_date` (`liked`, `disliked` and `recommended` are legacy fields Hostelworld no longer fills). A `property` row (free, one per hostel while `includePropertyRow` is true) has `property_type`, `star_rating`, `city`, `country`, `address`, `latitude`, `longitude`, the aggregate `rating` and `sub_ratings`, `total_ratings`, `facilities`, `best_for`, `lowest_price_per_night`, `currency` and the solo/couples/groups percentages. A `status` row (free, one per input) says `status` `ok`, `no_reviews`, `not_found`, `duplicate` or `error`, with `reviews` delivered, `filtered` (removed by a filter, never billed), `pages` read and `total` (what Hostelworld lists). Filters apply to the `maxReviewsPerProperty` rows fetched in `reviewsSort` order, so set the cap to 0 to scan a whole history. An input the actor cannot act on (a URL from another site, an id that is not a number, an empty list) ends the run with no rows and the reason on the run card, nothing charged; a source that refuses every hostel fails the run loudly.

## What does the Hostelworld reviews scraper do?

It reads one endpoint that Hostelworld's own property pages call, walks its pagination for you and flattens each record into a row:

- The **0-100 score** every Hostelworld guest gives, plus the seven sub-scores behind it — value, safety, location, staff, atmosphere, cleanliness, facilities — and the same overall score converted to the 0-5 star scale everyone else uses.
- The review **text**, its language and whether Hostelworld machine-translated it.
- The **owner reply**, when the hostel answered.
- **Who was travelling**: solo male or female, couple, all-female group, all-male group, mixed group; the age band (18-24, 25-30, 31-40, 41+); and the trip type (a gap year, a weekend away, a round-the-world trip, a college break, a regular vacation).
- The reviewer's nickname, nationality and how many reviews they have written.
- A free per-hostel context row: name, type, city, country, coordinates, aggregate **hostel ratings**, facilities, and the share of reviewers who came solo, as a couple or in a group.

Every filter runs before billing, so a run that keeps only the complaints pays only for the complaints.

## Hostelworld reviews by URL or property id

Two ways in, and neither costs a lookup request:

- **`startUrls`** — any Hostelworld property page. The modern form is `https://www.hostelworld.com/hostels/p/15529/home-lisbon-hostel/`; the older `https://www.hostelworld.com/pwa/hosteldetails.php/Home-Lisbon-Hostel/Lisbon/15529` works too. Every URL form Hostelworld serves carries the numeric id, so the actor never has to load a page to find it. A Hostelworld URL that somehow has no id is read once for the id its page carries.
- **`propertyIds`** — the bare number, e.g. `15529`. This is what an earlier run's `property_id` column gives you, so a saved list of hostels re-runs with no resolution at all.

A URL, its older URL form and its bare id are recognised as the same hostel: one of them is scraped and the rest come back as free `duplicate` status rows.

## Hostelworld negative reviews without paying for the happy ones

Hostels live and die on a handful of recurring complaints — the 4 a.m. door, the shower queue, the locker that will not close. Set `reviewsSort` to *Lowest rated first* and `maxRating` to 70 and the worst reviews arrive on page one and nothing else is charged. `minRating` is the other end of the same 0-100 scale if you want to study what a hostel is loved for. Both filters run in the actor before the charge, so **hostelworld negative reviews** cost exactly what they weigh.

## Hostel review data for operators, OTAs and analysts

- **Hostel operators**: read the reviews your competitors get, by sub-score. `sub_ratings` tells you whether you are losing on cleanliness or on atmosphere, which are very different fixes.
- **Hostel reputation management**: watch the last 30 days across a portfolio with `sinceDate: "30 days"` and alert on anything under 70.
- **OTAs and metasearch**: `hostel review data` for supply pages, with a rating you can normalise (`rating_5`) against Booking's 1-10 or TripAdvisor's 1-5.
- **Researchers and analysts**: **backpacker reviews** carry a group type, an age band and a nationality, which almost no other review source publishes. That is a demand-side dataset, not just sentiment.
- **AI teams**: a clean, dated, per-property corpus for **hostel sentiment analysis** and RAG over **hostel guest feedback**.

## Input

| Field | Type | Default | What it does |
|---|---|---|---|
| `startUrls` | array | `[]` | Hostelworld property URLs. Any form; the id is read from the URL. |
| `propertyIds` | array | `[]` | Hostelworld's numeric property ids, e.g. `15529`. |
| `maxReviewsPerProperty` | integer | `100` | `0` = every review the hostel has. `N` = the first `N` in the chosen order. The main cost control. |
| `reviewsSort` | string | `-date` | `-date` newest first, `date` oldest first, `rating` lowest rated first, `-rating` highest rated first. |
| `minRating` | integer | `0` | Keep only reviews scoring at or above this on the 0-100 scale. `0` = no floor. |
| `maxRating` | integer | `0` | Keep only reviews scoring at or below it. `0` = no ceiling. `70` is a complaints feed. |
| `requireText` | boolean | `false` | Drop score-only reviews before billing. |
| `groupTypes` | array | `[]` | Keep only `MALE`, `FEMALE`, `COUPLE`, `ALLFEMALEGROUP`, `ALLMALEGROUP`, `MIXEDGROUP` or `FAMILY`. Friendly spellings (`solo_female`, `mixed_group`) work. |
| `sinceDate` | string | `""` | `YYYY-MM-DD` or relative (`30 days`, `2 weeks`, `6 months`). |
| `includePropertyRow` | boolean | `true` | Emit the free per-hostel context row. |
| `sessions` | integer | `2` | Parallel proxy sessions (egress IPs). |
| `perIp` | number | `1` | Requests per second per session. |
| `proxyConfiguration` | object | Apify datacenter | Datacenter proxy is enough; residential works and costs more. |

### Example: a daily complaints feed for one hostel

```json
{
  "propertyIds": ["15529"],
  "reviewsSort": "rating",
  "maxRating": 70,
  "requireText": true,
  "sinceDate": "30 days",
  "maxReviewsPerProperty": 0,
  "includePropertyRow": true,
  "proxyConfiguration": { "useApifyProxy": true }
}
```

Lowest-rated first, nothing above 70 charged, nothing older than a month kept. On a quiet month this bills a handful of rows.

### Example: the full corpus of a competitor set

```json
{
  "startUrls": [
    "https://www.hostelworld.com/hostels/p/15529/home-lisbon-hostel/",
    "https://www.hostelworld.com/pwa/hosteldetails.php/Yes-Lisbon-Hostel/Lisbon/45010"
  ],
  "maxReviewsPerProperty": 0,
  "reviewsSort": "-date",
  "includePropertyRow": true,
  "sessions": 4,
  "perIp": 1
}
```

Every review both hostels have, newest first, plus a free context row each.

### Example: what solo female travellers say

```json
{
  "propertyIds": ["15529", "12000"],
  "groupTypes": ["solo_female"],
  "maxReviewsPerProperty": 500,
  "minRating": 0,
  "maxRating": 0,
  "requireText": true,
  "sinceDate": "12 months"
}
```

`groupTypes` is applied in the actor — Hostelworld's API has no server-side filter for it — so the pages are still read and the rows you did not want are simply never charged.

## Output

Three row types share one dataset, told apart by `type`, with dataset views for each.

### Review rows (`type: "review"`, charged)

| Field | Meaning |
|---|---|
| `review_id` | Hostelworld's numeric review id |
| `property_id`, `property_name`, `property_url` | Which hostel the review is about |
| `review_date` | Publication date, `YYYY-MM-DD` |
| `text` | The review itself (Hostelworld's `notes`); `null` when the guest scored without writing |
| `language`, `machine_translated` | The language served and whether it was machine-translated |
| `rating` | Overall score, 0-100 |
| `rating_5` | The same score on the 0-5 star scale, e.g. `94` → `4.7` |
| `sub_ratings` | `{value, safety, location, staff, atmosphere, cleanliness, facilities}`, each 0-100 |
| `owner_comment` | The hostel's public reply, if any |
| `group_type` | `MALE`, `FEMALE`, `COUPLE`, `ALLFEMALEGROUP`, `ALLMALEGROUP`, `MIXEDGROUP`, `FAMILY` |
| `age_group` | `18-24`, `25-30`, `31-40`, `41+` |
| `trip_types` | `REGULARVACATION`, `WEEKENDAWAY`, `GAPYEAR`, `RTWTRIP`, `COLLEGEBREAK`, `OTHER` |
| `reviewer_id`, `reviewer_nickname`, `reviewer_gender` | Who wrote it (`Anonymous` when they hid the name) |
| `reviewer_country`, `reviewer_country_code`, `reviewer_reviews`, `reviewer_image` | Where they are from, how many reviews they have written, their avatar |
| `liked`, `disliked`, `recommended` | Legacy split-review fields; Hostelworld no longer fills them, so they are almost always `null` |
| `target`, `fetched_at` | The input value this row came from, and when it was read |

### Hostel rows (`type: "property"`, free)

`property_id`, `property_name`, `property_type` (`HOSTEL`, `GUESTHOUSE`, `HOTEL`, …), `star_rating`, `city`, `country`, `region`, `address`, `latitude`, `longitude`, `rating` and `rating_5` (the hostel's aggregate), `sub_ratings`, `total_ratings` (every score, text or not), `currency`, `lowest_price_per_night`, `best_for`, `facilities`, `description`, `positive_count`, `negative_count`, `solo_percentage`, `couples_percentage`, `groups_percentage`, `reviews_listed`, `reviews_fetched`, `property_url`.

### Status rows (`type: "status"`, free)

One per target: `target`, `property_id`, `property_name`, `status` (`ok`, `no_reviews`, `not_found`, `duplicate`, `error`), `reviews` delivered, `filtered` (dropped before billing), `pages` read, `total` Hostelworld lists, `duplicates`, `error`.

A refusal is always `status: "error"` with the reason. A hostel with no reviews is `no_reviews` with `total: 0`, and an unknown or deactivated property id is `not_found`. The scraper never reports an empty hostel when it was really blocked — Hostelworld's API has no silent-empty answer, so neither does this actor.

The run also writes a `SUMMARY` record to the key-value store with the delivered, filtered and charged counts and the HTTP stats.

## How much does it cost?

$0.004 per review row. Hostel rows, status rows, duplicate targets, unknown ids and every review a filter dropped are free. A thousand reviews is $4; a daily 30-day watch over ten hostels is usually a few cents a day. Compute is included in the event price.

## Hostelworld reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/hostelworld-reviews-scraper").call(run_input={
    "propertyIds": ["15529"],
    "maxReviewsPerProperty": 200,
    "reviewsSort": "-date",
})
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
reviews = [r for r in rows if r["type"] == "review"]
print(len(reviews), "reviews", sum(r["rating"] for r in reviews) / len(reviews))
```

JavaScript (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/hostelworld-reviews-scraper').call({
    startUrls: ['https://www.hostelworld.com/hostels/p/15529/home-lisbon-hostel/'],
    maxReviewsPerProperty: 0,
    maxRating: 70,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((r) => r.type === 'review').length);
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~hostelworld-reviews-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"propertyIds":["15529"],"maxReviewsPerProperty":50,"reviewsSort":"-date"}'
```

Add `&format=csv` to that URL and you have **hostelworld reviews csv** without writing any code — the same route to download hostelworld reviews as Excel, JSON or XML.

**n8n**: the Apify node runs this actor and hands the dataset to the next step. **Make**: the Apify module does the same, so a low score can raise a Slack message or open a ticket. **MCP and AI agents**: Apify's MCP server exposes the actor as a tool, so an assistant can fetch **hostelworld property reviews** on demand and answer questions about a hostel without a scraping pipeline of its own.

## Is it legal to scrape Hostelworld reviews?

This actor reads only what Hostelworld publishes to anyone: the same public JSON its own property pages fetch, with no key, no login and no account. It never touches private data or anything behind a paywall. Public data collection of this kind is generally lawful in the EU, the UK and the US, and the reviews themselves are published statements. What you do afterwards is your responsibility: reviewer nicknames and nationalities are personal data under the GDPR, so treat them accordingly, keep republication within fair use, and check Hostelworld's terms for your own use case. This is not legal advice.

## Limits and honest notes

- **One language.** Hostelworld serves a single machine-translated English set. It accepts a `languages` parameter and then ignores it, so this actor deliberately offers no language filter rather than one that does nothing. `language` and `machine_translated` are on every row so you can see exactly what you got.
- **`liked`, `disliked` and `recommended` are legacy.** Hostelworld's schema still carries them; the data no longer fills them. They are kept so nothing is lost if the site starts writing them again.
- **`groupTypes`, `minRating`, `maxRating`, `requireText` and `sinceDate` are actor-side.** The API has no server-side filter, so the pages are read and the rows are then dropped before billing.
- **Page size is capped at 50** by the API, which is what the actor asks for.
- **`sinceDate` only stops paging early on a date sort.** With `-date` a run stops as soon as a whole page predates the cut; with a rating sort the dates are not ordered, so the filter still applies but every page is read.
- **Scores are 0-100, not 1-5.** `rating_5` is there for joins with other review sources.

## FAQ

### Does it need a Hostelworld API key or login?

No. This is **hostelworld reviews without an api key**: the endpoint is public and unauthenticated, and the actor sends no cookie, token or `Origin` header.

### Can I download Hostelworld reviews as CSV or Excel?

Yes. Every Apify dataset exports to CSV, Excel, JSON, XML or JSONL from the run's Storage tab or the API, and the `run-sync-get-dataset-items` call above takes `&format=csv` directly.

### How do I get only the bad reviews?

Set `reviewsSort` to `rating` and `maxRating` to about 70. The worst arrive first and everything above the ceiling is filtered before it is charged.

### Can I get Hostelworld reviews by property id instead of URL?

Yes — that is `propertyIds`, and it is the fastest path because nothing has to be resolved. Get **hostelworld reviews by property id** straight from an earlier run's `property_id` column.

### How many reviews can one hostel return?

All of them. A busy city hostel carries one to three thousand; the actor pages through the lot at 50 per request and stops on its own at the end of the list.

### Does it include the hostel's reply?

Yes — `owner_comment`. **Hostelworld owner replies** are common on hostels that manage their reputation and absent on the ones that do not, which is itself a signal.

### Can I scrape Hostelworld reviews without an API of my own?

Yes. That is what this actor is: no infrastructure, no proxies to buy, no browser to keep alive. Run it from the Console, the API, a schedule or an agent.

### Is the reviewer data really that detailed?

Yes. Group type, age band, trip type and nationality come from Hostelworld itself, which is why **backpacker reviews** here support demand analysis and not only sentiment.

### What do bulk hostel reviews cost?

$0.004 each, filters applied first. **Bulk hostel reviews** across a fifty-hostel city at 200 reviews per hostel is 10,000 rows, or $40.

### Can I use it for hostel sentiment analysis?

Yes. `text` is clean, `review_date` is exact and `rating` gives you a numeric label to train or evaluate against, per hostel and per group type.

## Review monitoring across a portfolio: hostel guest feedback every morning

Schedule the actor daily with `sinceDate: "2 days"` and every hostel you care about in `propertyIds`. Newest-first order means it reads one page per hostel and stops, so the run is quick and cheap. Push the dataset into a warehouse and you have **hostel guest feedback** as a time series: score by week, sub-score by week, complaint volume by group type. A **hostel review scraper** that returns nothing new on a quiet day costs nothing on a quiet day.

### Guest feedback data that keeps its structure

Every row carries every key, so a run with no owner replies still has an `owner_comment` column and your loader never sees a shifting schema. Rows are typed, dates are ISO, scores are integers.

### What this does not do

It does not book, price or check availability, and it does not read a city listing page — give it hostels, not searches. A Hostelworld scraper for rates and availability is a different job; pair this one with a prices actor.

### Choosing an order

`-date` for monitoring, `rating` for complaint triage, `-rating` for marketing copy, `date` when you want the oldest reviews a hostel ever received.

## Related scrapers

Hostelworld is one window on a property's reputation. These read the others, with the same row discipline:

- [Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper) — the same job on Booking's 1-10 scale, with liked/disliked split out.
- [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) — 1-5 bubbles, six sub-ratings and up to 30 site languages.
- [Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper) — the short-let side of the same market.
- [Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper) — the Asia-heavy OTA, with separate positives and negatives and the hotel's reply, by hotel name, URL or id.
- [Free Hotel Review Checker](https://apify.com/kestrel/hotel-reputation-checker) — the Hostelworld score next to Booking.com, Agoda, Tripadvisor, Google and Despegar for the same property, one row per site, free — run it first to see which site's text is worth reading.
- [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices) — what the same properties charge: every booking site's rate for a stay as its own row, for the price behind the score.

Together they cover the budget-travel stack: run the review scrapers over one city and you can compare what the same traveller says about a hostel bed, a hotel room and a spare room.
