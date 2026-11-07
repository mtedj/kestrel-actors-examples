# Amazon Best Sellers Scraper: Top 100 by Category, New Releases

An **amazon best sellers scraper** that turns the Best Sellers and New Releases charts of any category into ranked rows: **amazon best sellers rank**, **amazon asin**, title, price, rating, rating count, image and URL — every entry on every page, in any of 20 marketplaces. No login, no API key, no browser.

It is a **bsr tracker**, an **amazon new releases** monitor and an **amazon product research tool** in one, billed per product row. Two pages of a chart are the **amazon top 100** for that category, delivered as a table you can sort, chart and export.

Last verified working: 2026-10-19.

## Amazon 畅销榜、热销商品与新品榜：中文调用与语言设置

获取指定分类的 Best Sellers 或 New Releases 排名、ASIN、价格和评分。BSR 是排名，不是实际销量或营收。

domain 选择受支持的 Amazon 市场；com、de、co.jp 等市场分别运行。排名和币种随市场变化，不支持 cn 市场。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "categories": [
    "electronics"
  ],
  "chart": "bestsellers",
  "pages": 1,
  "maxResultsPerCategory": 1,
  "sessions": 1
}
```

Más vendidos / meilleures ventes / Bestsellerliste：使用分类榜单进行选品研究。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Amazon best sellers scraper for AI agents: which input answers which request?

**Use it for** the ranked chart of a category — every rank, 50 per page, 2 pages = the Top 100 — with ASIN, title, price, rating, ratings count and image per entry, in 20 marketplaces: BSR tracking on a schedule, spotting what is entering a category (New Releases), building ASIN lists for a reviews or product-details run.

**Do not use it for** the BSR of one specific ASIN ([Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper) reads it from the product page when rendered), Movers & Shakers, Most Wished For or Gift Ideas (not available), units sold (rank is a position, not a volume), or keyword search results ([Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper)).

| User request | Input |
| --- | --- |
| "Top 100 in electronics" | `{"categories": ["electronics"]}` (`pages` defaults to 2) |
| "Top 10 best sellers in kitchen" | `{"categories": ["kitchen"], "maxResultsPerCategory": 10}` |
| "New releases in books" | `{"categories": ["books"], "chart": "new_releases"}` |
| "Best sellers on amazon.de for a category" | `{"categories": ["<segment after /gp/bestsellers/ in the amazon.de URL>"], "domain": "de"}` |
| "Only best sellers rated 4 and up" | `{"categories": ["toys-and-games"], "minRating": 4}` |
| "Top 200 in a category" | `{"categories": ["electronics"], "pages": 4}` |
| "Track BSR daily / what is trending" | schedule one category per run; compare `rank` by `(domain, chart, category, asin)` across dated snapshots |
| "Fast and cheap, gaps are fine" | `{"categories": ["electronics"], "fillRanks": false}` — 30 of 50 per page |

**One `product` row** ($0.004): `rank`, `asin`, `title`, `url`, `chart`, `category`, `page`, `price`, `price_display`, `currency`, `rating`, `ratings_count`, `image`, `domain`, `marketplace` (`query` and `position` null, `sponsored` false). An entry whose tile the store withholds still comes with `rank`, `asin` and `url` and is counted under `partial` in the status row. **One `status` row per category** (free): `status` is `ok`, `no_results` or `error`, with `products`, `filtered`, `duplicates`, `partial`, `pages` and `error`.

**Empty results**: a chart page with no entries is `no_results` (free); a slug the store does not know ends as an `error` status row with a 404 (free; when it is the only category the run ends green with `No rows — …`). A bad input ends the run green with `Input problem — …` on the run card and nothing charged; when every category is blocked the run fails loudly. No start fee; the run stops at the `maxTotalChargeUsd` you set when starting it.

## What does the Amazon best sellers scraper do?

You give it category slugs. It gives you the chart — the **best sellers list** Amazon itself computes from real sales — as structured rows.

- **`product` rows** — one per chart entry: `rank`, `asin`, `title`, `price`, `price_display`, `currency`, `rating`, `ratings_count`, `image`, `url`, plus `chart`, `category` and `page` so you always know which list a row came from.
- **`status` rows** — free: one per category, with what was delivered, how many entries were filtered, and why anything failed.

Two charts are offered per category:

- **`bestsellers`** — the standing sales-rank chart. Slow to move, and the best baseline for what a category's price and rating norms look like.
- **`new_releases`** — the newest products gaining traction. A high rating on a low `ratings_count` here is a product still proving itself; it is where new competition shows up first.

The chart has its own name on each marketplace — Bestseller (amazon.de), Meilleures ventes (amazon.fr), Los más vendidos (amazon.es), I più venduti (amazon.it), 売れ筋ランキング (amazon.co.jp), Mais vendidos (amazon.com.br) — and the slug is still the segment after `/gp/bestsellers/` in that marketplace's URL.

## Every rank on every page — not 30 of 50

This is the part most chart scrapers get wrong. A chart page holds 50 ranks, but the store only renders 30 of them as HTML and lazy-loads the remaining 20 in the browser. A scraper that reads the page as served returns ranks 1–30, then 51–80, and calls that "the top 100". The gaps are silent.

This actor reads the complete ranked list the page carries for its own lazy-loader (every ASIN with its rank) and then makes the same load-more call the browser makes, which returns the remaining entries rendered exactly like the first 30: title, price, rating, rating count and image. `pages: 2` really is ranks 1–100, contiguous, in order. If that call is refused, the missing entries are completed from their product pages instead; and if a product page is unavailable too, the row is still delivered with its `rank`, `asin` and `url`, and the status row counts it under `partial`, so you can see exactly how complete the chart is.

Set `fillRanks: false` if you only want the entries the page renders — one request per page and nothing else, at the cost of the gaps described above.

## Amazon best sellers rank (BSR) tracking

`rank` is the product's position in this category chart, its **amazon sales rank** within that node. For **amazon bsr history**, schedule one category per run and retain `(domain, chart, category, asin, fetched_at, rank)`. Compare ranks only within the same marketplace, chart type and category; chart rank is not sales volume.

The actor delivers and bills each ASIN once across the entire run. If an ASIN appears in two input categories, only one category's row survives; concurrent jobs do not guarantee which one. A multi-category run is therefore useful for a deduplicated product list, but cannot preserve every category membership. Use separate runs when an **amazon best seller rank tracker** or **amazon rank tracker** needs independent chart observations. A missing ASIN in a capped, filtered or failed snapshot does not prove it left the source chart.

What makes the rank useful is the row it arrives on. The same record carries `price`, `rating` and `ratings_count`, so a weekly run answers the questions that actually change decisions:

- Who moved above me, and did they cut price to do it?
- Is the product beating me winning on rating, or on review volume?
- Which entries are new to the top 100 this week, and which fell out?
- How is the category's median price drifting?

The *change* in `ratings_count` between two runs is a better velocity signal than rank alone — it only exists if you keep your runs, which is the argument for scheduling rather than running ad hoc.

## Amazon new releases: what is entering the category

Best Sellers tells you what is established. New Releases tells you what is arriving. Pull both for the same category in two runs (or two schedules) and you get a picture neither gives alone: the incumbents and the entrants, each row with its economics attached. Products that appear in New Releases and then climb the Best Sellers chart within a few weeks are the **amazon trending products** worth studying — and you can detect that crossing automatically by joining the two datasets on `asin`.

## Amazon top 100 products by category, as a research surface

For **product research tool** workflows, a chart is the fastest read on a category you do not know. Search results tell you who bid or optimised for a phrase; the **amazon best sellers list by category** tells you what people are actually buying, ranked by the marketplace itself.

The **amazon top 100 products** of a node, with price and rating on every row, answer the first-pass questions of a launch: what does the category charge, how crowded is the top with one brand, how many ratings does a top-10 product carry, and is there a price band with strong ratings but few entries. Hand the run a list of sibling nodes (`electronics`, `electronics/headphones`, `electronics/speakers` …) and compare them in one dataset.

## Input

| Field | What it does |
| --- | --- |
| `categories` | Category slugs, e.g. `electronics`, `kitchen`, `books`, `toys-and-games` — the segment after `/gp/bestsellers/` in a Best Sellers URL. Nested paths work. |
| `chart` | `bestsellers` or `new_releases`, applied to each category. |
| `pages` | Chart pages per category. A page holds 50 ranks, so `2` = the Top 100. Walking stops early when a page adds nothing new. |
| `maxResultsPerCategory` | `0` = every entry on the pages requested. `N` = the top N only — the main cost control. Product pages are only fetched for ranks you asked for. |
| `minRating` | Keep only products rated at or above this. Filtered rows are never charged. |
| `fillRanks` | On by default: complete the 20 lazy-loaded ranks per page through the page's own load-more call (product pages only as a fallback) so the chart has no gaps. Off = only the 30 entries a page renders. |
| `domain` | Marketplace: `com`, `co.uk`, `de`, `fr`, `it`, `es`, `ca`, `com.au`, `co.jp`, `in`, `com.mx`, `com.br`, `nl`, `se`, `pl`, `sa`, `ae`, `sg`, `com.tr`, `com.be`. |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. Required — the store captchas datacentre traffic that is not rotated. Datacentre is a fine starting point: the run escalates to residential by itself when the store pushes back. |

### Example: the Top 100 of one category, daily

```json
{ "categories": ["electronics"], "chart": "bestsellers", "pages": 2, "fillRanks": true, "maxResultsPerCategory": 100, "minRating": 0 }
```

Set `callOptions.maxTotalChargeUsd: 0.40` on MCP `call-actor`, outside `input` (API: run option `maxTotalChargeUsd`). Repeat the same input daily and save each run's dataset externally. For two categories, make two separate calls with a $0.40 ceiling each, at most $0.80 combined. Retrieve the default dataset and paginate; inspect free `status` rows and `SUMMARY`, and verify the requested rank set before treating a snapshot as complete. `partial` counts delivered rows missing a title, not a count of missing ranks.

### Example: New Releases across several nodes, independent top 20 snapshots

```json
{ "categories": ["kitchen"], "chart": "new_releases", "pages": 1, "maxResultsPerCategory": 20 }
```

Run the same input separately for `home-garden` and `pet-supplies` to retain each category's membership. At most 20 collected entries cost $0.08 per run; set that monetary ceiling separately. `minRating` is applied after the collection cap, so fewer than 20 matching rows can remain.

### Example: only well-rated entries, UK marketplace

```json
{ "categories": ["books"], "domain": "co.uk", "pages": 1, "minRating": 4.5 }
```

## Output

```json
{
  "type": "product", "rank": 31, "asin": "B0CFPJYX7P", "title": "Example Wireless Earbuds, Bluetooth 5.4",
  "chart": "bestsellers", "category": "electronics", "page": 1,
  "price": 24.99, "price_display": "$24.99", "currency": "USD",
  "rating": 4.5, "ratings_count": 18342,
  "image": "https://m.media-amazon.com/images/I/example.jpg",
  "url": "https://www.amazon.com/dp/B0CFPJYX7P", "domain": "com", "marketplace": "US",
  "query": null, "position": null, "sponsored": false,
  "fetched_at": "2026-08-29T06:20:11+00:00"
}
```

`query`, `position` and `sponsored` are always null or false here; they are kept so this dataset lines up column-for-column with the [Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper), and a chart row and a search row can live in one table.

`status` rows carry `target` (the category), `chart`, `status` (`ok`, `no_results` or `error`), `products`, `filtered`, `duplicates`, `partial`, `pages`, `error` and `fetched_at`. A `SUMMARY` record in the run's key-value store totals the same counts across categories, together with the charged event count and the HTTP statistics.

## How much does it cost?

Pay per event, one per **delivered** product row. Free: `status` rows, every row removed by `minRating` or the cap, empty categories, and failed jobs. A product that sits in two categories' charts is delivered and billed once per run.

A chart page has up to 50 ranks. Ten separate category runs requesting Top 100 each have a combined ceiling of 1,000 delivered rows ($4 at the current event price). A single multi-category run can deliver fewer because shared ASINs are deduplicated; it does not preserve every chart membership. Completing the lazy-loaded ranks is one small extra request per page (the page's own load-more call), so a Top 100 run is four requests in total — platform compute and proxy traffic stay at a fraction of a cent. Exact per-row pricing is on this page's pricing tab.

## Amazon best sellers scraper in Python, JavaScript, curl, n8n, Make or an AI agent

In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-best-sellers-scraper").call(run_input={
    "categories": ["electronics"], "chart": "bestsellers", "pages": 2,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "product":
        print(row["rank"], row["asin"], row["price"], row["rating"], row["title"])
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-best-sellers-scraper').call({
    categories: ['kitchen'], chart: 'new_releases', pages: 1, maxResultsPerCategory: 20,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'product').map((p) => [p.rank, p.asin, p.title]));
```

