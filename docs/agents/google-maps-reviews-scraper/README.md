# Google Maps Reviews Scraper — Date Range, New-Only, Complete

This Google Maps reviews scraper reads the Google reviews of any place — a restaurant, a hotel, a clinic, a competitor, all 40 branches of your own brand — and gives you, as a Google reviews scraper should, one clean row per review: stars, the full text, **exact** publish and edit dates, the **owner replies**, likes, photos, the reviewer, and the sub-ratings (food, service, rooms…) when the reviewer gave them. It was built from what users of other Google reviews scrapers complain about: it checks every place against the total Google lists and tells you the result, it has a **true date range** and **new-reviews-only** review monitoring so repeat runs stay cheap, and it accepts whatever you have — a Maps URL, a short link, a place id, or just "name, city". No login, no API key, no browser. $1 per 1,000 reviews.

Last verified working: 2026-09-21

## 谷歌地图评论、商家评价与店主回复：中文调用与语言设置

按地点 ID、URL 或名称读取评论、精确日期、图片和店主回复，可筛选日期或新评论。

reviewLanguages=["zh"] 筛选中文原文；language 设置界面及 translate 的目标语言。翻译模式和原文筛选用途不同；country 不会按评论者国家过滤。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "places": [
    "https://www.google.com/maps/place/?q=place_id:ChIJD3uTd9hx5kcR1IQvGfr8dbk"
  ],
  "maxReviewsPerPlace": 1,
  "language": "zh-CN",
  "translate": "original",
  "sessions": 1
}
```

Avis Google Maps / reseñas / Google Bewertungen：精确日期不依赖界面语言。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Google Maps reviews scraper for AI agents: which input answers which request?

Built to be called by an AI agent (Claude, ChatGPT, or any MCP client through the Apify MCP server) as well as by people: one call, one flat table back, no API key, no login, and the cost is known before the run — at most `maxReviewsPerPlace` × $0.001 per place, and only reviews that pass the filters count.

Use it when the task is to **read the reviews of known places** — a restaurant, a hotel, a clinic, a competitor, every branch of a brand — and get stars, text, exact dates, owner replies and reviewer details, or to **watch places for new reviews** on a schedule. Do not use it to find businesses by category or to get phone numbers, websites or emails (that is `kestrel/google-maps-scraper`), and do not pass a search term expecting reviews of many places: give it the places.

| The user asks for | Input |
| --- | --- |
| "all reviews of this place" | `{"places": ["https://maps.app.goo.gl/AbCdEfGh12345"], "maxReviewsPerPlace": 0}` |
| "the latest 100 reviews" | `{"places": ["Katz's Delicatessen, New York"], "maxReviewsPerPlace": 100}` (`sort` newest is the default) |
| "reviews from the last 30 days" / "since 1 July" / "Q2 2026" | add `"fromDate": "30 days"` or `"fromDate": "2026-07-01"`, optionally `"toDate": "2026-09-30"`, with `"maxReviewsPerPlace": 0` |
| "new reviews every week" (scheduled feed) | add `"onlyNew": true, "monitorKey": "my-feed"` |
| "negative reviews" / "complaints" | add `"maxStars": 2, "sort": "lowest"` |
| "reviews that mention parking" | add `"keywords": ["parking"]` |
| "reviews with text only" (sentiment, summaries) | add `"onlyWithText": true` |
| "reviews we have not replied to" | add `"hasOwnerReply": "no"` |
| "everything in English" | add `"translate": "translated", "language": "en"` |
| "reviews written in German only" | add `"reviewLanguages": ["de"]` |
| "by place id" / "by CID" / "this short link" | `{"places": ["ChIJD3uTd9hx5kcR1IQvGfr8dbk"]}` — a place id, CID, feature id, place URL, short link or search URL all go in `places` |
| "rating and review count only" | `{"places": ["…"], "maxReviewsPerPlace": 1}` — the free `place` row carries the rating, the listed total and the histogram; one review is billed |

What comes back: rows with `type: "review"` (`review_id`, `place_id`, `place_name`, `stars`, `text`, `text_translated`, `original_language`, `published_at`, `updated_at`, `edited`, `likes`, `photos`, `owner_reply_text`, `owner_reply_at`, `reviewer_name`, `reviewer_url`, `reviewer_is_local_guide`, `sub_ratings`, `visit_details`), one free `type: "place"` row per place (`rating`, `reviews_total`, `histogram`, `reviews_read`, `reviews_delivered`, `completeness`, `stopped_by`, `trend`) and one free `type: "status"` row per input line (`status` = `ok`, `no_reviews`, `not_found`, `duplicate` or `error`, plus `found`, `filtered`, `filtered_by`, `already_seen`, `charged`). An unknown place, a place with no reviews and a date range nothing falls in are all successful runs that cost $0 — read the status row to explain an empty result instead of guessing. Charged review events always equal delivered review rows. The text comes back in its original language or translated, so reseñas de Google Maps, Google Bewertungen (Rezensionen), avis Google, recensioni Google and avaliações do Google are all the same call.

## What does the Google Maps Reviews Scraper do?

You give it places. For each place it:

1. **Finds the place** — from a Google Maps URL, a `maps.app.goo.gl` or `share.google` short link, a place id (`ChIJ…`), a CID, or a plain `name, city`. No place id is needed for a name or a search URL; the actor resolves it.
2. **Reads what Google lists** — the rating, the total number of reviews and the per-star histogram. This is the number your delivery is checked against.
3. **Walks the reviews** in the order you choose, 50 at a time, applying your filters *before* anything is charged, and stopping as early as your date range or new-only memory allows.
4. **Reports honestly** — one free `place` row per place with a completeness verdict such as `4,404 listed, 4,404 read — complete`, and one free `status` row per input line saying what was found, filtered, skipped and charged.

It is a reviews tool, not a general Google Maps scraper: it does not list places or collect contacts, it reads business reviews — all of them, or exactly the slice you ask for — and it works as a Google reviews API for your own code: one HTTP call in, JSON out.

Three row types share one dataset: `review` (charged), `place` (free) and `status` (free).

## Google reviews you can trust: complete Google reviews, checked on every place

The most common complaint about Google reviews scrapers is silent incompleteness: *"we have over 1,950 Google reviews, only got 1,850 back"*, *"scraping the same place twice leads to different datasets"*, *"out of 9,000 reviews there are 6,437 duplicates"*. This actor treats that as the main job:

- **Completeness check on every place.** The reviews read are compared with the total Google lists. If a full walk comes up more than 2% short, the actor walks the place again in another sort order and merges the two passes. The verdict is printed on the `place` row and is never silent: `1,950 listed, 1,948 read, 2 withheld by Google`.
- **Zero duplicates.** Reviews are de-duplicated by Google's own review id, within a walk and across passes. The `status` row tells you how many repeats Google served (`duplicates`), none of which you see or pay for.
- **No false empties.** Google sometimes answers an empty page to a busy IP. An empty page while Google still lists more reviews is never read as "no more reviews": the same page is asked again from another IP.
- **Repeatable.** The newest-first feed is strictly ordered by last-modified time (measured: 0 order inversions in a 4,404-review walk), so the same place walked twice gives the same set — on the release test, identical id sets on places of 4,222 and 1,215 reviews, and a difference of one review on a third. That last one is Google, not the actor: its feed serves about one review in several thousand intermittently, and the listed total moves by one with it.
- **Honest billing.** The number of `review` events charged always equals the number of review rows delivered. Your spending limit is honoured mid-place. A place Google does not know ends as a green run with a `not_found` status row and a $0 charge.

On the release test a bakery with 4,404 listed reviews was read in full: 4,404 delivered, 0 duplicates, and the delivered stars matched Google's histogram star for star (277 / 220 / 363 / 692 / 2,852).

## Google reviews by date range — without rescraping everything

*"Would love a 'from date' and 'to date'… now I need to rescrape everything I already have."* Set `fromDate` and/or `toDate`, as a date (`2026-07-01`) or a look-back (`30 days`, `6 months`).

With the default newest-first order the actor **stops reading at your From date**. A place with 50,000 reviews and 40 reviews from the last 30 days costs one page and 40 reviews — not a thousand pages. Reviews newer than `toDate` are read past and not charged.

```json
{
  "places": ["Katz's Delicatessen, New York"],
  "fromDate": "2026-04-01",
  "toDate": "2026-06-30",
  "maxReviewsPerPlace": 0
}
```

Dates are compared with `published_at`, the moment the review was first posted. Turn on `includeEdited` and a review that was *edited* inside the range counts as inside it too.

## Review monitoring: only new reviews, and a quiet run costs $0

For agencies, multi-location brands and anyone who wants new Google reviews in Slack — Google reviews for multiple locations is exactly what this mode is for: turn on `onlyNew` and put the run on a schedule.

- The first run delivers up to `maxReviewsPerPlace` reviews per place and remembers them.
- Every later run delivers — and bills — **only reviews it has not delivered before**, then stops at the first page of already-delivered reviews. For most places that is a single request.
- A run that finds nothing new delivers 0 rows and charges **$0**.
- With `includeEdited`, a review whose author edited it after you received it is delivered again (`edited` = true, with both dates).
- `monitorKey` names the memory. Runs with the same key share it; give each separate feed — a client, a channel, a test — its own key.
- Only what was actually delivered is remembered, so a review your spending limit refused comes back next run.

```json
{
  "places": ["ChIJD3uTd9hx5kcR1IQvGfr8dbk", "https://maps.app.goo.gl/your-branch-link", "Your Brand, Lyon"],
  "onlyNew": true,
  "monitorKey": "acme-weekly",
  "maxReviewsPerPlace": 200
}
```

**Recipe — new reviews to Slack, n8n or Make:** schedule the input above (daily or weekly) → add an Apify integration that fires on *run succeeded* → in Make or n8n use the *Get dataset items* step with `type=review` → post `place_name`, `stars`, `text` and `review_url` to your channel. Filter `stars <= 3` there, or set `maxStars: 3` here and never pay for the good ones.

## What data does each Google Maps review row contain?

A flat row, no nested junk to clean, and no empty columns that are empty for everyone:

| Field | Meaning |
|---|---|
| `review_id` | Google's id of the review — the same id Google Maps uses; stable across runs |
| `place_id`, `place_name`, `place_url` | The place the review belongs to |
| `review_url` | Direct link to this review on Google Maps |
| `report_url` | Google's "report this review" link |
| `stars` | 1–5 |
| `text` | The review text; `null` for a star-only rating |
| `text_translated` | Google's translation (with `translate` = both) |
| `original_language` | Language the review was written in (`en`, `fr`, `ja` …) |
| `published_at` | When it was first posted — **exact** ISO 8601 UTC, not guessed from "3 weeks ago" |
| `updated_at`, `edited` | When it was last edited, and whether it was |
| `published_text` | Google's own relative date, e.g. `3 weeks ago`, `Edited a month ago` |
| `likes` | Helpful votes |
| `photos` | URLs of the photos attached to the review |
| `owner_reply_text`, `owner_reply_at` | The owner's response and its exact date (`owner_reply_text_translated` with `translate` = both) |
| `reviewer_name`, `reviewer_id`, `reviewer_url`, `reviewer_photo_url` | The reviewer's public profile |
| `reviewer_review_count`, `reviewer_photo_count`, `reviewer_is_local_guide` | How experienced the reviewer is |
| `sub_ratings` | Aspect ratings when given: `{"Food": 5, "Service": 4, "Atmosphere": 4}` for restaurants, rooms / service / location for hotels |
| `visit_details` | Answers to Google's visit questions: `{"Meal type": "Dinner", "Price per person": "€20–30", "Wait time": "No wait"}` |
| `visited_in` | Month of the visit, `YYYY-MM`, when stated |
| `target`, `fetched_at` | The input line the row came from, and when it was read |

Because Google sends an exact timestamp with every review, `published_at` is the real moment of posting in every language — there is no fragile conversion of "vor 3 Wochen" or "3 週間前" into a date.

```json
{
  "type": "review",
  "review_id": "Ci9DQUlRQUNvZENodHljRjlvT2w5UVVsa3hUV0ZJWVc5eUxXVmpZbTlNV2t0NWRHYxAB",
  "place_name": "Du Pain et des Idées",
  "stars": 4,
  "text": null,
  "published_at": "2026-08-29T14:56:53+00:00",
  "updated_at": "2026-08-29T14:56:53+00:00",
  "published_text": "3 weeks ago",
  "edited": false,
  "likes": 0,
  "owner_reply_text": "Bonjour,\n\nMerci pour cette note ! Nous ferons le nécessaire pour mériter la cinquième étoile…",
  "owner_reply_at": "2026-08-30T13:30:12+00:00",
  "reviewer_name": "Yüksel Savaş",
  "reviewer_review_count": 6,
  "reviewer_is_local_guide": false,
  "sub_ratings": {"Food": 5, "Service": 4, "Atmosphere": 4},
  "visited_in": "2026-08"
}
```

## Place rows and status rows: the summary, free

One `place` row per place (switch off with `includePlaceRow`):

| Field | Meaning |
|---|---|
| `rating`, `reviews_total`, `histogram` | What Google lists: the average, the total and reviews per star |
| `reviews_read`, `reviews_delivered` | Distinct reviews this run read before filters, and how many it delivered |
| `stars_read` | The reviews read, per star — compare with `histogram` |
| `completeness` | The verdict sentence |
| `stopped_by` | What ended the walk early — `maxReviewsPerPlace`, `fromDate`, `onlyNew`, `spendingLimit` — or `null` for a full walk |
| `trend` | Average stars of the last 90 days against the 90 days before, with the review counts (only when a newest-first walk covered the 180 days) |
| `address`, `category`, `cid`, `place_url` | Context for joining with your own data |

One `status` row per input line: `status` (`ok`, `no_reviews`, `not_found`, `duplicate`, `error`), `listed`, `found`, `reviews`, `filtered`, `filtered_by` (how many each filter removed, e.g. `{"onlyWithText": 31}`), `already_seen`, `duplicates`, `pages`, `passes`, `charged` and `error`.

## Google reviews scraper filters — all free, all before billing

*"If I ask for the latest 100 reviews, many won't contain any text. For my purpose the text is the important part."* Every filter runs before billing, so you pay only for rows you keep, and `maxReviewsPerPlace` counts only rows that pass:

- `onlyWithText` — skip star-only ratings (about a third of all Google reviews).
- `minStars` / `maxStars` — e.g. `maxStars: 2` for negative Google reviews only.
- `keywords` / `excludeKeywords` — words or phrases to require or to drop, matched in the text and in its translation.
- `reviewLanguages` — only reviews written in these languages.
- `hasOwnerReply` — `yes` for Google reviews with owner responses (study a competitor's tone), `no` for the ones still waiting for a reply (a reputation manager's to-do list).
- `hasPhotos` — only reviews carrying photos.
- `sort` — `newest`, `most_relevant`, `highest`, `lowest`.
- `translate` — `original`, `translated` (Google's translation into `language`), or `both`.

```json
{
  "places": ["Du Pain et des Idées, Paris"],
  "sort": "lowest",
  "maxStars": 2,
  "onlyWithText": true,
  "translate": "both",
  "maxReviewsPerPlace": 100
}
```

## How do I run the Google Maps reviews scraper?

1. Paste your places into **Places**, one per line. Any mix works:

```text
https://www.google.com/maps/place/Louvre+Museum/@48.86,2.33,17z/data=!4m6!3m5!1s0x47e671d877937b0f:0xb975fcfa192f84d4
https://maps.app.goo.gl/AbCdEfGh12345
ChIJD3uTd9hx5kcR1IQvGfr8dbk
10222232094831998944
https://www.google.com/maps/search/?api=1&query=Katz+Delicatessen+New+York
Du Pain et des Idées, Paris
```

   A column copied from Excel or Google Sheets pastes as it is. The same place given twice — as a URL and as a place id, say — is read once; the second line becomes a free `duplicate` status row.
2. Set **Max reviews per place** (`0` = all). Optionally a date range, filters, or new-only monitoring.
3. Run. Export Google reviews as CSV, Excel, JSON or XML — a Google reviews CSV opens straight in Excel or Google Sheets — or read them over the API.

**Coming from another actor?** Paste your Compass input as it is: `startUrls`, `placeIds`, `maxReviews`, `reviewsSort` (`newest`, `mostRelevant`, `highestRanking`, `lowestRanking`), `reviewsStartDate` and `language` are all understood.

Other inputs: `language` (interface and translation language, e.g. `de`, `pt-BR`), `country` (the two-letter country Google is asked from), `sessions` and `perIp` (parallelism and pacing), and `proxyConfiguration` — datacenter proxies are enough, which is what keeps the price low.

## Scrape Google reviews from Python, JavaScript, curl, n8n, Make and AI agents

Python:

```python
from apify_client import ApifyClient
client = ApifyClient("<APIFY_TOKEN>")
run = client.actor("kestrel/google-maps-reviews-scraper").call(run_input={"places": ["Katz's Delicatessen, New York"], "fromDate": "30 days", "onlyWithText": True, "maxReviewsPerPlace": 0})
reviews = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "review"]
```

JavaScript (Node.js):

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<APIFY_TOKEN>' });
const run = await client.actor('kestrel/google-maps-reviews-scraper').call({ places: ['ChIJD3uTd9hx5kcR1IQvGfr8dbk'], maxReviewsPerPlace: 500 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl — run and get the rows in one call:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~google-maps-reviews-scraper/run-sync-get-dataset-items?token=<APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"places": ["Du Pain et des Idées, Paris"], "maxReviewsPerPlace": 50}'
```

