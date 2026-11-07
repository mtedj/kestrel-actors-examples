# Trustpilot Reviews Scraper — Customer Reviews & TrustScore

A **trustpilot reviews scraper** that turns any company profile into structured **company reviews**: the 1–5 star `rating`, the headline, the body text, the language it was written in, when it was published and when the experience happened, who wrote it and from which country, whether it is verified, how many readers found it useful, and the company's own public reply. Alongside the reviews it hands you the free company block — **TrustScore**, the star histogram, the per-language breakdown and the public contact details — so one run returns both the **customer feedback** and the Trustpilot data about the profile it came from.

Give it a domain (`www.booking.com`, `www.monzo.com`, `ryanair.com`) or a review-page URL. No login, no API key, no cookies to paste. It bills per review row, and every filter runs *before* you are billed.

Last verified working: 2026-10-28.

## Trustpilot 公司评论、客户评价与 TrustScore：中文调用与语言设置

按公司域名或 URL 获取客户评论、评分、公司回复及公开公司资料。

languages="all" 保留全部语言；例如 "de" 或 "fr" 筛选对应原文。评论不自动翻译；应先查看免费公司行中的语言分布，再缩小语言范围。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "companyDomains": [
    "www.booking.com"
  ],
  "maxReviewsPerCompany": 1,
  "sort": "most_recent",
  "languages": "all",
  "sessions": 1
}
```

Trustpilot Bewertungen / avis clients / reseñas：关注原文、日期和已验证标记。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Trustpilot scraper for AI agents: which input answers which request?

Use this actor when the request names a company and wants its Trustpilot customer reviews (star rating, text, dates, reviewer country, verified flag, the company's reply) or its TrustScore and star histogram. Give it the company's **domain** (`www.booking.com`) or its Trustpilot review-page URL. Do not use it to find companies by name or category, to read a transparency report, to scrape product reviews per SKU, or to translate reviews: none of that exists here. A bare company name ("Monzo") is rejected before anything is charged — pass `monzo.com`.

| user request | input JSON |
|---|---|
| reviews of company X | `{"companyDomains": ["www.monzo.com"]}` (up to 100 newest reviews; `"maxReviewsPerCompany": 1000` requests a capped star-band sample, not a full corpus) |
| negative reviews / complaints about X | `{"companyDomains": ["www.monzo.com"], "maxRating": 2, "requireText": true}` |
| reviews published since yesterday (deduplicate repeat windows externally) | `{"companyDomains": ["www.monzo.com"], "sinceDate": "1 day", "sort": "most_recent"}` |
| reviews from the last 3 months | `{"companyDomains": ["www.monzo.com"], "dateRange": "last3months"}` |
| what people say about refunds | `{"companyDomains": ["www.monzo.com"], "keyword": "refund"}` |
| German-language reviews only | `{"companyDomains": ["www.monzo.com"], "languages": "de"}` |
| verified reviews only | `{"companyDomains": ["www.monzo.com"], "verifiedOnly": true}` |
| TrustScore, star histogram, contact details of X (cheapest) | `{"companyDomains": ["www.monzo.com"], "maxReviewsPerCompany": 1}` (one billed review; the company row is free) |
| compare competitors | `{"companyDomains": ["www.monzo.com", "www.revolut.com", "www.starlingbank.com"], "maxReviewsPerCompany": 200}` |
| from a Trustpilot URL | `{"startUrls": ["https://www.trustpilot.com/review/www.monzo.com"]}` |

Output rows share one dataset and are told apart by `type`. A `review` row (billed, $0.0015 each) carries `review_id`, `company_domain`, `company_name`, `rating` (1–5), `title`, `text`, `language`, `review_date`, `experience_date`, `updated_date`, `reviewer_name`, `reviewer_country`, `reviewer_reviews`, `verified`, `verification_level`, `source`, `likes`, `reply_text`, `reply_date`, `location`, `url`. A `company` row (free, one per company) carries `trust_score`, `stars`, `review_count`, `reviews_last_12_months`, `ratings` (the 1–5 histogram), `review_languages`, `categories`, `website`, `email`, `phone`, `address`, `is_claimed`, `is_closed`, `is_collecting`, `verified_payment`, `verified_identity`. A `status` row (free, one per input) says `ok`, `no_reviews`, `not_found` or `error`, how many reviews were delivered and `filtered`, and `capped: true` when Trustpilot's 200-review wall, not the end of the reviews, stopped the walk. A domain with no Trustpilot profile is a free `not_found` status row, never an empty success; bad input ends the run with the reason on the run card and nothing charged.

## What does the Trustpilot reviews scraper do?

You give it companies. It gives you their reviews as rows you can sort, filter and export.

- **`review` rows** — `review_id`, `rating` (1–5), `title`, `text`, `language`, `review_date`, `experience_date`, `updated_date`, `reviewer_name`, `reviewer_id`, `reviewer_country`, `reviewer_reviews`, `verified`, `verification_level`, `source`, `likes`, `reply_text`, `reply_date`, `location`, `url`, plus `company_domain`, `company_name` and `fetched_at`.
- **`company` rows** — free context per profile: `company_id`, `company_domain`, `company_name`, `trust_score`, `stars`, `review_count`, `reviews_last_12_months`, `review_count_filtered`, `ratings` (the one-to-five histogram), `review_languages`, `categories`, `website`, `country_code`, `email`, `phone`, `address`, `is_claimed`, `is_closed`, `is_collecting`, `verified_payment`, `verified_identity`, `reviews_fetched` and `url`.
- **`status` rows** — free, one per input: `target`, `company_domain`, `company_name`, a `status` of `ok`, `no_reviews`, `not_found` or `error`, how many `reviews` were delivered, how many were `filtered`, how many `pages` were read, the site's own `total`, a `capped` flag, a `duplicates` flag, the `error` if any, and `fetched_at`.

Reviews come back **in the language they were written in**, tagged with the language code. One large travel brand returned forty languages across 120,000 reviews.

## Trustpilot reviews by domain or by review-page URL

- **`companyDomains`** — the domain a profile is listed under: the part after `/review/` in the address bar. `www.booking.com`, `www.monzo.com`, `ryanair.com`. A company's own website URL works too; the domain is taken from it. If the site prefers a different spelling — `monzo.com` really lives at `www.monzo.com` — the redirect is followed automatically and the canonical domain comes back in every row.
- **`startUrls`** — full review pages such as `https://www.trustpilot.com/review/www.booking.com`. Any query string on the URL is ignored; set the filters below instead so the run stays reproducible. A country subdomain such as `uk.trustpilot.com` is read as the same profile.

