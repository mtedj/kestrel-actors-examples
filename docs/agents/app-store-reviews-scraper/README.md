# Apple App Store Reviews Scraper — iOS App Reviews & Ratings

An **Apple App Store reviews scraper** that returns every customer review of any iOS app as structured rows: the 1–5 star rating, title, review text, reviewer nickname, date, edited flag, the developer's public reply and the app version where Apple attaches it (it rarely does — see the notes) — **apple app reviews** from every country storefront in a single run, each row tagged with its `country`. It reads the same JSON endpoint the App Store's own web page calls, so it pages far past the 500-review cap of Apple's old RSS feed (which now answers empty for most apps) and works for **ios app reviews** in the tens of thousands per app.

Give it app ids, App Store URLs, or plain app names. No login, no **apple app store reviews api** key, no browser. It bills per review row, and four filters cut what you pay for *before* billing: a rating band, a since-date, written-text-only, and a per-app cap. It is built for **app review monitoring** on a schedule as much as for one-off exports.

Last verified working: 2026-08-29.

## Apple App Store 应用评论、评分与开发者回复：中文调用与语言设置

按应用 ID、URL 或名称读取各 App Store 店面的评论。每个国家店面单独取数，不能用单一店面代表全球评价。

countries=["cn"] 选择中国大陆店面，["tw"] 或 ["hk"] 选择对应店面。店面不是翻译语言；应用必须在该店面提供。费用上限随应用数 × 店面数 × maxReviewsPerApp 增长。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "appIds": [
    "310633997"
  ],
  "countries": [
    "cn"
  ],
  "maxReviewsPerApp": 1,
  "sort": "most_recent",
  "sessions": 1
}
```

Avis applications / App Bewertungen：按店面比较应用评价。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Apple App Store reviews scraper for AI agents: which input answers which request?

Use this actor when the request names an iOS / Apple App Store app and wants its customer reviews (text, stars, developer response) or its store rating — by app id, App Store URL or plain app name, for one or many country storefronts in one run. Do **not** use it for Google Play / Android reviews (use the [Google Play Reviews Scraper](https://apify.com/kestrel/google-play-reviews-scraper)), for star ratings without text (Apple does not expose them per user; only written reviews are pageable), for downloads, sales or top charts, or for a "what changed since the last run" memory (schedule a relative `sinceDate` and dedupe on `review_id` yourself).

| user request | input JSON |
|---|---|
| "Reviews of WhatsApp on the App Store" | `{"appNames": ["WhatsApp"]}` or `{"appIds": ["310633997"]}` — the 100 newest US reviews, $0.40 at most |
| "Reviews of app id 310633997 in the UK and Germany" | `{"appIds": ["310633997"], "countries": ["gb", "de"]}` — one job per storefront, every row carries `country` |
| "Reviews from this App Store link" | `{"startUrls": ["https://apps.apple.com/us/app/whatsapp-messenger/id310633997"]}` — only the id is read from the URL; set `countries` for the storefronts |
| "Negative / 1-star reviews of X", "complaints" | `{"appNames": ["X"], "sort": "most_critical", "maxRating": 2, "maxReviewsPerApp": 300}` — reads the 300 most critical, bills only the 1–2★ ones |
| "Reviews from the last 7 days", daily monitoring | `{"appIds": ["310633997"], "sort": "most_recent", "sinceDate": "7 days"}` — schedule it with `"sinceDate": "1 day"`; older reviews read are not charged |
| "Every review, every country" | `{"appIds": ["310633997"], "countries": ["us", "gb", "de", "…"], "maxReviewsPerApp": 0}` — tens of thousands per storefront for big apps: start the run with `maxTotalChargeUsd` |
| "Which reviews did the developer answer?" | any input above, then filter rows on `developer_response` (the reply) and `developer_response_date` |
| "App Store rating, rating count, star histogram of X" | `{"appIds": ["310633997"], "maxReviewsPerApp": 1}` — the free `app` row carries `rating_avg`, `rating_count`, `hist_1`…`hist_5`, `written_reviews`; at most one billed review ($0.004) |
| "Reviews of three competitors, the most helpful ones" | `{"appNames": ["Duolingo", "Babbel", "Memrise"], "sort": "most_helpful", "maxReviewsPerApp": 200}` |
| "Tell me the cost first, cap it at $5" | 100 reviews per app and storefront = $0.40 (`maxReviewsPerApp` × apps × countries × $0.004); start the run with `maxTotalChargeUsd: 5` and it stops there |

**Output.** `type: "review"` rows (billed): `review_id`, `app_id`, `app_name`, `country`, `rating` (1–5), `title`, `text`, `author`, `version` (null when Apple omits it — most rows), `is_edited`, `review_date`, `review_day`, `developer_response`, `developer_response_date`, `url`. One free `type: "app"` row per app and storefront: `rating_avg`, `rating_count`, `hist_1`…`hist_5`, `written_reviews`, `developer`, `genre`, `price`, `version`, `released`, `updated`. One free `type: "status"` row per app and storefront: `status` is `ok`, `no_reviews`, `not_found` or `error`, with `reviews`, `filtered`, `pages`, `duplicates`, `error`.

**Empty results and errors.** An app with no reviews, an id that is not an app on a storefront, or a name that matches nothing produces a status row and no charge. Bad input — a URL from another site, a storefront code outside the 48 known, a number out of range — ends the run before anything is charged, with the reason on the run card. A throttled or broken source fails the run loudly; nothing is charged for a failed job. Filters (`minRating`, `maxRating`, `sinceDate`, `requireText`) apply to the reviews read under `maxReviewsPerApp`, before billing.

The same actor answers the request in other languages: App Store Bewertungen / Rezensionen (German), reseñas de apps / opiniones (Spanish), avis application (French), avaliações de apps (Portuguese), アプリ レビュー (Japanese), 앱 리뷰 (Korean) — storefront codes de, es, fr, pt/br, jp, kr return the reviews written in those markets.

## What does the App Store reviews scraper do?

You give it apps and storefronts. It gives you their **app store reviews** as rows you can sort, filter and export.

- **`review` rows** — `rating` (1–5), `title`, `text`, `author`, `version` (null when Apple omits it, which it does for most reviews), `is_edited`, `review_date` (ISO 8601) and `review_day` (YYYY-MM-DD), `developer_response` and `developer_response_date`, `country`, `app_id`, `app_name`, `url`, `fetched_at`. These are the rows you pay for.
- **`app` rows** — free context per app and storefront: `app_name`, `developer`, `seller`, `bundle_id`, `genre`, `price`, `currency`, `version`, `age_rating`, `rating_avg`, `rating_count`, `rating_avg_current`, `rating_count_current`, the star histogram `hist_1`, `hist_2`, `hist_3`, `hist_4`, `hist_5`, `written_reviews`, `released`, `updated`, `icon`, `app_url` and `reviews_fetched`.
- **`status` rows** — free: per app and country (`target` is the id, URL or name you gave), what was harvested (`reviews`, `filtered`, `pages`, `duplicates`), whether the app was `not_found` on that storefront, and why anything failed (`error`).

Every row of a type carries every column, so the dataset drops straight into a spreadsheet or a database without a cleaning step.

## App store reviews by country, in one run

Reviews live per storefront. A US-only export of a global app misses most of its **app reviews by country**, and the incumbent tools make you run once per storefront. Here `countries` is a list:

```json
{ "appIds": ["310633997"], "countries": ["us", "gb", "de", "fr", "jp", "br", "in"], "maxReviewsPerApp": 200 }
```

That is one run, seven `app` rows (one per storefront, each with its own rating histogram), and up to 1,400 review rows, every one tagged with `country`. Apple occasionally lists the same review on two storefronts; the first storefront to deliver it keeps it, so you never pay for a review twice.

Forty-eight storefronts are known by their two-letter code (us, gb, ca, au, de, fr, it, es, nl, se, no, dk, fi, ch, at, be, ie, pt, pl, cz, ru, tr, il, ae, sa, eg, za, ng, ke, br, mx, ar, cl, co, pe, jp, kr, cn, tw, hk, sg, in, nz, ph, id, my, th, vn).

## Apple app reviews by id, by URL, or by name

Most tools want Apple's numeric id first. All three inputs work here, and they can be mixed:

- **`appIds`** — the digits after `/id` in any App Store link, e.g. `310633997`. Fastest, and what an earlier run's `app_id` gives you.
- **`startUrls`** — App Store pages such as `https://apps.apple.com/us/app/whatsapp-messenger/id310633997`. The id is read from the URL for you.
- **`appNames`** — the name as you would type it into App Store search: `Duolingo`. Each is resolved to the top hit on each storefront through Apple's own search API.

