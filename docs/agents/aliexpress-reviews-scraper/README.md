# AliExpress Reviews Scraper & API — product reviews, ratings, buyer photos and sentiment

This AliExpress reviews scraper turns any product page into a clean table of AliExpress product reviews: the 1-5 star rating, the buyer's own words plus a machine translation into the language you pick, the buyer's country, the exact SKU variant the review is about, the photos they uploaded, the shipping method the order used, the follow-up review they came back and wrote weeks later, and the helpful votes other shoppers gave it. Give it product URLs or item ids and it reads the same public AliExpress feedback endpoint the product page's own review widget calls — no API key, no login, no cookies, no headless browser. It is built as an AliExpress product research tool for dropshipping product validation: buyer reviews and buyer photos are how you tell a product worth listing from one that will drown you in refunds, and this is the cheapest way to pull them in bulk.

Version 1.1 adds what no other AliExpress review scraper on Apify has in one place: a **date filter** (`sinceDate`: reviews from the last 30 days), a **keyword filter**, a **monitoring mode that delivers and bills only new reviews** on every scheduled run, **free sentiment analysis, topic tags and a per-product insights row**, the praise-and-complaint **topics AliExpress itself mines** from the texts, **sixteen translation languages**, and an option to hide buyer details. Everything a 1.0 run sent and received works exactly as before — every addition is optional and off by default — and the price has not changed.

Last verified working: 2026-09-20.

## Current price for API callers

The active price is **$0.003 per review row**, effective since **2026-10-27**: 1,000 delivered rows cost $3. Set `maxTotalChargeUsd` in Apify run options for a spending cap. Proxy and compute are included in this event price. This documentation correction changes no prices.

中文：当前每条已交付记录为 $0.003，自 2026-10-27 起生效。1,000 条记录费用为 $3，代理与计算费用已包含。请在 Apify 运行选项中设置费用上限。

## AliExpress 速卖通商品评论、买家评价与图片：中文调用与语言设置

按商品 URL 或 ID 获取评分、买家反馈、图片和 SKU。可按星级、日期、关键词筛选。

