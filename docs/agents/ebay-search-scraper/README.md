# eBay Scraper — Search, Listings, Prices, Items & Sellers

An eBay scraper that turns active search results into clean rows: price, struck-through list price, shipping cost, condition, buying format, bids and time left, **units sold**, **watchers**, seller feedback score and percentage, item location and image. No API key, no login, no browser. It reads public search pages on 10 supported marketplaces and bills you per listing row it actually delivers. Fields depend on what eBay displays. Use it for ebay price research, for bulk ebay product data, and as an ebay api alternative when the official Browse API's onboarding is more than your project needs.

**Last verified working: 2026-11-06 — US keyword search only (3 listings).** Item-detail requests for all 3 fresh URLs from that search were blocked by eBay challenge/error pages. Those detail requests returned no item rows and incurred no item charges. **Item-page details are currently unreliable.** Do not choose this Actor when item specifics, quantity or item-page category data are required. A successful search does not guarantee access to its item pages. This is a measured limitation of the current checks, not a claim that every item page will always fail.

The differentiator is the **demand column**. Most ebay listing scraper output tells you what sellers are asking. This one also tells you what shoppers are doing about it: how many units a listing has already sold, how many people are watching it, how many bids an auction has drawn and how long it has left, whether the seller takes offers, and how far the current price sits below the seller's own list price. Those five numbers are what separate a price you can copy from a price nobody pays.

## Pricing dates for API callers

The active price is **$0.004 per delivered listing row**, effective since **2026-10-27**. One page of 60 delivered listings costs $0.24. Set `maxTotalChargeUsd` separately in Apify run options. This documentation correction changes no prices.

中文：当前每条已交付商品记录为 $0.004，自 2026-10-27 起生效。60 条记录费用为 $0.24。请在 Apify 运行选项中设置费用上限。

## eBay 商品搜索、价格、拍卖与卖家反馈：中文调用与语言设置

按关键词或 URL 获取商品、价格、运费、商品成色、竞价及来源展示的售出数量。它不是完整已售成交历史数据库。

