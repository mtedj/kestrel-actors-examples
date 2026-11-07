# Amazon Product Scraper — Details, Prices & Availability by ASIN

An **amazon product scraper** that turns any ASIN or product URL into one clean row of **amazon product data**: title, brand, the buybox price and the struck-through list price, currency, the availability line and a stock flag, rating and rating count, the main image and the whole gallery, bullet points, description, category, the product-details tables, seller and Best Sellers Rank when the page shows it. It is an **amazon price scraper**, an **amazon asin lookup** and an **amazon stock checker** in one call, across 20 marketplaces — the **amazon scraper** the rest of the kestrel suite feeds on.

Give it ASINs or URLs. No login, no **amazon product api** key, no browser. It bills per product row, and two filters cut what you pay for *before* you are billed: `inStockOnly` and `maxPrice`. Unknown ASINs, blocked pages and duplicates are free. Read the **Scope** section before you buy: it reads the public product page, not a seller-central feed.

Last verified working: 2026-10-19.

## Amazon 商品数据、价格、库存状态与 ASIN 查询：中文调用与语言设置

按 ASIN 或商品 URL 获取标题、品牌、当前价格、库存状态、图片和 BSR。库存状态不是精确库存数量，BSR 不是销量；历史需要保存多次快照。

domain 选择受支持市场，例如 com、de、co.jp。完整 URL 自带市场。价格币种由市场决定，不支持 cn；非 com 市场可能需要住宅代理以获取购买框价格。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "asins": [
    "B0CHWRXH8B"
  ],
  "domain": "com",
  "sessions": 1
}
```

Amazon Produktdaten / données produits：使用相同 ASIN 和市场比较快照。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Amazon product scraper for AI agents: which input answers which request?

**Use it for** one row of product data per ASIN or product URL — buybox price, list price, stock, rating, images, bullet points, the details table, Best Sellers Rank when the page shows it — in 20 marketplaces: price checks, stock checks, catalogue enrichment, and price history by scheduling the same list.

**Do not use it for** review text ([Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)), keyword search results or keyword rank ([Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper)), a whole category's chart ([Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper)), sales or revenue estimates (not public), variation-level prices (variations are counted, not expanded: pass each variation's ASIN), or a guaranteed `bsr` (null when the page does not render the rank).

| User request | Input |
| --- | --- |
| "Price and stock of B0CHWRXH8B" | `{"asins": ["B0CHWRXH8B"]}` |
| "Details of this amazon.de product" | `{"asins": ["https://www.amazon.de/dp/B09B8V1LZ3"], "proxyConfiguration": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}}` |
| "Which of these 200 ASINs are in stock" | `{"asins": [...], "inStockOnly": true}` |
| "Products under $100 from this list" | `{"asins": [...], "maxPrice": 100}` |
| "Track the price of these ASINs daily" | schedule `{"asins": [...]}` daily and compare `price` and `list_price` across runs (no change detection built in) |
| "Images and bullet points for a listing audit" | `{"asins": [...]}` — `images`, `features`, `description` and `details` are on every row |
| "BSR of these products" | `{"asins": [...]}` — `bsr` and `bsr_top` when the page renders the rank, else null |

**One `product` row** ($0.004): `asin`, `domain`, `marketplace`, `url`, `title`, `brand`, `price`, `price_display`, `currency`, `list_price`, `list_price_display`, `availability`, `in_stock`, `prime`, `rating`, `ratings_count`, `image`, `images`, `features`, `description`, `breadcrumbs`, `category`, `details`, `bsr`, `bsr_top`, `date_first_available`, `sold_by`, `variations_count`, `5_star_pct` … `1_star_pct`. **One `status` row per target** (free): `status` is `ok`, `filtered`, `not_found`, `blocked`, `error` or `limit`, with `products`, `filtered`, `duplicates` and `error`.

**Empty results**: an unknown ASIN is `not_found` after one attempt (free); a product dropped by `inStockOnly` or `maxPrice` is `filtered` (free); a page still blocked after eight IP rotations is `blocked` (free). A bad input ends the run green with `Input problem — …` on the run card and nothing charged; when every target fails the run fails loudly. No start fee; the run stops at the `maxTotalChargeUsd` you set when starting it.

## What does the Amazon product scraper do?

You give it products. It gives you their details as rows you can sort, filter, join and export — the **amazon product information** a listing page shows a shopper, in a fixed column set that never changes shape from one ASIN to the next.

- **`product` rows** — `asin`, `marketplace`, `url`, `title`, `brand`, `price`, `price_display`, `list_price`, `list_price_display`, `currency`, `availability`, `in_stock`, `prime`, `rating`, `ratings_count`, `image`, `images`, `features`, `description`, `breadcrumbs`, `category`, `details`, `bsr`, `bsr_top`, `date_first_available`, `sold_by`, `variations_count` and the five `5_star_pct` … `1_star_pct` histogram shares.
- **`status` rows** — free: per `target` you gave, whether the product was delivered (`products`), dropped by a filter (`filtered`), already covered by another input (`duplicates`), or why it failed (`status`, `error`).

Every row is stamped `fetched_at`, so a scheduled run builds an **amazon price history** you own.

## Amazon product data by ASIN, URL or marketplace

- **`asins`** takes either form: a bare **amazon asin** like `B0CHWRXH8B`, or a full product URL from any marketplace.
- A URL's marketplace is used automatically. `https://www.amazon.de/dp/B07XJ8C8F5` is read from the German site and priced in EUR without you setting anything.
- **`domain`** sets the marketplace for bare ASINs. Twenty are supported: `com`, `co.uk`, `de`, `fr`, `it`, `es`, `ca`, `com.au`, `co.jp`, `in`, `com.mx`, `com.br`, `nl`, `se`, `pl`, `sa`, `ae`, `sg`, `com.tr`, `com.be`.

