# AliExpress Product Search - Prices, Ratings & Sales

AliExpress Product Search provides prices and ratings as structured research data. Search AliExpress products by keywords with US/USD locale preferences. One row per product: title, displayed price, rating, sales label, discount, promotions and URL. Filter price or rating; skip saved IDs or hashes. Welcome offers are labeled; prices are not checkout quotes.

Product-research agents comparing advertised offers and source demand labels, with explicit promotional-price caveats. This independent community Actor is maintained by kestrel and is not affiliated with or endorsed by the source platform. Only an Apify token is needed for API use; no source-site password, account cookies or extra paid API key is required.

## AliExpress Product Search for AI agents: which input answers which request?

Use this Actor for the specific data contract below. Fields absent from the source stay null; errors do not become fabricated results. Search-card observations using US region and USD preference cookies, without login. Any page returning another currency is rejected before billing. USD currency is verified; the source does not provide a reliable confirmation of delivery destination, so do not treat this as a shipping quote. Prices may be for selected variants, welcome offers, coupons, bundles or other conditions. price_is_promotional, promotion_tags and selling_points retain those qualifications. sales_text is a display label, not an exact order count. No complete variants, supplier contacts, checkout prices or review bodies are collected.

| Request | Input or action |
|---|---|
| First small sample | `{"queries": ["ceramic mug"], "maxResults": 3, "maxPagesPerSource": 1}` |
| Apply useful filters | `{"queries": ["ceramic mug"], "maxResults": 3, "maxPagesPerSource": 1, "maxPrice": 10, "minRating": 4.5}` |
| Skip records already collected | Add `excludeIds` from the previous dataset's `id` values. |
| Return new or changed observations | Add `excludeContentHashes` from previous `content_hash` values. Do not also exclude their IDs if changes matter. |
| Repeat tomorrow | Save the input as an Apify Task, schedule it, and carry prior IDs or hashes in your workflow. This Actor does not create schedules or persist history. |
| Set a dollar limit | Pass `maxTotalChargeUsd: 1` in Apify run options, outside the Actor input JSON. |

## AliExpress Product Search: how do I make the first call?

```json
{
  "queries": [
    "ceramic mug"
  ],
  "maxResults": 3,
  "maxPagesPerSource": 1
}
```

`maxResults` is a **global cap across the whole run**, after filtering and deduplication. It is not a promise that this many matches exist. Targets run in input order; earlier targets may exhaust the global cap. Use separate runs when each target needs its own budget. `maxPagesPerSource` controls the depth per query/video. A small cap can leave later targets unvisited. Duplicate inputs and duplicate row IDs are removed across the run.

## AliExpress Product Search: what are the inputs and filters?

| Field | Meaning |
|---|---|
| `queries` | Required search phrases, e.g. ["project management"]. Up to 20 queries, visited in order. One maxResults cap is shared across the whole run. Use specific terms in any language. Successful parsed pages and delivered matching rows are separate paid events. |
| `maxResults` | Maximum paid rows across the ENTIRE run after filters, deduplication and exclusions. Default 20; range 1–1000. Earlier targets can fill this cap. Set maxTotalChargeUsd in the Apify run options for a dollar cap; it is not an input field. |
| `titleContains` | Optional case-insensitive OR substring filter on the video/product title, e.g. ["wireless", "bluetooth"]. Empty disables. Filters run before maxResults; inspected pages still carry page fees. No extra filter fee. |
| `minPrice` | Minimum displayed USD price, e.g. 5. 0 disables. Source offer conditions still apply. Missing prices fail an active price filter. Filters before maxResults. No extra filter fee. |
| `maxPrice` | Maximum displayed USD price, e.g. 50. 0 disables. This is not a checkout-total or shipping-inclusive limit. Missing prices fail an active filter; minimum must not exceed a positive maximum. No extra filter fee. |
| `minRating` | Minimum source star rating from 0 to 5, e.g. 4.5. 0 disables. Missing ratings fail a positive threshold. No sentiment is inferred. Filters before maxResults; no extra filter fee. |
| `excludeSponsored` | false (default) keeps sponsored and organic cards. true keeps only source-confirmed organic cards; unknown sponsorship is also excluded. Filters before maxResults; no extra filter fee. |
| `maxPagesPerSource` | Maximum successfully parsed result pages per query/video, default 2; range 1–20. Each page has a fee even if filters leave zero rows. Bootstrap/sort requests are included in that fee. This limits search depth, not a guarantee of enough matching results. |
| `excludeIds` | Row id values from a previous dataset, e.g. [] on the first run. Up to 5,000 IDs. Skips matching IDs even if their content changed. Excluded rows have no row fee; parsed-page fees still apply. Keep IDs in your workflow; no history is stored automatically. |
| `excludeContentHashes` | Prior content_hash values, e.g. [] initially. Up to 5,000 SHA-256 values. Skips unchanged records while allowing changed prices/text/metrics through. Collection time, query, page position and images do not affect hashes. Caller-managed history; parsed-page fees apply. |

Unknown inputs and invalid bounds fail before source requests. Empty keyword filters disable filtering. Phrase lists use case-insensitive OR matching. Missing numeric values do not pass an active threshold. Filters and exclusions apply before the result limit, so the Actor continues within the page budget to find matches. It never invents a price, rating, stock label or engagement count.

## What does a result look like?

One dataset row is one **product**. Main keys: `product_id, title, price, currency, rating, sales_text, discount_percent, promotion_tags, url`. Every row includes `id`, `source_url`, `content_hash` and `fetched_at`. The example below is a captured public-source observation, not a promise that the source will keep the same values.

