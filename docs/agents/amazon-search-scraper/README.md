# Amazon Search Scraper — Search Results, Keyword Rank & Prices

An **amazon search scraper** that turns **amazon search results** and category charts into structured rows: **amazon asin**, title, price, rating, rating count, image, sponsored flag, and the exact position on the page.

Search any keyword, or pull **amazon best sellers** and New Releases for any category, in any of 20 marketplaces. No login, no API key, no browser. It is an **amazon product scraper**, an **amazon price scraper** and an **amazon rank tracker** in one, billed per product row.

Last verified working: 2026-10-19.

## Amazon 搜索结果、商品排名与价格：中文调用与语言设置

按关键词获取搜索结果、ASIN、价格、自然或广告位置。skipSponsored 可跳过广告商品；搜索排名不是销量。

domain 选择市场，例如 com、de、co.jp；各市场分开运行。关键词应使用目标市场的语言，货币来自该市场；没有 cn 市场或自动翻译开关。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "queries": [
    "wireless earbuds"
  ],
  "pages": 1,
  "skipSponsored": true,
  "maxResultsPerQuery": 1,
  "sessions": 1
}
```

Amazon Suchergebnisse / résultats de recherche：每个市场单独查询。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Amazon search scraper for AI agents: which input answers which request?

**Use it for** the products a keyword returns, in the order a shopper sees them (sponsored rows flagged), with price, rating and ratings count: keyword rank tracking, competitor listings, price checks by keyword, and a quick read of a category's Best Sellers or New Releases chart (30 of its 50 entries per page).

**Do not use it for** the complete Top 100 of a chart ([Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper) fills the lazy-loaded ranks), product details beyond the result tile ([Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper)), review text ([Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)), Movers & Shakers (client-rendered, not readable), or filters by price, Prime or brand (not available: filter the rows after the run).

| User request | Input |
| --- | --- |
| "Search results for wireless earbuds" | `{"queries": ["wireless earbuds"]}` |
| "Where does B0CHWRXH8B rank for wireless earbuds, organic only" | `{"queries": ["wireless earbuds"], "pages": 3, "skipSponsored": true}` — find the ASIN's `position` |
| "Top 10 results for X in Electronics" | `{"queries": ["X"], "department": "electronics", "maxResultsPerQuery": 10}` |
| "Results on amazon.co.uk" | `{"queries": ["X"], "domain": "co.uk"}` |
| "Products rated 4.5 and up for X" | `{"queries": ["X"], "minRating": 4.5}` |
| "Which ads run on keyword X" | `{"queries": ["X"]}` — keep the sponsored rows and read `sponsored: true` |
| "Best sellers in kitchen, quick look" | `{"categories": ["kitchen"], "chart": "bestsellers"}` |
| "Track rank weekly" | schedule the same input and compare `position` per ASIN across runs |

**One `product` row** ($0.004): `asin`, `title`, `url`, `query`, `chart`, `category`, `position`, `rank`, `page`, `price`, `price_display`, `currency`, `rating`, `ratings_count`, `image`, `sponsored`, `domain`, `marketplace`. Search rows fill `query` and `position`; chart rows fill `chart`, `category` and `rank`; the rest is null. `price` is null when the results page shows none. **One `status` row per keyword or category** (free): `status` is `ok`, `no_results` or `error`, with `products`, `filtered`, `duplicates`, `pages` and `error`.

**Empty results**: a keyword with no results is `no_results` and costs nothing. A bad input ends the run green with `Input problem — …` on the run card and nothing charged; when every job fails (blocked) the run fails loudly. No start fee; the run stops at the `maxTotalChargeUsd` you set when starting it.

## What does the Amazon search scraper do?

You give it keywords or categories. It gives you **amazon product data** as rows you can sort, filter and export.

- **`product` rows** — from a search: `query`, `page`, `position` (the slot on the page, ads included), `asin`, `title`, `price`, `currency`, `rating`, `ratings_count`, `image`, `sponsored`, `url`. From a chart: `chart`, `category` and `rank` instead.
- **`status` rows** — free: per keyword or category, what was delivered, how many were filtered, and why anything failed.

**Sponsored results are flagged, not silently dropped.** That matters more than it sounds: a rank tracker that counts ads as organic reports the wrong number every time. Set `skipSponsored` and **amazon sponsored products** are removed *before* you are billed for them, leaving **amazon organic rank**.

## Amazon keyword rank tracking

`position` is the slot on the results page with ads included — which is what "where do I rank" actually means to a shopper looking at the page. Pair it with `sponsored` and you can report both numbers honestly:

- **Blended rank** — `position` as-is, the shopper's view.
- **Organic rank** — run with `skipSponsored: true`, or filter `sponsored == false` yourself.

Schedule a daily run over your keywords and store `position` per ASIN. Every row is timestamped with `fetched_at`, so **amazon keyword tracking** history falls out of the dataset with no extra work. That is the whole of **amazon rank tracker** functionality without a subscription to one.

## Amazon best sellers and new releases

Category charts answer a different question from search: not "who ranks for this phrase" but "what is selling, and what is accelerating".

- **`bestsellers`** — the standing **amazon category bestsellers** chart.
- **`new_releases`** — **amazon new releases**, the newest products gaining traction.
- **Movers & Shakers** — the **amazon movers and shakers** chart is rendered client-side by Amazon (its HTML carries no products), so this actor does not offer it; diff two daily Best Sellers runs for the same signal.

Each row carries `rank`, plus price and rating, so one run gives you the chart and the economics together.

## Feeding a review run

Every row carries an `asin`. That is deliberate: pipe the ASINs from a search or a chart straight into an Amazon reviews scrape and you go from "what ranks" to "what customers say" in two steps, without assembling a product list by hand. For **amazon seller research** and **product research tool** workflows, that pairing is the whole loop.

## Input

| Field | What it does |
| --- | --- |
| `queries` | Keywords to search, as a shopper would type them. About 20 organic products plus sponsored ones per page. |
| `categories` | Category nodes for charts, e.g. `electronics`, `kitchen`, `books` — the slug from a Best Sellers URL. |
| `chart` | `bestsellers` or `new_releases`, applied to each category (Movers & Shakers is client-rendered and not available). |
| `pages` | How many result pages to walk (about 20 organic products per search page, ~30 per chart page). |
| `maxResultsPerQuery` | `0` = everything found. `N` = the first N in Amazon's order. |
| `skipSponsored` | Drop ad placements and keep only organic results. Never charged for what it drops. |
| `minRating` | Keep only products rated at or above this. |
| `domain` | Marketplace: `com`, `co.uk`, `de`, `fr`, `it`, `es`, `ca`, `com.au`, `co.jp`, `in`, `com.mx`, `com.br`, `nl`, `se`, `pl`, `sa`, `ae`, `sg`, `com.tr`, `com.be`. |
| `department` | Optional department to search inside, e.g. `electronics`. |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. Required — Amazon captchas datacentre traffic that is not rotated. Datacentre is a fine starting point: the run escalates to residential by itself when Amazon pushes back. |

### Example: daily organic rank tracking on three keywords

```json
{ "queries": ["wireless earbuds", "bone conduction headphones", "sleep earbuds"], "pages": 2, "skipSponsored": true }
```

### Example: what is climbing in a category

```json
{ "categories": ["electronics"], "chart": "new_releases", "pages": 1 }
```

### Example: a keyword and a chart together, cost-capped

```json
{ "queries": ["cast iron skillet"], "categories": ["kitchen"], "chart": "bestsellers", "pages": 1, "maxResultsPerQuery": 15 }
```

## Output

```json
{
  "type": "product", "asin": "B0H9LRGB3B", "title": "Wireless Earbuds, Bluetooth 5.4 Ear Buds",
  "query": "wireless earbuds", "chart": null, "category": null,
  "page": 1, "position": 2, "rank": null, "sponsored": false,
  "price": 73.42, "price_display": "$73.42", "currency": "USD",
  "rating": 4.7, "ratings_count": 941,
  "image": "https://m.media-amazon.com/images/I/example.jpg",
  "url": "https://www.amazon.com/dp/B0H9LRGB3B", "domain": "com", "marketplace": "US"
}
```

A chart row carries its rank instead of a page position:

```json
{
  "type": "product", "asin": "B08JHCVHTY", "title": "Blink Plus Plan",
  "chart": "bestsellers", "category": "electronics", "rank": 1, "page": 1,
  "query": null, "position": null, "sponsored": false,
  "price": 39.99, "currency": "USD", "rating": 4.4, "ratings_count": 12034,
  "url": "https://www.amazon.com/dp/B08JHCVHTY", "domain": "com", "marketplace": "US"
}
```

`status` rows carry `target`, `kind`, `status`, `products`, `filtered`, `duplicates`, `pages`, `error` and `fetched_at`.

## How much does it cost?

Pay per event, one per **delivered** product row. Free: `status` rows, every row removed by `skipSponsored`, `minRating` or the cap, empty searches, and failed jobs. An ASIN found by two keywords is delivered and billed once per run.

A search page is roughly 20 organic products; a chart page about 30. Three keywords × 2 pages is a little over 100 rows. Verified runs behind this listing cost $0.0002–$0.0052 each in platform compute. Exact per-row pricing is on this page's pricing tab.

## Amazon search scraper in Python, JavaScript, curl, n8n, Make or an AI agent

In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/amazon-search-scraper").call(run_input={
    "queries": ["wireless earbuds"], "pages": 2, "skipSponsored": True,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "product":
        print(row["position"], row["asin"], row["price"], row["rating"])
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-search-scraper').call({
    categories: ['electronics'], chart: 'new_releases', pages: 1,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'product').map((p) => [p.rank, p.asin, p.title]));
```

