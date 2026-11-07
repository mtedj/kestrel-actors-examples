# Google Play Reviews Scraper — Android App Reviews & Ratings

A **Google Play reviews scraper** that returns every user review of any Android app as structured rows: the 1–5 star rating, review text, reviewer name, thumbs-up count, app version, date and the developer's public reply — **google play reviews** for every language and country you name, in a single run, each row tagged with its `language` and `country`. It makes the same review call the Play Store's own web page makes, follows the continuation token to the end of the list, and works for **android app reviews** in the hundreds of thousands per app.

Give it package names or Play URLs. No login, no **google play reviews api** key, no browser. It bills per review row, and four filters cut what you pay for *before* billing: a rating band, a since-date, written-text-only, and a per-app cap — and when the band is a single star value, Google itself does the filtering, so the other reviews are never fetched at all. It is built for **app review monitoring** on a schedule as much as for one-off exports, and it is the Android half of a pair with the [Apple App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper).

Last verified working: 2026-08-29.

## Google Play 安卓应用评论与开发者回复：中文调用与语言设置

按应用包名或 URL 获取评论、评分、版本及开发者回复。每个语言与国家组合分别查询。

languages 选择 Play 请求语言，countries 选择地区，例如 languages=["zh-TW"], countries=["tw"]。不自动翻译；费用随应用数 × 语言数 × 国家数 × maxReviewsPerApp 增长，重复评论去重。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "appIds": [
    "com.whatsapp"
  ],
  "languages": [
    "zh-TW"
  ],
  "countries": [
    "tw"
  ],
  "maxReviewsPerApp": 1,
  "sort": "most_recent",
  "sessions": 1
}
```

Android app reviews / avis Google Play / Play Store Bewertungen：语言和地区分别设置。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Google Play reviews scraper for AI agents: which input answers which request?

Use this actor when the request names an Android / Google Play / Play Store app and wants its user reviews (text, stars, thumbs-up, app version, developer reply) or its store rating — by package name or Play URL, for one or many languages and countries in one run. Do **not** use it for Apple App Store / iOS reviews (use the [Apple App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper)), for an app named only by its title (Play has no open search: take the `id=` part of the app's Play URL), for Play Console data (installs, crashes, private reviews), for translations (reviews come in the language they were written in), or for a "what changed since the last run" memory (schedule a relative `sinceDate` and dedupe on `review_id` yourself).

| user request | input JSON |
|---|---|
| "Reviews of WhatsApp on Google Play" | `{"appIds": ["com.whatsapp"]}` — the 100 newest en/us reviews, $0.40 at most |
| "Reviews from this Play Store link" | `{"appUrls": ["https://play.google.com/store/apps/details?id=com.whatsapp"]}` — only the package name is read; set `languages` / `countries` for the locales |
| "Reviews in German and Portuguese, Brazil and Germany" | `{"appIds": ["com.whatsapp"], "languages": ["de", "pt-BR"], "countries": ["de", "br"]}` — one job per language × country pair, every row carries both |
| "Negative / 1-star reviews of X", "complaints" | `{"appIds": ["X"], "minRating": 1, "maxRating": 1, "requireText": true, "maxReviewsPerApp": 300}` — one star value is filtered by Google itself, so 300 one-star reviews come back and nothing is read to be discarded; `"maxRating": 2` alone keeps the 1–2★ among the 300 read |
| "Reviews from the last 7 days", daily monitoring | `{"appIds": ["com.whatsapp"], "sort": "most_recent", "sinceDate": "7 days"}` — schedule it with `"sinceDate": "1 day"`; older reviews read are not charged |
| "Every review" | `{"appIds": ["com.whatsapp"], "maxReviewsPerApp": 0}` — hundreds of thousands for big apps: start the run with `maxTotalChargeUsd` |
| "Which reviews did the developer answer?" | any input above, then filter rows on `reply_text` and `reply_date` |
| "Google Play rating and rating count of X" | `{"appIds": ["X"], "maxReviewsPerApp": 1}` — the free `app` row carries `rating_avg`, `rating_count`, `category`, `price`; at most one billed review ($0.004) |
| "Reviews of three competitors, Google's own order" | `{"appIds": ["com.whatsapp", "org.telegram.messenger", "org.thoughtcrime.securesms"], "sort": "most_relevant", "maxReviewsPerApp": 200}` |
| "Tell me the cost first, cap it at $5" | 100 reviews per app, language and country = $0.40 (`maxReviewsPerApp` × apps × languages × countries × $0.004); start the run with `maxTotalChargeUsd: 5` and it stops there |

**Output.** `type: "review"` rows (billed): `review_id`, `app_id`, `app_name`, `language`, `country`, `rating` (1–5), `text`, `author`, `author_id`, `thumbs_up`, `app_version` (97 of 100 rows in the recorded pages carry it), `review_date`, `review_day`, `reply_text`, `reply_date`, `url` (the Play page deep-linked to the review). One free `type: "app"` row per app, language and country: `rating_avg`, `rating_count`, `developer`, `category`, `content_rating`, `price`, `currency`, `icon`, `description`. One free `type: "status"` row per app, language and country: `status` is `ok`, `no_reviews`, `not_found` or `error`, with `reviews`, `filtered`, `pages`, `duplicates`, `error`.

**Empty results and errors.** An app with no reviews or a package that is not on Play in that country produces a status row and no charge. Bad input — a URL from another site, a string that is not a package name, a number out of range — ends the run before anything is charged, with the reason on the run card. An answer without a review payload is treated as a refusal and retried from another IP, never as "no reviews"; a source that stays blocked fails the run loudly, and nothing is charged for a failed job. Filters (`minRating`, `maxRating`, `sinceDate`, `requireText`) apply to the reviews read under `maxReviewsPerApp`, before billing — except a single star value, which Google filters before the read.

The same actor answers the request in other languages: Play Store Bewertungen / App Rezensionen (German), reseñas de apps / opiniones (Spanish), avis application (French), avaliações de apps (Portuguese), アプリ レビュー (Japanese), 앱 리뷰 (Korean) — `languages` de, es, fr, pt-BR, ja, ko return the reviews written in those languages.

## What does the Google Play reviews scraper do?

You give it apps and locales. It gives you their **play store reviews** as rows you can sort, filter and export.

- **`review` rows** — `rating` (1–5), `text`, `author`, `author_id`, `thumbs_up`, `app_version`, `review_date` (ISO 8601) and `review_day` (YYYY-MM-DD), `reply_text` and `reply_date` when the developer answered, `language`, `country`, `app_id`, `app_name`, `review_id`, `url` (the Play page deep-linked to that review), `fetched_at`. These are the rows you pay for.
- **`app` rows** — free context per app and locale: `app_name`, `developer`, `developer_url`, `category`, `content_rating`, `rating_avg`, `rating_count`, `price`, `currency`, `icon`, `description`, `app_url` and `reviews_fetched`.
- **`status` rows** — free: per app, language and country (`target` is the package you gave), what was harvested (`reviews`, `filtered`, `pages`, `duplicates`), whether the package was `not_found` on Play in that country, and why anything failed (`error`).

Every row of a type carries every column, so the dataset drops straight into a spreadsheet or a database without a cleaning step.

## Google play reviews by language and country, in one run

Google Play lists reviews per language, and what a user sees also depends on the country of their store. An English-only export of a global app misses most of its **app reviews by country**, and the incumbent tools make you run once per locale. Here `languages` and `countries` are lists, and every combination is one job:

```json
{ "appIds": ["com.whatsapp"], "languages": ["en", "es", "pt-BR", "hi"], "countries": ["us", "br", "in"], "maxReviewsPerApp": 500 }
```

That is one run, twelve jobs, twelve `app` rows and up to 6,000 review rows, every one tagged with `language` and `country`. Google surfaces the same review under more than one locale — an English review of a US app shows under en/us and en/gb — so a review is delivered and billed once per run, whichever job reaches it first; the `duplicates` column on the `status` row shows how many the later jobs skipped for free.

Language codes are Play's `hl` values (en, de, fr, es, it, pt-BR, pt-PT, ja, ko, zh-TW, zh-CN, ru, tr, ar, hi, id, th, vi…) and countries are Play's two-letter `gl` values.

## Android app reviews by package name or URL

Two inputs, mixable:

- **`appIds`** — Android package names such as `com.whatsapp` or `com.spotify.music`: the `id=` part of any Play URL, and what an earlier run's `app_id` gives you. Fastest.
- **`appUrls`** — Play pages such as `https://play.google.com/store/apps/details?id=com.whatsapp`. The package name is read from the URL for you.

