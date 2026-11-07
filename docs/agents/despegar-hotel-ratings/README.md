# Despegar Hotel Ratings Scraper - Guest Scores, AI Summary

Scrape **despegar hotel ratings** from any hotel page on Latin America's largest online travel agency: the 0-10 overall guest score, the number of reviews behind it, six category scores, the AI-written **hotel review summary** Despegar publishes, and the individual comments the page shows. One request per hotel, no browser, no login, no API key. If you have been looking for **despegar hotel reviews**, **hotel guest ratings** or **guest scores** for the LatAm market in a machine-readable form, this is the fastest path to them.

**Read this before you buy: the hotel page publishes at most four individual comments per hotel, no matter how large the review count is.** A hotel with 4,511 reviews renders four of them; the site's own analytics beacon says so (`"review_count":"4511","total_comments":"4"`). Two full browser captures of a hotel page recorded 109 and 101 requests and **zero** review-bearing XHRs — there is no reviews endpoint, no "load more", no paging. So this actor is priced and named for what the page really is: a **hotel rating** product with four sample comments attached, not a deep review dump. If you need hundreds of reviews per property, use [Booking Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper) or [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) instead — both page through the full review list.

## Despegar 拉美酒店评分、评价摘要与公开评论：中文调用与语言设置

返回每酒店一行的 0–10 分评分、评论数量、分类评分和来源 AI 摘要。最多附带四条公开评论，不是完整评论采集。