The same ASIN on two marketplaces is two products — different price, stock, currency and often a different title. The page says Preis on amazon.de, prix on amazon.fr, precio on amazon.es, prezzo on amazon.it, 価格 on amazon.co.jp and preço on amazon.com.br; `price` comes back as a number and `currency` as the code Amazon rendered, whatever the page's language. An ASIN and its own URL are one product, fetched and billed once. That makes **amazon multi marketplace** comparison explicit: put the ASIN and the `co.uk` URL in the same run and you get two rows you can lay side by side.

## Amazon price scraper: the buybox price, and only the buybox price

A product page prints many prices — the offer, other sellers, bundles, "customers also bought" carousels. Most scrapers grab the first one they see. This one reads the **buybox** block only, the price a shopper would pay if they clicked *Buy now*:

- `price` and `price_display` are the buying option's price, as a number and exactly as printed.
- `list_price` is the struck-through **amazon list price** when the page shows one, so a discount is a subtraction you can do in a spreadsheet.
- `currency` is read from the printed price, not assumed from the marketplace. The site prices in the *caller's* location's currency, so `currency` tells you what you actually got.
- An unavailable product has a **null** price. It does not inherit a neighbour's from a carousel — an earlier page-wide approach labelled a discontinued iPad at 149 GBP that way.

Schedule the run daily and keep the rows: that is **amazon price tracking** and **amazon price monitoring** for a catalogue at a few cents a day, with `list_price` telling you whether a drop is a real cut or a discount against a list price nobody paid.

## Amazon stock checker with filters that run before billing

- **`inStockOnly`** keeps only products whose availability line says they are in stock. Unavailable products — and products whose stock cannot be determined — are dropped before billing.
- **`maxPrice`** keeps only products whose buybox price is at or below the number you give, in the marketplace's currency. Products with no visible price are dropped too.

Filtered products are never charged. In a verified run over three products, `inStockOnly: true` plus `maxPrice: 100` delivered **one row** (the $54.99 speaker), dropped the $263.86 earbuds and the discontinued laptop, and billed one row. That is what makes an **amazon availability check** across a thousand ASINs affordable: the dead listings cost nothing.

`in_stock` is derived from the availability wording in six languages, falling back to whether a buybox price exists; when neither is there it is `null`, and `null` is not "in stock".

## Amazon product details, images and bullet points