```json
{
  "id": "3256813221675352",
  "type": "product",
  "product_id": "3256813221675352",
  "title": "300ml Handmade Ceramic Mug with 3D Shell Design Ocean-Themed Underglaze Coffee Cup Reusable Hand Wash Only for Tea Coffee Creative Gifts Coffee Bar Accessory",
  "query": "ceramic mug",
  "url": "https://www.aliexpress.com/item/3256813221675352.html",
  "price": 1.09,
  "price_text": "US $1.09",
  "currency": "USD",
  "discount_percent": 97,
  "rating": null,
  "sales_text": "2 sold",
  "selling_points": [
    "Fastest delivery in 5 days",
    "Free shipping",
    "$51.41 saved",
    "New shoppers - $51.41",
    "Save $51.41"
  ],
  "promotion_tags": [
    "ETA_atm",
    "Free_Shipping_atm",
    "attributeCountry",
    "bigSale_atm",
    "localplus_flag",
    "welcomedeal_save_atm",
    "card_new_user_welcomedeal_atm",
    "welcomedeal_test",
    "bigSale_discount"
  ],
  "price_is_promotional": true,
  "sponsored": false,
  "image_url": "https://ae-pic-a1.aliexpress-media.com/kf/S5314c05b950c4ca6a596672fd079f678H.jpg",
  "page": 1,
  "source_url": "https://www.aliexpress.com/w/wholesale-ceramic-mug.html?SearchText=ceramic+mug&page=1",
  "content_hash": "19b0032eed23b72199d90f1b0a9d56346298615036b1b087c8fb9c7aa28bca17",
  "fetched_at": "2026-11-08T08:24:23.738738+00:00"
}
```

The key-value store's `SUMMARY` record contains per-target outcomes, source request and parsed-page counts, delivered/filtered/duplicate counts, charged events, errors and the spending-limit flag. Summary/status information is not a paid dataset row. A partial run can retain useful results while listing failures in SUMMARY. If every attempted source fails, the run fails. A recognized empty source is different from an unavailable or blocked source.

## What does it cost?

- **Parsed page:** $0.008 each ($8 per 1,000 pages).
- **Delivered product:** $0.002 each ($2 per 1,000 rows), in addition to parsed pages.
- No start fee. Proxy and compute are included in those event prices.

One parsed page with three delivered rows costs **$0.014**. One successfully parsed page with no matches costs **$0.008**. Invalid input and failed/blocked source responses have no page or row fee. Filtered, duplicate and excluded records have no row fee, but their inspected pages are still paid. Bootstrap and sort-control requests are included in the parsed-page fee. A parsed page may hold many source records; only matching delivered rows get the row event.

With N unique targets, a conservative maximum before a dollar cap is:

`N × maxPagesPerSource × 0.008 + maxResults × 0.002`

The Actor checks available budget before advancing to another source page and requires enough room for one page plus at least one row. A cap below **$0.01** performs no source requests and produces no charges. It stops after a billing failure rather than returning unpaid rows. Charges and dataset writes are separate platform operations; an interruption can leave charged rows unwritten. SUMMARY distinguishes billing and delivery failures.

## How does repeat monitoring work across runs?

Save each result's `id` and `content_hash`. Use `excludeIds` to retrieve unseen identities only, or `excludeContentHashes` to keep changed prices/text/metrics eligible. Both are caller-managed lists with at most 5,000 values. The hash excludes collection time, query, page position and image URLs. Changing source values or labels changes the hash; a hash change does not by itself prove a price change. Compare the relevant fields yourself.

No history is stored automatically, and no schedule is created. Source search rankings and availability can change between runs. Search results are not a complete inventory; absence from a later search does not prove a product was discontinued or a record was deleted. Use a saved task or your own workflow for repeated calls, carry your history, and avoid overlapping schedules if your workflow updates shared state.

## How do I call it through the API or MCP?

Python (apify-client 3.x):

```python
from decimal import Decimal
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/aliexpress-product-search").call(run_input={'queries': ['ceramic mug'], 'maxResults': 3, 'maxPagesPerSource': 1}, max_total_charge_usd=Decimal("1"))
assert run is not None and run.status == "SUCCEEDED", run
rows = client.dataset(run.default_dataset_id).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/aliexpress-product-search').call(
  {"queries": ["ceramic mug"], "maxResults": 3, "maxPagesPerSource": 1}, { maxTotalChargeUsd: 1 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~aliexpress-product-search/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"queries": ["ceramic mug"], "maxResults": 3, "maxPagesPerSource": 1}'
```

The same input works in n8n and Make integrations. The asynchronous endpoint returns a run record. Wait for a terminal status, then retrieve its default dataset and SUMMARY. MCP clients can discover `kestrel/aliexpress-product-search`, read its schema and call it through Apify. Inspect the current MCP call schema for supported run options; do not invent a spending-cap input if that MCP tool does not expose one. Use the Apify API when a monetary cap is required and the client lacks that option.

## FAQ: what should I check when a run returns fewer results?

Check SUMMARY for page limits, filtering, duplicates, exclusions, source failures and spending limits. A successful zero-row check can still have a page fee. Public layouts and access can change. This Actor uses bounded timeouts, response-size limits and retries; an unrecognized response is an error, not empty success. No complete historical archive, permanent availability or commercial outcome is guaranteed.

Export JSON for nested fields or CSV/Excel through Apify's dataset export. Preserve IDs and observation timestamps in downstream reports. For legal use, respect source terms and applicable rights when using or sharing collected data.

Last verified working: 2026-11-08 (public-source probes; each published build is additionally checked in Apify).
