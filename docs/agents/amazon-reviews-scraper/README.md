# Amazon Reviews Scraper — Customer Reviews, Product Reviews

An **amazon reviews scraper** for product-page samples of **amazon customer reviews** and **amazon product reviews**. **UK examples are verified; current US review pages require sign-in.** Available rows contain rating, text, reviewer, country, date, Verified Purchase and helpful votes; an optional product row carries **amazon ratings** and their count. This is a public-page sample, not the full review history.

## Current availability — 2026-11-07

Two distinct UK product URLs returned real review text and IDs in owner validation, with matching review charges. The first-call form uses a verified UK URL and a three-review limit. **US access has not recovered:** current desktop and mobile US tests explicitly say “Sign in to see customer reviews” and contain no review records. Do not use this Actor for a working US review fetch. Other configured marketplaces are not newly verified by these checks.

```json
{"asins":["https://www.amazon.co.uk/dp/B09G9FPHY6"],"maxReviewsPerProduct":3,"requireText":true}
```

The URL selects `co.uk` automatically. API defaults are unchanged: bare ASINs still use `domain: "com"`, `maxReviewsPerProduct: 0` means all source-visible reviews, and `includeProductRow: true` adds a $0.003 product row. The form's three-review sample costs at most $0.015 for reviews plus that optional product row. A blocked page is not a successful empty result and is not billed. The platform maintenance notice may remain while its checks catch up; these results establish partial regional availability, not US recovery.

When the source exposes public reviews, it turns **amazon product reviews** into **amazon review data** you can query, with **amazon ratings** attached to available product rows. Give it ASINs or product URLs. No login, no **amazon review api** key, no browser. Filters run before billing. Read the **Scope** section: the Actor reads source-visible product-page samples, not a full archive or a guaranteed review count.

Last verified working: 2026-11-07 (UK examples only).

## Amazon 商品评论与买家评价：中文调用与语言设置

使用 ASIN 或商品 URL 获取评论、星级、认证购买标记和有用票数。英国示例已验证；当前美国测试要求登录，无法获取评论。只交付来源公开返回的评论，不能保证完整历史评论。