**n8n and Make:** use the Apify node/module → *Run an Actor and get dataset*. **AI agents and MCP:** the actor is available through the Apify MCP server, so Claude, ChatGPT or your own agent can call it as a tool — "get the negative Google reviews of this place from the last 90 days".

**Recipe — AI sentiment analysis:** run with `onlyWithText: true` and `translate: "translated"` so every row has text in one language, then send `text`, `stars` and `sub_ratings` to your model. You pay for no star-only rows, and the exact `published_at` lets the model see trends by month.

**Recipe — back up your Google reviews (Google Business Profile reviews included, replies and all):** run once with `maxReviewsPerPlace: 0` for all your locations and keep the CSV; then schedule the same places with `onlyNew: true` and append. If a review is ever removed or your Business Profile is suspended, you still have every review, reply and date.

## How much does it cost to scrape Google Maps reviews?

One event, **$0.001 per delivered review** — $1 per 1,000, $10 for 10,000. There is no start fee.

Free: place rows, status rows, filtered reviews, duplicates, translations, the completeness second pass, reviews an earlier new-only run already delivered, places with no reviews, and places Google does not know. With `onlyWithText` on you pay only for reviews that have text. `maxReviewsPerPlace` and your run's spending limit cap the bill; when the limit is reached the run stops cleanly and says so.