With **curl**, synchronously:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-best-sellers-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"categories":["electronics"],"pages":1,"maxResultsPerCategory":20}'
```

For **n8n**, **Make** and Zapier, add the actor as a step through Apify's integration and map `rank`, `asin` and `price` into a sheet or an alert — "a new product entered the top 10" is a schedule, this actor and one IF node. For **AI agents**, the actor is callable over Apify's MCP server, so an agent can ask for the top 20 of a category by name. To get an **amazon best sellers csv**, run it and use the dataset's Export button, or append `?format=csv` to the dataset items API.

## Feeding the ASINs into a reviews run

Every row carries an `asin`. That is deliberate: pipe the ASINs from a chart straight into the [Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper) and you go from "what sells" to "what customers say about it" in two steps, without assembling a product list by hand. For keyword rank rather than chart rank — where your ASIN sits on the results page for a search phrase, ads flagged — use the [Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper); it writes the same product columns, so the three datasets join on `asin`.

## Is it legal to scrape Amazon Best Sellers?

This reads publicly visible chart and product pages with no login and no account, and it collects **no personal data** — a row is a rank, an ASIN, a title, a price and a rating. Scraping public pages that contain no personal data is broadly accepted, and *hiQ v. LinkedIn* is the usual US reference point.

The caveats: the store's Conditions of Use discourage automated access, so this is a terms question rather than a criminal one, and the risk sits with whoever operates the run. Facts such as prices and ranks are not copyrightable, though a database of them can attract *sui generis* protection in the EU — so do not resell the raw dataset as a product. None of this is legal advice; if your use is commercial or large, ask a lawyer.

## Limits and honest notes

- **`rank` is the chart position, not units sold.** The marketplace does not publish sales volume; `ratings_count` and its change between runs are the closest public proxies.
- **Prices are what the page shows, in the currency it rendered.** The store localises prices to the caller's location, so a `com` run can return a few rows in another currency; `currency` is read from the price itself, never assumed from the marketplace. A row shows `price: null` when the page prints a range or no price at all.
- **The product-page fallback is rare but slower.** When the load-more call is refused, each missing entry costs a product-page fetch; details from a product page occasionally print a different price or image size than the chart tile would. Both are the product's own data.
- **With `minRating` set, an entry whose details could not be read has no rating and is filtered** — free, and counted in the status row's `filtered`. Without a rating filter it is delivered with its `rank`, `asin` and `url` and counted under `partial`.
- **Movers & Shakers is not offered.** That chart is rendered entirely in the browser — the page as served carries no entries — so it cannot be read honestly with this approach. See the FAQ.
- **A captcha is served to repeat callers.** The run detects it and rotates to a fresh IP rather than parsing the captcha page as an empty chart.
- **Cheap proxies first, residential only when the store pushes back.** A run starts on the proxies you chose — datacentre is the cheapest — and rotates to a fresh IP on a captcha or a 503. When the same page is refused twice in a row that is the IP range being blocked, not the page, so the run stops trusting that pool: its sessions re-open on a residential proxy and stay there for the rest of the run. Nothing to configure, no run has to fail to teach it, and a run that is never refused never leaves the cheap pool — so a run costs the least that still succeeds. The run's SUMMARY reports it as `http.escalated`.
- **Slugs differ between marketplaces.** If a category returns `no_results`, open the chart in a browser on that marketplace and copy the segment exactly as it is written.

## FAQ

### How many products does one run return?

50 per page per category. `pages: 2` is the Top 100; `pages: 4` is the Top 200 where the category goes that deep. `maxResultsPerCategory` caps collection per category before rating filters, and the walk stops when a page adds nothing new. Run-wide ASIN deduplication can remove a category's row when the ASIN was already delivered for another category; use one category per run for independent charts.

### Why do other chart scrapers return 30 entries per page?

Because that is how many the page renders as HTML — the other 20 are lazy-loaded by the browser. This actor reads the page's complete ranked list and makes the page's own load-more call for the rest (falling back to product pages if that is refused), so no rank is skipped. Turn `fillRanks` off if you would rather have the 30 rendered entries and a single request per page.

### Can I track Amazon BSR over time?

Yes — that is the main use. Schedule the run, keep the dataset, and `rank` plus `fetched_at` give you rank history per ASIN per category. Join two days on `asin` to get movement, entries and exits.

### Does it need an Amazon API key?

No. The Product Advertising API needs an affiliate account with ongoing sales requirements, and it does not expose the chart as a shopper sees it. This reads the public pages.

### Which categories can I use?

Any node that has a Best Sellers page: top-level slugs like `electronics` or `books`, and nested paths copied from a chart URL. The slug is the part after `/gp/bestsellers/`; New Releases uses the same slugs.

### What about Movers & Shakers, Most Wished For and Gift Ideas?

**Amazon movers and shakers** is rendered client-side — the served page carries no entries — so it is not offered rather than offered broken. **Amazon most wished for** and Gift Ideas are not charts this actor pulls today. If you need one of them, open an issue on this page; demand decides what gets built next.

### Is the rank the same as the BSR on a product page?

It is the product's position in *this* category chart. A product page prints its rank in several nodes at once (a top-level category and one or more sub-categories); the chart for a given node lists products in that node's rank order, so the two agree for the node you pulled.

### Does it return the ASIN so I can scrape reviews next?

Yes, every product row carries `asin`. Feed those into the Amazon Reviews Scraper and you have rank and price from here, customer opinion from there.

### Which marketplaces are supported?

Twenty, listed in the input table. Set `domain` per run; the same category in two marketplaces should be two runs, because ranks are not comparable across them.

### Can I export to CSV or Excel?

Yes. Every run writes an Apify dataset, exportable to CSV, Excel, JSON or XML from the Console, or over the API with `?format=csv`.

### Is there a free tier?

Empty categories, filtered rows, `status` rows and failed jobs are always free, so a run that finds nothing has no event charge; compute is included in the event price. Apify's free plan includes monthly credit you can spend here.

## Scrape Amazon best sellers into a workflow

A few patterns that come up often, all of which are one schedule plus this actor:

- **New entrant alert.** Daily Top 100 of your category; compare today's `asin` set with yesterday's; alert on anything new inside the top 20.
- **Price-band watch.** Weekly Top 100; bucket `price` into bands and count entries per band; alert when a band you compete in gains more than N products.
- **Launch tracking.** Daily New Releases of your node; keep the dataset; a product that reaches the Best Sellers Top 50 within 30 days of appearing in New Releases is a launch that worked — study it.
- **Marketplace comparison.** The same category on `com`, `co.uk` and `de`; join on `asin`; products that chart in one marketplace but not another are import candidates.

Because every row is timestamped and every run is a dataset, none of these need a database of their own to get started — a spreadsheet and a schedule are enough, and an **amazon bestsellers scraper** that fills every rank is what keeps the comparison honest from day to day.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Top 100 Products by Category](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/amazon-top-100-by-category)
- [New Releases by Category](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/amazon-new-releases-tracker)
- [BSR History from a Daily Run](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/amazon-bsr-history)
- [Best Sellers List Across 10 Categories](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/best-sellers-list-across-10-categories)
- [Scrape Best Sellers on .co.uk](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/scrape-amazon-best-sellers-on-amazon-co-uk)
- [Best Sellers Rank on .de](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/amazon-best-sellers-rank-on-amazon-de)
- [Sales Rank Charts for Japan](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/amazon-sales-rank-charts-for-japan)
- [Product Research Tool: 4+ Stars](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/amazon-product-research-tool-4-stars-plus)
- [Best Sellers CSV, 1000 Ranks Deep](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/amazon-best-sellers-csv-1000-ranks-deep)
- [BSR Tracker at 30 Ranks a Page (Cheaper)](https://apify.com/kestrel/amazon-best-sellers-scraper/examples/bsr-tracker-at-30-ranks-a-page)

## Related scrapers

Charts tell you what sells. The rest of the suite tells you where a product ranks for a phrase and what buyers say about it — every product row here carries an `asin` you can feed straight into either:

- **[Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper)** — feed a chart's ASINs in for price, list price, availability, images, bullet points and the details table per product.
- **[Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper)** — keyword search results with page position and a sponsored flag, plus the same charts when you want both in one run.
- **[Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)** — customer reviews and ratings by ASIN, with filters that run before billing.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