A URL and its id are the same app, and an app is harvested once per storefront however many inputs point at it.

## App store negative reviews without paying for the happy ones

`minRating` and `maxRating` keep only reviews inside a star band, and they run **before** billing. A complaints feed:

```json
{ "appIds": ["310633997"], "countries": ["us", "gb"], "sort": "most_critical", "maxRating": 2, "requireText": true, "maxReviewsPerApp": 300 }
```

reads up to 300 reviews per storefront in most-critical order and delivers — and bills — only the 1★ and 2★ ones that actually say something. The `status` row's `filtered` column shows how many were dropped for free. `sinceDate` does the same for time: `"7 days"` with `"sort": "most_recent"` is a daily new-reviews feed that never goes stale.

## Input

| field | what it does |
|---|---|
| `appIds` | Apple's numeric app ids. |
| `startUrls` | App Store app URLs; the id is read from each. |
| `appNames` | App names, resolved through Apple's search API on each storefront. |
| `countries` | Storefront codes to read each app on. Default `["us"]`. |
| `maxReviewsPerApp` | Per app *and* storefront. 0 = everything Apple pages out; N = the first N in the chosen order. The main cost control. Default 100. |
| `sort` | `most_recent` (schedule this), `most_helpful` (the App Store's own order), `most_critical` (1★ first), `most_favorable` (5★ first). |
| `minRating` / `maxRating` | 0 = all; 1–5 = keep only reviews inside the band. Filters before billing. |
| `sinceDate` | Keep reviews on or after a date: `2026-08-01`, or relative — `"7 days"`, `"2 weeks"`, `"3 months"`. Filters before billing. |
| `requireText` | Drop reviews that are a rating with no words. Filters before billing. Apple's endpoint returns written reviews only (60 of 60 in the recorded pages had text), so it rarely removes anything here. |
| `includeAppRow` | Emit the free `app` row per app and storefront (default on). |
| `sessions` / `perIp` | Parallel proxy sessions and the per-IP pace. Apple answers about one request a second per IP. |
| `proxyConfiguration` | Apify Proxy (default datacentre group). Apple's endpoints need no login, but a large run needs several IPs to stay under the per-IP cap. |

### Example: a scheduled new-reviews feed for your own app

```json
{ "appIds": ["570060128"], "countries": ["us", "gb", "de", "jp"], "sort": "most_recent", "sinceDate": "1 day", "maxReviewsPerApp": 200 }
```

### Example: the full US corpus for a competitor set, by name

```json
{ "appNames": ["Duolingo", "Babbel", "Memrise"], "countries": ["us"], "maxReviewsPerApp": 0, "sort": "most_helpful" }
```

### Example: only what the developer has replied to, from the last quarter

```json
{ "startUrls": ["https://apps.apple.com/us/app/whatsapp-messenger/id310633997"], "countries": ["us"], "sinceDate": "3 months", "maxReviewsPerApp": 2000 }
```

then filter the dataset on `developer_response` — the reply, its date, and the review it answers sit on the same row.

## Output

A `review` row:

```json
{
  "type": "review",
  "review_id": "13657831289",
  "app_id": "310633997",
  "app_name": "WhatsApp Messenger",
  "country": "us",
  "rating": 5,
  "title": "WhatsApp not bad",
  "text": "WhatsApp's not bad at all—it's actually great for what it does. End-to-end encryption keeps your actual messages and calls private…",
  "author": "Ed Bradway",
  "version": null,
  "is_edited": false,
  "review_date": "2026-01-21T04:48:38Z",
  "review_day": "2026-01-21",
  "developer_response": null,
  "developer_response_date": null,
  "url": "https://apps.apple.com/us/app/id310633997?see-all=reviews",
  "fetched_at": "2026-08-29T06:10:04+00:00"
}
```

An `app` row carries `rating_avg` 4.68, `rating_count` 18,484,827, `hist_1` … `hist_5` (630,438 one-star ratings against 15,611,785 five-star), `written_reviews` 198,881, `genre` "Social Networking", `price` 0, `version`, `released`, `updated`, `icon` and `app_url`. The dataset has five views — Overview, Reviews, Complaints, Apps and Run status — and exports to CSV, Excel or JSON from the Apify Console or API.

## How much does it cost?

Pay per delivered **review** row, and nothing else: app rows, status rows, filtered reviews, apps with no reviews, unknown apps and failed jobs are free. A 200-review pull of one app on one storefront is 200 rows; a complaints feed that reads 300 reviews and keeps 40 bills 40. Apple pages ten reviews per request, so cost tracks rows, not requests. The price per row is on the pricing tab, and a spending limit on the run caps the total — whatever the limit refuses is never delivered.

## App store reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

**Python**

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/app-store-reviews-scraper").call(run_input={
    "appIds": ["310633997"], "countries": ["us", "gb", "de"],
    "sort": "most_recent", "maxReviewsPerApp": 100,
})
rows = client.dataset(run["defaultDatasetId"]).list_items().items
reviews = [r for r in rows if r["type"] == "review"]
for r in reviews[:5]:
    print(r["country"], r["rating"], r["title"], "—", (r["text"] or "")[:80])