country 选择地区站点，优先于 locale；locale 仅支持 auto、es、en。没有中文翻译。巴西 Decolar 站在测试中受限，不承诺可用。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.despegar.com.ar/hoteles/h-265543/riu-cancun"
  ],
  "country": "ar",
  "includeComments": true,
  "sessions": 1
}
```

Español: calificaciones y opiniones de hoteles; hasta cuatro comentarios publicados por hotel. Português: avaliações e resumo dos sites suportados; não promete acesso ao Decolar bloqueado.

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Despegar scraper for AI agents: which input answers which request?

Use this actor when the request names Despegar (or one of its country sites) and wants a hotel's guest rating, the review count behind it, the six category scores, Despegar's AI-written review summary, stars, city or coordinates, for hotels you can identify by URL or id, on any of 14 Latin American sites plus us.despegar.com in English. Do not use it for a full list of reviews (the page publishes at most four comments per hotel and there is no reviews endpoint: use a Booking or TripAdvisor reviews scraper for that), to find hotels by city or name (there is no search: take the URL from despegar.com first), for prices or availability, or for Brazil's decolar.com (listed, but it refused every request in testing).

| user request | input JSON |
|---|---|
| the guest rating and category scores of one hotel | `{"startUrls": ["https://www.despegar.com.ar/hoteles/h-265543/riu-cancun"]}` |
| ratings of a list of hotels by id | `{"hotelIds": ["265543", "123456"]}` |
| the AI summary in English | `{"hotelIds": ["265543"], "locale": "en"}` or `"country": "us"` |
| ratings as seen from Mexico, in Spanish | `{"hotelIds": ["265543"], "country": "mx"}` |
| only well-rated hotels (8 or more out of 10) | `{"hotelIds": ["265543", "123456"], "minRating": 8}` |
| ratings only, no comment rows | `{"hotelIds": ["265543"], "includeComments": false}` |
| opiniones y calificaciones de hoteles, puntuación de huéspedes | the same inputs; a Spanish-language site (`ar`, `mx`, ...) returns the summary, labels and dates in Spanish |

Every row carries `type`. A `hotel` row (billed, $0.004) has `hotel_id`, `hotel_name`, `hotel_url`, `city`, `country`, `address`, `latitude`, `longitude`, `stars`, `rating` (0-10) with `rating_scale`, `rating_5` and `rating_label`, `review_count`, `reviews_shown`, `score_service`, `score_staff`, `score_location`, `score_internet`, `score_cleanliness`, `score_value`, `category_scores`, `summary` (the AI-written review summary), `verified_note`, `providers`, `trip_types`, `page_language` and `page_country`. A `review` row (free, up to four per hotel while `includeComments` is true) has `review_id`, `rating`, `rating_5`, `review_date`, `review_month`, `text`, `good`, `bad`, `reviewer`, `reviewer_country`, `trip_type`, `language`, `provider` and `helpful_votes`. A `status` row (free, one per input) says `status` `ok`, `no_reviews` (unrated hotel, free), `not_found`, `filtered` (below `minRating`, free), `duplicate`, `blocked` (DataDome), `limited` (spending limit reached first) or `error`, with `hotels` and `comments` delivered and the reason. An input the actor cannot act on (a URL from another site, an id that is not a number, an unknown country, an empty list) ends the run with no rows and the reason on the run card, nothing charged; a site that blocks every hotel fails the run loudly.

Last verified working: 2026-08-29.

## What the Despegar Hotel Ratings Scraper returns

Two row types plus a status row, all in one dataset:

| Row | Charged | What it is |
|---|---|---|
| `hotel` | **$0.004** | The ratings payload: score, review count, six category scores, AI summary, stars, place, coordinates |
| `review` | free | The up-to-four published comments, with their own scores, months, traveller types and reviewer countries |
| `status` | free | One per target: `ok`, `no_reviews`, `not_found`, `filtered`, `duplicate`, `blocked`, `limited` or `error` |

A `hotel` row, trimmed — this is a **despegar hotel score** for a five-star resort in Cancún, the kind of **cancun hotel ratings** row a comp-set table is built from:

```json
{
  "type": "hotel",
  "target": "265543",
  "hotel_id": "265543",
  "hotel_name": "Riu Cancun",
  "hotel_url": "https://www.despegar.com.ar/hoteles/h-265543/riu-cancun-cancun",
  "city": "Cancún",
  "country": "México",
  "address": "Blvd. Kukulcan, Km 9, Manzana 50, Lote 5, Zona Hotelera Cancún - Quintana Roo",
  "latitude": 21.1370565,
  "longitude": -86.7485229,
  "stars": 5,
  "rating": 8.4,
  "rating_scale": 10,
  "rating_5": 4.2,
  "rating_label": "Muy bueno",
  "review_count": 4511,
  "reviews_shown": 4,
  "score_service": 8.3,
  "score_staff": 9.1,
  "score_location": 9.6,
  "score_internet": 8.9,
  "score_cleanliness": 8.9,
  "score_value": 8.6,
  "category_scores": {"service": 8.3, "servicePersonal": 9.1, "location": 9.6, "internetAccessAndQuality": 8.9, "cleaning": 8.9, "qualityprice": 8.6},
  "summary": "El Riu Cancún es un lugar increíble para relajarse y disfrutar…",
  "verified_note": "Clientes verificados por Grupo Despegar.",
  "providers": ["DESPEGAR"],
  "trip_types": ["couple", "friends", "singles", "family"],
  "page_language": "es",
  "page_country": "AR",
  "fetched_at": "2026-08-29T18:20:11+00:00"
}
```

A `review` row — one of at most four:

```json
{
  "type": "review",
  "review_id": "661ec3c8fe92b10bfdade9ca",
  "hotel_id": "265543",
  "hotel_name": "Riu Cancun",
  "rating": 9.7,
  "rating_5": 4.85,
  "review_date": "Abril 2024",
  "review_month": "2024-04",
  "text": "Hospitalidad de parte de todo el personal… — No alcance a darme cuenta que faltara algo.",
  "good": "Hospitalidad de parte de todo el personal…",
  "bad": "No alcance a darme cuenta que faltara algo.",
  "reviewer": "Lisbeth",
  "reviewer_country": "Chile",
  "reviewer_country_code": "CL",
  "trip_type": "couple",
  "trip_type_label": "En pareja",
  "language": "es",
  "provider": "DESPEGAR",
  "provider_label": "Huésped verificado",
  "helpful_votes": 25
}
```

The `summary` field deserves a note, because it is the most useful thing on the page and it is **not our text**: Despegar generates it from all of a hotel's reviews and prints it above the comments. Treat it as the site's editorial output, cite it as such, and it becomes a ready-made **hotel review summary** for a report, a comparison table or an LLM prompt — you get the gist of 4,511 reviews without reading them.

## Despegar hotel ratings: every field, explained

| Field | Rows | Meaning |
|---|---|---|
| `type` | all | `hotel`, `review` or `status` |
| `target` | all | The input value this row came from |
| `hotel_id` | all | Despegar's numeric id, the number in `/h-<id>/`; identical on every country site |
| `hotel_name` | hotel, review, status | Hotel name in the page's language |
| `hotel_url` | hotel, review | Canonical page URL on the domain that was read |
| `city`, `country`, `address` | hotel | Place, read from the location line and the map block |
| `latitude`, `longitude` | hotel | Coordinates of the hotel marker |
| `stars` | hotel | Star rating printed above the name |
| `rating` | hotel, review | The 0-10 **hotel score**; on a review row, that guest's own score |
| `rating_scale` | hotel | Always `10`, so a consumer never has to guess the scale |
| `rating_5` | hotel, review | The same value on the 0-5 star scale, for joins with other sources |
| `rating_label` | hotel | Despegar's word for the score: `Muy bueno`, `Excelente`, `Very good`… |
| `review_count` | hotel | How many reviews the score is based on — **not** how many rows you get |
| `reviews_shown` | hotel | How many comments the page actually published: 0-4 |
| `score_service` | hotel | Category score: services and installations |
| `score_staff` | hotel | Category score: accommodation staff |
| `score_location` | hotel | Category score: location |
| `score_internet` | hotel | Category score: internet / Wi-Fi |
| `score_cleanliness` | hotel | Category score: cleaning |
| `score_value` | hotel | Category score: price/quality |
| `category_scores` | hotel | The same six, keyed by Despegar's own codes |
| `summary` | hotel | Despegar's AI-written summary of what guests say |
| `verified_note` | hotel | Their provenance line, e.g. "Clientes verificados por Grupo Despegar." |
| `providers` | hotel | Which review providers the comments come from (`DESPEGAR` everywhere we looked) |
| `trip_types` | hotel | Traveller profiles the page offers: couple, friends, singles, family |
| `page_language`, `page_country` | hotel | Which country site answered, e.g. `es` / `AR` |
| `review_id` | review | The comment's id |
| `review_date` | review | The month as printed, e.g. `Agosto 2023` — there is no day |
| `review_month` | review | The same normalised to `YYYY-MM` |
| `text`, `good`, `bad` | review | The **despegar hotel comments** themselves; Despegar splits it into a liked half and a disliked half and has no titles |
| `reviewer`, `reviewer_country`, `reviewer_country_code` | review | Who wrote it, when they published a name |
| `trip_type`, `trip_type_label` | review | `couple` / `family` / `friends` / `singles` and the page's wording |
| `language` | review | Language the comment was written in |
| `provider`, `provider_label` | review | Source and badge, e.g. `DESPEGAR` / `Huésped verificado` |
| `helpful_votes` | review | How many readers marked it useful |
| `status`, `hotels`, `comments`, `filtered`, `duplicates`, `error` | status | What happened to each target and why |
| `fetched_at` | all | UTC timestamp of the request |

## How to run it

Give hotel URLs, hotel ids, or both. Ids are cheapest: they need no lookup at all.

```json
{
  "hotelIds": ["265543", "4382832", "6599128"],
  "country": "mx",
  "includeComments": true,
  "minRating": 8,
  "sessions": 2,
  "perIp": 0.5,
  "proxyConfiguration": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}
}
```

- **startUrls** — full hotel page URLs on any country domain. Each URL is read on the domain you gave it, so one run can mix Argentina, Mexico and the English site.
- **hotelIds** — the numbers from `/h-<id>/`. They are global: an id found on the Chilean site works on the Mexican one.
- **country** — which site to read ids from: `com` (auto by exit IP), `us` (English), `ar`, `mx`, `co`, `cl`, `pe`, `uy`, `ec`, `bo`, `py`, `pa`, `cr`, `gt`. Brazil is `decolar.com` and it refused every request we made, so it is listed but not recommended.
- **locale** — `auto`, `es` or `en`. The site has no language switch of its own, so the language *is* the domain; this picks one when `country` is left at `com`.
- **includeComments** — emit the up-to-four comments as free rows. Off makes a run smaller, not cheaper.
- **minRating** — 0-10 floor applied **before billing**. A hotel below it costs nothing.
- **sessions**, **perIp** — how many proxy sessions run in parallel and how fast each goes. Defaults 2 and 0.5/s.
- **proxyConfiguration** — Apify Proxy, RESIDENTIAL group, and it is the default for a reason (see below).

Python, using the Apify client:

```python
from apify_client import ApifyClient
client = ApifyClient("<APIFY_TOKEN>")
run = client.actor("kestrel/despegar-hotel-ratings").call(run_input={
    "hotelIds": ["265543", "4382832"], "country": "ar", "minRating": 8})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "hotel":
        print(row["hotel_name"], row["rating"], row["review_count"], row["score_value"])
