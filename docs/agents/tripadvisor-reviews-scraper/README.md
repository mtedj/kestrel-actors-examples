# TripAdvisor Reviews Scraper & API: Hotel Reviews, Guest Reviews

A **tripadvisor reviews scraper** — a **hotel reviews scraper** for **tripadvisor hotel reviews** — that returns every review a hotel has as structured rows: **tripadvisor ratings** as 1–5 bubbles, the title and the full text, the six sub-ratings (value, rooms, location, cleanliness, service, sleep quality), the language it was written in and whether you are reading a machine translation, the stay date and trip type, the reviewer's profile, photos, helpful votes and the hotel's management response. It is a **tripadvisor scraper** for **guest reviews** built for **review monitoring**: give it hotels, get **tripadvisor review data** — **hotel review data** you can sort, filter and export.

Give it TripAdvisor hotel URLs, TripAdvisor location ids or hotel names. No login, no **tripadvisor api** key, no browser. It reads the same review pages a visitor sees — server-rendered, with the full review record inside — through a residential proxy and a browser-grade TLS fingerprint, so runs are fast and steady where plain scrapers are turned away. It bills per review row, and every filter (rating, trip type, date, text, translation) runs before billing, so a complaints feed pays only for complaints.

Last verified working: 2026-10-02.

## TripAdvisor 酒店评论、点评与管理方回复：中文调用与语言设置

按酒店名称、ID 或 URL 获取评论、星级、分项评分和管理方回复。