With **curl**, synchronously:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~amazon-search-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"queries":["wireless earbuds"],"pages":1,"skipSponsored":true}'
```

For **n8n**, **Make** and Zapier, add the actor as a step through Apify's integration and map `position`, `asin` and `price` into a sheet or an alert — "my ASIN dropped below position 10" is two nodes. For **AI agents**, the actor is callable over Apify's MCP server. To get **amazon search results csv**, run it and use the dataset's Export button, or append `?format=csv` to the dataset items API.

## Amazon competitor tracking, in practice

Rank on its own is a vanity number. What makes it useful is the row it arrives on: the same record carries the competitor's `price`, `rating` and `ratings_count`. So a weekly run over your keywords answers the questions that actually change decisions:

- Who moved above me, and did they cut price to do it?
- Is the ASIN beating me winning on rating, or on review volume?
- How much of page one is **amazon sponsored products** — that is, how much of this keyword must be bought rather than earned?
- Which of my ASINs appear for keywords I never targeted?

Because the dataset accumulates, **amazon competitor tracking** becomes a table you can chart rather than a screenshot you take.

### Bulk amazon product data

For **bulk amazon product data**, widen `pages` and hand the run a list of keywords or categories. Each ASIN is delivered once per run even when several keywords surface it, so a broad sweep does not pay twice for the same product. `maxResultsPerQuery` bounds each job independently, which is the safest way to keep a large sweep predictable.

## Is it legal to scrape Amazon search results?

This reads publicly visible search and chart pages with no login and no account, and it collects **no personal data** — a product row is an ASIN, a title, a price and a rating. Scraping public pages that contain no personal data is broadly accepted, and *hiQ v. LinkedIn* is the usual US reference point.

The caveats: Amazon's Conditions of Use discourage automated access, so this is a terms question rather than a criminal one, and the risk sits with whoever operates the run. Facts such as prices and ranks are not copyrightable, though a database of them can attract *sui generis* protection in the EU — so do not resell the raw dataset as a product. None of this is legal advice; if your use is commercial or large, ask a lawyer.

## Limits and honest notes

- **`position` includes ads.** That is intentional — it is the shopper's view. Use `sponsored` or `skipSponsored` for organic rank.
- **Price is what the results page shows.** Some listings show a range, or nothing until you open the product; `price` is then null. Chart pages in particular often omit prices for a portion of entries.
- **Chart `rank` is Amazon's own** where it prints one, and otherwise the position in the returned order.
- **Search pages carry about 20 organic products**, plus ads. Walking more `pages` is how you go deeper, and a page that adds nothing new ends the walk automatically.
- **Amazon serves a captcha to repeat callers.** The run detects it and rotates to a fresh IP rather than parsing the captcha page as an empty result set.
- **Cheap proxies first, residential only when Amazon pushes back.** A run starts on the proxies you chose — datacentre is the cheapest — and rotates to a fresh IP on a captcha or a 503. When the same page is refused twice in a row that is the IP range being blocked, not the page, so the run stops trusting that pool: its sessions re-open on a residential proxy and stay there for the rest of the run. Nothing to configure, no run has to fail to teach it, and a run that is never refused never leaves the cheap pool — so a run costs the least that still succeeds. The run's SUMMARY reports it as `http.escalated`.
- **Marketplaces differ.** The same keyword ranks differently in `com` and `co.uk`; run each marketplace as its own job.

## FAQ

### Does it need an Amazon API key?

No. Amazon's Product Advertising API needs an affiliate account with ongoing sales requirements, and it does not expose search rank the way a shopper sees it. This is an **amazon search without api** route: it reads the public results page.

### Can I track Amazon keyword rank over time?

Yes — that is the main use. Schedule the run, keep the dataset, and `position` plus `fetched_at` give you rank history per ASIN per keyword. Use `skipSponsored` if you want organic rank only.

### How do I separate sponsored from organic results?

Every row has a `sponsored` boolean. Leave it in to see the page as a shopper does, filter it out for organic analysis, or set `skipSponsored: true` so ads are dropped before billing and you never pay for them.

### Can I scrape Amazon Best Sellers and New Releases?

Yes. Put the category slug in `categories` and choose `chart`: `bestsellers` or `new_releases`. Each row carries `rank`, so the chart arrives ready to sort. The slug is the part of a Best Sellers URL after `/gp/bestsellers/`.

### How many products does one search return?

About 20 organic results per page plus ads, so a 2-page run is roughly 40 organic products. Charts return about 30 per page. Set `pages` for depth and `maxResultsPerQuery` to cap cost.

### Can I get results for a specific category or department?

Two ways: `department` narrows a keyword search to a department, and `categories` pulls the chart for a category node. They answer different questions — the first is "who ranks for this phrase in kitchen", the second is "what sells best in kitchen".

### Does it return the ASIN so I can scrape reviews next?

Yes, every product row carries `asin`. Feed those into an Amazon reviews run and you have the full picture: rank and price from here, customer opinion from there.

### Which marketplaces are supported?

Twenty, listed in the input table. Set `domain` per run; the same keyword in two marketplaces should be two runs, because ranks are not comparable across them.

### Can I export to CSV or Excel?

Yes. Every run writes an Apify dataset, exportable to CSV, Excel, JSON or XML from the Console, or over the API with `?format=csv`.

### Is there a free tier?

Empty searches, filtered rows, `status` rows and failed jobs are always free, so a run that finds nothing has no event charge; compute is included in the event price. Apify's free plan includes monthly credit you can spend here.

## Amazon bestsellers scraper: charts as a research surface

An **amazon bestsellers scraper** is the fastest read on a category you do not know. Search tells you who bid or optimised for a phrase; the charts tell you what people are actually buying, ranked by Amazon itself from real sales.

Three charts, three questions:

- **Best Sellers** answers *what is established*. Slow to move, and a good baseline for what a category's price and rating norms look like.
- **New Releases** answers *what is entering*. Products here are young; a high rating on a low `ratings_count` is a product still proving itself, and it is where new competition shows up first.
- **Movers & Shakers** would answer *what changed today*, but Amazon renders that chart in the browser, so it is not available here; the same signal comes from diffing today's Best Sellers run against yesterday's.

Run both on the same category in one job list and you get a picture no single chart gives: the incumbents and the entrants — each row with price, rating and rating count attached.

### Reading the numbers honestly

A chart position is not sales volume, and Amazon does not publish units. `rank` tells you the ordering, `ratings_count` gives you a rough proxy for cumulative demand, and the *change* in `ratings_count` between two runs is a better velocity signal than either. That last one only exists if you keep your runs — which is the argument for scheduling rather than running ad hoc.

Likewise `price` on a chart page is often absent for a portion of entries. That is Amazon's rendering, not a parsing gap; when you need reliable prices for a specific set of ASINs, feed them into a product-level run instead.

### Category slugs

The `categories` input takes the slug from a Best Sellers URL — the part after `/gp/bestsellers/`. `electronics`, `kitchen`, `books`, `toys-and-games` and so on. Nested nodes work too if you paste the full path. If a slug returns nothing, open the chart in a browser and copy the segment exactly as Amazon writes it; slugs differ between marketplaces.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Keyword Rank Tracking for ASINs](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-keyword-rank-tracking)
- [Sponsored Products Share of Page](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-sponsored-products-share)
- [Scrape Search Results to CSV](https://apify.com/kestrel/amazon-search-scraper/examples/scrape-amazon-search-results-csv)
- [Category Bestsellers in One Run](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-category-bestsellers-in-one-run)
- [Product Research Tool: Top 100 by Keyword](https://apify.com/kestrel/amazon-search-scraper/examples/product-research-tool-top-100-by-keyword)
- [Keyword Tracking on .co.uk](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-keyword-tracking-on-amazon-co-uk)
- [Search Results on .de](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-search-results-on-amazon-de)
- [Product Data Inside a Department](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-product-data-inside-a-department)
- [Bulk Product Data, 10 Keywords](https://apify.com/kestrel/amazon-search-scraper/examples/bulk-amazon-product-data-10-keywords)
- [Search Without API Access, No Key](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-search-without-an-api-key)
- [Bestsellers Scraper for Japan](https://apify.com/kestrel/amazon-search-scraper/examples/amazon-bestsellers-scraper-for-japan)

## Related scrapers

Search tells you what ranks. Reviews tell you why — every product row here carries an `asin` you can feed straight into the reviews run:

- **[Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper)** — full details, buybox and list price, stock flag, gallery and details table for any ASIN the search returns, in the same 20 marketplaces.
- **[Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper)** — the Top 100 of any category with every rank filled (a chart page renders only 30 of its 50 entries), plus New Releases.
- **[Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper)** — Amazon customer reviews and ratings by ASIN.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site’s rate for a stay.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