```

JavaScript / Node:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<APIFY_TOKEN>' });
const run = await client.actor('kestrel/despegar-hotel-ratings').call({
    startUrls: ['https://www.despegar.com.ar/hoteles/h-265543/riu-cancun'], includeComments: true });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'hotel'));
```

curl, straight against the API:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~despegar-hotel-ratings/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"hotelIds":["265543"],"country":"us","includeComments":true}'
```

## Hotel rating data you can actually use

A few jobs this pays for, all of which need the score and the category scores rather than a wall of text:

- **Competitor hotel ratings.** Pull your rivals' scores on a schedule and keep a table of **competitor hotel ratings** that updates itself; because you can **scrape despegar hotel ratings** by id, the same list works every day without re-resolving anything.
- **Rate-and-review benchmarking.** Pull the whole comp set in one run and compare `rating`, `score_location`, `score_value` and `score_staff` side by side. Because `rating_5` is on the 0-5 scale, the table joins straight to Google, TripAdvisor and Booking numbers.
- **LatAm market coverage.** Despegar is where a large share of Latin American leisure demand books, and its **latam hotel reviews** are a different guest population — for **latin america hotel reviews** there is no larger single source from the English-language OTAs — a resort can sit at 8.4 here and 3.9 on a US-facing site.
- **Hotel reputation monitoring.** Hotel review monitoring here means watching one number and six sub-numbers, which is exactly what **hotel reputation monitoring** dashboards consume. Schedule a daily run over your properties and watch `rating` and `review_count` move. A rising count with a falling score is the earliest signal a property has a problem.
- **Content and comparison pages.** `summary`, `rating_label` and the six category scores are enough to generate an honest "what guests say" block per hotel without scraping anybody's paragraphs wholesale.
- **Feeding an LLM.** The AI summary plus four dated comments is a compact, cheap context for a model that has to answer "is this hotel good for families?".

## Despegar hotel ratings vs a review scraper: which do you need?

Be blunt with yourself about the question you are answering:

| You need | Use |
|---|---|
| A score, category scores and a gist, for many hotels, cheaply | this actor |
| Hundreds of full reviews per property, with dates and replies | [Booking Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper) |
| Full review text, sub-ratings and trip types at TripAdvisor's depth | [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) |
| Nightly prices rather than opinions | [Booking Prices Scraper](https://apify.com/kestrel/booking-prices-scraper) |

Note what the pocket's other listings are called: a **despegar reviews scraper** or plain **despegar reviews** — wording that implies a review feed. Any listing that promises you "100 reviews per hotel" from this source is promising something the public page does not contain. We measured it, twice, with a real browser.

## How the Despegar scraper works under the hood

The hotel page is server-rendered. Everything the Opiniones section displays is already inside `<script id="serverApp-state">` as JSON: `landingModel.modules[]`, the module whose `id` is `ReviewsSummaryModule`, then `data.summary`. That object holds the score, the six categories, the generated summary and `user_reviews.items` — the comments. One HTTP GET per hotel returns all of it.

Three things make this a **despegar scraper** rather than a two-line script:

1. **The bot gate.** The site runs DataDome. Datacenter IPs are refused outright; a residential IP with a Chrome TLS fingerprint is served. The opposite of TripAdvisor, where a Firefox fingerprint is the one that passes — so the profile is pinned, and the actor ships `curl_cffi>=0.16`.
2. **The first-request 403.** A fresh session is often refused once; the refusal sets a `datadome` cookie and the *immediate retry on the same session* succeeds. The actor does exactly that before it rotates to a new IP, which is why a run does not burn residential traffic on rotations.
3. **The 200 that is not your hotel.** An id the site no longer has does not 404 — it redirects to the hotel list with HTTP 200. The actor checks the canonical URL still carries `/h-<id>/` **and** that the id matches the one you asked for. A page for a different hotel is reported `not_found`, never billed as yours.

Pacing is deliberately slow. Measured on the live site, one session served four hotel pages at 1 req/s and was then refused for the rest of the minute, so the default `perIp` is 0.5 and `sessions` is 2. Raising them does not make a run faster; it makes it retry.

## Frequently asked questions

### Why only four comments per hotel?

Because that is all the page publishes. `review_count` can say 4,511 while `reviews_shown` says 4. The site's own tracking call reports `total_comments: 4`, and a headed browser session found no endpoint that returns more — no XHR, no "see all reviews" route, no provider feed. Adding dates to the URL (the booking funnel) changes nothing: still four, still one provider. We would rather sell you the rating honestly than a review scraper that quietly returns four rows.

### Is `review_count` the number of rows I get?

No, and this is the single most important line in this readme. `review_count` is Despegar's own total; `reviews_shown` is how many comments came back (0-4). You are billed once per hotel either way — the comments are free.

### Does the country site change the numbers?

No. We fetched the same hotel on nine domains: identical id, identical 0-10 score, identical review count, identical four comments. What changes is the **language** of the AI summary, the category labels and the review dates, plus the page currency. Pick `us` for English, any LatAm code for Spanish.

### Can I get Brazilian hotel ratings?

Brazil is served by `decolar.com`, and it refused every request we made (six attempts across three residential sessions, all DataDome 403). The domain is in the input list for completeness, but expect `blocked` status rows. Brazilian *hotels* are of course covered by every other site — the id is global.

### What exactly is the AI review summary?

An **ai review summary** written by Despegar, not by us and not by an LLM we run. It is one paragraph distilling every review a hotel has, printed above the comments. It arrives in the `summary` field verbatim.

### What does a hotel with no reviews look like?

Its page simply has no ratings module. You get a `status` row with `no_reviews`, no hotel row, and **no charge**. That is an honest empty answer, and it is never confused with a block: a block is an HTTP 403 with a DataDome body, and it is reported as `blocked` with the reason in `error`.

### How much does a run cost?

$0.004 per hotel row delivered, including compute and residential proxy traffic. Comments, status rows, unknown ids, unrated hotels and hotels dropped by `minRating` are all free. Ten thousand hotels is $40 of events.

### Is scraping this legal?

You are reading a public page that requires no login, and taking facts from it — scores, counts, dates — which are not themselves copyrightable in most jurisdictions. That is generally lawful, and *hiQ v. LinkedIn* is the usual reference for public data. The legal caveats are real, though: the site's terms of use, the personal data in a reviewer's name and country (GDPR/LGPD apply if you store it), and the AI `summary`, which is Despegar's own creative text — quote it with attribution rather than republishing it as your own. Ask your own counsel before you build a product on it.

### Can I use it from n8n, Make.com or an AI agent?

Yes. The actor is a standard Apify actor, so it appears in the Apify nodes for n8n and Make.com, and through Apify's MCP server it can be called directly by an AI agent or by Claude. The dataset is available as JSON, CSV, Excel or an API URL, and the run summary is a single record in the key-value store under `SUMMARY`.

### What happens when I hit my spending limit?

Nothing is delivered that was not paid for. Every hotel is charged before its row is pushed; if the platform refuses the charge, the row is not pushed and the target is marked `limited`. Charged always equals delivered — that invariant is covered by the actor's own test suite across every input mode and budget.

### Can I fetch despegar hotel ratings by id, with no API key?

Yes — that is the normal way to run it. There is no public API here, so **despegar hotel ratings by id** is exactly what this actor does: you pass `hotelIds`, it reads the page. Using **despegar without an api key** is the point; the source publishes no key-based endpoint at all, and none is needed.

### How do I find hotel ids in the first place?

Any hotel URL contains one. Beyond that, the site's sitemaps in `robots.txt` all 404, so harvesting means reading city and home pages, which inline a dozen or two `/h-<id>/` links each. If you already have a list of properties, the fastest route is to search the site once by hand and keep the ids: they never change and they work on every country domain.

## Opiniones de hoteles: what LatAm buyers get

For Spanish-speaking users: este actor devuelve la puntuación de 0 a 10, las seis puntuaciones por categoría (servicios, personal, ubicación, Wi-Fi, limpieza y precio/calidad), el resumen automático y hasta cuatro comentarios por hotel, tal y como los publica la página. Las **opiniones de hoteles** completas no están disponibles públicamente en esta fuente — la página muestra cuatro, y este actor no promete más. Para avaliacoes de hoteis em português, os mesmos dados estão disponíveis em qualquer domínio do grupo, exceto o brasileiro.

## Guest scores in your warehouse

Each run writes one flat dataset, so the export is a single table:

```bash
curl "https://api.apify.com/v2/datasets/<datasetId>/items?format=csv&clean=1" > ratings.csv
```

That is how you **download despegar ratings csv** in one line. Filter `type == "hotel"` for the rating table, `type == "review"` for the comments, `type == "status"` for the audit trail. The dataset ships with prebuilt views — Overview, Hotel ratings, Category scores, Comments, Map and Status — so the Apify UI shows the right columns without any configuration. Schedule the actor daily and each run appends a dated snapshot, which is all a rating trend needs.

## Limits, and what this actor will never do

- **Four comments per hotel, maximum.** Not a setting, not a paging bug: the ceiling of the public page. `reviews_shown` tells you the exact number every time.
- **No day-level review dates.** The source publishes month and year only; `review_month` gives you `YYYY-MM`.
- **No management replies, no photos.** They are not on the page.
- **No search.** Give the actor hotels; it does not crawl destinations. That keeps costs predictable on a residential proxy.
- **No Brazilian domain.** `decolar.com` is hard-blocked, as described above.
- **Residential proxy required.** Datacenter ranges are refused by the source, so a run without residential proxy will produce `blocked` rows. It is the default in the input form; leave it alone.

Everything above was measured on 2026-08-29 against the live site through Apify's residential proxy, and the actor's fixtures are the captured pages themselves, so the next time the source changes shape the tests fail before your run does.

## Related scrapers

Despegar gives you the score and four comments. These read the full review text on the other sites, or the prices behind the scores:

- [Free Hotel Review Checker](https://apify.com/kestrel/hotel-reputation-checker) — the Despegar score next to Google, Tripadvisor, Booking.com, Agoda and Hostelworld for the same hotel, one row per site and the spread between them, free — run it first to see which site's text is worth paying for.
- [Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper) — hundreds of full reviews per property with the liked and disliked text split out, traveller type and the property's reply, when four comments are not enough.
- [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) — full review text with six sub-ratings, trip type, photos and the management response, in 30 site languages.
- [Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper) — Agoda guest reviews with separate positives and negatives and the hotel's reply, by hotel name, URL or id.
- [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices) — what the same hotels charge: every booking site's rate for a stay as its own row, for the price column next to a rating table.
- [Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity) — one row per property and stay with every OTA side by side and which ones undercut the hotel's own site, by how much.

The paid ones bill per delivered row and never charge for rows a filter or a spending limit removed; every one of them writes an Apify dataset you can export to CSV, Excel or JSON.
