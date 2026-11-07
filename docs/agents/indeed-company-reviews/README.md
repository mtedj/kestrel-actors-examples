# Indeed Company Reviews Scraper — every employee review of any company

This Indeed company reviews scraper turns any company page on Indeed into a clean dataset of employee reviews: the 1-5 star rating, the five sub-ratings, the headline and the full text, pros and cons, the reviewer's job title and location, whether they still work there, the date, the helpful votes and the employer's public reply. Give it company names (`Home Depot`), slugs or `/cmp/` URLs and it walks every page for you. It is a plain HTTP scraper — no API key, no login, no browser — so a run of company reviews costs a fraction of what a headless-browser scraper costs, and the same job runs the same way whether you want employer reviews for one company or for a thousand.

Last verified working: 2026-11-07.

## Indeed 公司评价、员工评论与雇主评分：中文调用与语言设置

按公司名称或 URL 获取员工评论、优缺点、职位、地点和雇主回复。可用于员工体验与雇主研究，不提供求职者资料。

countries=["all"] 查询所有支持地区；国家未指定时应优先使用 all。国家代码按 Indeed 域名，例如 uk、tw、hk；不支持 cn，不会自动把评论翻译为中文。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "companies": [
    "https://www.indeed.com/cmp/Google/reviews"
  ],
  "countries": [
    "all"
  ],
  "maxReviewsPerCompany": 1,
  "sort": "newest",
  "sessions": 1
}
```

Avis employés / Arbeitgeberbewertungen / opiniones de empleados：按评论实际地区与语言解释。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Indeed company reviews at a glance

| | |
|---|---|
| **What you give it** | Company names (`Home Depot`, `Ernst & Young`), slugs (`Google`) or company URLs (`https://www.indeed.com/cmp/Starbucks/reviews`) |
| **What you get** | One row per employee review + a free company row + a free status row per company and country |
| **Reviews per page** | 20, walked automatically until the cap or the end |
| **Country domains** | 44, plus `all` — nearly every review of a company in a single walk |
| **Price** | $0.003 per review. Company rows, status rows, empty companies and filtered reviews are free |
| **Speed** | Typically about 1,200 reviews per minute at the default two sessions (measured on the platform: 2,000 Walmart reviews in 96 seconds); slower when the proxy IPs Indeed serves to your account are slow |
| **Monitoring** | `onlyNewReviews` on a schedule: each run delivers and bills only what is new since the last one |
| **Needs a browser?** | No. No API key, no cookie, no login |

## What does the Indeed Company Reviews Scraper do?

Indeed publishes employee reviews on a company page at `indeed.com/cmp/<Company>/reviews`. Each review carries far more structure than a star rating: the reviewer grades work-life balance, compensation and benefits, job security and advancement, management and culture separately, writes a headline and a body, may fill in a Pros and a Cons field, and is tagged with a job title, a location and whether they are a current or former employee. Employers can reply publicly, and other readers vote reviews helpful or unhelpful.

This scraper reads all of that, one company at a time, and writes it to a dataset you can export as JSON, CSV, Excel or XML, or read straight from the API. It also collects the aggregate picture Indeed shows in the sidebar — the overall score, the 1-5 star histogram, the five category averages, the Work Happiness score, the topic breakdown and the pros and cons Indeed extracts from the whole corpus — and puts it in one free company row, so you get the company ratings and the individual reviews in the same run.

Typical uses:

- **Employer brand tracking.** Watch what current and former staff say about you and about the companies you compete with for the same talent.
- **Employee feedback analysis.** Feed the text into a topic model or an LLM and find out which of the five categories is actually dragging the score down.
- **Recruitment marketing.** Quote real strengths, and fix the objections candidates read before they apply.
- **Due diligence and market research.** Culture and management scores across an industry, an acquisition target, or a franchise network location by location.
- **Review monitoring.** Run it on a schedule with `onlyNewReviews` and each run delivers, and bills, only the reviews written since the last one — employer reputation monitoring without a vendor contract.
- **Indeed negative reviews only.** Lowest-rated first with a rating ceiling gives a complaints feed you can route to whoever owns the fix.