A URL and its package name are the same app, and an app is harvested once per locale however many inputs point at it.

## Google play negative reviews without paying for the happy ones

`minRating` and `maxRating` keep only reviews inside a star band, and they run **before** billing. A complaints feed:

```json
{ "appIds": ["com.spotify.music"], "languages": ["en"], "countries": ["us", "gb"], "sort": "most_recent", "maxRating": 2, "requireText": true, "maxReviewsPerApp": 300 }
```

reads up to 300 reviews per locale in most-recent order and delivers — and bills — only the 1★ and 2★ ones that actually say something. The `status` row's `filtered` column shows how many were dropped for free. When you want exactly one star value, set both bounds to it (`"minRating": 1, "maxRating": 1`): the star filter is then sent to Google inside the review call, so only 1★ reviews come back and nothing is fetched merely to be discarded — a cheaper, faster complaints feed than any client-side filter.

`sinceDate` does the same for time: `"7 days"` with `"sort": "most_recent"` is a daily new-reviews feed that never goes stale.

## Input

| field | what it does |
|---|---|
| `appIds` | Android package names. |
| `appUrls` | Google Play app URLs; the package name is read from each. |
| `languages` | Play language codes (`hl`) to read each app in. Default `["en"]`. |
| `countries` | Play country codes (`gl`) to read each app in. Default `["us"]`. |
| `maxReviewsPerApp` | Per app, language *and* country. 0 = everything Google pages out; N = the first N in the chosen order. The main cost control. Default 100. |
| `sort` | `most_recent` (schedule this), `most_relevant` (Google Play's own order), `rating` (5★ first). |
| `minRating` / `maxRating` | 0 = no bound; 1–5 keeps only reviews inside the band. Filtered reviews are never billed; a single star value is filtered by Google server-side. |
| `sinceDate` | Keep only reviews on or after a date — `2026-08-01`, or relative: `"7 days"`, `"2 weeks"`, `"3 months"`. |
| `requireText` | Drop star-only reviews with no words. |
| `includeAppRow` | Emit the free `app` row per app and locale (default on). |
| `sessions` | Parallel proxy sessions (egress IPs). Default 4. |
| `perIp` | Requests per second per session. Default 1 — Google's tolerance. |
| `proxyConfiguration` | Apify Proxy, datacentre group by default; needed to spread a large run over several IPs. |

### Example: a scheduled new-reviews feed for your own app

```json
{ "appIds": ["com.example.myapp"], "languages": ["en", "de", "fr"], "countries": ["us", "de", "fr"], "sort": "most_recent", "sinceDate": "1 day", "maxReviewsPerApp": 200 }
```

Run it every morning: `"1 day"` is resolved on the day it runs, so the schedule never drifts, and only yesterday's reviews are delivered and billed.

### Example: the full US corpus for a competitor set

```json
{ "appIds": ["com.whatsapp", "org.telegram.messenger", "org.thoughtcrime.securesms"], "languages": ["en"], "countries": ["us"], "maxReviewsPerApp": 0, "sort": "most_relevant" }
```

`maxReviewsPerApp: 0` means everything Google pages out — hundreds of thousands of rows for apps this size, so put a spending limit on the run if you want a ceiling.

### Example: only what the developer has replied to, from the last quarter

```json
{ "appIds": ["com.spotify.music"], "sort": "most_relevant", "sinceDate": "3 months", "maxReviewsPerApp": 2000 }
```

The `reply_text` and `reply_date` columns are filled for reviews the developer answered; filter on them in the dataset view or in your own code.

## Output

One dataset, three row types. A review row:

```json
{
  "type": "review",
  "review_id": "22aacbd1-267e-445b-948c-629ad3d87a2a",
  "app_id": "com.whatsapp",
  "app_name": "WhatsApp Messenger",
  "language": "en",
  "country": "us",
  "rating": 5,
  "text": "so strict",
  "author": "Emmanuel Shimison",
  "author_id": "105709602236647094141",
  "thumbs_up": 0,
  "app_version": "2.26.21.75",
  "review_date": "2026-08-28T06:25:25Z",
  "review_day": "2026-08-28",
  "reply_text": null,
  "reply_date": null,
  "url": "https://play.google.com/store/apps/details?id=com.whatsapp&hl=en&gl=us&reviewId=22aacbd1-267e-445b-948c-629ad3d87a2a",
  "fetched_at": "2026-08-29T10:25:00Z"
}
```

The `app` row for the same job carries `app_name`, `developer` ("WhatsApp LLC"), `developer_url`, `category` ("COMMUNICATION"), `content_rating` ("Everyone"), `rating_avg` (4.62), `rating_count` (242 million), `price` and `currency`, `icon`, `description`, `app_url` and `reviews_fetched`. The `status` row carries `target`, `app_id`, `language`, `country`, `status` (`ok`, `no_reviews`, `not_found`, `error`), `reviews`, `filtered`, `pages`, `duplicates` and `error`.

Five dataset views are built in: **Overview** (every row, the columns that matter), **Reviews**, **Complaints** (sort by `rating`), **Apps** and **Status**. Export any of them to CSV, Excel, JSON or XML from the run page or the API.

## How much does it cost?

You pay per delivered review row — **$0.004 a review** — and nothing else: app rows, status rows, filtered reviews, apps with no reviews, unknown packages and failed jobs are free. A run that reads 300 reviews per locale for two locales and keeps the 1–2★ ones with text typically delivers 60–120 rows, so it costs 25–50 cents. The full corpus of a big app is priced by the row too: 100,000 reviews are $400, and `maxReviewsPerApp` or a spending limit on the run caps it wherever you like.

Compute is tiny: one review call returns up to 100 reviews in about a second, so a thousand-review job is ten calls.

## Google play reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

The actor runs on Apify, so every client Apify has works. Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/google-play-reviews-scraper").call(run_input={
    "appIds": ["com.whatsapp"],
    "languages": ["en", "de"],
    "countries": ["us", "de"],
    "sort": "most_recent",
    "maxRating": 2,
    "requireText": True,
    "maxReviewsPerApp": 200,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["language"], row["country"], row["rating"], row["review_day"], (row["text"] or "")[:80])
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/google-play-reviews-scraper').call({
    appIds: ['com.spotify.music'], languages: ['en'], countries: ['us', 'gb'],
    sort: 'most_recent', sinceDate: '7 days', maxReviewsPerApp: 500,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter(r => r.type === 'review');