languages=["zh"] 选择中文站点；includeTranslated=false 排除机器翻译，只保留原文。2026-10-16 实测中文站点未返回可用页面，当前不承诺中文采集可用；下面示例使用英文站点。每种语言单独查询及计费；开启翻译后，同一评论可能按不同语言分别出现。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon_Lisbon_District_Central_Portugal.html"
  ],
  "languages": [
    "en"
  ],
  "maxReviewsPerHotel": 3,
  "includeTranslated": false,
  "sessions": 1
}
```

Avis TripAdvisor / recensioni / opiniones：跨语言分析时区分原文与机器翻译。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## TripAdvisor scraper for AI agents: which input answers which request?

Use it when the user wants the reviews of specific hotels on TripAdvisor — by name, URL or location id — with the bubble rating, text, six sub-ratings, trip type, stay date, reviewer, photos and the management response, once or on a schedule, in one or several languages. Do not use it to find hotels in a city (it takes hotels, not a destination search), for restaurant or attraction reviews (use kestrel/tripadvisor-restaurant-reviews), for prices, or for other sites' reviews (kestrel/hotel-reputation-checker compares the ratings of six sites for free; Booking.com, Agoda and Google have their own scrapers).

| The user asks for | Input |
|---|---|
| Reviews of a hotel by name | `{"hotelNames": ["Memmo Alfama Hotel, Lisbon"]}` — the newest 100 English reviews, at most $0.50 |
| Reviews of a hotel by URL | `{"startUrls": ["https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon.html"]}` |
| Every review the hotel has | add `"maxReviewsPerHotel": 0` |
| Only negative reviews, a complaints feed | add `"maxRating": 2, "maxReviewsPerHotel": 0` (filtered reviews are free; the cap is applied before the filter) |
| Only new reviews since the last run, review monitoring | add `"sinceDate": "2 days"` and an Apify schedule |
| What business travellers say | add `"tripTypes": ["business"]` |
| French and German reviews as written by those guests | add `"languages": ["fr", "de"], "includeTranslated": false` |
| Rating, review count, city ranking, address, amenities of each hotel | already in the free `hotel` row (`includeHotelRow` defaults to true) |
| The same hotels every day | pass the `location_id` values of a first run in `locationIds` |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `maxReviewsPerHotel` bounds the rows per hotel and language |

Rows come in three types. `review` (billed, $0.005): `review_id`, `rating`, `title`, `text`, `sub_ratings` (value, rooms, location, cleanliness, service, sleep_quality), `language`, `original_language`, `translated`, `review_date`, `stay_date`, `trip_type`, `helpful_votes`, `reviewer_name`, `reviewer_username`, `reviewer_hometown`, `reviewer_contributions`, `photos`, `response`, `response_date`, `url`. `hotel` (free, one per hotel and language): `rating`, `review_count`, `rating_counts`, `reviews_by_language`, `sub_ratings`, `ranking`, `ranking_position`, `ranking_of`, `address`, `city`, `latitude`, `longitude`, `phone`, `website`, `amenities`. `status` (free, one per hotel and language): `status` is `ok`, `no_reviews`, `not_found`, `duplicate` or `error`, with `reviews`, `filtered`, `pages`, `total` and `error`. A hotel with no reviews, an unknown id or a name that matches nothing is a `status` row that says why — never a charge and never a failed run; a blocked or throttled source fails the run so it is not mistaken for "no reviews". `maxReviewsPerHotel` is applied to the reviews read (newest first) before the filters, so 100 with `maxRating: 2` delivers the low-rated reviews among the newest 100: for a complete complaints list set it to 0 or use `sinceDate`.

**TripAdvisor reviews in other languages.** `languages` picks the country site, so one run can return avis TripAdvisor (tripadvisor.fr), recensioni TripAdvisor (tripadvisor.it), opiniones de TripAdvisor (tripadvisor.es), TripAdvisor Bewertungen (tripadvisor.de) and avaliações do TripAdvisor (tripadvisor.com.br): 30 country sites, 24 languages, each row saying which language it was written in.

## What does the TripAdvisor reviews scraper do?

You give it hotels. It gives you their **tripadvisor hotel reviews** as rows, in the languages you choose.

- **Every review, newest first.** TripAdvisor lists reviews ten to a page, newest first; the actor walks the pages until it has what you asked for or the list ends. A 2,000-review hotel is 200 pages; `maxReviewsPerHotel` keeps that under control.
- **The whole record.** Bubbles, title, text, six sub-ratings, stay month, trip type (family, couples, solo, business, friends), the reviewer's name, handle, verified flag, contribution counts and hometown, attached photos, helpful votes, and the management response with its date. Each review also carries its own URL, so any row can be checked against the site.
- **Thirty country sites, 24 languages.** TripAdvisor is not one site: tripadvisor.com serves English, tripadvisor.de German, tripadvisor.fr French, and so on — each domain shows reviews written in its language plus machine translations of the rest. `languages` picks the domains; each row says which language it was read in, which language it was written in, and whether it is a translation.
- **A hotel row for context.** Bubble rating, total review count, reviews per rating and per language, the six aspect averages, the city ranking ("#33 of 372 hotels in Lisbon"), address, coordinates, phone, website and amenities. Never charged.
- **Filters that run before billing.** `maxRating` for complaints feeds, `tripTypes`, `sinceDate` for schedules, `requireText`, `includeTranslated`. Filtered reviews are never charged.

## TripAdvisor reviews by hotel: URL, location id or name

Three ways to point at a hotel, mixed freely:

- **URLs** — any TripAdvisor hotel page, on any domain: `https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon.html`. Only the numeric `d4509998` matters; TripAdvisor redirects a wrong geo id or slug to the canonical page.
- **Location ids** — `4509998` or `d4509998`, the number after `d` in any TripAdvisor URL. What an earlier run's `location_id` gives you; the fastest path because nothing needs resolving.
- **Names** — "Memmo Alfama Lisbon". Resolved through TripAdvisor's own typeahead. Its answer must share at least half of the words you typed; a name TripAdvisor does not know comes back as an error row instead of a random hotel, and the resolved name is in the hotel and status rows so you can check the match.

A URL, its id and its name are one hotel: the actor resolves first, then dedupes, so the reviews are read and billed once, and the extra targets are reported as duplicates.

## TripAdvisor negative reviews without paying for the happy ones

`maxRating: 2` keeps only one- and two-bubble reviews; `maxRating: 3` adds the middling ones. The rejected reviews are never billed. Because TripAdvisor serves reviews newest first with no rating sort, the pages are still read (each page is about a megabyte of residential proxy traffic, which is the actor's own cost, not yours), so pair a complaints feed with a sensible `maxReviewsPerHotel` or a `sinceDate`. A hotel with 1,599 five-bubble reviews and 30 low ones delivers and bills 30 rows out of the pages it read.

Add `requireText: true` to skip rating-only reviews, `tripTypes: ["business"]` to hear only from business travellers, and `includeTranslated: false` to keep only reviews written in the language you are reading.

## Hotel review data for revenue, operations and analysts

- **Hotel reputation management.** Schedule one run a day with `sinceDate: "2 days"` for your properties and a comp set. Pages come newest first, so the run stops after the first page that predates the cut — two or three pages per hotel per day — and every new review lands in a dataset you can route to Slack, a sheet or a ticket.
- **Tripadvisor competitor reviews.** The hotel row's `rating_counts`, `reviews_by_language` and `sub_ratings` describe a hotel in one line; the review rows explain the numbers. Ten hotels, one run, one table.
- **Voice of the customer.** Six sub-ratings per review plus free text is the input every **hotel sentiment analysis** wants: the sub-ratings tell you *what* slipped (rooms 2, service 5), the text tells you why.
- **Multi-language listening.** A Lisbon hotel has 1,393 English reviews, 220 French, 141 German and 74 Portuguese. Read the French and German sites to hear those guests in their own words, with `includeTranslated: false` so each review arrives once.

## Input

| Field | What it does |
|---|---|
| `startUrls` | TripAdvisor hotel URLs on any domain; only the `d<id>` matters. |
| `locationIds` | TripAdvisor location ids, `4509998` or `d4509998`. |
| `hotelNames` | Hotel names, ideally with the city; resolved through TripAdvisor's typeahead with a word-overlap guard. |
| `languages` | Which sites to read, one job per hotel and language: `en` (tripadvisor.com), `en-gb`, `de`, `fr`, `es`, `it`, `pt` (tripadvisor.com.br), `nl`, `ja`, `zh`, `ru`, `sv`, `da`, `no`, `fi`, `pl`, `tr`, `el`, `ko`, `th`, `vi`, `id`, `cs`, `hu`, `he`, `en-au`, `en-ca`, `en-in`, `en-ie`, `en-sg`. Default `["en"]`. |
| `maxReviewsPerHotel` | 0 = every review the site lists in that language; N = the newest N. Default 100. The main cost control. |
| `maxRating` | 0 = all; 1–5 = keep reviews with that many bubbles or fewer. Filtered reviews are never charged. |
| `tripTypes` | Keep only `family`, `couples`, `solo`, `business`, `friends`. Empty = all. |
| `sinceDate` | Keep reviews published on or after this date — `2026-06-01` or relative (`"30 days"`, `"2 weeks"`). Paging stops once a whole page predates it. |
| `requireText` | Drop rating-only reviews before billing. |
| `includeTranslated` | Include machine-translated reviews (default true). Off = only reviews written in the site's language. |
| `includeHotelRow` | Emit the free hotel context row per hotel and language (default true). |
| `sessions`, `perIp` | Residential proxy sessions in parallel (default 2) and the pace per session (default 1 request/s). |
| `proxyConfiguration` | Apify Proxy, `RESIDENTIAL` group — required, and the default. |

### Example: a scheduled complaints feed

Every morning, every new one- or two-bubble review of five properties, in English and German, with text:

```json
{
  "locationIds": ["4509998", "228423"],
  "hotelNames": ["The Lumiares Lisbon", "Bairro Alto Hotel Lisbon", "Memmo Príncipe Real"],
  "languages": ["en", "de"],
  "sinceDate": "2 days",
  "maxRating": 2,
  "requireText": true,
  "maxReviewsPerHotel": 0
}
```

Most days this reads two pages per hotel and language and bills nothing, because nothing new was under three bubbles. When something lands, it is in the dataset before the morning meeting.

### Example: the full French corpus of a competitor set

```json
{
  "startUrls": [
    "https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon.html",
    "https://www.tripadvisor.com/Hotel_Review-g189158-d190364-Reviews-x.html"
  ],
  "languages": ["fr"],
  "includeTranslated": false,
  "maxReviewsPerHotel": 0
}
```

The .com URLs are fine even though the run reads tripadvisor.fr — the id is what counts. `includeTranslated: false` means each row is a review a French-speaking guest actually wrote.

### Example: what business travellers say, by id

```json
{
  "locationIds": ["d4509998"],
  "tripTypes": ["business"],
  "maxReviewsPerHotel": 300,
  "includeHotelRow": false
}
```

## Output

Three row types share one dataset, told apart by `type`.

**`review`** — one per review, charged:

```json
{
  "type": "review",
  "target": "https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon_Lisbon_District_Central_Portugal.html",
  "review_id": "1075128384",
  "location_id": "4509998",
  "hotel_name": "Memmo Alfama Hotel",
  "language": "en",
  "original_language": "en",
  "translated": false,
  "title": "A Gem in the Heart of Alfama",
  "text": "This place is a gem!\nOn a quiet side street just off the route of the famous tram Electrico #28, this is a gorgeous haven in the heart of Alfama. Our room had a view out over the Tagus River…",
  "rating": 5,
  "sub_ratings": {"value": 4, "rooms": 4, "location": 5, "cleanliness": 5, "service": 5, "sleep_quality": 5},
  "review_date": "2026-08-27",
  "created_date": "2026-08-27",
  "stay_date": "2026-08-31",
  "trip_type": "COUPLES",
  "helpful_votes": 0,
  "reviewer_name": "Frank S",
  "reviewer_username": "992franks",
  "reviewer_verified": false,
  "reviewer_contributions": 391,
  "reviewer_helpful_votes": 169,
  "reviewer_hometown": "Brooklyn, New York",
  "photos": [],
  "photo_count": 0,
  "response": "Dear Frank, thank you so much for your incredible review…",
  "response_date": null,
  "response_id": "974781822",
  "url": "https://www.tripadvisor.com/ShowUserReviews-g189158-d4509998-r1075128384-Memmo_Alfama_Hotel-Lisbon_Lisbon_District_Central_Portugal.html",
  "hotel_url": "https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon_Lisbon_District_Central_Portugal.html",
  "fetched_at": "2026-08-29T15:20:11+00:00"
}
```

`rating` is 1–5 bubbles. `sub_ratings` carries only the aspects the reviewer rated. `language` is the site the row was read on; `original_language` is what the guest wrote in; `translated` is true when the text is TripAdvisor's machine translation. `stay_date` is the month of the stay as TripAdvisor records it. `trip_type` is one of `FAMILY`, `COUPLES`, `SOLO`, `BUSINESS`, `FRIENDS` or null. `response` is the management response text, with `response_date` and `response_id` when TripAdvisor exposes them. `photos` are 1,200-pixel renditions.

**`hotel`** — one per hotel and language, free: `location_id`, `geo_id`, `hotel_name`, `url`, `rating` (the hotel's bubble rating, e.g. 4.7), `review_count` (all languages), `rating_counts` (`{"1": 13, "2": 17, "3": 68, "4": 280, "5": 1599}`), `reviews_by_language` (`{"en": 1393, "fr": 220, "de": 141, …}`), `sub_ratings` (six aspect averages), `ranking` (`"#33 of 372 hotels in Lisbon"`) with `ranking_position` and `ranking_of`, `address`, `city`, `postal_code`, `country_code`, `latitude`, `longitude`, `phone`, `website`, `price_range`, `amenities`, `reviews_listed` (what the site lists in this language, translations included), `reviews_fetched`, `fetched_at`.

**`status`** — one per hotel and language plus one per duplicate or failed target, free: `target`, `location_id`, `hotel_name`, `language`, `status` (`ok`, `no_reviews`, `not_found`, `duplicate`, `error`), `reviews` delivered, `filtered` (dropped by your filters, never charged), `pages` read, `total` listed, `duplicates`, `error`, `fetched_at`.

The run's key-value store holds a `SUMMARY` record: hotels, jobs, reviews, filtered, duplicates, pages, not_found, errors, what was charged, whether the spending limit was hit, HTTP stats (including how many DataDome refusals were rotated past) and the run time.

## How much does it cost?

**$0.005 per review row.** Hotel rows, status rows, filtered reviews, unknown ids, duplicate targets and reviews the spending limit refused are free. Every review a hotel has on the English site — say 1,456 — is $7.28; a daily complaints feed that finds two complaints a week costs cents a month. Set `maxReviewsPerHotel` and `sinceDate` to keep runs the size you want, and the run's `maxTotalChargeUsd` as a hard ceiling. Residential proxy traffic (about a megabyte per ten reviews) is included in the price.

## TripAdvisor reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

**Python**

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/tripadvisor-reviews-scraper").call(run_input={
    "locationIds": ["4509998"],
    "languages": ["en", "fr"],
    "maxRating": 3,
    "requireText": True,
    "maxReviewsPerHotel": 500,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["language"], row["rating"], row["review_date"], row["title"], "-", (row["response"] or "")[:40])
```