A URL and its bare domain count as the same company and are harvested once, so mixing the two inputs never double-bills. The duplicate shows up as a free `status` row with `duplicates: 1`.

## How many reviews can one company return?

This is the number nobody else on the Store states plainly, so here it is: **an anonymous visitor gets ten pages — 200 reviews — of any one filtered view.** Ask for page eleven and the site answers with a redirect to its login screen. That is a hard wall, and it is why some listings quietly return 200 rows and call a brand "done".

This actor gets past it honestly. The five star ratings are five *separate* filtered views, each with its own 200-review allowance, and they are disjoint — a review is one star or four, never both. With **`deepPaging`** on (the default) a request for more than 200 reviews is split across the 1★, 2★, 3★, 4★ and 5★ views, the results are merged and de-duplicated, and up to **1,000 reviews per company per run** come back. Quotas use the profile's histogram, but per-band caps and filters can change the resulting mix. This is a capped sample, not a complete corpus or necessarily the globally newest 1,000 reviews. For a chronological latest sample, use `sort: "most_recent"` with `maxReviewsPerCompany` at most 200.

A walk that reaches the source wall reports `capped: true` in its free status row. A requested result cap can stop earlier without setting this flag, so `capped: false` does not prove you collected the full history. Check the requested cap, delivered count, filters and source status together.