- **`images`** is the full gallery from the page's own image state, highest resolution first; `image` is the first of them. Seven to thirteen **amazon product images** per listing is typical.
- **`features`** are the bullet points under the title — the **amazon bullet points** sellers write for the listing.
- **`description`** is the product description block as plain text, up to 2,000 characters, null when the page renders none.
- **`details`** is the *Product information*, *Technical details* and *Product overview* tables merged into one `{label: value}` object: dimensions, weight, manufacturer, model number, colour, batteries, `Date First Available` and whatever else the listing declares. `date_first_available` is lifted out for convenience.
- **`breadcrumbs`** and **`category`** come from the breadcrumb bar. Most amazon.com pages render no breadcrumb bar, so they are null there and present on most other marketplaces.
- **`bsr`** and **`bsr_top`** carry the **amazon best sellers rank** entries when the page renders them — `[{"rank": 1234, "category": "Electronics"}, …]`. The site serves the rank to some sessions and not others; expect null on many pages and never a fabricated number.
- **`sold_by`** is the seller line ("Amazon.com", "Amazon Resale and Fulfilled by Amazon", a third-party name); **`variations_count`** is how many colours, sizes or models the listing carries; **`prime`** is the Prime badge on the offer.

## Input

| field | what it does |
|---|---|
| `asins` | ASINs or product URLs, one per line. A URL's marketplace wins; each ASIN is fetched and billed once per run. |
| `domain` | Marketplace for bare ASINs (`com` by default). Outside `com`, choose RESIDENTIAL in `proxyConfiguration` so the buybox appears. |
| `inStockOnly` | Keep only products in stock. Filters before billing. |
| `maxPrice` | `0` = all. `N` = keep only products priced at or below N in the marketplace's currency. Filters before billing. |
| `sessions` | Parallel proxy sessions (egress IPs). More is faster; each is paced separately. |
| `perIp` | Requests per second per IP. About 0.5 is what the site tolerates; faster earns captchas, not speed. |
| `proxyConfiguration` | Apify Proxy. Datacentre is enough for amazon.com and the run escalates to residential by itself if the site pushes back; choose RESIDENTIAL outright for other marketplaces — either way it is routed through the marketplace's own country so the buybox appears. |

### Example: a price and stock check across a catalogue

```json
{
  "asins": ["B0CHWRXH8B", "B09B8V1LZ3", "B0BSHF7WHW"],
  "domain": "com"
}
```

### Example: only what is in stock under a budget

```json
{
  "asins": ["B0CHWRXH8B", "B09B8V1LZ3", "B0BSHF7WHW"],
  "inStockOnly": true,
  "maxPrice": 100
}
```

### Example: the same product on two marketplaces

```json
{
  "asins": ["B09B8V1LZ3", "https://www.amazon.co.uk/dp/B09B8V1LZ3"],
  "proxyConfiguration": { "useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"] }
}
```

## Output

One `product` row, exactly as a verified run returned it (gallery and details shortened):

```json
{
  "type": "product",
  "asin": "B09B8V1LZ3",
  "domain": "com",
  "marketplace": "US",
  "url": "https://www.amazon.com/dp/B09B8V1LZ3?th=1&psc=1",
  "title": "Amazon Echo Dot (newest model), Vibrant sounding Alexa speaker, Great for bedrooms, dining rooms and offices, Charcoal",
  "brand": "Amazon",
  "price": 54.99,
  "price_display": "$54.99",
  "currency": "USD",
  "list_price": 79.99,
  "list_price_display": "$79.99",
  "availability": "In Stock",
  "in_stock": true,
  "prime": false,
  "rating": 4.7,
  "ratings_count": 198808,
  "image": "https://m.media-amazon.com/images/I/61J2sQtBYDL._AC_SL1000_.jpg",
  "images": ["https://m.media-amazon.com/images/I/61J2sQtBYDL._AC_SL1000_.jpg", "https://m.media-amazon.com/images/I/71xoR4A6q-L._AC_SL1500_.jpg"],
  "features": ["Our most popular smart speaker with a fabric design. It is our most compact smart speaker that fits perfectly into small spaces."],
  "description": null,
  "breadcrumbs": null,
  "category": null,
  "details": null,
  "bsr": null,
  "bsr_top": null,
  "date_first_available": null,
  "sold_by": null,
  "variations_count": 3,
  "5_star_pct": 82,
  "4_star_pct": 11,
  "3_star_pct": 4,
  "2_star_pct": 1,
  "1_star_pct": 2,
  "fetched_at": "2026-08-29T10:31:04+00:00"
}
```

And the free `status` row for a target that was dropped by a filter:

```json
{ "type": "status", "target": "B0BSHF7WHW", "asin": "B0BSHF7WHW", "domain": "com", "status": "filtered", "products": 0, "filtered": 1, "duplicates": 0, "error": null, "fetched_at": "2026-08-29T10:31:05+00:00" }
```