domain 选择 Amazon 市场，例如 com、de、co.jp。没有中国大陆 cn 市场，也没有评论语言筛选或自动翻译；中文用户应选择目标商品实际销售的受支持市场。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "asins": [
    "https://www.amazon.co.uk/dp/B09G9FPHY6"
  ],
  "requireText": true,
  "maxReviewsPerProduct": 1,
  "sessions": 1,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyGroups": [
      "RESIDENTIAL"
    ]
  }
}
```

Amazon Bewertungen / avis Amazon / opiniones Amazon：市场决定可见评论，保留原文。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Amazon reviews scraper for AI agents: which input answers which request?

**Use it for** the source-visible product-page sample and available rating summary. UK examples are verified; current US review requests are blocked. The input recognizes 20 marketplace codes, with availability dependent on the source. Suitable uses include: complaint feeds, verified-purchase samples, sentiment and voice-of-customer corpora, competitor review tracking, catalogue-wide rating sweeps.

**Do not use it for** a product's full review archive (this Actor only reads the public product-page sample and does not log in), review photos or videos, the "Customers say" AI summary, reviews filtered by date or keyword, or prices (`price` on the product row is best-effort; use the [Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper)).

| User request | Input |
| --- | --- |
| "A small verified UK review sample" | `{"asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6"], "maxReviewsPerProduct": 3, "requireText": true}` |
| "Negative reviews / complaints for these products" | `{"asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6", "https://www.amazon.co.uk/dp/B0F23KT34P"], "minRating": 2, "requireText": true}` |
| "Only verified purchase reviews" | `{"asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6"], "verifiedOnly": true}` |
| "Reviews of this amazon.de product" | `{"asins": ["https://www.amazon.de/dp/B09B8V1LZ3"]}` or `{"asins": ["B09B8V1LZ3"], "domain": "de"}` |
| "Review text for sentiment analysis" | `{"asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6"], "requireText": true}` |
| "Rating and review count for 500 ASINs, as little review text as possible" | `{"asins": [...], "minRating": 1, "requireText": true}` — the product rows carry `rating` and `ratings_count`; only one-star reviews with text are delivered as review rows |
| "At most 5 reviews per product" | `{"asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6"], "maxReviewsPerProduct": 5}` |
| "Review rows only, no product rows" | `{"asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6"], "includeProductRow": false}` |
| "Only new reviews since yesterday" / "track new reviews" | not built in: schedule the same input and compare `review_id` with the previous dataset; every run re-reads the visible product-page sample |
| "Rating and 5-to-1 histogram only, no review text" | `{"asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6"], "maxReviewsPerProduct": 1}` — the product row (free of review text, $0.003) plus one review row; review rows cannot be switched off entirely |

**One `review` row** ($0.005): `rating` (1–5), `title` (often null), `text`, `author`, `country`, `date_text`, `verified`, `helpful_votes`, `variant`, `review_id`, `url`, `asin`, `domain`, `product_title`. **One `product` row** ($0.003, `includeProductRow` on by default): `rating`, `ratings_count`, `reviews_visible`, `5_star_pct` … `1_star_pct` when shown, `title`, `brand`, `availability`, `image`, `features`, `price` (best-effort). **One `status` row per target** (free): `status` is `ok`, `no_reviews` or `error`, with `reviews`, `filtered`, `duplicates` and `error`.

**Empty results**: a product with no visible reviews delivers its product row and a `no_reviews` status row, and no review row is charged. An ASIN that is not an ASIN, an unknown marketplace or an empty list ends the run green with `Input problem — …` on the run card and nothing charged. When every product is blocked or fails, the run fails loudly so you see it. No start fee; the run stops at the `maxTotalChargeUsd` you set when starting it.

## What does the Amazon reviews scraper do?

You give it products. It gives you their **amazon product reviews** as rows you can sort, filter and export.

- **`review` rows** — `rating` (1–5), `title`, `text`, `author`, `country`, `date_text`, `verified`, `helpful_votes`, `variant`, and a permalink to the review.
- **`product` rows** — `title`, `brand`, `rating`, `ratings_count`, `reviews_visible`, `availability`, `image`, `features`, `price` and `currency`.
- **`status` rows** — free: per product, what was delivered, how many were filtered, and why anything failed.

Amazon mixes **international reviews** into a product page, so `country` lets you separate domestic from imported opinion — a UK page returned reviews from three countries in testing.

## Amazon reviews by ASIN, URL or marketplace

- **`asins`** takes either form: a bare **amazon asin** like `B0BSHF7WHW`, or a full product URL from any marketplace.
- A URL's marketplace is used automatically. `https://www.amazon.co.uk/dp/B09G9FPHY6` is scraped from the UK site without changing `domain`; the currency field follows the price Amazon actually displays.
- **`domain`** sets the marketplace for bare ASINs. The parser recognizes twenty marketplace codes; this does not guarantee current anonymous review access on each: `com`, `co.uk`, `de`, `fr`, `it`, `es`, `ca`, `com.au`, `co.jp`, `in`, `com.mx`, `com.br`, `nl`, `se`, `pl`, `sa`, `ae`, `sg`, `com.tr`, `com.be`.

The same ASIN on two marketplaces is two products, because the reviews genuinely differ. The non-English marketplaces call them Bewertungen or Rezensionen (amazon.de), avis (amazon.fr), opiniones (amazon.es), recensioni (amazon.it), レビュー (amazon.co.jp) and avaliações (amazon.com.br); the matching domain code selects the requested marketplace, while current public review availability must be checked; `country` says where an available review was written. An ASIN and its own URL are one product, fetched and billed once — so **amazon reviews by marketplace** comparisons are explicit rather than accidental.

## Amazon negative reviews without paying for the five-star ones