## Review monitoring that costs what it should

Six controls run **before** billing, and together they are why watching a hundred brands is affordable:

- **`minRating` / `maxRating`** map to the site's own `stars=` URL parameter, which runs on their servers. `minRating: 1, maxRating: 2` on a 125,000-review brand fetches and bills only the one- and two-star rows. Nothing else is ever downloaded, so a complaints feed costs what a complaints feed should.
- **`dateRange`** is the site's own date filter — Trustpilot reviews by date, in one parameter: `last30days`, `last3months`, `last6months`, `last12months`. Also server-side.
- **`languages`** keeps a single language, filtered on their side. The default here is `all` — the public page shows English only, which hides most reviews of a global brand — and the `review_languages` field on the company row tells you how many reviews each language holds before you commit.
- **`keyword`** is their review search: `refund`, `delivery`, `chargeback`, `cancellation`. Non-matching reviews are never fetched.
- **`verifiedOnly`** keeps only reviews carrying the verified badge.
- **`sinceDate`** and **`requireText`** run inside the actor before billing. `sinceDate` accepts a date or relative `7 days`; newest-first order can stop when older reviews are reached. Page count depends on activity and caps. There is no cross-run review memory: an overlapping date window can deliver and bill the same review again. `requireText` is applied after the collection cap, so the delivered count can be lower.

Filtered reviews are never charged. Neither are company rows, status rows, profiles with no reviews, or domains that turn out not to exist.

## Company reviews for support, marketing and due diligence

- **Support and CX teams** run a daily complaints feed across their own profile and their rivals' — Trustpilot competitor reviews next to their own, in one dataset: `minRating: 1, maxRating: 2, sinceDate: "2 days", sort: "most_recent"`. Every row carries `reply_text` and `reply_date`, so "which complaints did we answer" is a filter, not a project.
- **Marketing and reputation monitoring** track `trust_score` and the `ratings` histogram over time. Schedule the run, keep `maxReviewsPerCompany: 0` off and `includeCompanyRow: true` on, and you have a cheap daily reputation monitoring series for a whole category.
- **Analysts** pull a capped sample for review sentiment analysis and voice of customer data: `maxReviewsPerCompany: 1000`, `requireText: true`, one language at a time so the model gets clean input.
- **Sales and lead generation** use the free company row on its own — `email`, `phone`, `address`, `categories`, `website`, `is_claimed` — to qualify a list of domains before anyone picks up the phone.
- **Due diligence and marketplace risk** read `is_closed`, `is_collecting`, `verified_payment` and `verified_identity` next to the score.

## Input

| field | what it does |
|---|---|
| `companyDomains` | Domains as listed on the profile, e.g. `www.booking.com`. A website URL works too. |
| `startUrls` | Full review-page URLs. Query strings are ignored; use the filters instead. |
| `maxReviewsPerCompany` | 0 = as deep as an anonymous visitor can go (up to 1,000 with deep paging); N = the first N. The main cost control. Default 100. |
| `sort` | `most_recent` (default) or `most_relevant`. |
| `deepPaging` | On by default: split a big request across the five star views to beat the 200-review wall. Off: one view, never more than 200 rows or 10 page requests. |
| `languages` | `all` (default) or one language code — `en`, `de`, `fr`, `es`, `it`, `nl`, `da`, `sv` … Server-side. |
| `minRating` | 0 = any; 1–5 = keep only reviews at or above it. Server-side, so it is a cost control. |
| `maxRating` | 0 = any; 1–5 = keep only reviews at or below it. Server-side. |
| `dateRange` | `all`, `last30days`, `last3months`, `last6months`, `last12months`. Server-side. |
| `sinceDate` | `YYYY-MM-DD` or relative (`7 days`, `2 weeks`, `1 month`). Stops the walk early on newest-first runs. |
| `verifiedOnly` | Keep only reviews with the verified badge. Server-side. |
| `keyword` | Only reviews mentioning a word or phrase. Server-side. |
| `requireText` | Drop rating-and-title-only reviews before billing. |
| `includeCompanyRow` | Emit the free company row (default on). |
| `sessions` | Parallel proxy sessions (egress IPs). Default 2. |
| `perIp` | Requests per second per session. Default 1. |
| `proxyConfiguration` | Apify Proxy, RESIDENTIAL group by default. Required. |