language 使用枚举中的翻译代码，如 en_US、es_ES、pt_BR、ja_JP；不支持中文翻译代码。text 保留原文，text_translated 为来源翻译。analyzeReviews=true 时保留 en_US。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "productUrls": [
    "https://www.aliexpress.com/item/1005006255429323.html"
  ],
  "maxReviewsPerProduct": 1,
  "reviewsFilter": "all",
  "language": "en_US",
  "sessions": 1
}
```

Opiniones / avaliações / отзывы：分析时区分原文与翻译，翻译缺失不应补造。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## AliExpress scraper for AI agents: which input answers which request?

Use this actor when the request names an AliExpress product (URL or item id) and wants its buyer reviews: star ratings, review text with a translation, buyer country, SKU variant, buyer photos, follow-up reviews, or a product's rating histogram and review topics. Do not use it to search AliExpress for products by keyword, to read product prices, stock or seller data, or for Temu, Alibaba or Amazon reviews: none of that exists here. A keyword in `keywords` filters review text; it does not find products.

| user request | input JSON |
|---|---|
| reviews of this product | `{"productUrls": ["https://www.aliexpress.com/item/1005006255429323.html"]}` (every review, $0.003 each; add `"maxReviewsPerProduct": 200` to cap) |
| by item id | `{"productIds": ["1005006255429323"]}` |
| negative reviews / complaints | `{"productIds": ["1005006255429323"], "maxRating": 2, "requireText": true, "sort": "lowest_rating"}` |
| reviews from the last 30 days | `{"productIds": ["1005006255429323"], "sinceDate": "30 days"}` |
| only new reviews each day (monitoring) | `{"productIds": ["1005006255429323"], "onlyNewReviews": true}` on a daily schedule |
| reviews mentioning battery or broke | `{"productIds": ["1005006255429323"], "keywords": ["battery", "broke"]}` |
| reviews with photos only | `{"productIds": ["1005006255429323"], "reviewsFilter": "with_photos"}` |
| reviews from US buyers | `{"productIds": ["1005006255429323"], "countries": ["US"]}` |
| reviews translated into Spanish | `{"productIds": ["1005006255429323"], "language": "es_ES"}` |
| sentiment, top complaints and praise | `{"productIds": ["1005006255429323"], "analyzeReviews": true}` (free: sentiment columns plus one insights row per product) |
| rating histogram only, cheapest | `{"productIds": ["1005006255429323"], "maxReviewsPerProduct": 1}` (one billed review; the product row is free) |

Output rows share one dataset and are told apart by `type`. A `review` row (billed, $0.003 each) carries `review_id`, `product_id`, `rating`, `text`, `text_translated`, `language`, `review_date`, `buyer_name`, `buyer_country`, `sku_info`, `images`, `logistics`, `helpful_votes`, `attributes`, `follow_up_text`, `follow_up_translated`; with `analyzeReviews` also `sentiment`, `sentiment_score`, `topics`, `rating_text_mismatch`. A `product` row (free, one per product) carries the title, image, average rating, the 1-5 star histogram, the positive/neutral/negative split and `review_topics`. A `status` row (free, one per target) says `ok`, `no_reviews`, `not_found` or `error`, with `reviews`, `filtered` and `already_seen`. A product with no reviews is a free `no_reviews` row and an unknown item id a free `not_found` row, never an empty success; bad input ends the run with the reason on the run card and nothing charged.

## What does the AliExpress Reviews Scraper do?

You hand it a list of products. For each one it walks every review page AliExpress will serve, drops the duplicates AliExpress serves twice, applies your filters, and writes one dataset row per review. Alongside the reviews it can emit a free product row carrying the whole rating breakdown — the average, the 5/4/3/2/1-star histogram, the positive/neutral/negative split, how many reviews carry photos, how many carry a follow-up, and the structured attributes buyers were asked to rate the item on.

Nothing here needs a browser. The endpoint answers plain HTTP requests from datacenter IP ranges, so a run is fast and cheap: a 2,836-review best-seller reads in about 15 requests, not 142.

Three row types share one dataset, and you can filter them apart in the **Output** tab with the built-in views:

| Row | What it is | Charged |
| --- | --- | --- |
| `review` | One buyer review | Yes |
| `product` | The product's title, image and rating statistics | Free |
| `status` | One per target: what happened, how many rows, why not | Free |
| `insights` | Only with **Analyze reviews** on — one per product: sentiment split, top complaints and praise, ratings by variant, country and month | Free |

## AliExpress reviews for product research and dropshipping

If you sell online, the review list is the product. A 4.6 average hides the fact that eleven buyers in a row said the cable frays; a 4.2 average with 313 photo reviews and a hundred people writing "arrived in 9 days, exactly as described" is a better bet than either. This scraper gives you the raw material for that judgement in bulk:

- **Photos.** `images` and `follow_up_images` are the buyer's own pictures. AliExpress buyer photos show what the product actually looks like out of the bag, which is very often not what the listing photos show — for dropshipping research, AliExpress review photos are worth more than the whole listing.
- **Follow-up reviews.** AliExpress lets a buyer return weeks later and add to their review. `follow_up_text` and `follow_up_days` are the closest thing the site has to a durability signal: a product with hundreds of positive first reviews and a wall of angry follow-ups at day 45 is a returns problem.
- **Variant-level truth.** `sku_info` tells you which colour, size or plug type the review is about, so you can find out that the black one is fine and the white one arrives scratched.
- **Shipping reality.** `logistics` is the shipping method the order actually used, which lets you separate "the product is bad" from "the shipping line is slow".
- **Buyer country.** `buyer_country` lets you read only the reviews from the market you sell into. Delivery complaints do not transfer between countries.

Because the output is one flat row per review, bulk AliExpress reviews drop straight into whatever you already use: pipe `text` and `rating` into an AliExpress review sentiment model, group `attributes` by SKU, or join `sku_info` against your own catalogue.

## What data does each AliExpress review row contain?

```json
{
  "type": "review",
  "review_id": "60094105248269979",
  "product_id": "1005006255429323",
  "product_title": "Original Lenovo LP40 wireless headphones TWS Bluetooth Earphones",
  "product_url": "https://www.aliexpress.com/item/1005006255429323.html",
  "rating": 5,
  "rating_100": 100,
  "review_date": "2025-11-29",
  "review_date_raw": "29 Nov 2025",
  "text": "Fast delivery! Package came within estimate delivery. The headphones came in perfect condition, and the sound and connection is very nice.",
  "text_translated": "Fast delivery! Package came within estimate delivery.",
  "language": "en",
  "buyer_name": "AliExpress Shopper",
  "buyer_country": "US",
  "buyer_anonymous": true,
  "sku_id": "12000036486711239",
  "sku_info": "Color:LP40 white",
  "images": ["https://ae-pic-a1.aliexpress-media.com/kf/Ab1b4386f35a14c28b499f08897b6fea0y.jpg"],
  "image_count": 1,
  "logistics": "AliExpress Selection Standard",
  "helpful_votes": 0,
  "unhelpful_votes": 0,
  "attributes": {"Quality of sound": "Fast", "Durability": "Fast", "User Friendly": "Good"},
  "follow_up_text": null,
  "follow_up_days": null,
  "featured": true,
  "ai_generated": false
}
```

Every review row also carries `target` (the URL or id you asked for), `buyer_gender`, `buyer_avatar`, `follow_up_translated`, `follow_up_date`, `follow_up_images` and `fetched_at`.

## Product rows: the whole rating breakdown, free

Set **Include a product row** (`includeProductRow`, on by default) and every product also gets one free row:

```json
{
  "type": "product",
  "product_id": "1005006255429323",
  "product_title": "Original Lenovo LP40 wireless headphones",
  "product_image": "https://ae-pic-a1.aliexpress-media.com/kf/Haa1bfb60935a4a3ca5e24c9ef3bcd163R.jpg",
  "product_url": "https://www.aliexpress.com/item/1005006255429323.html",
  "rating": 4.2,
  "rating_percent": 84.9,
  "reviews_total": 2836,
  "reviews_fetched": 100,
  "five_star": 1888, "four_star": 380, "three_star": 207, "two_star": 106, "one_star": 266,
  "positive_count": 2268, "neutral_count": 207, "negative_count": 372,
  "positive_rate": 79.7, "negative_rate": 13.0,
  "with_photos_count": 313,
  "with_follow_up_count": 82,
  "same_country_count": 257,
  "product_type": "ORDINARY",
  "review_attributes": [{"attribute": "Durability : Fits ok", "reviews": 1493, "value_id": 1500325947}],
  "review_topics": [
    {"topic": "good sound", "sentiment": "positive", "reviews": 112},
    {"topic": "poor sound quality", "sentiment": "negative", "reviews": 107},
    {"topic": "fast delivery", "sentiment": "positive", "reviews": 86},
    {"topic": "good value for price", "sentiment": "positive", "reviews": 83}
  ]
}
```

`review_attributes` is the part most people miss. It is the structured attribute panel AliExpress builds from every review of the item, with the count behind each phrase — a one-row summary of what 1,493 buyers said about durability, before you read a single sentence.

`review_topics` (new in 1.1) is the other half: the topics AliExpress's own text mining pulls out of the review texts, each tagged positive or negative with the number of reviews behind it. "good sound" from 112 buyers next to "poor sound quality" from 107 tells you in one row that this product is a coin flip — which a 4.2 average never will. It rides on the same answer as the reviews, so it costs nothing and no extra request.

## Review filters that run before you are charged

Every filter runs **before billing**. A review the filters drop is never delivered and never charged, so a complaints-only run on a 3,000-review product costs you the handful of rows you keep.

Three of them are applied by AliExpress itself, through **Server-side review filter** (`reviewsFilter`), so the pages you do not want are never fetched at all:

| `reviewsFilter` | What AliExpress returns |
| --- | --- |
| `all` | Every review (default) |
| `with_photos` | Only reviews carrying buyer photos |
| `with_follow_up` | Only reviews the buyer came back and added to |
| `same_country` | Only buyers in the one country you list in `countries` |

The rest run inside the actor, on rows already in memory:

- `minRating` / `maxRating` — whole stars, 1 to 5. `maxRating: 3` is the complaints feed. AliExpress has no server-side star filter, so this one has to be ours.
- `requireText` — drop star-only reviews. About one review in five on a busy product is a bare rating with nothing written.
- `sinceDate` — only reviews written on or after a date: `2026-06-01`, or a look-back window such as `30 days`, `2 weeks`, `6 months`, `1 year`. AliExpress reviews from the last 30 days answer the question a supplier check actually asks: what are buyers saying about the batch shipping *now*. AliExpress cannot filter or sort by date on its side, so set `maxReviewsPerProduct` to `0` with it — reading is cheap, and older reviews are dropped before billing.
- `keywords` — only reviews that mention at least one of your words or phrases, e.g. `["battery", "broke", "fake", "refund", "customs"]`. Case-insensitive, and it searches the original text, the translation and the follow-up, so an English keyword finds a Portuguese review once it is translated.
- `countries` — ISO-2 buyer countries, e.g. `["US", "BR"]`. The first entry also tells AliExpress which market to answer as, which changes the order it serves.

## AliExpress review monitoring: pay only for new reviews

Turn on **Only new reviews** (`onlyNewReviews`) and put the actor on an [Apify schedule](https://docs.apify.com/platform/schedules). The first run is the baseline and delivers everything your filters keep. Every run after that delivers — and bills — only reviews it has never given you before. A day with nothing new is a run with zero rows and zero charges.

```json
{
  "productUrls": ["https://www.aliexpress.com/item/1005006255429323.html"],
  "maxReviewsPerProduct": 0,
  "maxRating": 3,
  "requireText": true,
  "onlyNewReviews": true
}
```

That input, scheduled daily, is a complaint alert for a product you sell — or for a competitor's. Connect the dataset to a webhook, Slack, Google Sheets, Make or n8n and new one-to-three-star reviews arrive the day they are written.

- The memory is a named key-value store in **your own account** (`stateStoreName`, default `aliexpress-reviews-seen`), one small record of review ids per product. Give each independent monitor its own name; delete the store to start again from a fresh baseline.
- Only *delivered* reviews are remembered. A review your spending limit refused, or one your filters dropped, is not marked as seen — loosen the filter later and it is delivered then.
- Keep `maxReviewsPerProduct` at `0`. AliExpress does not serve reviews newest-first, so a new review can land anywhere in the list; reading a 2,800-review product takes about 15 requests, and reading is not what you pay for.
- Each status row reports `already_seen`, so you can see that the run looked and found nothing new rather than wondering whether it worked.

## AliExpress review sentiment analysis, topics and insights — free

AliExpress sentiment analysis usually means exporting the reviews and running them through something else. Here it is a checkbox: turn on **Analyze reviews** (`analyzeReviews`) and every review row gains four columns:

```json
{
  "rating": 2,
  "text": "The left airpods doesn’t even work after 1 day it doesn’t work and just says power on but never connects",
  "sentiment": "negative",
  "sentiment_score": -0.75,
  "rating_text_mismatch": false,
  "topics": ["durability", "functionality"]
}
```

- `sentiment` / `sentiment_score` — positive, neutral or negative, and -1 to 1. The star rating, pulled toward what the words of the review actually say.
- `topics` — which of eleven things the review talks about: `quality`, `delivery`, `packaging`, `size_fit`, `description_match`, `value`, `durability`, `functionality`, `seller_service`, `authenticity`, `damaged_or_missing`.
- `rating_text_mismatch` — true when a 4 or 5 star review reads as a complaint. AliExpress buyers do this constantly ("5 stars. Arrived broken, seller refused refund"), and it is exactly what an average rating hides.

Each product also gets one free `insights` row — AliExpress review insights and AliExpress review topics rolled up per product, the answer to "should I sell this?" without opening a spreadsheet:

```json
{
  "type": "insights",
  "product_id": "1005008342451530",
  "reviews_analyzed": 235,
  "avg_rating": 4.41,
  "sentiment_positive": 205, "sentiment_neutral": 4, "sentiment_negative": 26,
  "avg_sentiment_score": 0.7,
  "rating_text_mismatches": 0,
  "top_complaints": ["functionality", "delivery", "packaging", "durability", "quality"],
  "top_praise": ["functionality", "quality", "value", "authenticity", "delivery"],
  "topics": [{"topic": "delivery", "reviews": 11, "positive": 5, "negative": 6, "avg_rating": 3.18}],
  "by_variant": [{"value": "Color:earphone", "reviews": 235, "avg_rating": 4.41, "negative": 26}],
  "by_country": [{"value": "US", "reviews": 83, "avg_rating": 4.37, "negative": 9}, {"value": "GB", "reviews": 30, "avg_rating": 4.8, "negative": 0}],
  "by_month": [{"value": "2026-07", "reviews": 35, "avg_rating": 4.46, "negative": 4}, {"value": "2026-08", "reviews": 186, "avg_rating": 4.43, "negative": 19}],
  "with_photos": 43, "follow_ups": 4, "follow_ups_negative": 1
}
```

`by_variant` finds the one colour or plug type dragging the rating down. `by_country` separates "bad product" from "bad shipping lane to Chile". `by_month` shows whether the supplier's current batch is better or worse than last year's. `follow_ups_negative` counts the buyers who came back weeks later to complain — the durability signal.

This is deliberately not an LLM: it is a transparent word list plus the star rating, it runs inside the actor, it sends your data nowhere and it costs nothing. It reads English, so leave `language` on English (the default) and every review, whatever language the buyer wrote in, is readable to it. If you want model-grade AliExpress review sentiment analysis, the same rows — `text_translated`, `rating`, `sku_info` — are the clean input your own model needs. Insights summarise the reviews *this run delivered*, after your filters; for a whole-product picture run with `maxReviewsPerProduct: 0` and no filters.

## How do I run the AliExpress reviews scraper?

Paste product URLs into **AliExpress product URLs** (`productUrls`) or numeric item ids into **AliExpress item ids** (`productIds`), set **Max reviews per product** (`maxReviewsPerProduct`, `0` = every review), press Start.

```json
{
  "productUrls": ["https://www.aliexpress.com/item/1005006255429323.html"],
  "productIds": ["1005008342451530"],
  "maxReviewsPerProduct": 200,
  "reviewsFilter": "all",
  "minRating": 0,
  "maxRating": 3,
  "sinceDate": "6 months",
  "requireText": true,
  "keywords": [],
  "countries": ["US"],
  "sort": "lowest_rating",
  "language": "en_US",
  "includeProductRow": true,
  "hideBuyerDetails": false,
  "analyzeReviews": true,
  "onlyNewReviews": false,
  "sessions": 2,
  "perIp": 1,
  "proxyConfiguration": {"useApifyProxy": true}
}
```

Every URL form works: `aliexpress.com/item/<id>.html`, `aliexpress.us`, `aliexpress.ru`, the `/i/<id>.html` short form, and share links with a tail of tracking parameters. All three id namespaces (`1005…`, `3256…` on the US site, and legacy `2255…`/`4000…` ids) resolve to the same review list, and the id is always in the path, so nothing has to be loaded first to resolve a target. URLs and bare ids are accepted in either list, and `startUrls` — the field Make, n8n, Zapier and most Apify integrations send — is an alias for `productUrls`, so the output of any AliExpress product scraper can be piped straight in.

`sort` orders what you get back: `default`, `newest`, `oldest`, `lowest_rating`, `highest_rating`. `language` picks the translation language for `text_translated` from sixteen options (English, Spanish, Portuguese, French, German, Italian, Dutch, Polish, Turkish, Russian, Japanese, Korean, Arabic, Hebrew, Indonesian, Thai). `hideBuyerDetails` blanks the buyer's name, avatar and gender for datasets that must not carry reviewer identity. `sessions` and `perIp` control pace, `proxyConfiguration` the proxy — the defaults are right for almost every run.

## Scrape AliExpress reviews from Python, JavaScript, curl, n8n and AI agents

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/aliexpress-reviews-scraper").call(run_input={
    "productUrls": ["https://www.aliexpress.com/item/1005006255429323.html"],
    "maxReviewsPerProduct": 500,
    "reviewsFilter": "with_photos",
    "requireText": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "review":
        print(row["rating"], row["buyer_country"], row["sku_info"], row["text"])
```