console.log(reviews.length, 'new reviews this week;', reviews.filter(r => r.reply_text).length, 'answered');
```

curl, synchronous, JSON back:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~google-play-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"appIds": ["com.whatsapp"], "languages": ["en"], "countries": ["us"], "maxReviewsPerApp": 50}'
```

**n8n and Make**: use the Apify node (or a plain HTTP Request node to the `run-sync-get-dataset-items` endpoint above) on a Schedule trigger, filter rows on `type === "review"`, and send the ones with `rating <= 2` to Slack, a Google Sheet or a ticketing system. **AI agents**: the actor is listed in Apify's MCP server, so Claude, Cursor or any MCP client can call `kestrel/google-play-reviews-scraper` with the same input and read the dataset back — the schema tells the agent what every field means.

## Is it legal to scrape Google Play reviews?

Reviews on Google Play are public: anyone can read them without an account. This actor reads the same public review call the Play Store web page makes, sends no credentials, and stores only what the page shows — the reviewer's public display name and their words. Whether you may store and process that data depends on your purpose and jurisdiction: reviews are personal data under the GDPR and similar laws, so process them for a legitimate purpose, keep them no longer than you need, and honour deletion requests. Respect Google's terms for your use case; this actor is a tool, and the responsibility for how its output is used is yours.