### Example: a daily complaints feed for a comp set

```json
{
  "companyDomains": ["www.booking.com", "www.expedia.com", "www.agoda.com"],
  "maxReviewsPerCompany": 60,
  "sort": "most_recent",
  "minRating": 1,
  "maxRating": 2,
  "sinceDate": "2 days",
  "requireText": true,
  "languages": "all"
}
```

### Example: the deep corpus of one brand for sentiment work

```json
{
  "companyDomains": ["www.monzo.com"],
  "maxReviewsPerCompany": 1000,
  "deepPaging": true,
  "requireText": true,
  "languages": "en",
  "includeCompanyRow": true
}
```

### Example: what people say about refunds, last quarter

```json
{
  "startUrls": ["https://www.trustpilot.com/review/www.booking.com"],
  "keyword": "refund",
  "dateRange": "last3months",
  "maxReviewsPerCompany": 200,
  "deepPaging": false,
  "sort": "most_relevant"
}
```

## Output

Three row types share one dataset, and the Output tab ships five ready-made views: **Overview**, **Reviews**, **Complaints**, **Companies** and **Status**.

**Review fields.** `review_id` is stable across runs, so an incremental pipeline can key on it. `rating` is 1–5. `title` and `text` are the headline and the body; `text` is empty when someone left only a rating, which is what `requireText` removes. `language` is the ISO code of the text. `review_date` is when it was published and `experience_date` is when the experience happened — they are often weeks apart, and the second is the one you want for cohort work. `updated_date` is set when the author edited the review. `reviewer_name`, `reviewer_id`, `reviewer_country` and `reviewer_reviews` describe the author; a reviewer with one lifetime review reads differently from one with two hundred. `verified` and `verification_level` say whether the platform vouched for the transaction, and `source` says how the review was collected (`Organic`, `Invitation`, `BusinessGeneratedLink`). `likes` counts readers who found it useful. `reply_text` and `reply_date` are the company's public answer. `location` is set on multi-branch profiles. `url` is the permalink.

**Company fields.** `trust_score` is the headline score out of five and `stars` is the rounded Trustpilot star rating shown on the profile. `review_count` is the lifetime total and `reviews_last_12_months` the recent one — the gap between them tells you whether a profile is alive. `review_count_filtered` is how many reviews matched this run's filters. `ratings` is the one-to-five histogram, `review_languages` is `[{code, name, count}]`, and `categories` lists the category names the company is filed under. `website`, `country_code`, `email`, `phone` and `address` are the public contact block. `is_claimed`, `is_collecting`, `is_closed`, `verified_payment` and `verified_identity` are the trust flags. `reviews_fetched` is how many reviews this run read for the company before the actor-side filters.

**Status fields.** One row per input: `target` echoes what you gave, `status` is `ok` / `no_reviews` / `not_found` / `error`, `reviews` is what was delivered, `filtered` is what was dropped before billing, `pages` is how many page requests were spent, `total` is the site's own count for your filters, `capped` marks a walk that stopped at the paging wall, `duplicates` marks an input already covered by another, `error` explains a failure, and `fetched_at` timestamps the run. A challenge that never clears is reported as `error` — never as an empty success.

Export as JSON, CSV, Excel, XML or RSS from the Console, or pull the dataset over the API.

## How much does it cost?

Pay per `review` row. `company` and `status` rows are free, and so is any company that turns out to have no reviews or no profile at all. Filters run before billing, so the rows you filter out cost nothing.