**JavaScript**

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/tripadvisor-reviews-scraper').call({
    hotelNames: ['Memmo Alfama Lisbon', 'The Lumiares Lisbon'],
    sinceDate: '30 days',
    includeTranslated: false,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter(r => r.type === 'review');
console.log(reviews.length, 'reviews;', reviews.filter(r => r.response).length, 'answered by the hotel');
```

**curl**

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~tripadvisor-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"startUrls": ["https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon.html"], "maxReviewsPerHotel": 50}'
```

**n8n and Make.** Use the Apify node (or a plain HTTP Request node calling `run-sync-get-dataset-items` as above), then a filter on `type = review` and whatever you want to do with the rows — a Slack alert for `rating <= 2`, a Google Sheet, a CRM ticket. The `sinceDate` field takes relative dates so the schedule never goes stale. Ready-made review-alert workflows for the sister actors are in [github.com/mtedj/kestrel-actors-examples](https://github.com/mtedj/kestrel-actors-examples).

**MCP and AI agents.** The actor is on Apify's MCP server, so a Claude, Cursor or custom agent can ask for "the latest negative TripAdvisor reviews of hotel X" and get the rows; the input schema tells the agent what every field does.

## Is it legal to scrape TripAdvisor reviews?

The actor reads public review pages that any visitor sees without logging in and returns what is on them; it stores nothing beyond the rows in your dataset. Reviews are user-generated content that reviewers published under a public name or handle: if you build a product on top, you are the data controller for whatever you keep, so retain what you need (for most review monitoring that is the text, rating and date), respect deletion, and read TripAdvisor's terms before scraping at scale — they restrict automated access, and the responsibility for how the data is used is yours. Do not use it to republish reviews wholesale; do use it to understand what guests say about a property.

## Limits and honest notes

- **Newest first only.** TripAdvisor's pages sort by date and expose no rating or helpfulness sort, so `maxRating` reads pages and filters them. A complaints feed on a huge hotel is best combined with `sinceDate`.
- **Language counts differ from the total.** `review_count` on the hotel row is the all-language total (1,977); `reviews_listed` and `total` are what the site you read lists in its language, translations included (1,456 on the English site, 595 on the German site). Native-language counts are in `reviews_by_language`.
- **A translation is a separate row per language.** With `languages: ["en", "de"]` a German-written review appears once from tripadvisor.de (original) and once from tripadvisor.com (machine-translated). `includeTranslated: false` keeps each review exactly once.
- **Residential proxy is not optional.** TripAdvisor's bot gate refuses every datacenter range; the actor also needs a Firefox-grade TLS fingerprint, which it carries itself. A refused page is rotated and retried, and after six refusals the hotel is reported as an `error` — never as "no reviews".
- **Pages are heavy.** About one megabyte per ten reviews, paced at one page per second per session. Two sessions read roughly 20 reviews a second.
- **Hotels only.** Restaurants, attractions and vacation rentals have different page shapes; give the actor `Hotel_Review` pages.

## FAQ

### Does it need a TripAdvisor API key or login?

No. There is no public **tripadvisor api** for reading reviews (the Content API is for partners and does not return review text); the actor reads the public review pages, which carry the full record.

### Can I download TripAdvisor reviews as CSV or Excel?

Yes. Every run writes an Apify dataset; open it in the Console and export **tripadvisor reviews CSV**, Excel, JSON or XML, or pull it through the API. The `reviews` and `complaints` views are ready-made column layouts.

### How do I get only TripAdvisor negative reviews?

Set `maxRating` to 2 (or 3). Reviews above it are dropped before billing. Add `requireText: true` so every row has something to read, and `sinceDate` for a rolling window.

### Can I get TripAdvisor reviews by location id, URL or name?

Any of the three. Ids are fastest; URLs need no lookup either (only the `d<id>` in them matters); names go through TripAdvisor's typeahead with a guard against wrong matches.

### How many reviews can one hotel return?

All of them, per language: `maxReviewsPerHotel: 0` walks every page the site lists. Large hotels have thousands; a `sinceDate` or a cap keeps a scheduled run small.

### Can I get TripAdvisor reviews in multiple languages, and are they translated?

You choose the sites with `languages`; each site shows reviews written in its language plus machine translations of the others, marked `translated: true` with the `original_language`. Untick `includeTranslated` to keep originals only.

### Does it include the TripAdvisor management response?

Yes — the **tripadvisor management response** is in `response`, with `response_date` and `response_id` when TripAdvisor exposes them.

### Can I scrape TripAdvisor reviews without an API?

That is what this is — **tripadvisor reviews without API** access: the review pages are read directly, no GraphQL, no tokens, no browser. If TripAdvisor changes its pages the actor is fixed, and a daily canary run catches breakage within a day.

### Can I use it for hotel sentiment analysis?

Yes — the six sub-ratings, the free text and the trip type per review are the inputs sentiment work needs, and the `original_language` lets you route each text to the right model.

### What do bulk hotel reviews cost?

$0.005 per review, nothing else. Ten hotels × 500 newest reviews = 5,000 rows = $25; the daily feed that follows costs only what is new.

## Review monitoring across a portfolio: TripAdvisor guest feedback every morning

Put every property and its comp set in `locationIds`, schedule the actor daily with `sinceDate: "2 days"` and `maxReviewsPerHotel: 0`, and dedupe on `review_id` + `language` downstream. Each run reads two or three pages per hotel and language, delivers the new reviews, and its status rows tell you how many were filtered, how many pages were read and whether any hotel failed.

### Guest feedback data that keeps its structure

Rows never change shape: every review row carries every field (null where TripAdvisor has nothing), so a sheet or a table built on the first run keeps working. `sub_ratings` and `photos` are nested where the data is naturally nested and flat everywhere else.

### What this does not do

It does not write reviews, vote, flag or contact reviewers; it does not read restaurants or attractions; it does not sort by rating (TripAdvisor does not expose that on its pages); and it does not bypass TripAdvisor's residential-only gate with anything other than a residential proxy.

### Choosing languages

Read the site your guests use. For an international hotel that is usually `en` plus the two or three languages with the highest `reviews_by_language` counts on the hotel row; with `includeTranslated: false` each review arrives once, in the words the guest wrote.

## Related scrapers

Hotel reviews live on more than one site. These read the others, and they share the same row conventions, the same pay-per-delivered-row billing and the same scheduling story:

- **[Despegar Hotel Ratings Scraper](https://apify.com/kestrel/despegar-hotel-ratings)** — Latin America's largest OTA: guest score, six category scores and the site's own summary of what guests say, per property.
- **[TripAdvisor Restaurant Reviews Scraper](https://apify.com/kestrel/tripadvisor-restaurant-reviews)** — the same engine on restaurants and attractions, with the food/service/value/atmosphere sub-ratings and the dish keywords a hotel page does not carry.
- **[Hostelworld Reviews Scraper](https://apify.com/kestrel/hostelworld-reviews-scraper)** — hostel guest reviews with eight sub-ratings, traveller group and trip type, and the owner's reply.
- **[Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper)** — Booking.com guest reviews with liked and disliked text split, traveller type and the property's reply.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives.
- **[Trip.com Reviews Scraper](https://apify.com/kestrel/trip-com-reviews-scraper)** — Trip.com and Ctrip reviews with four sub-scores and the Chinese-language corpus.
- **[HRS Reviews Scraper](https://apify.com/kestrel/hrs-reviews-scraper)** — HRS business-travel reviews with twelve category votes.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — what the same hotels charge, per booking source and stay.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