```

**JavaScript**

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/app-store-reviews-scraper').call({
    appNames: ['Duolingo'], countries: ['us'], sort: 'most_critical', maxRating: 2, maxReviewsPerApp: 300,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const complaints = items.filter(r => r.type === 'review');
console.log(complaints.length, 'low-star reviews');
```

**curl**

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~app-store-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&timeout=300" \
  -H "Content-Type: application/json" \
  -d '{"appIds":["310633997"],"countries":["us"],"sinceDate":"7 days","sort":"most_recent","maxReviewsPerApp":200}'
```

**n8n / Make / Zapier** — call the same `run-sync-get-dataset-items` URL from an HTTP Request node with a Header Auth credential (`Authorization: Bearer <token>`), filter rows on `type === 'review'`, dedupe on `review_id` in the workflow's static data, and route new 1–2★ reviews to Slack, a Google Sheet or a ticket queue. Relative `sinceDate` values keep a daily schedule from ever going stale. Apify's native n8n and Make apps work too.

**AI agents / MCP** — the actor is on Apify's MCP server, so an agent with Apify MCP access can call it by name with the same input and read the rows back. The input and output schemas are complete, which is what lets an agent fill the input from a plain-English request.

## Is it legal to scrape App Store reviews?

Reviews are public content that Apple shows to anyone without an account, and this actor reads them through the same public endpoints a browser uses, with no login, no circumvention of access controls and no personal data beyond the public nickname a reviewer chose. Whether you may store and process the data depends on your jurisdiction and purpose — GDPR treats a nickname plus review text as personal data, so keep what you need, and read Apple's terms for the App Store website. This is not legal advice.

## Limits and honest notes

- **Depth.** Apple's endpoint pages ten reviews at a time by offset and keeps answering deep into an app's history (tens of thousands for the biggest apps). A run's `maxReviewsPerApp` and its spending limit decide when to stop; 0 means "everything Apple pages out".
- **Ratings versus reviews.** An app's `rating_count` counts star ratings, most of which have no text. Only written reviews are pageable; `written_reviews` on the `app` row is how many the storefront holds.
- **Version.** Apple's current endpoint rarely attaches the app version to a review: 0 of the 60 reviews in the recorded pages (WhatsApp, us/gb/de, three sort orders) carried one. The column is null when it is absent; the `app` row's `version` is the app's current version, not the reviewer's.
- **Pace.** Apple answers roughly one request a second per IP and replies 429 beyond that. The fetcher paces each session and rotates on 429, so a big run is slower with one IP than with several — use Apify Proxy for anything over a few hundred rows.
- **Names.** `appNames` takes the top search hit on each storefront; when a name is ambiguous, use the id.

## FAQ

### Does it need an Apple developer account or API key?

No. Everything is read from public endpoints. The App Store Connect API gives developers their own app's reviews only; this reads any app's.

### Can I download App Store reviews as CSV or Excel?

Yes. Every run writes an Apify dataset; open it in the Console and export as CSV, Excel, JSON or XML, or fetch it from the API with `?format=csv`. This is the **download app store reviews** and **app store reviews csv** path — an **app store reviews export** with no extra step.

### How do I get only App Store negative reviews?

Set `maxRating` to 2 (or 1), `sort` to `most_critical`, and optionally `requireText`. Five-star reviews are dropped before billing.

### Can I scrape reviews for many countries at once?

Yes — that is the point of `countries`. Each storefront gets its own `app` row and its own review rows, all in one dataset with a `country` column, which makes **app store reviews by country** a pivot rather than a project.

### How many reviews can one app return?

As many as Apple pages out, which for large apps is tens of thousands per storefront. The old RSS feed stopped at 500; this does not use it.

### Does it include the developer's reply?

Yes — `developer_response` and `developer_response_date` on the review row, which makes an **app store developer response** audit a filter.

### Can I use it as a general app review API?

Yes: call `run-sync-get-dataset-items` and you have an **app store review api** that returns JSON for any app and storefront. Pair it with a Google Play reviews source to cover both stores.

### Can I scrape App Store reviews without an API?

That is what this is: **scrape app store reviews** with a JSON input and get rows back, no Apple API, no browser.

### What does bulk work cost?

Rows delivered times the per-row price, nothing for the rest. A filtered run pays for what it keeps. For **competitor app reviews** across a portfolio, cap per app and per storefront and let a schedule spread the work.

### Which order should I schedule?

`most_recent` with a relative `sinceDate`. Every other order is for one-off pulls.

## App review monitoring across a portfolio

For a studio or an agency the unit of work is a list of apps and a list of storefronts, run daily:

- `appIds` for every app you ship or track, `countries` for every market that matters, `sort: "most_recent"`, `sinceDate: "1 day"`.
- Route by `rating`: 1–2★ to support, 5★ to marketing, anything with `developer_response` null and `rating` ≤ 2 to the reply queue.
- Keep `app` rows: `rating_avg`, `rating_count` and the histogram per storefront per day is the **app store ratings** history nobody exports for you.

### App review analysis that keeps its structure

Because every row carries `country`, `version`, `rating` and the dates, an **app review analysis** does not need a parser: group by version to see whether a release moved the rating, by country to find a market with a localisation problem, by week to spot a spike. **iOS app feedback** with the text, the stars and the metadata in the same row is what makes sentiment and topic models useful.

### What this does not do

It does not read Google Play (a different store), it does not read ratings without text (Apple does not expose them per user), and it does not write reviews or replies.

### Choosing between sort orders

`most_helpful` is what a shopper sees first and what the App Store defaults to; `most_recent` is chronological; `most_critical` and `most_favorable` front-load one end of the star scale and are the cheap way to sample complaints or praise.

## Related scrapers

Reviews from other places customers talk, with the same row discipline, the same pay-per-delivered-row billing and the same scheduling story:

- **[Indeed Company Reviews Scraper](https://apify.com/kestrel/indeed-company-reviews)** — employee reviews with five sub-ratings, pros and cons, job title and location, and the employer's reply.
- **[Trustpilot Reviews Scraper](https://apify.com/kestrel/trustpilot-reviews-scraper)** — company reviews and TrustScore from Trustpilot, past the 200-review wall an anonymous reader normally hits.
- **[Google Play Reviews Scraper](https://apify.com/kestrel/google-play-reviews-scraper)** — the Android half of this pair: Play Store reviews per language and country, matching columns and the same pre-billing filters.
- **[Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)** — product reviews across 20 marketplaces, with pre-billing filters.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — guest reviews of any listing, `minRating` bills only what you keep.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — hotel reviews with separate positives and negatives.
- **[Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper)** — the Top 100 of any category with every rank filled.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