## Limits and honest notes

- **Locale is a list, not a filter.** Google decides which reviews it shows under a given `hl`/`gl`; a review can appear under several locales (delivered once) and a few may appear under none. For a complete corpus, name every language the app has meaningful traffic in.
- **`most_relevant` is Google's ranking, not a date order.** It surfaces the reviews Play itself promotes — good for sentiment, wrong for "what changed since yesterday". Schedule `most_recent`.
- **Text can be empty.** Many Android reviews are a star rating with no words; `requireText` drops them before billing.
- **The reviewer's name is what they chose to display**, and `author_id` is Google's opaque id for that account — useful for de-duplicating across apps, not for identifying people.
- **Throttling.** Google answers refusals to bursts from one IP. The fetcher paces each session at `perIp` requests a second, treats an answer without a review payload as a refusal — never as "no reviews" — rotates the session and backs off. Large runs finish; they do not fail silently.
- **Not supported:** app names as input (Play has no open search API; use the package name from the URL), review images, and the per-version breakdown of ratings.

## FAQ

### Does it need a Google account or API key?

No. Google Play has no public **google play review api** for reading reviews; this actor uses the public review call that the Play Store web page itself makes, without a login. You only need an Apify account.

### Can I download Google Play reviews as CSV or Excel?

Yes. Every run writes an Apify dataset; open the **Reviews** view and export it as CSV, Excel, JSON or XML, or fetch it from the API. **Google play reviews csv** exports are the most common use — the columns are flat, so nothing needs cleaning.