Three filters run **before** billing:

- **`minRating`** keeps only reviews at or below a star rating. `2` is the classic complaints feed.
- **`verifiedOnly`** keeps only **verified purchase reviews**, which is the fastest way to strip noise.
- **`requireText`** drops rating-only reviews with no written body.

Filtered rows are never charged. In a verified run, a product with 8 visible reviews delivered **0 rows** under `minRating: 3` — all its reviews were above the ceiling — and the run cost a fraction of a cent instead of billing for eight rows nobody asked for. That is what makes **amazon negative reviews** monitoring across a catalogue affordable.

## Amazon review data for sellers, brands and analysts

- **Rating monitoring.** Schedule a run over your ASINs and your competitors' and track `rating` and `ratings_count` over time — every row is timestamped. There is no only-new review mode: each run re-reads the visible sample, so compare `review_id` between runs.
- **Amazon competitor reviews.** Pull the visible review set for a rival's catalogue and read what their customers actually complain about.
- **Voice of customer.** Rated, dated review text with the reviewer's country and the variation bought is the right shape for **amazon review sentiment analysis** or topic modelling.
- **Listing audits.** `verified` and `helpful_votes` separate genuine purchase feedback from noise.
- **Amazon seller research.** `ratings_count` and `rating` on the product row give you **amazon product rating data** for a whole ASIN list in one run.

## Input

| Field | What it does |
| --- | --- |
| `asins` | ASINs (`B0BSHF7WHW`) or product URLs from any marketplace. A URL's marketplace is used automatically. |
| `domain` | Marketplace for bare ASINs. Twenty supported, listed above. |
| `minRating` | `0` = everything. `1`–`5` = only reviews at or **below** that rating (`2` = the complaints feed). Never charged for what it drops. |
| `verifiedOnly` | Keep only Verified Purchase reviews. |
| `requireText` | Drop rating-only reviews with no written body. |
| `maxReviewsPerProduct` | `0` = every source-visible review; the form prefills `3` for a small UK sample. `N` = the first N, applied after the filters. |
| `includeProductRow` | `true` (default) = one product row per ASIN at $0.003 with `rating`, `ratings_count`, `reviews_visible` and the star histogram when shown. `false` = review rows only. |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. Required — Amazon captchas datacentre traffic that is not rotated. Datacentre is a fine starting point: the run escalates to residential by itself when Amazon pushes back. |

### Example: a complaints feed across a catalogue

```json
{ "asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6", "https://www.amazon.co.uk/dp/B0F23KT34P"], "minRating": 2, "requireText": true, "verifiedOnly": true }
```

### Example: two verified UK products

```json
{ "asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6", "https://www.amazon.co.uk/dp/B0F23KT34P"], "maxReviewsPerProduct": 0 }
```

### Example: rating summaries with one-star text filtering

```json
{ "asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6", "https://www.amazon.co.uk/dp/B0F23KT34P"], "maxReviewsPerProduct": 0, "minRating": 1, "requireText": true }
```

## Output

Historical response shapes are shown below. Their US sample values illustrate the schema and do not imply current US availability; use the verified UK first-call input above.

```json
{
  "type": "review", "asin": "B0BSHF7WHW", "domain": "com", "marketplace": "US",
  "product_title": "Apple 2023 MacBook Pro Laptop", "review_id": "RCA7TI5EBH5VK",
  "rating": 5.0, "title": null,
  "text": "I upgraded from the i9 Intel MacBook Pro from 2019, and this laptop seriously blows that away.",
  "author": "Michael M", "country": "the United States", "date_text": "July 22, 2023",
  "verified": true, "helpful_votes": 65, "variant": null,
  "url": "https://www.amazon.com/gp/customer-reviews/RCA7TI5EBH5VK"
}
```

The `product` row carries the rating summary:

```json
{
  "type": "product", "asin": "B0BSHF7WHW", "domain": "com", "marketplace": "US",
  "title": "Apple 2023 MacBook Pro Laptop", "brand": null,
  "rating": 4.7, "ratings_count": 387, "reviews_visible": 13,
  "price": null, "price_display": null, "currency": "USD",
  "availability": null, "image": "https://m.media-amazon.com/images/I/example.jpg",
  "features": ["Apple M2 Pro chip"], "url": "https://www.amazon.com/dp/B0BSHF7WHW?th=1&psc=1"
}
```

`status` rows carry `target`, `asin`, `domain`, `status`, `reviews`, `filtered`, `duplicates`, `error` and `fetched_at`.

## How much does it cost?

Pay per event: one per **delivered** review row and one per product row. Free: `status` rows, every review removed by a filter, and failed products. A genuine accessible product with no reviews has no review charge; its optional product row is still charged if delivered. An ASIN and its URL are one product, fetched and billed once per run.

Verified runs behind this listing cost $0.0002–$0.0024 each in platform compute. Exact per-row pricing is on this page's pricing tab.

## Amazon reviews scraper in Python, JavaScript, curl, n8n, Make or an AI agent

In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-reviews-scraper").call(run_input={
    "asins": ["https://www.amazon.co.uk/dp/B09G9FPHY6"], "maxReviewsPerProduct": 3, "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["country"], row["text"][:80])
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-reviews-scraper').call({
    asins: ['https://www.amazon.co.uk/dp/B09G9FPHY6'], maxReviewsPerProduct: 3, requireText: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'product').map((p) => [p.marketplace, p.rating, p.ratings_count]));
```

With **curl**, synchronously:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-reviews-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"asins":["https://www.amazon.co.uk/dp/B09G9FPHY6"],"maxReviewsPerProduct":3,"requireText":true}'
```

For **n8n**, **Make** and Zapier, add the actor as a step through Apify's integration and map `rating`, `text` and `date_text` into an alert — "new one-star review on any of my ASINs" is two nodes. For **AI agents**, the actor is callable over Apify's MCP server. To get **amazon reviews csv**, run it and use the dataset's Export button, or append `?format=csv` to the dataset items API.

## Scope — read this before you buy

This reads the reviews Amazon publishes on the **public product page**, whose review count varies by product and marketplace, ordered by Amazon's own mix of recent and most-helpful. Amazon requires a signed-in session for its full review archive, and this actor deliberately does not attempt that — no account sharing, no cookie injection, no session resale. If you need every review a product has ever had, this is not the tool, and no honest listing should tell you otherwise.

When the page is accessible and exposes these fields, the optional product row includes `rating` and `ratings_count` alongside the visible sample, which is enough for rating trends, complaint detection and competitor tracking across a large catalogue.

Likewise, **`price` is best-effort**. Amazon frequently withholds price markup from unauthenticated clients — on a 1.8 MB product page in testing there was no price element at all. When Amazon serves one, you get it; treat the field as a bonus, not a price-tracking feature. If you want prices and rank, use the companion Amazon Search & Best Sellers actor, which reads them from result pages where Amazon does render them.

## Is it legal to scrape Amazon reviews?

This reads publicly visible product pages with no login and no account. Reviews are published deliberately for anyone to read, and *hiQ v. LinkedIn* is the usual US reference point for scraping public data.

Two caveats worth taking seriously. Reviews contain **personal data** — a display name, a country, someone's words — so under GDPR you are a controller once you store them: have a lawful basis, retain only as long as you need, and do not republish reviewer identities. This actor exposes no email, phone or full legal name, and has no input that would produce one. Separately, Amazon's Conditions of Use discourage automated access, making this a terms question rather than a criminal one, with the risk on whoever operates the run. None of this is legal advice; if your use is commercial or large, ask a lawyer.

## Limits and honest notes