domain 选择已支持市场，如 com、de、fr。每个市场使用其货币；没有 cn 市场或语言翻译开关。买家所在国家不会自动转换结果币种。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "queries": [
    "mechanical keyboard"
  ],
  "pages": 1,
  "maxResultsPerQuery": 1,
  "sessions": 1
}
```

eBay Angebote / enchères / subastas：固定市场与购买方式后比较价格。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## eBay scraper for AI agents: which input answers which request?

Use this actor when the request wants eBay's **active search listings** for a keyword or pasted eBay search URL: asking prices, shipping, condition, Buy It Now or auction, bids, units sold, watchers and seller feedback where eBay displays them. **Do not select it for required item specifics, quantity or item-page category data: item-detail mode is currently unreliable.** It also does not support sold or completed listings and sold prices (eBay keeps those behind a sign-in wall), eBay Kleinanzeigen (a different site), seller stores by name, or eBay UK, Ireland, Canada, Switzerland, Hong Kong and Austria.

| user request | input JSON |
|---|---|
| listings for X | `{"queries": ["mechanical keyboard"]}` (first page, up to 60 listings, $0.24) |
| 200 listings for X | `{"queries": ["mechanical keyboard"], "pages": 4, "maxResultsPerQuery": 200}` |
| the 20 cheapest X | `{"queries": ["mechanical keyboard"], "sortBy": "price_low", "maxResultsPerQuery": 20}` |
| new X under 100 | `{"queries": ["mechanical keyboard"], "conditions": ["new"], "maxPrice": 100}` |
| auctions ending soon | `{"queries": ["rolex submariner"], "buyingFormat": "auction", "sortBy": "ending_soonest"}` |
| used or refurbished X on eBay Germany | `{"queries": ["iphone 13"], "domain": "de", "conditions": ["used", "certified_refurbished", "seller_refurbished"]}` |
| X inside one category | `{"queries": ["gpu"], "category": "175672"}` |
| this active-listing eBay search | `{"startUrls": ["https://www.ebay.com/sch/i.html?_nkw=gpu&LH_BIN=1"]}` |
| details of one item | Currently unreliable: all 3 fresh US item URLs in the 2026-11-06 check were blocked. Use a currently verified item-detail source when these fields are required |
| search results with item specifics | Search rows do not contain item specifics. A second item-URL run is not a verified enrichment workflow; successful search does not guarantee detail rows |
| eBay UK or sold/completed transaction history | Unsupported; use another Actor that explicitly supports the requested mode |
| newest listings every morning | `{"queries": ["mechanical keyboard"], "sortBy": "newly_listed", "pages": 1}` on a schedule; dedupe on `item_id` |

Output rows share one dataset and are told apart by `type`. An `item` row (billed, $0.004 each) has fields `item_id`, `title`, `url`, `marketplace`, `price`, `currency`, `list_price`, `discount_pct`, `shipping_cost`, `free_shipping`, `condition`, `buying_format`, `bids`, `time_left`, `best_offer`, `units_sold`, `watchers`, `returns`, `seller`, `seller_feedback_pct`, `seller_feedback_count`, `location`, `image`, `results_total`; values depend on the source display. The schema also retains item-page fields `quantity_available`, `breadcrumbs`, `category`, `item_specifics`, `seller_url`, `rating`, `ratings_count`, but current item-page access is unreliable, so their presence in the schema is not a promise of detail delivery. A `status` row (free, one per keyword or URL) says `ok`, `no_results` or `error`, with `items`, `filtered`, `duplicates` and `results_total`. A search that matches nothing is a free `no_results` row; an eBay refusal is `error`, never an empty success; bad input ends the run with the reason on the run card and nothing charged.

## eBay listings: what does this scraper collect?

Every item row uses the same columns; fields not present in the source can be null. Item-page fields remain in the schema for compatibility, but that mode is currently unreliable.

| Field | What it is |
| --- | --- |
| `item_id` | eBay's numeric listing id — the number in any `/itm/` URL |
| `title` | Listing title as the seller wrote it |
| `url` | Canonical item page URL |
| `query` / `search_url` | The keyword, and the exact URL the page was read from |
| `page` / `position` | Where the listing sat in eBay's own order, counted across pages |
| `domain` / `marketplace` | Supported host such as `com`, `de` or `fr`, and the country name |
| `price` / `price_display` / `currency` | The number, the string exactly as printed, and the currency read from the price itself. `price` is null on the occasional MAP-restricted listing where eBay prints "See price" instead of a number — `price_display` then says so, and price bounds drop those rows free |
| `list_price` / `list_price_display` / `discount_pct` | The struck-through original and how far below it the listing sits |
| `shipping_cost` / `shipping_display` / `free_shipping` | Delivery charge as a number, the full line, and the free-delivery flag |
| `condition` | Brand New, Pre-Owned, Open Box, Certified - Refurbished, For parts … |
| `buying_format` | `buy_it_now` or `auction` |
| `bids` / `time_left` | Auction rows: bid count and eBay's own countdown text |
| `best_offer` | Whether the seller accepts offers |
| `units_sold` | How many units this listing has sold |
| `watchers` | How many shoppers are watching it |
| `returns` | The returns line, e.g. "Free returns" or "30 days returns" |
| `seller` / `seller_feedback_pct` / `seller_feedback_count` | Username or store, positive-feedback percentage, and the score expanded from eBay's `40.6K` shorthand to `40600` |
| `location` | Where the item ships from |
| `image` | Listing image URL |
| `rating` / `ratings_count` | Product star rating, when the listing is matched to a catalogue product |
| `results_total` | How many listings eBay reports for the whole search |
| `quantity_available`, `breadcrumbs`, `category`, `item_specifics`, `seller_url` | Item-page fields: availability text, category path, leaf category, seller's specifics table and store URL. Currently unreliable; search rows do not supply these details |
| `fetched_at` | UTC timestamp |

A second row type, `status`, is emitted once per keyword or URL and is **always free**: `kind`, `target`, `status` (`ok` / `no_results` / `error`), `items`, `filtered`, `duplicates`, `pages`, `results_total`, `error`, `fetched_at`. Read it to know that a job ran and what it produced, without inferring anything from row counts.

## eBay search results by keyword: how do I get them?

To scrape eBay search results by keyword, give it keywords and a depth. Each page carries 60 listings.

```json
{
  "queries": ["mechanical keyboard", "keycap set"],
  "domain": "com",
  "pages": 2,
  "maxResultsPerQuery": 60
}
```

That run reads two pages per keyword, keeps the first 60 listings of each in eBay's own order, and charges for 120 rows at most — fewer if a keyword returns fewer.

## How do I use my own eBay search URL?

Build an active-listing search on a supported eBay marketplace and copy its URL into `startUrls`. Supported search filters are retained; paging is controlled by the Actor. Sold/completed flags (`LH_Sold` and `LH_Complete`) are stripped, so passing those URLs does not enable sold-price history. The marketplace comes from the URL, so one run can mix supported countries. UK and the other unsupported marketplaces remain a source-coverage limitation, not an input-format workaround.

```json
{
  "startUrls": [
    "https://www.ebay.com/sch/i.html?_nkw=lego+star+wars&_sacat=19006",
    "https://www.ebay.de/sch/i.html?_nkw=nintendo+switch+oled"
  ],
  "pages": 3
}
```

Individual item URLs are still accepted by `startUrls`, but **item-detail mode is currently unreliable**. All 3 fresh US URLs checked on 2026-11-06 were blocked before a detail row could be extracted. Keep search URL mode separate from item-page enrichment; a returned item URL does not establish that this Actor can fetch its details.

## How does the price filter save me money?

`minPrice` and `maxPrice` become eBay's own `_udlo` and `_udhi` parameters, so eBay does the filtering **before it sends the page**. You pay for the pages that come back, not for thousands of rows you throw away afterwards. The bound is then checked a second time here, because eBay applies its own bound to price *plus shipping* in some views and a row can still arrive outside your range — anything that fails the second check is dropped and never billed. Those drops show up in the `filtered` count on the status row.

```json
{
  "queries": ["vintage pocket watch"],
  "minPrice": 50,
  "maxPrice": 400,
  "buyingFormat": "auction",
  "sortBy": "ending_soonest",
  "pages": 2
}
```

`buyingFormat`, `conditions`, `category` and `sortBy` are server-side in exactly the same way. `conditions` is a multi-select because eBay grades refurbished in four separate tiers — Certified, Excellent, Very good, Good — and a filter that sends only "refurbished" silently drops most of that market.

## Can I add item specifics to eBay search results?

**Do not rely on this workflow currently.** On 2026-11-06, a US search returned 3 listings, then item-page requests for those same 3 fresh URLs returned no detail rows after eBay challenge/error responses. Search-card rows do not fetch `item_specifics`, `quantity_available`, `category` or `seller_url` automatically. A successful search does not guarantee a successful second stage.

The existing input still accepts item URLs in `startUrls`. When item-page access works, enriching a search result requires a separate run: duplicate item IDs are delivered only once within a run, so combining search and item URLs may keep the search row. This describes the input contract, not a currently verified enrichment path. If item specifics are required, use a source with verified item-detail access.

Billing remains $0.004 per delivered item in each run: ten search rows cost $0.04; a separate detail run would cost another $0.04 only if it actually delivered ten detail rows. Blocked attempts and error status rows incur no item charge, as observed in the current check. Neither input mode supports UK listings or sold/completed transaction history.

## eBay price research: how do I compare a market?

Point the actor at a product's keywords, take the whole first page or two, and the distribution answers the question. This is bulk ebay data extraction with the analysis columns already attached. `price` plus `shipping_cost` is the real landed cost, and it is the number ebay buy it now shoppers actually compare. `units_sold` tells you which of those prices has ever transacted. The ebay units sold figure is the strongest signal on the page. The ebay watchers count tells you where interest sits without a sale yet, and a listing with many ebay watchers and no sales is usually priced above the market. `results_total` tells you how crowded the listing is. `condition` lets you split the used market from the new one, `best_offer` shows which sellers will negotiate — an ebay best offer flag on most of a page means the printed prices are ceilings, not clearing prices — and ebay seller feedback lets you discount the outliers from accounts nobody buys from.

A practical routine for resellers and sourcing teams:

1. Run the keyword with `sortBy: "price_low"` and `pages: 2` to find the floor.
2. Run it again with `buyingFormat: "auction"` and `sortBy: "ending_soonest"` to see what is clearing right now. That is ebay auction data in its most useful form: `bids` and `time_left` on those rows are live competition, and a lot of bids with little time left is a price about to be proved.
3. Sort your export by `units_sold` descending. The top rows are the listings that have proven the price.
4. Compare `price` against `list_price` — a large `discount_pct` across many sellers is a category in decline, not a bargain.
5. Schedule the same run daily and diff on `item_id` to watch new listings, price moves and `units_sold` growth.

This is the ebay market research loop that ebay reseller tools charge a monthly subscription for, except it lands in your own dataset and you pay by the row.

## eBay seller data: how do I find who dominates a category?

The `sellers` view groups the same rows by who is selling. `seller_feedback_count` is expanded from eBay's abbreviated card display, so `40.6K` becomes `40600` and you can sort on it numerically. Combined with `units_sold`, `location` and `condition`, this ebay seller feedback view is enough to find the handful of accounts that dominate a category, to check whether they are stores or private sellers, and to see how their pricing differs from the long tail. Auction cards do not print the seller line, so those search rows can lack seller data. Item-page enrichment is currently unreliable and should not be relied on to fill it.

## eBay marketplaces: which ones are supported?

`com`, `de`, `fr`, `it`, `es`, `nl`, `pl`, `com.au`, `com.sg`, `com.my` — ten, each measured on 2026-08-29 (re-measured 2026-10-11) returning a full 60-listing page on the first request. Set `domain` for keyword searches, or paste marketplace URLs into `startUrls` and mix as many as you like in one run.

Six hosts are deliberately **not** offered: eBay UK, Ireland, Canada, Switzerland, Hong Kong and (since 2026-10-11, 0 of 47 attempts on every pool and a home IP) Austria; the first five answered eBay's anti-bot challenge on 18 of 18 attempts, across datacentre and residential proxies, country-pinned and not, warm and cold — while Germany and Australia answered 5 of 5 on the same proxies in the same minute. eBay's posture there is per-host and outside our control, and listing them as supported would sell you a run that cannot finish. Do not use these hosts for a supported workflow; pasting a URL does not add support. If a pasted URL is refused, it returns `status: "error"` rather than an empty market. We re-check this on every release. Condition labels, buying-format wording and the shipping line are all parsed in each site's own language, so a German run returns `Gebraucht` and `Sofort-Kaufen` rather than nulls. `currency` is read from the rendered price rather than assumed from the marketplace, because eBay localises the price block to the caller's egress and a run proxied through another country would otherwise be labelled with the wrong currency.

## How much does it cost?

Pay per event: **$0.004 per listing row**, and nothing else. There is no per-run start fee and no compute charge on top.

- A search that returns nothing is free.
- Listings where eBay withholds the price ("See price") are dropped free whenever you have set a price bound.
- Rows dropped by your price bounds are free.
- A listing found by two of your keywords is delivered and billed **once** per run.
- `status` rows are free.
- If your spending limit is reached mid-run, the run stops delivering rather than delivering rows it could not charge for — you never receive unpaid data and never pay for data you did not receive.

One page of 60 listings is $0.24. Five keywords × two pages × 60 delivered listings × $0.004 is at most $2.40 per run, or $72 for 30 daily runs at the current rate.

## Every input, explained

| Input | Default | What it does |
| --- | --- | --- |
| `queries` | `[]` | Keywords to search, one job each |
| `startUrls` | `[]` | Active eBay search URLs with supported filters; item URLs remain accepted but detail access is currently unreliable |
| `domain` | `com` | Marketplace for the keyword searches (10 supported hosts; UK unsupported) |
| `buyingFormat` | `all` | `all`, `buy_it_now` or `auction` |
| `conditions` | `[]` | Multi-select of the nine eBay condition grades |
| `minPrice` | `0` | Lower bound, sent to eBay and re-checked before billing |
| `maxPrice` | `0` | Upper bound; `0` means none |
| `category` | `""` | eBay numeric category id (the `_sacat` number in any category URL) |
| `sortBy` | `best_match` | `best_match`, `ending_soonest`, `newly_listed`, `price_low`, `price_high` |
| `pages` | `1` | Result pages per job, 60 listings each, up to 34 |
| `maxResultsPerQuery` | `0` | Cap per job; `0` means everything the pages returned |
| `sessions` | `4` | Parallel proxy sessions (egress IPs) |
| `perIp` | `0.5` | Requests per second per IP |
| `proxyConfiguration` | Apify Proxy | Required; the run escalates to residential on its own |

## How do I call it from Python, JavaScript or curl?

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/ebay-search-scraper").call(run_input={
    "queries": ["mechanical keyboard"],
    "pages": 2,
    "minPrice": 30,
    "maxPrice": 200,
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "item":
        print(row["price"], row["currency"], row["units_sold"], row["title"])
```