### How do I get only Google Play negative reviews?

Set `maxRating` to 2 (or `minRating` and `maxRating` both to 1 for one-star only, which Google filters server-side), add `requireText: true` so star-only reviews are dropped, and sort by `most_recent`. You pay only for the rows that survive — **google play negative reviews** for a fraction of the price of reading everything.

### Can I scrape reviews in many languages and countries at once?

Yes — `languages` and `countries` are lists, every combination is one job, and each row carries `language` and `country`. That is the difference between an English-only export and **google play reviews by language** that reflect the whole user base.

### How many reviews can one app return?

Everything Google pages out. There is no fixed cap: the actor follows the continuation token until the list ends, which for the biggest apps is hundreds of thousands of reviews per locale. `maxReviewsPerApp` and a spending limit on the run are the two ways to stop earlier.

### Does it include the developer's reply?

Yes. `reply_text` and `reply_date` carry the **google play developer reply** when there is one — the basis of a response-rate report or a "which complaints went unanswered" view.

### Can I use it for competitor app reviews?

Yes. Give several package names, one language and country set, and `sort: "most_relevant"`; you get **competitor app reviews** side by side with the same columns, ready for **app review analysis** — theme counting, sentiment, feature requests — in the tool of your choice.

### Can I scrape Google Play reviews without an API?

That is exactly what this does: **scrape google play reviews** through the store's own web call, no SDK, no quota to apply for, no browser to run.

### What does bulk work cost?

$0.004 a review row, nothing for anything else. 10,000 reviews are $40; a scheduled feed that delivers 20 new reviews a day is $2.40 a month.

### Which order should I schedule?

`most_recent` with a relative `sinceDate`. `most_relevant` for a one-off portrait of what users think; `rating` when you want the praise first.

## App review monitoring across a portfolio

Product teams run this daily with `sort: "most_recent"`, `sinceDate: "1 day"`, every language they ship in, and a downstream rule: 1–2★ reviews with text go to a support queue, reviews mentioning a crash or a version number go to engineering, everything else lands in a weekly digest. Because filtered reviews are free, the daily cost is proportional to what you act on, not to what users write. Pair it with the [Apple App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper) and one schedule covers both stores with matching columns — the same `rating`, `text`, `review_day`, developer-reply and `country` fields, so one dashboard serves iOS and Android.

### Android app feedback that keeps its structure

Each row keeps `app_version`, so a spike of 1★ reviews can be tied to the release that caused it; `thumbs_up` shows which complaints other users endorsed; **google play ratings** in the `app` row (`rating_avg`, `rating_count`) give the denominator for a daily rating history. Store the dataset each day and you have a **play store reviews export** with history for free.

### What this does not do

It does not read reviews from the Play Console (those need your developer login and include private data the public page never shows), it does not resolve app names (use the package from the URL), and it does not translate — reviews come in the language they were written in, which is why `languages` exists.

### Choosing between sort orders

`most_recent` is chronological and the only order that makes a since-date feed exact. `most_relevant` is Google's own blend of recency, helpfulness and rating — the order the Play Store shows first. `rating` puts five-star reviews first, which is useful for testimonial mining and useless for monitoring.

## Related scrapers

Reviews from the other store and from other public sources, with the same row discipline, the same pay-per-delivered-row billing and the same scheduling story:

- **[Trustpilot Reviews Scraper](https://apify.com/kestrel/trustpilot-reviews-scraper)** — company reviews and TrustScore from Trustpilot, past the 200-review wall an anonymous reader normally hits.
- **[Apple App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper)** — the iOS half of this pair: App Store reviews across every country storefront, matching columns.
- **[Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)** — customer reviews for any product across 20 marketplaces, with the same pre-billing rating filters.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** and **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — guest reviews for hospitality, filtered before billing.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