- **A variable product-page sample**, as covered in Scope; no minimum or complete history is promised. `reviews_visible` on the product row tells you exactly how many were on the page.
- **`title` is often null.** The compact review blocks Amazon renders on product pages frequently omit a headline; the body is always there.
- **Amazon serves a captcha to repeat callers.** The run detects it and rotates to a fresh IP rather than parsing the captcha page as an empty product.
- **Cheap proxies first, residential only when Amazon pushes back.** A run starts on the proxies you chose — datacentre is the cheapest — and rotates to a fresh IP on a captcha or a 503. When the same page is refused twice in a row that is the IP range being blocked, not the page, so the run stops trusting that pool: its sessions re-open on a residential proxy and stay there for the rest of the run. Nothing to configure, no run has to fail to teach it, and a run that is never refused never leaves the cheap pool — so a run costs the least that still succeeds. The run's SUMMARY reports it as `http.escalated`.
- **`country` is where the review was written**, not where the reviewer lives — Amazon phrases it "Reviewed in …".
- **Rating is a float 1–5.** Amazon renders "5.0 out of 5 stars"; the row carries `5.0`.
- **`brand` and `availability` are frequently null** on pages where Amazon does not render them.

## FAQ

### Does it need an Amazon API key or login?

No. There is no public **amazon review api** for product reviews, and Amazon's Product Advertising API requires an affiliate account with sales requirements and does not return review text. This uses neither — it reads the public product page.

### Can I download Amazon reviews as CSV or Excel?

Yes. Every run writes an Apify dataset, exportable to CSV, Excel, JSON or XML from the Console or over the API with `?format=csv`. That is the quick path to **download amazon reviews** for an ASIN list.

### How do I get only Amazon negative reviews?

Set `minRating` to your ceiling (`2` for one- and two-star) and add `requireText: true` so you only pay for reviews with actual words. `verifiedOnly: true` strips unverified noise. Everything above the ceiling is dropped **before** billing.

### How many reviews will I get per product?

Only the reviews currently visible on the product page; the number can vary and may be zero. The first-call example caps delivery at three. No minimum count or full history is promised. `reviews_visible` on each product row reports the exact number.

### Can I scrape Amazon reviews by ASIN in bulk?

Yes. Put as many ASINs in `asins` as you like; each is fetched once and billed once. **Bulk amazon reviews** are billed per delivered row, so cost scales with data rather than time, and the filters cut it directly.

### Which marketplaces are supported?

Twenty, listed in the input section. A product URL selects its own marketplace automatically; bare ASINs use `domain`. The same ASIN in two marketplaces is treated as two products because the reviews and ratings genuinely differ.

### Does it return prices?

Best-effort only — see Scope. Amazon commonly withholds price markup from unauthenticated clients. For prices and keyword rank, use the companion Amazon Search & Best Sellers actor.

### Can I get the star-rating breakdown?

An accessible product row carries `rating` and `ratings_count` when those fields are present in the source. The 5/4/3/2/1 percentage split is included when Amazon renders it on the page, which is not always.

### Can I scrape Amazon reviews without an API?

That is what this is — **amazon reviews without api** access, no key to apply for and no affiliate account. You call an Apify actor and read rows back.

### Is there a free tier?

Products with no visible reviews, filtered reviews, `status` rows and failed products are always free, so a run that finds nothing has no event charge; compute is included in the event price. Apify's free plan includes monthly credit you can spend here.

## Product review data that keeps its structure

Three fields decide whether a review corpus is analysable or just text, and this actor keeps all three separate.

- **Rating apart from words.** `rating` and `text` are distinct, so a four-star review with an angry paragraph reads differently from a four-star review saying "fine". Weight them independently.
- **Verified apart from unverified.** `verified` is a boolean on every row. Filtering to Verified Purchase before analysis removes a large share of the noise that makes **product review data** unreliable.
- **Helpfulness as a signal.** `helpful_votes` is the crowd's own weighting. Sorting by it surfaces the reviews that actually shape a buying decision, which is rarely the newest one.

Add `country` and `variant` and you can answer questions the Amazon interface will not: does the 128 GB variant generate more complaints than the 256, and are the complaints coming from one market?