## Indeed scraper for AI agents: which input answers which request?

Use this actor when the request is about **what employees say about a company on Indeed**: employee reviews, employer ratings, complaints, the five category scores, employer replies, or the company's Indeed profile (industry, size, headquarters, CEO). Do not use it for Indeed job listings, salaries, interview questions or Glassdoor data — it returns none of those.

| The user asks for | Input |
|---|---|
| "200 most recent reviews of Home Depot" | `{"companies": ["Home Depot"], "maxReviewsPerCompany": 200, "countries": ["all"]}` |
| "what do Starbucks employees complain about" | `{"companies": ["Starbucks"], "sort": "rating_asc", "maxRating": 2, "requireText": true, "maxReviewsPerCompany": 100}` |
| "50 reviews by nurses at Kaiser Permanente in California, last 12 months" | `{"companies": ["Kaiser Permanente"], "jobTitleContains": "nurse", "locationContains": ", CA", "sinceDate": "12 months", "maxReviewsPerCompany": 50}` |
| "compare Walmart, Target and Costco as employers" (ratings, no reviews) | `{"companies": ["Walmart", "Target", "Costco"], "maxReviewsPerCompany": 1}` and read the `type: "company"` rows |
| "new reviews of Marriott every morning" | `{"companies": ["Marriott International"], "onlyNewReviews": true, "countries": ["all"]}` on a daily schedule |
| "reviews UK employees left about Tesco, worst first" | `{"companies": ["Tesco"], "countries": ["uk"], "sort": "rating_asc", "maxReviewsPerCompany": 0}` |
| "Amazon reviews worldwide, budget $20" | `{"companies": ["Amazon"], "countries": ["all"], "maxReviewsPerCompany": 10000}` plus Apify run option `maxTotalChargeUsd: 20` outside the input. At $0.003 each, that budget allows at most 6,666 delivered reviews ($19.998), even though the result cap is 10,000. |

What comes back: one dataset, three row types told apart by `type`. `review` rows are the only charged ones. One free `company` row per company carries Indeed's own rating, review count, star histogram and category averages. One free `status` row per company and country says what happened: `ok`, `no_reviews`, `not_found` (with the closest company names Indeed knows in `suggestions`), `duplicate`, `partial` (some reviews delivered, then a page was refused) or `error`. A run in which no company resolves ends successfully with the reason on the run and nothing charged. The most a run can cost is companies x `maxReviewsPerCompany` x $0.003.

## How do I run the Indeed reviews scraper?

Open the actor, type one or more companies into **Indeed companies**, and hit Start. Everything else has a working default. The three inputs that matter most are `companies`, `countries` and `maxReviewsPerCompany`.

A company can be a plain name, the slug (the part of the URL after `/cmp/`) or the whole URL, and you can mix them freely. Indeed resolves a name to the page it files the company under — `Home Depot` becomes `The-Home-Depot`, `Ernst & Young` becomes `Ey` — and every row carries that slug in `company`:

```json
{
  "companies": ["Home Depot", "Google", "https://www.indeed.com/cmp/Starbucks/reviews"],
  "countries": ["us"],
  "maxReviewsPerCompany": 200,
  "sort": "newest",
  "includeCompanyRow": true
}
```

From Python, with the Apify client:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/indeed-company-reviews").call(run_input={
    "companies": ["Google", "Starbucks"],
    "countries": ["us"],
    "maxReviewsPerCompany": 500,
    "sort": "rating_asc",
    "maxRating": 2,
    "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["job_title"], "|", row["title"])
```

From JavaScript / Node:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/indeed-company-reviews').call({
    companies: ['Google'],
    countries: ['all'],
    maxReviewsPerCompany: 1000,
    sinceDate: '90 days',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'employee reviews');
```

And from curl, if you just want to download Indeed reviews as CSV in one command:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~indeed-company-reviews/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>&format=csv" \
  -H 'Content-Type: application/json' \
  -d '{"companies":["Google"],"countries":["us"],"maxReviewsPerCompany":100}' \
  -o indeed-reviews.csv