`status` is one of `ok`, `filtered`, `not_found` (the marketplace answered 404 or the page carried no product), `blocked` (a captcha survived every rotation), `limit` (your spending limit stopped the run before this product) or `error`. The **Prices** view lists price columns only; the **Content** view lists text, images and the details table; the **Run status** view lists the status rows. Export any view as JSON, CSV or Excel — an **amazon products csv** is one click.

## How much does it cost?

**$0.004 per product row.** Status rows, filtered products, duplicates, unknown ASINs and blocked pages are free. A daily check over 500 ASINs is $2 a day; the same check with `inStockOnly` on a catalogue where half the listings are dead is $1. Compute and proxy usage for the run are included in the event price.

## Amazon product scraper in Python, JavaScript, curl, n8n, Make or an AI agent

### Python

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-product-scraper").call(run_input={
    "asins": ["B0CHWRXH8B", "B09B8V1LZ3"],
    "domain": "com",
    "inStockOnly": True,
})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "product"]
for r in rows:
    print(r["asin"], r["price_display"], r["availability"], r["rating"], r["ratings_count"])
```

An **amazon product scraper python** loop that runs this once a day and appends the rows to a file gives you a price and stock series per ASIN; `list_price` beside `price` tells you which drops are real.

### JavaScript

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-product-scraper').call({
    asins: ['B09B8V1LZ3', 'https://www.amazon.co.uk/dp/B09B8V1LZ3'],
    proxyConfiguration: { useApifyProxy: true, apifyProxyGroups: ['RESIDENTIAL'] },
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.filter(r => r.type === 'product').map(r => ({ asin: r.asin, marketplace: r.marketplace, price: r.price_display, inStock: r.in_stock })));
```