### Amazon ratings across a catalogue

Every product row carries `rating` and `ratings_count`, so a single run over an ASIN list gives you **amazon ratings** for the whole catalogue in one table. Schedule it weekly and `ratings_count` becomes review velocity — how fast each product is accumulating opinion — while `rating` shows whether that opinion is improving or slipping.

Because `includeProductRow` can be left on with `maxReviewsPerProduct: 0` and a strict filter, you can run a cheap catalogue-wide rating sweep that delivers product rows and almost no review rows.

### Comparing marketplaces properly

The same ASIN often sells in a dozen Amazon marketplaces, and its reception differs by market. Use full product URLs for the marketplaces you intend to compare, and check each status row before combining results. Only the UK examples were newly verified; current US review requests are blocked, so do not assume a US/UK comparison will return both sides.

That is why the run treats an ASIN plus a marketplace as the identity, rather than the ASIN alone. Mixing a bare ASIN with its own URL still collapses to one product — the de-duplication is on identity, not on string.

### What this deliberately does not do

No login, no cookie injection, no session resale, and no attempt at Amazon's signed-in review archive. No seller contact details, no buyer emails. The public product page is the boundary, and there is no input that crosses it.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Negative Reviews by ASIN (1-3 Stars)](https://apify.com/kestrel/amazon-reviews-scraper/examples/amazon-negative-reviews-by-asin)
- [Verified Purchase Reviews Only](https://apify.com/kestrel/amazon-reviews-scraper/examples/verified-purchase-reviews-only)
- [Reviews by Marketplace: UK, DE, FR](https://apify.com/kestrel/amazon-reviews-scraper/examples/amazon-reviews-by-marketplace)
- [Voice of Customer Across 25 ASINs](https://apify.com/kestrel/amazon-reviews-scraper/examples/voice-of-customer-across-25-asins)
- [Product Reviews at One Star Only](https://apify.com/kestrel/amazon-reviews-scraper/examples/amazon-product-reviews-at-one-star)
- [Customer Reviews on .de](https://apify.com/kestrel/amazon-reviews-scraper/examples/amazon-customer-reviews-on-amazon-de)
- [Ratings and Reviews on .co.jp](https://apify.com/kestrel/amazon-reviews-scraper/examples/amazon-ratings-and-reviews-on-amazon-co-jp)
- [Review Monitoring for Your Own ASINs](https://apify.com/kestrel/amazon-reviews-scraper/examples/review-monitoring-for-your-own-asins)
- [Reviews Without API Approval](https://apify.com/kestrel/amazon-reviews-scraper/examples/amazon-reviews-without-api-approval)
- [Product Rating Data by ASIN](https://apify.com/kestrel/amazon-reviews-scraper/examples/amazon-product-rating-data-by-asin)
- [Scrape Reviews on .co.uk](https://apify.com/kestrel/amazon-reviews-scraper/examples/scrape-amazon-reviews-on-amazon-co-uk)

## Related scrapers

Reviews tell you what customers said. Search and charts tell you what ranks and what sells — feed the ASINs from one into the other:

- **[AliExpress Reviews Scraper](https://apify.com/kestrel/aliexpress-reviews-scraper)** — buyer feedback with photos, variant chosen and buyer country, for product research and dropshipping.
- **[Trustpilot Reviews Scraper](https://apify.com/kestrel/trustpilot-reviews-scraper)** — company reviews and TrustScore from Trustpilot, past the 200-review wall an anonymous reader normally hits.
- **[Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper)** — the product itself: buybox price, list price, stock, gallery, bullets and details, without the review rows.
- **[App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper)** — Apple App Store reviews for any app across every storefront in one run, with the same pre-billing rating filters.
- **[Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper)** — the Top 100 of any category by best seller rank; its `asin` column is the natural input for a reviews run.
- **[Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper)** — Amazon search results, Best Sellers and keyword rank.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site’s rate for a stay.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