```

## Input reference

Every field below is optional except `companies`, and every one of them has a sensible default.

**Which companies**

- `companies` — company names, Indeed slugs or `/cmp/` URLs. A name is resolved by Indeed itself and the rows carry the slug it chose; a name Indeed does not know costs nothing and comes back as `not_found` with the closest names it does know. A URL that names a country domain (`https://ca.indeed.com/cmp/Google`) is read on that domain only; anything else uses the `countries` list. Two spellings of one company (`Home Depot`, `The-Home-Depot`) are recognised and billed once.
- `countries` — which Indeed domains to read each company on. Default `["us"]`. See the section below.

**Which reviews**

- `maxReviewsPerCompany` — `0` takes every review the chosen domains list; `N` delivers the first `N` reviews **that pass your filters**, in the chosen order, counted across all countries: 50 with `jobTitleContains: "nurse"` is 50 nurse reviews, not the nurses among the first 50. Default 100. This is the main cost control.
- `sort` — `newest` (default), `helpfulness`, `rating_desc` (highest first) or `rating_asc` (lowest first). Indeed silently ignores any other value and serves newest first, which is why this is a fixed list rather than free text.
- `minRating` / `maxRating` — keep only reviews at or above / at or below a 1-5 star rating. `0` means no bound.
- `requireText` — drop rating-only reviews.
- `jobTitleContains` — case-insensitive substring of the reviewer's job title, e.g. `engineer`, `nurse`, `driver`.
- `locationContains` — case-insensitive substring of the review's location, e.g. `Mountain View`, `TX`.
- `sinceDate` — `YYYY-MM-DD` or a relative string such as `30 days`, `2 weeks`, `12 months`, so a saved input never goes stale.
- `onlyNewReviews` — monitoring mode. The actor remembers what it delivered (per company, country and filter set) and each later run delivers, and bills, only reviews it has not given you before. The first run is the baseline: the newest `maxReviewsPerCompany` reviews. Needs the default `newest` order.
- `includeCompanyRow` — emit the free company row (default on). This costs one extra free request per company, to the company overview page, which is where industry, size, headquarters, website, founded year, revenue band and CEO live.

**Performance**

- `sessions` — how many proxy sessions (egress IPs) run in parallel, each carrying up to three downloads at once. Default 2.
- `perIp` — requests per second per session. Default 1.
- `proxyConfiguration` — keep the default. The actor tests your account's datacenter IPs, keeps the ones Indeed serves and switches to residential by itself only when none of them is served.

Two notes on where the filters run. `minRating`, `maxRating`, `requireText`, `jobTitleContains`, `locationContains` and `sinceDate` are applied inside the actor, before billing, so a review a filter drops is never charged. `sort` is applied by Indeed itself. The combination is what makes a complaints feed cheap: `sort: "rating_asc"` with `maxRating: 2` puts the one- and two-star reviews on the first page and stops the walk as soon as a whole page is above the ceiling.

## Review rows: every field this Indeed scraper returns

Three row types share one dataset and are told apart by `type`.

**`type: "review"` — charged, $0.003 each**

| Field | What it is |
|---|---|
| `review_id` | Indeed's stable encrypted review id, also the id in the review URL |
| `company` | The slug Indeed files the company under, the part after `/cmp/` — also when you gave a plain name |
| `company_name` | Company name as Indeed displays it |
| `country` | Which domain the row was read on: `us`, `all`, `ca`, `de`, … |
| `rating` | Overall rating, 1-5 stars |
| `work_life_balance` | The reviewer's 1-5 rating for work/life balance, or null if they skipped it |
| `compensation_benefits` | Their 1-5 rating for pay and benefits, or null |
| `job_security_advancement` | Their 1-5 rating for job security and advancement, or null |
| `management` | Their 1-5 rating for management, or null |
| `culture_values` | Their 1-5 rating for culture, or null |
| `title` | The headline the employee wrote |
| `text` | The full review body, untruncated |
| `pros` | The Pros field, when the review was submitted with the pros/cons form |
| `cons` | The Cons field, likewise |
| `job_title` | The reviewer's job title |
| `location` | Where they worked, e.g. `Mountain View, CA` |
| `review_country` | ISO country code Indeed files the review under |
| `employment_status` | `current` or `former` |
| `review_date` | Publication date as `YYYY-MM-DD` |
| `review_date_text` | The date exactly as Indeed printed it, in that domain's language |
| `helpful_count` | How many readers voted it helpful |
| `unhelpful_count` | How many voted it not helpful |
| `employer_reply` | The employer's official public response, if any |
| `employer_reply_date` | Date of that response |
| `url` | Direct link to the review |