### curl

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-product-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"asins": ["B0CHWRXH8B"], "domain": "com"}'
```

### n8n and Make

In **n8n**, an HTTP Request node calling the `run-sync-get-dataset-items` endpoint above, on a Schedule trigger, followed by a Filter on `type = product` and an IF on `price` against yesterday's value, is a price-drop alert in five nodes. The same shape works in **Make** (Apify module → Iterator → Filter → Slack/Email). Both are how most users run this on a schedule.

### MCP and AI agents

The actor is exposed through Apify's MCP server, so an **AI agent** in Claude, Cursor or any MCP client can call it by name: "look up these ASINs and tell me which are in stock under $60" becomes one tool call with `asins`, `inStockOnly` and `maxPrice` filled in. The fixed row shape is what makes that reliable — the agent always gets the same columns.

## Scope — read this before you buy

This reads the **public product page** as an anonymous visitor sees it. That is exactly the **amazon product information** a shopper gets, and no more:

- **Price** is the buybox offer. Pages with no buying option (discontinued products, or an offer the marketplace hides from the caller's location) have a null price, and the row is still delivered with everything else filled in — use `inStockOnly` or `maxPrice` if you do not want to pay for those.
- **Best Sellers Rank** is rendered for some sessions and not others. When it is not on the page, `bsr` is null. If you need ranks for a whole category, the **[Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper)** reads the chart itself and fills every rank.
- **Reviews are not here.** The product row carries `rating`, `ratings_count` and the star histogram; the review text belongs to the **[Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)**.
- **Variations** are counted, not expanded. Give each variation's ASIN if you need each one priced.

## Is it legal to scrape Amazon products?

The actor reads publicly available product pages — the same data a shopper sees without logging in — and stores nothing personal. Price, availability, rating and product descriptions are facts about products, not people. Scraping public data is legal in most jurisdictions for legitimate purposes such as price comparison, market research and catalogue management, but you are responsible for how you use it: respect the site's terms, keep request rates modest (the defaults are), and do not republish copyrighted images or descriptions as your own. Apify's guidance on the **legal** side of web scraping is a good starting point if you are unsure.

## Limits and honest notes

- **One request per product.** Ten ASINs is ten page fetches; a thousand is a thousand, paced at about one every two seconds per session, so four sessions do a thousand products in roughly eight minutes.
- **Captchas happen.** The site challenges repeat visitors from the same IP. The client detects the captcha page, rotates to a fresh IP and retries up to eight times; a product that is still blocked after that is reported `blocked` in its status row and never billed.
- **Cheap proxies first, residential only when the site pushes back.** A run starts on the proxies you chose — datacentre is the cheapest — and rotates to a fresh IP on a captcha or a 503. When the same page is refused twice in a row that is the IP range being blocked, not the page, so the run stops trusting that pool: its sessions re-open on a residential proxy and stay there for the rest of the run. Nothing to configure, no run has to fail to teach it, and a run that is never refused never leaves the cheap pool — so a run costs the least that still succeeds. The run's SUMMARY reports it as `http.escalated`. Residential sessions keep the marketplace routing, so the buybox stays the one a local shopper sees.
- **A 404 is an answer.** An unknown ASIN is reported `not_found` after one attempt, not after five rotations.
- **The buybox can hide.** For marketplaces outside the US, a datacentre egress sometimes gets a page with no offer. Choose RESIDENTIAL in `proxyConfiguration` and the run routes through the marketplace's own country, which is what the verified `co.uk` run used.
- **Language follows the marketplace.** `availability` and `details` labels come back in the site's language; `in_stock` normalises the common wordings, `details` keys do not.

## FAQ

### Does it need an Amazon API key or login?

No. There is no key and no account. The Product Advertising API needs an approved associate account and rate-limits by sales; this reads the page instead.

### Can I look up an ASIN and get the price only?

Yes. Every row has `price`, `price_display`, `list_price` and `currency`; the **Prices** view shows nothing else. That is the **amazon asin lookup** most people want.

### How do I track prices over time?

Schedule the run (daily is typical), keep the rows, and group by `asin`. `fetched_at` timestamps every row; `price` versus `list_price` separates real cuts from list-price theatre.

### Does it work for marketplaces other than amazon.com?

Yes — 20 of them, by URL or by `domain`. Use RESIDENTIAL proxies for marketplaces outside the US so the buybox renders; the run picks the right country for you.

### What happens with a product that is out of stock?

The row is delivered with `availability` (e.g. `Currently unavailable.`), `in_stock: false` and a null `price` — unless `inStockOnly` is on, in which case it is dropped free of charge.

### Can I get the product images?

Yes: `image` is the main image at the highest resolution the page offers, `images` is the full gallery.

### Why is Best Sellers Rank null?

Because the page did not render it for that session. It is never invented. The Best Sellers Scraper is the reliable source for ranks.

### Can I feed it from a keyword search or a chart?

That is the intended flow: the **[Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper)** and the Best Sellers Scraper both emit `asin` columns; paste them into `asins` here for full details, then into the Reviews Scraper for the review text.

### Is there a free tier?

Apify's free plan includes monthly platform credit; the per-row price applies on top. Filtered rows, duplicates and unknown ASINs never cost anything.

## Amazon product research tool for sellers, brands and analysts

- **Catalogue hygiene.** Run your own **amazon product catalog** nightly with `inStockOnly` off and watch `in_stock`, `sold_by` and `price` — a buybox lost to another seller shows up as a changed `sold_by` line the next morning.
- **Competitor pricing.** A comp set of 50 rival ASINs, daily, is 20 cents a day. Join on `asin`, chart `price`, and you have the **amazon price history** nobody sells you.
- **Content audits.** `features`, `description` and `images` per ASIN across a brand's catalogue tell you which listings are thin. Counting `images` and the length of `features` is a five-line script.
- **Product research.** Pull the Best Sellers Scraper's Top 100 for a category, feed the ASINs here, and you have price, rating, rating count, variation count and details for the whole chart — an **amazon product research tool** built from two runs.
- **Multi-marketplace launches.** The same ASIN across `com`, `co.uk` and `de` shows where a listing is live, priced and in stock, and where it is not.

### What this deliberately does not do

It does not log in, does not read seller-central data, does not expand variations, does not fetch reviews, and does not invent a rank or a price the page did not show. Every column is either what the page printed or null.

## Related scrapers

Products are one half of the picture. These read the rest, share the same row discipline and the same pay-per-delivered-row billing:

- **[eBay Scraper](https://apify.com/kestrel/ebay-search-scraper)** — eBay listings with price, shipping, condition, seller feedback, watchers and units sold, across 11 verified marketplaces.
- **[AliExpress Reviews Scraper](https://apify.com/kestrel/aliexpress-reviews-scraper)** — buyer feedback with photos, variant chosen and buyer country, for product research and dropshipping.
- **[Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper)** — keyword results with sponsored placements flagged; its `asin` column is the natural input here.
- **[Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper)** — the Top 100 of any category with every rank filled.
- **[Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)** — the review text behind `rating` and `ratings_count`.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