One run pays a small fixed overhead: a headless browser solves the site's bot challenge once, which takes five to twenty seconds of compute and a megabyte or so of proxy traffic. Every page after that is fetched without a browser, so the overhead is amortised across the whole run — it is noticeable on a twenty-review test and invisible on a thousand-review harvest. The token is re-solved every four minutes because the site stops honouring it at about five.

## Trustpilot scraper in Python, JavaScript, curl, n8n, Make or an AI agent

Start it with the Apify API or any client library. Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_API_TOKEN>")
run = client.actor("kestrel/trustpilot-reviews-scraper").call(run_input={
    "companyDomains": ["www.booking.com"],
    "maxReviewsPerCompany": 200,
    "sort": "most_recent",
    "languages": "all",
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["review_date"], row["title"])
```

JavaScript (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_API_TOKEN>' });
const run = await client.actor('kestrel/trustpilot-reviews-scraper').call({
    companyDomains: ['www.monzo.com'],
    maxReviewsPerCompany: 100,
    minRating: 1,
    maxRating: 2,
    requireText: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'reviews');
```

curl, run synchronously and get the dataset back in one call:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~trustpilot-reviews-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"companyDomains":["www.booking.com"],"maxReviewsPerCompany":40,"sort":"most_recent"}'
```

**n8n, Make and MCP.** In n8n use the Apify node, pick this actor, paste the same JSON as the run input and wire the dataset straight into a Slack, Sheets or Postgres node. In Make (Integromat) the Apify app's *Run an Actor* module does the same, and *Get Dataset Items* pages the result. For an AI agent, the actor is reachable over Apify's MCP server, so a Claude or ChatGPT agent can call it as a tool and read the rows back as JSON — the flat, non-ragged row shape is deliberate: every review row carries every key, so an agent never has to guess whether a field exists.

## Is it legal to scrape Trustpilot reviews?

Only public pages are read: the same review pages any visitor sees, with no account, no login and no paywall. No personal data beyond what the platform itself publishes next to each review (a display name, a country code, a review count) is collected, and nothing behind an authentication wall is touched. Public data collection of this kind is generally lawful in the EU and the US, but the legal picture depends on what you do next: republishing review text verbatim, or processing reviewer names, brings copyright and GDPR duties of your own. Read the platform's terms, keep personal fields out of anything you publish, and take legal advice before commercial redistribution. This tool provides the data; the compliance is yours.

## Limits and honest notes

- **200 reviews per filtered view** is the platform's wall for anonymous visitors, and 1,000 per company per run is the practical ceiling once the five star views are combined. If you need more, narrow with `dateRange` or `languages` and run again — each combination has its own allowance.
- The bot challenge is solved with a real browser once per run and refreshed every four minutes. If a run is very short, that fixed cost is a real share of it.
- `verifiedOnly` reflects the platform's own badge, which many companies never use; some large profiles have only a handful of verified reviews.
- Reviews are returned as written, never translated.
- `location` is only populated for profiles that run multiple branches.

## FAQ

### Does it need a Trustpilot API key or login?

No. There is no account, no key and no cookie to paste. It reads the same public pages a visitor sees.

### Can I download Trustpilot reviews as CSV or Excel?

Yes. Every run writes an Apify dataset, so a Trustpilot review export is one click: Trustpilot reviews CSV, Excel, JSON, XML or RSS from the Console, or straight from the API. The Reviews view is already trimmed to the fields most people want.

### How do I get only Trustpilot negative reviews?

Set `minRating: 1` and `maxRating: 2` — that is how you pull Trustpilot reviews by rating. That becomes the site's own star filter, so the four- and five-star rows are never downloaded and never billed. Add `requireText: true` to drop the rating-only rows.

### How far back can I go?

As far as 200 reviews per filtered view takes you — a few weeks on a very busy brand, years on a quiet one. Use `dateRange` to aim a window, and `sinceDate` to stop a scheduled run as soon as it reaches material it already has.

### Which companies can I scrape?

Any profile that exists. Give the domain exactly as the profile lists it. If the profile does not exist you get a free `status` row with `not_found` — you are never charged for a miss, and it is never reported as "no reviews".

### Does it include the company's replies?

Yes: `reply_text` and `reply_date` on every review that has one. Response rate and median response delay are both computable from a single run.

### What is TrustScore, and where do I find it?

TrustScore is the platform's weighted score out of five, and it lives on the free `company` row as `trust_score`, next to `stars`, `review_count` and the full `ratings` histogram. You are never billed for it.

### Can I use this for review sentiment analysis?

Yes, and `requireText: true` plus a single `languages` value is the combination to use — it gives a model clean, one-language input with no rating-only rows to skew the corpus.

### How fast is it?

About one page (20 reviews) per second per session, two sessions by default, plus the one-off browser bootstrap. A 1,000-review company takes a couple of minutes; a hundred small profiles take about the same.

### What does bulk work cost?

Cost scales with delivered rows, not with companies, which is what makes bulk company reviews practical. A hundred profiles at 50 recent reviews each is 5,000 rows; the same hundred profiles at `minRating: 1, maxRating: 2` is a fraction of that, because the rest are never fetched.

## Scrape Trustpilot on a schedule

Set an Apify schedule separately; this Actor does not create one or remember delivered review IDs between runs. `sinceDate: "1 day"` includes yesterday and today, so daily windows overlap. Reviews delivered again are billed again, even if your database already holds their IDs. Downstream deduplication prevents duplicate stored records, not repeat Actor charges.

Use this bounded input for a daily complaints feed, then store the review data externally:

```json
{"companyDomains":["www.monzo.com"],"maxReviewsPerCompany":50,"maxRating":2,"requireText":true,"sinceDate":"2 days","sort":"most_recent","includeCompanyRow":true}
```

The first and repeat calls use the same input. Up to 50 reviews cost $0.075 per company per run; set `callOptions.maxTotalChargeUsd: 0.075` on MCP `call-actor`, outside `input` (API: run option `maxTotalChargeUsd`). Fewer rows can remain after `requireText`. Retrieve and paginate the run's default dataset. Separate `type="review"`, free `company`, and free `status` rows; join company context by `company_domain` and upsert review rows by `review_id`, retaining `fetched_at`, `updated_date`, `reply_text` and `reply_date`. An overlapping publication-date window can catch late arrivals, but it does not guarantee later edits or replies on older reviews are revisited. A capped daily snapshot can miss reviews on a busy profile; inspect `status.capped`, counts and the requested cap.

### Customer feedback that keeps its structure

Every review row carries every key, always in the same order, with `null` where the platform had nothing. No ragged rows, no fields that appear only sometimes, no nested blobs to flatten — the point is that a warehouse load or a dataframe read never breaks because one review happened to lack a reply.

### Reputation monitoring across a portfolio

Run one job per brand family, keep the free company row on, and store `trust_score`, `review_count` and `ratings` per day. That series — plus the review text behind it — is what turns "our score dropped" into "our score dropped because refunds started taking three weeks on 12 August".

### What this does not do

It does not post, reply to or flag reviews, does not read private business dashboards, and does not reach the invitation or transaction data only a profile owner can see. It reads public pages.

## Related scrapers

Same house, same row discipline, same charged-equals-delivered promise:

- [Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper) — product reviews with ratings, verified-purchase flags and variants.
- [App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper) — iOS reviews by app and country, with developer responses.
- [Google Play Reviews Scraper](https://apify.com/kestrel/google-play-reviews-scraper) — Android reviews with app version, thumbs-up counts and replies.
- [Indeed Company Reviews Scraper](https://apify.com/kestrel/indeed-company-reviews) — the same company from the inside: employee reviews with five sub-ratings, pros and cons, job title and location, and the employer's reply.
- [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) — guest reviews with six sub-ratings and the management response, when the company is a hotel or a chain and its customers talk there rather than on Trustpilot.

Run one of each and you have the customer reviews and the employee reviews for a company across its web profile, its marketplace listings, both app stores and its own workforce, in one row shape.