## How fast is it, and what are the limits?

- About 1,000 reviews per minute per place (50 reviews a request), and places run in parallel — `sessions` sets how many.
- Google does not publish every review: spam-filtered and very fresh star-only ratings can be listed in the total before they appear in any feed. That is what `withheld by Google` in the verdict means; it is usually 0 and rarely above a fraction of a percent.
- `likes` is the helpful-vote count at the time of the run.
- Reviews come from Google's public reviews feed for signed-out visitors. The actor never logs in and cannot see anything a signed-out visitor cannot.
- A `share.google` or `maps.app.goo.gl` link is followed to the place it points at; a link that points at a list, a route or nothing at all is reported as `not_found`, free.

## Is it legal to scrape Google Maps reviews?

Google reviews are public: anyone can read them without an account. This actor reads only that public data and never logs in. Review rows contain personal data the reviewers chose to publish (display name, profile link, photo), so the GDPR and similar laws apply to what *you* do with it: have a legitimate reason, keep only what you need — drop the `reviewer_*` columns if you only analyse text — and do not use it to contact or profile individuals. If in doubt, ask your lawyer. This is not legal advice.

## FAQ

### Do I need a Google API key or a Google account?

No — this is Google reviews without an API key. The official Places API returns at most five reviews per place; this actor reads the public reviews feed and needs no key, no account and no cookies.