**`type: "company"` — free, one per company**

`review_count` (all reviews Indeed holds worldwide), `found_review_count` (what the domain you read actually lists), `rating`, `histogram` (how many gave 1, 2, 3, 4 and 5 stars), `ratings_breakdown` (the company averages for the same five categories), `happiness_score` and `happiness_grade` (Indeed's Work Happiness measure), `top_pros` and `top_cons` (what Indeed extracts from the corpus), `topics` (name, rating and count per theme), `industry`, `company_size`, `headquarters`, `website`, `founded`, `revenue`, `ceo`, `reviews_fetched` and `company_url`.

**`type: "status"` — free, one per company and country**

`target` (what you typed), `company` (the slug it resolved to), `company_name`, `country`, `status` (`ok`, `no_reviews`, `not_found`, `duplicate`, `partial` or `error`), `reviews` delivered and charged, `filtered` dropped before billing, `already_seen` skipped by `onlyNewReviews`, `pages` read, `total` reviews Indeed holds worldwide, `found_review_count`, `duplicates`, `error` and `suggestions` (on `not_found`: the closest companies Indeed knows, each with `name`, `company` and `url`). This row is the contract: if a company could not be read, you get `status: "error"` with the reason, never a silent empty result that looks like a company with no reviews; if Indeed refused a page half-way, you get `partial` and keep every review delivered before it. The run also writes a `SUMMARY` record to the key-value store with the same counts for the whole run.

The dataset ships with five views in the Output tab: **Overview**, **Reviews**, **Complaints** (rating, cons, management and work-life-balance scores, and the employer reply side by side), **Companies** and **Status**.

## Company reviews across 44 Indeed country domains

This is the part people usually get wrong. Indeed does not serve one global review list. `www.indeed.com` shows the reviews filed under the United States — 4,050 of Google's 6,270 on the day this was verified, but only 130 of Tesco's 1,596 — while `uk.indeed.com` shows the ones filed under the United Kingdom (218 for Google, 1,365 for Tesco) and `de.indeed.com` the German ones, each in that country's language. Every row says which in `review_country`. The subsets barely overlap.

So `countries` is a multiplier, and it has one special value:

- `"us"` — `www.indeed.com`, the reviews filed under the United States. The default.
- `"all"` — `www.indeed.com` with Indeed's own worldwide filter. For Google that is 6,270 of 6,270 reviews in a single walk. **If you want everything for a company, or the company is not American, this is the value to pass.**
- Any of `ca`, `uk`, `ie`, `au`, `nz`, `in`, `sg`, `ph`, `za`, `ae`, `hk`, `id`, `th`, `vn`, `lu`, `ch`, `be`, `de`, `at`, `fr`, `nl`, `es`, `it`, `pt`, `br`, `mx`, `ar`, `cl`, `co`, `pe`, `pl`, `se`, `dk`, `no`, `fi`, `tr`, `gr`, `hu`, `cz`, `ro`, `ua`, `jp`, `tw` — that country's own subset, in that country's language.

List several and they are walked in order until the cap is met. A review that appears on two domains is delivered and charged **once**: the run keeps one set of review ids per company. Dates are converted to `YYYY-MM-DD` whatever language they arrive in — `3. September 2025`, `2026, augusztus 25.` and `2026年2月27日` all resolve — and the original string is kept in `review_date_text` so nothing is lost.

```json
{
  "companies": ["Google"],
  "countries": ["all"],
  "maxReviewsPerCompany": 0,
  "sort": "newest"
}
```

## Employee reviews for employer brand and HR analytics

The five sub-ratings are what make this dataset useful rather than merely large. An overall score of 3.8 says nothing actionable; `management: 2` against `compensation_benefits: 4` says exactly where the problem is, and `job_title` plus `location` says for whom and where.

A few patterns that work well:

- **Category deltas over time.** Group by month and average each sub-rating. A management score sliding while pay holds steady is a leadership problem, not a budget one.
- **Role-level segmentation.** `jobTitleContains: "nurse"` or `"driver"` isolates the population you actually recruit, instead of averaging it with head office.
- **Site-level segmentation.** `locationContains` does the same for one plant, store or region — the level at which employee feedback usually becomes actionable.
- **Competitive employer brand.** Run the same input across five competitors and compare histograms rather than headline scores; a 4.0 built from mostly 5s and a few 1s is a very different workplace from a flat 4.0.
- **Response coverage.** `employer_reply` is empty on most reviews at most companies. The share of negative reviews you have answered is a cheap, honest employer-brand metric.
- **Employee sentiment analysis.** `text`, `pros` and `cons` are full length and untruncated, which is what a topic model or an LLM needs.

## Why is this a Glassdoor alternative?

Because Glassdoor is, in practice, unreadable without an account. Its review pages answer an interactive Cloudflare challenge to every ordinary client, and its paging URLs redirect to a login wall for anonymous visitors. Any tool that promises bulk Glassdoor data is either logging in as somebody, paying a challenge-solving vendor, or quietly returning very little.

Indeed publishes the same kind of workplace review data openly: the same five categories, the same current/former split, the same employer responses, at a far larger scale for hourly and frontline roles in particular. For most employer-brand, recruitment and market-research questions, Indeed company data is the better source and it is the one you can actually collect at volume. If you need consumer-side reputation as well, pair this with the [Trustpilot Reviews Scraper](https://apify.com/kestrel/trustpilot-reviews-scraper); if your product is an app, the [App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper) covers the other side of the same story.

## How much does it cost?

$0.003 per review row, and nothing else. There is no monthly rental and no per-run fee.

| You want | Input | Reviews | Cost |
|---|---|---|---|
| A quick look at one company | `maxReviewsPerCompany: 100` | 100 | $0.30 |
| One company, everything the US domain lists | `countries: ["us"], maxReviewsPerCompany: 0` | ~4,000 | ~$12.00 |
| One company, everything worldwide | `countries: ["all"], maxReviewsPerCompany: 0` | ~6,250 | ~$18.75 |
| Daily monitoring of 20 employers | `onlyNewReviews: true` on a schedule | ~40 new a day | $0.12 a day |
| A complaints-only feed | `sort: "rating_asc", maxRating: 2, maxReviewsPerCompany: 200` | 200 | $0.60 |

Free, always: the company row, the status rows, a company that has no reviews, an unknown company, and every review a filter dropped before billing. The run bills for exactly the review rows it delivers — that invariant is asserted in the test suite across every input mode and every spending limit.

## Integrations: n8n, Make, MCP and AI agents

- **n8n** — use the Apify node, pick this actor, map the JSON input above, then filter on `type == "review"` in a following node.
- **Make** — the Apify app's *Run an Actor* module followed by *Get Dataset Items*; set the input to the same JSON.
- **MCP / AI agents** — Apify's MCP server exposes this actor as a tool, so an AI agent can ask for "the last 50 reviews of Starbucks by former employees" and get structured rows back. The `SUMMARY` record and the status rows give the agent an honest signal about what it actually got.
- **Zapier, Webhooks, scheduling** — standard Apify plumbing. A daily schedule with `onlyNewReviews: true` reads one or two pages per company and bills only the new reviews.
- **Straight to a warehouse** — the dataset API serves CSV, JSON, XML and Excel; the CSV column set is stable because every row of a type carries every field.

## Is scraping Indeed reviews legal?

Short answer: the data is public and collecting it is generally lawful in the EU and the US, but it is personal data about identifiable people, and how you use it is where the legal risk lives. Nothing here is legal advice — take your own.

What we can say plainly:

- **This actor reads only what any visitor can read.** No login, no account, no paywall, no private endpoint. It does not collect anything Indeed hides from an anonymous reader.
- **Employee reviews are personal opinions written by real people.** A review carries a job title, a location, a date and an employment status. At a small employer, or for an unusual role, that combination can identify an individual even though no name is published. Treat every row as personal data under the GDPR and equivalent laws.
- **Do not try to re-identify reviewers.** Do not join these rows against your HR system, your rota, your leaver list or LinkedIn to work out who wrote what. That is the single most likely way to turn a legitimate analysis into an unlawful one — and, at many employers, a retaliation problem as well.
- **Have a lawful basis and minimise.** If you are relying on legitimate interests, aggregate analysis of your employer brand is a much easier case to make than storing individual reviews indefinitely. Keep what you need, for as long as you need it, and no longer.
- **Publishing is a separate question.** Reproducing review text verbatim raises copyright and database-right questions on top of privacy ones. Aggregates, scores and short quotes with attribution are far safer than republishing corpora.
- **Respect Indeed's terms and be polite.** The defaults here are deliberately gentle — one request per second per session — and there is no reason to raise them.

## Limits and known traps

- **A page past the end silently repeats page one.** Indeed answers `?start=` beyond the last page with HTTP 200 and the first twenty reviews again, never an error. A naive scraper pages forever and bills you for the same rows over and over. This actor bounds the walk three ways — by the review count Indeed declares, by the page number Indeed reports, and by review ids it has already seen — so it stops on the first repeated page and charges you for nothing extra.
- **Indeed refuses more than half of all datacenter IPs.** Its Cloudflare check judges the IP: an address is either served every time or never (measured 2026-10-05: 93 of 100 fresh sessions gave the same answer three times running, and a served session answered 125 of 125 consecutive pages). So the actor sweeps your account's proxy pool once, keeps the sessions that are served for the whole run, and falls back to residential IPs only when the whole pool is refused. If even that fails, the company gets `status: "error"` with the reason — never a fake empty result.
- **A refusal half-way keeps what was delivered.** Reviews are written to the dataset page by page. If Indeed stops answering on page 40, the first 39 pages are yours and charged, and the status row says `partial`. The same holds when you abort a run or it reaches your maximum cost.
- **A name several companies share goes to Indeed's own pick.** `Meta` is a small company of that name; the Facebook parent is `Meta-dd1502f2` (which is where `Facebook` resolves). The `company`, `company_name` and review count on the free company row show what you got — pass the `/cmp/` URL when it has to be exact.
- **`onlyNewReviews` starts from a baseline.** The first run delivers the newest `maxReviewsPerCompany` reviews and everything older is history, not news: it is never delivered by a later run. A run also delivers at most `maxReviewsPerCompany` new reviews, so keep that number above what the company receives between two runs.
- **A sub-rating of `0` means "not rated", not zero stars.** Indeed writes `0` when a reviewer skipped a category. Those become `null` here, so an average is not silently dragged to the floor.
- **Counts differ by domain.** `review_count` is what Indeed holds worldwide; `found_review_count` is what the domain you read actually lists. They are supposed to differ.
- **A handful of Indeed hosts are not country domains.** `my.indeed.com` is the account subdomain and serves a sign-in page, so Malaysia is not in the list; a few other hosts have no company section at all. Only verified domains are offered.
- **Dates in a language we have not met.** Every domain in the list was checked, and the raw string is always kept in `review_date_text`; if a format ever changes, `review_date` becomes null rather than wrong, and `sinceDate` keeps such a review rather than silently dropping it.
- **Reviews are moderated by Indeed.** Only approved reviews appear on the page, so this is Indeed's published corpus, not every review ever submitted.

## FAQ

### How do I find a company's Indeed slug?

You do not need it: type the company's name. Indeed itself redirects `Home Depot` to `The-Home-Depot`, `Amazon` to `Amazon.com` and `Ernst & Young` to `Ey`, and the rows carry the slug it chose. If you want to be exact — some names are shared by several companies — open the company on Indeed and paste its URL, or just the part after `/cmp/`. Either way you get Indeed reviews by company rather than by keyword.

### Can I get all Indeed reviews for a company, not just the US ones?

Yes: set `countries` to `["all"]` and `maxReviewsPerCompany` to `0`. That reads `www.indeed.com` with Indeed's worldwide filter and returns essentially the complete corpus in one walk.

### How do I export Indeed reviews to CSV?

Run the actor, open the run's Storage tab and choose CSV, or add `&format=csv` to the dataset API call as in the curl example above. Every review row carries the same fields, so the Indeed reviews CSV has stable columns and can be loaded straight into a spreadsheet or a warehouse.

### Can I get only the negative reviews?

Set `sort` to `rating_asc` and `maxRating` to `2`. The lowest-rated reviews arrive first and the walk stops at the first page above the ceiling, so you pay only for the complaints.

### Does it return the employer's replies?

Yes — `employer_reply` and `employer_reply_date`, when the company has responded. Indeed employer replies are missing from most reviews at most companies, which is itself a useful metric: the share of one- and two-star reviews you have answered.

### How do I monitor new reviews every day?

Schedule the actor with `onlyNewReviews: true`. The first run is the baseline; every later run stops at the first page it already knows and delivers only the reviews written since, so a quiet day costs one request per company and no money. Use minRating or maxRating with it to be told about new complaints only.

### Is there an Indeed employee reviews API?

Not a public one. This actor is the practical substitute, and it reads Indeed reviews without an API key of any kind: a stable JSON contract over the public company pages, with paging, retries and the wrap-around trap handled for you.

### What happens if a company has no reviews?

You get a `status` row with `no_reviews` and `found_review_count: 0`, plus the free company row, and you are charged nothing.

### Do I need proxies or my own API key?

No key and nothing to configure. Proxies come from Apify Proxy: the actor finds the datacenter IPs Indeed serves, and uses residential ones by itself only when your account has none that are served. No browser is involved.

### How fast is it?

Typically about 1,200 reviews per minute at the default two sessions: one page — twenty reviews — per second per session, with the pages of a long walk requested ahead so a slow download does not hold up the next one. Measured on the platform on 2,000-review walks of Walmart: 1,250 a minute with two fast proxy sessions, 760 when Indeed served only one of the account's IPs, 320 when the served IPs were slow ones. For an employer with more than 50,000 reviews raise `sessions` to 4-8 and the run timeout; whatever was delivered before a timeout or an abort is kept. Raise `sessions` for bulk company reviews across many employers as well.

### Can I scrape Indeed reviews for many companies at once?

Yes. Put every name or slug in `companies`; they are processed in parallel across your sessions, duplicates are recognised, and the per-company cap applies to each one independently.

## Related scrapers

Indeed is the employee's view of a company. These read the customer's, with the same row discipline and the same pay-per-delivered-row billing:

- [Trustpilot Reviews Scraper](https://apify.com/kestrel/trustpilot-reviews-scraper) — the same company as its customers see it: reviews and TrustScore from Trustpilot, past the 200-review wall an anonymous reader normally hits.
- [App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper) — Apple App Store reviews of the company's apps across every country storefront in one run, with rating filters that run before billing.
- [Google Play Reviews Scraper](https://apify.com/kestrel/google-play-reviews-scraper) — the Android half: Play Store reviews per language and country, matching columns.
- [Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper) — customer reviews and ratings of the company's products by ASIN, when it sells on Amazon.
- [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) — guest reviews with six sub-ratings and the management response, when the employer is a hotel or a chain and its customers talk there instead.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