JavaScript (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/ebay-search-scraper').call({
    queries: ['keycap set'],
    pages: 1,
    sortBy: 'price_low',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((r) => r.type === 'item').length, 'listings');
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~ebay-search-scraper/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H 'content-type: application/json' \
  -d '{"queries":["vintage pocket watch"],"buyingFormat":"auction","pages":1}'
```

## Does it work with n8n, Make and AI agents?

Yes. The actor is a standard Apify Actor, so it appears in the **n8n** Apify node and in **Make**'s Apify app as "Run an Actor", and the dataset comes back as ordinary JSON you can map straight into a sheet, a database or an alert. For agents, the Apify **MCP** server exposes it as a callable tool, so an AI agent can ask for eBay listings by keyword and get typed rows back rather than a page of HTML. The `status` rows make it safe for an agent to run unattended: a failure is a row with `status: "error"` and a readable message, never a silently empty result.

Zapier, Airtable and Google Sheets all work through the same dataset endpoint, and the "Run Actor and get dataset" pattern needs no code.

## eBay API alternative: why not use the official API?

The eBay Browse API is excellent if you are already an eBay developer: you register an application, complete the onboarding, manage OAuth tokens and live inside its rate limits and its field set. For a one-off market study, a price watch, a sourcing spreadsheet or an agent tool, that is a lot of ceremony. This actor is the ebay api alternative for those cases — paste keywords, get rows, pay for what you got. It also returns things the catalogue-shaped API does not surface the same way: the struck-through list price a seller is advertising against, the watcher count, the units already sold on that specific listing, and the exact position the listing held in eBay's own results.

If you need order management, listing creation, or guaranteed contractual access, use the official API. If you need to read the public market, use this.

## Does this scraper collect eBay sold items?

**No, and here is why.** eBay's completed and sold search — the `LH_Sold=1&LH_Complete=1` view — is behind a **sign-in gate**. A logged-out request to it is redirected to `signin.ebay.<tld>` with `sgfl=srch`, on every marketplace. We verified this on 2026-08-29 across seven marketplaces, datacentre and residential proxies in seven countries, eight different URL routes including eBay's own "Sold items" rail link and the RSS feed, and three browser fingerprints: **not one of roughly 115 attempts returned sold results.** A headless browser does not change the answer, because the block is an HTTP redirect and not a JavaScript challenge — only a signed-in eBay account gets through, which we will not do on your behalf or ours.

So this actor scrapes active listings only, and says so plainly rather than shipping a "sold" toggle that returns nothing. If you came here for ebay sold items to build price comps, the honest substitute is the `units_sold` column: it is the number of units a live listing has actually sold at its current price, published by eBay on the public results page, and for pricing decisions it answers most of the same question — *has anyone paid this?* — using data that is genuinely available.

## FAQ

### How many listings are on each eBay page?

Sixty. The actor requests `_ipg=60`, which is eBay's ceiling. `pages: 3` therefore reads up to 180 listings per job. eBay stops paginating any single search at roughly 2000 items however many it reports in `results_total`, which is why `pages` is capped at 34.

### Why did my search return no rows?

Either eBay genuinely found nothing, or the run was refused. The two are never confused: a genuine miss produces a status row with `status: "no_results"` and costs nothing, and a refusal produces `status: "error"` with the reason. This matters more than it sounds — eBay's zero-result page still renders about twenty "results matching fewer words" cards from *other* searches, and a scraper that delivers those bills you for listings you never asked for. This one drops them.

### Do I need a proxy?

Yes, and Apify Proxy is the default. eBay is behind Akamai Bot Manager and refuses unrotated callers with a `/splashui/challenge` interstitial. The run opens several proxy sessions, warms each one against the marketplace homepage, paces every session separately, retries on a different IP whenever a page is refused, and escalates from datacentre to residential proxies by itself once eBay has pushed back twice. Measured at one request per second on 2026-08-29: datacentre answered 5 of 10 searches and residential 8 of 10. These historical search checks do not guarantee current access; on 2026-11-06, all 3 tested item URLs remained blocked despite retries.

### Are sponsored listings flagged?

There is deliberately no `sponsored` column. eBay's current results page prints the (deliberately obfuscated) "Sponsored" disclosure on **every** card — 60 of 60 on four different searches across two marketplaces and both buying formats, all from the same organic results module. A column that is always `true` is worse than no column, so we left it out and documented the finding instead.

### Can I track prices over time?

Yes — schedule the run and keep the datasets. Each row carries `fetched_at`, `item_id` and `price`, which is everything a time series needs. A daily run of the same keywords, appended to one table and grouped by `item_id`, gives you an ebay price tracker with the listing's `units_sold` and `watchers` moving alongside the price, which is far more informative than the price alone.

### What about eBay Kleinanzeigen or eBay Motors?

Kleinanzeigen is a separate site with its own markup and is not covered. Motors search listings use the same search-row format. Vehicle-specific attributes would require item-page `item_specifics`, and that mode is currently unreliable; do not choose this Actor when those attributes are required.

### Is scraping eBay legal?

This actor reads only publicly available pages — the same search results and item pages any visitor sees without logging in — and collects no personal data beyond the seller usernames and store names eBay itself publishes next to every listing. Public-data scraping of this kind is broadly lawful in the US and the EU, and courts have repeatedly declined to treat access to a public web page as unauthorised access. That is not the whole story, though: eBay's own Terms of Service restrict automated access, so scraping can be a contractual matter between you and eBay even where it is not a legal one. You are responsible for your own use — respect robots directives and rate limits, do not republish listing content wholesale, keep collection proportionate to your purpose, and take your own legal advice for anything commercial. We do not scrape anything behind a login, and we will not: that is exactly why the sold-listings view above is absent rather than faked.

### How do I find an eBay category id?

Open any eBay category in a browser and read the `_sacat` number out of the URL, or click into a category from a search and copy it from the address bar. Pass it as `category` and every keyword in the run is searched inside that category only.

## Changelog and support

See `CHANGELOG.md` for version history. If a field stops populating, open an issue on the actor's Issues tab with the input you used — the parsers are covered by an offline test suite built from captured pages, and a fixture from a real failing run is the fastest possible fix.

## Related scrapers

eBay is one marketplace. These read the others, with the same row-per-item shape and the same pay-per-delivered-row billing:

- [Amazon Product Scraper](https://apify.com/kestrel/amazon-product-scraper) — one ASIN in, the whole product page out: buybox and list price, stock flag, gallery, bullet points and the details table, across 20 marketplaces — the Amazon column of a price-spread table.
- [Amazon Search Scraper](https://apify.com/kestrel/amazon-search-scraper) — Amazon keyword results with page position and a sponsored flag, when you want to know what ranks for a phrase there the way this actor tells you for eBay.
- [Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper) — the Top 100 of any Amazon category with every rank filled, plus New Releases, for demand ranking rather than price.
- [Amazon Reviews Scraper](https://apify.com/kestrel/amazon-reviews-scraper) — customer reviews and ratings by ASIN with filters that run before billing, for the feedback behind a listing you priced here.
- [AliExpress Reviews Scraper](https://apify.com/kestrel/aliexpress-reviews-scraper) — buyer feedback with photos, the variant chosen and the buyer's country, for checking a supplier's product before you list it on eBay.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