### Can I get Google Maps reviews by place id?

Yes — put the `ChIJ…` place id in `places` (or in `placeIds`). A CID, a feature id (`0x…:0x…`) and any Maps URL work the same way.

### Why do search URLs and short links work here without a place id?

The actor resolves them itself: a Google Maps short link (`maps.app.goo.gl`, `share.google`) is followed, a name or a search URL is looked up on Google Maps, and only a real business is accepted — a name Google cannot place is reported as `not_found` instead of silently returning some other place's reviews.

### A name resolved to the wrong branch — what now?

A plain name is looked up the way Google Maps search does it, and for a name that several places share (a chain, or a restaurant with a sister venue in another city) Google's first result can differ between runs. The `place` and `status` rows always show the `place_name` and `address` that were read, so a wrong match is visible at once. For anything you run repeatedly, use the place's Maps URL, place id or CID instead of its name — those always mean exactly one place.

### Can I download Google reviews as CSV or Excel?

Yes. To download Google reviews, open the run's dataset: Every run's dataset exports to CSV, Excel, JSON, XML and RSS. Use the *Reviews* view for a clean table of review rows only.

### How do I get only new reviews each week?

Turn on `onlyNew`, schedule the run weekly. Each run delivers only reviews not delivered before; a week with no new reviews costs $0.