JavaScript / Node:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/aliexpress-reviews-scraper').call({
    productIds: ['1005006255429323'],
    maxReviewsPerProduct: 0,
    maxRating: 3,
    sort: 'lowest_rating',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'complaints');
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~aliexpress-reviews-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"productUrls":["https://www.aliexpress.com/item/1005006255429323.html"],"maxReviewsPerProduct":100}'
```

**n8n**, **Make.com** and **Zapier** all have an Apify connector: drop in a "Run an Actor" step, paste the same JSON, and pipe the dataset into Google Sheets, Airtable, Slack or a warehouse. For **AI agents**, Apify's **MCP** server exposes this actor as a tool, so a Claude or GPT agent can pull buyer feedback for a product mid-conversation and reason over it. The dataset is also exportable straight to CSV, JSON, Excel or XML from the run page — an AliExpress reviews CSV is two clicks away.

## Buyer photos, follow-up reviews and the fields nobody else exports

| Field | Why it matters |
| --- | --- |
| `review_id` | AliExpress's own evaluation id — a stable key for deduping across runs |
| `rating` / `rating_100` | Stars 1-5, and AliExpress's raw 0-100 score behind them |
| `review_date` / `review_date_raw` | An ISO date parsed back from whatever language the review was requested in, plus the original string |
| `text` / `text_translated` / `language` | The buyer's own words, the translation, and the served language code |
| `sku_info` / `sku_id` | The exact variant the review is about |
| `images` / `image_count` | Full-size buyer photo URLs |
| `logistics` | The shipping method the order used |
| `helpful_votes` / `unhelpful_votes` | How other shoppers voted on the review |
| `attributes` | The structured attributes this buyer rated, e.g. `{"Durability": "Good"}` |
| `follow_up_text` / `follow_up_translated` / `follow_up_date` / `follow_up_days` / `follow_up_images` | The review the buyer added later, and how long they waited |
| `buyer_name` / `buyer_country` / `buyer_gender` / `buyer_anonymous` / `buyer_avatar` | Who wrote it, as far as AliExpress publishes it |
| `featured` / `ai_generated` | AliExpress promotes this review; AliExpress believes it was AI-written |
| `product_title` / `product_url` / `product_id` / `product_image` | Product context on every row |
| `type` / `target` / `fetched_at` | Row type, the input it came from, and when it was read |

Product rows add `rating_percent`, `reviews_total`, `reviews_fetched`, `five_star`, `four_star`, `three_star`, `two_star`, `one_star`, `positive_count`, `neutral_count`, `negative_count`, `positive_rate`, `negative_rate`, `with_photos_count`, `with_follow_up_count`, `same_country_count`, `product_type` and `review_attributes`. Status rows add `status`, `reviews`, `filtered`, `pages`, `total`, `repeats`, `duplicates` and `error`.

Five saved views sit in the **Output** tab: **Overview**, **Reviews**, **Complaints** (low stars with the text, photos, shipping method and follow-up next to each other), **Photo reviews** and **Products**, plus **Status**.

## How much does this AliExpress scraper cost?

You pay **$0.003 per review row** and nothing else. Product rows, insights rows, status rows, sentiment analysis, duplicate targets, item ids that do not exist, every review your filters remove, and — in monitoring mode — every review an earlier run already delivered are free. No start fee; proxy and compute are included in the event price. At the current rate, 1,000 buyer reviews cost $3.

Because filtering happens before billing, a run with `maxRating: 3` on a 3,000-review product reads the whole product but only charges for the complaints it keeps.

## What are the limits of the AliExpress feedback endpoint?

Worth knowing before you plan a job, all measured on 2026-08-29:

- **AliExpress does not sort.** Every sort value its own endpoint accepts returns the identical page. That is why `sort` here orders the reviews the run collected rather than pretending the site does it.
- **Page 1 always returns 20 rows**, whatever page size is requested, while later pages honour up to 500 at a plain offset. A naive scraper asking for 100 per page silently loses reviews 21-100 of every product. This one only ever asks for a page size that divides the offset and counts the rows it actually received, so nothing is skipped.
- **The backend shuffles.** Two result orderings are served at random, so a deep walk sees a small share of reviews twice. They are deduped by `review_id`, and the count that was dropped is reported in `repeats`.
- **An empty answer is ambiguous.** A product with no reviews and an item id that does not exist return byte-identical responses. This actor never guesses: an empty list is re-asked on a fresh IP and then settled against the product page, so you get `no_reviews` or `not_found`, never a false "no reviews" because of a throttle. A genuine refusal is reported as `status: "error"` with the reason.
- **Price, stock and seller data are not in this dataset.** The product page renders them in the browser, so a reviews scraper cannot read them without one. Use a product scraper for those.

## Is scraping AliExpress reviews legal?

Scraping publicly available data is generally lawful in the EU and the US, and reading public product reviews is one of the clearest cases: there is no login, no paywall and no personal account involved. Court decisions such as *hiQ v. LinkedIn* have repeatedly held that accessing public web pages is not unauthorised access. That said, this is general information and not legal advice.

Practical guidance: the buyer names this endpoint publishes are already masked by the site (`S***l`, or "AliExpress Shopper"), but review text and photos can still contain personal data, so if you are in the EU or UK, treat the dataset under the GDPR — have a lawful basis, keep only what you need, and do not re-publish reviews in a way that identifies an individual. Respect the site's terms for your use case, do not use the data to impersonate buyers or to build fake reviews, and keep request rates reasonable. The defaults here are deliberately gentle.

## FAQ

### Do I need an AliExpress API key or account?

No. This reads the same public feedback endpoint the product page itself calls. No key, no cookies, no login, no browser.

### How do I get AliExpress reviews by product id?

Put the numeric id straight into `productIds`. It is the number in `/item/<id>.html`, and it is what the `product_id` column of an earlier run gives you, so a two-stage pipeline (find products, then pull reviews) needs no URL building at all.

### Can I download AliExpress reviews as a CSV?

Yes — every run's dataset exports to CSV, JSON, Excel, XML or RSS from the run page, or through the Apify API. Use the **Reviews** or **Complaints** view first if you want a tidy column set.

### How do I get AliExpress negative reviews only?

Set `maxRating: 3` and `sort: "lowest_rating"`. The **Complaints** view then puts the text, the photos, the variant, the shipping method and any follow-up side by side. Filtered-out reviews are never charged.

### Can I get only AliExpress review photos?

Yes. Set `reviewsFilter: "with_photos"` — that is the site's own filter, so the pages without photos are never fetched. The `images` and `image_count` columns carry the full-size URLs of the AliExpress buyer photos.

### Is there an AliExpress reviews API?

There is no public AliExpress reviews API you can sign up for. This actor is the practical substitute: a REST endpoint you call with a token, returning AliExpress reviews without an api key of your own, in JSON or CSV.

### How many reviews can I get per product?

Every review the site will page through. `maxReviewsPerProduct: 0` takes them all; the ceiling in practice is what a product actually has. Very large products run to a few thousand and take a couple of minutes.

### Does it translate reviews?

Yes. `text` keeps the buyer's original words and `text_translated` carries the site's machine translation into whichever of the sixteen `language` options you choose, so a Polish buyer's complaint arrives readable in English — or in Arabic, Hebrew, Indonesian or Thai. AliExpress translates lazily: a page nobody has opened recently first answers with its translations missing. The actor notices, re-asks that page once and fills them in, at no charge.

### Can I schedule it to monitor new reviews?

Yes, and you only pay for what is new. Turn on `onlyNewReviews`, set `maxReviewsPerProduct` to `0` and schedule the actor daily or weekly: the first run is the baseline, and every later run delivers and bills only reviews it has not given you before. See [AliExpress review monitoring](#aliexpress-review-monitoring-pay-only-for-new-reviews) above.

### Can I get only AliExpress reviews from the last 30 days?

Yes. Set `sinceDate` to `30 days` (or `2 weeks`, `6 months`, or a date such as `2026-06-01`) and `maxReviewsPerProduct` to `0`. Older reviews are dropped before billing, so you pay only for the recent ones.

### Does it do AliExpress review sentiment analysis?

Yes, free. `analyzeReviews` adds `sentiment`, `sentiment_score`, `topics` and `rating_text_mismatch` to every review and one `insights` row per product with top complaints, top praise and ratings by variant, country and month. It is a transparent word list, not an AI model, and nothing leaves the actor.

### Can I search AliExpress reviews for a keyword?

Yes. `keywords: ["battery", "broke"]` keeps only reviews that mention one of them — in the original text, the translation or the follow-up — and the rest are never charged.

### Can I hide reviewer names?

Yes. `hideBuyerDetails` blanks the buyer's display name, avatar and gender in every row. The country and the review itself stay.

### What happens if a product id is wrong?

You get a free `status` row with `status: "not_found"` and a reason, and the run carries on with the other targets. Nothing is charged.

## Related scrapers

Product research rarely stops at one marketplace. These share the same row discipline and the same pay-per-delivered-row billing:

- [Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper) — the same job on Amazon, for comparing the same product across both marketplaces.
- [Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper) — titles, prices, ratings and specifications when you need the listing rather than the feedback.
- [eBay Scraper](https://apify.com/kestrel/ebay-search-scraper) — eBay search results with price, shipping, condition, seller feedback, watchers and units sold, for the third marketplace in a resale or dropshipping price check.
- [Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper) — Amazon keyword results with page position and a sponsored flag, when the question is what ranks for a phrase rather than what buyers said.
- [Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper) — the Top 100 of any Amazon category with every rank filled, for finding products worth sourcing before you read their feedback.