### Can I get reviews from the last 30 days only?

Set `fromDate` to `30 days`. With newest-first order the actor stops reading at that date, so you do not pay to walk the older reviews.

### Is there a Google Maps reviews API I can call from my own code?

Yes — the actor *is* one. Call it with the `run-sync-get-dataset-items` endpoint shown above and you get the review rows back in the same HTTP response, as JSON or CSV. The same call works from Python, JavaScript, n8n, Make, Zapier and MCP-connected AI agents.

### Can I get Google reviews with text only?

Turn on `onlyWithText`. Star-only ratings are read past for free, and `maxReviewsPerPlace` counts only the reviews that have text.

### Does it return the owner's replies?

Yes: `owner_reply_text` and the exact `owner_reply_at`. Filter with `hasOwnerReply`.

### Can I scrape reviews for many locations at once?

Yes. Paste hundreds of places; they are read in parallel, each gets its own place and status row, and one bad line never fails the run.

### What happens if a place has no reviews, or does not exist?

A place with no reviews gives a `no_reviews` status row; an unknown place gives `not_found`. Both are free and the run still succeeds.

### Are competitor reviews allowed?

You can read the public reviews of any place, including competitors — a common use for sector research and for benchmarking owner response times.

## Related scrapers

From the same author, with the same charged-equals-delivered billing: Tripadvisor, Booking.com, Agoda, Trip.com, Airbnb and Trustpilot review scrapers for the other half of a location's reputation, and Google Hotels prices for hotel rate monitoring.
