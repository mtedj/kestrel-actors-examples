# Zillow Properties - Rentals, New Listings & Price Changes

Zillow Properties collects rentals with price changes for repeatable business research. Search Zillow properties from city search URLs. One row per property or rental building: address, price, beds, baths, area, status and URL; building unit options included. Price and bedroom filters; monitor new listings and price changes. Parsed pages are billed even when no rows match. Export results as JSON, CSV or Excel, or connect a saved task to an existing workflow. This actor is independent of the source platform. Last verified working: 2026-10-30.

## Zillow Properties for AI agents: which input answers which request?

Use this actor for the public search records described below. Read both pricing events before estimating a run: a successful page check can cost money even when it returns no matching or changed rows. Result counts alone do not describe the complete bill.

| Request | Input |
|---|---|
| Small first sample | `{"searchUrls": ["https://www.zillow.com/austin-tx/"], "maxResultsPerSource": 3}` |
| Repeated monitoring | `{"searchUrls": ["https://www.zillow.com/austin-tx/"], "maxResultsPerSource": 3, "onlyNewOrChanged": true, "monitorKey": "daily-watch"}` |
| Apply the main optional features | `{"searchUrls": ["https://www.zillow.com/austin-tx/"], "maxResultsPerSource": 3, "minPrice": 200000, "maxPrice": 700000, "minBeds": 3}` |
| Exclude records already stored elsewhere | Add `excludeIds` using exact output `id` values. |
| Cap spend | Set `maxTotalChargeUsd: 1` in Apify run options, outside the input JSON. |

## Zillow Properties input: how do I start?

```json
{
  "searchUrls": [
    "https://www.zillow.com/austin-tx/"
  ],
  "maxResultsPerSource": 3
}
```

Each source runs sequentially. `maxResultsPerSource` limits delivered matches after filters, monitoring and deduplication. `maxPagesPerSource` separately limits source search pages. Asking for fifty rows does not guarantee that fifty matches are available. When a page contains fewer than the requested rows, the actor follows recognized source pagination until it reaches a limit or the source ends.

| Field | Meaning |
|---|---|
| `searchUrls` | Zillow city sale or rental search URLs, for example ["https://www.zillow.com/austin-tx/"] or ["https://www.zillow.com/austin-tx/rentals/"]. Up to 20. HTTPS www.zillow.com only; property-detail and building-detail URLs are not accepted. Query parameters from pasted searches are preserved. |
| `maxResultsPerSource` | Maximum matching rows per search after filters and monitoring; for example 50. Default 50, maximum 1000. A ceiling, not a guarantee. Deduplicated across the run; Google IDs include domain, query and country; only the first visible result per domain is kept. |
| `minPrice` | Minimum price in source numeric fields, for example 400000. Zero disables the bound. Missing values do not pass active bounds; rental buildings usually have null scalar price/beds and are excluded when those bounds are active. Unit options are preserved separately. |
| `maxPrice` | Maximum price in source numeric fields, for example 400000. Zero disables the bound. Missing values do not pass active bounds; rental buildings usually have null scalar price/beds and are excluded when those bounds are active. Unit options are preserved separately. |
| `minBeds` | Minimum bedrooms in source numeric fields, for example 3. Zero disables the bound. Missing values do not pass active bounds; rental buildings usually have null scalar price/beds and are excluded when those bounds are active. Unit options are preserved separately. |
| `maxBeds` | Maximum bedrooms in source numeric fields, for example 3. Zero disables the bound. Missing values do not pass active bounds; rental buildings usually have null scalar price/beds and are excluded when those bounds are active. Unit options are preserved separately. |
| `onlyNewOrChanged` | true emits new IDs or changes in price text, numeric price, currency, status or building unit options. First run delivers the baseline; use the same monitorKey later. Successful unchanged checks still pay page fees. Default false. |
| `titleContains` | Keep titles containing any phrase, case-insensitive, for example ["engineer"]. For Zillow, title is building name or address. Empty disables it. Applied before row billing; parsed pages are still billed. |
| `titleExcludes` | Drop titles containing any phrase, case-insensitive, for example ["senior"]. Empty disables it. Filtered rows have no row fee; parsed pages still carry their fee. |
| `monitorKey` | Persistent history name, for example "daily-watch". Use 1–60 letters, digits, underscores or hyphens. Use the same targets, filters and name for repeat runs. Keeps the latest 50,000 delivered IDs. Do not overlap runs sharing this name. |
| `excludeIds` | Skip exact output id values. Up to 10,000. Useful for external deduplication; excluded rows have no row fee, but parsed pages are billed. |
| `maxPagesPerSource` | Safety cap on parsed pages per search, for example 5. Default 5, maximum 20. Each parsed page costs $0.02, including filtered or unchanged checks. Both this cap and maxResultsPerSource apply. |

## Zillow Properties output: what is a result row?

One row is one property. Main keys: `id`, `zpid`, `listing_type`, `title`, `url`, `address`, `street`, `city`, `state`, `zipcode`, `price`, `price_text`, `currency`, `status`, `status_text`, `beds`, `baths`, `area_sqft`, `home_type`, `latitude`, `longitude`, `days_on_zillow`, `broker_name`, `unit_options`, `image_url`, `source_url`, `search_url`, `fetched_at`, `change`, `previous_price`, `price_change`. Missing source values stay null. Use `id` for deduplication and keep `fetched_at` to distinguish an observation time from source posting dates. The source URL records the search page used for that observation.

The key-value store's `SUMMARY` record contains parsed pages, delivered rows, duplicates, filtered and unchanged rows, charge counts, per-source statuses and errors. It is not a paid dataset row. A source refusal or unknown layout is an error, not fabricated empty data. If there are errors and no rows can be delivered, the run fails. A partial run retains valid rows and records errors in SUMMARY. Check that record before assuming a successful partial run covered all inputs.

## How much does the actor cost?

A successfully parsed page costs **$0.02** ($20 per 1,000 pages). Each delivered property costs **$0.002** ($2 per 1,000 rows).  No start fee; proxy and compute are included.

One page and ten basic rows cost **$0.040**. One successfully parsed page with zero matches or zero changes costs **$0.02**. Failed source requests and unrecognized page responses have no page fee. Filtered, duplicate, excluded and unchanged rows have no row fee. Successfully parsed search pages retain their fee even if a later job-description request or destination-link resolution fails.

A conservative ceiling is `number_of_sources × (maxPagesPerSource × page_price + maxResultsPerSource × row_price)`. Use the enriched-job row price if descriptions are enabled. Set the monetary `maxTotalChargeUsd` run option for a hard charge cap. Work stops before requesting another page when the remaining budget cannot cover its page fee and one chosen row event. Billing failures stop subsequent work.

Charging, dataset writing and monitor-state writing are separate platform operations. An interruption between them can leave a charged row unwritten or a delivered row not remembered. Use event counters and SUMMARY to investigate interrupted runs. Monetary limits apply to charged events; page and result caps also bound source work.

## How do monitoring and schedules work?

```json
{
  "searchUrls": [
    "https://www.zillow.com/austin-tx/"
  ],
  "maxResultsPerSource": 3,
  "onlyNewOrChanged": true,
  "monitorKey": "daily-watch"
}
```

The first monitored run delivers the matching baseline. Later runs with the same monitor name suppress unchanged records already delivered. Property comparisons include price, price text, currency, status and building unit options. A status-only change can therefore have price_change=0.

History keeps the most recently delivered 50,000 IDs in a named key-value store under the account running the actor. Evicted older IDs may reappear. Reuse the same targets and filters; change monitorKey when starting an independent baseline. Overlapping runs sharing one key are not transactionally coordinated, so configure schedules without overlap. No schedule is created automatically: save an Apify task and add an Apify Schedule for daily or weekly execution. Unchanged checks still incur parsed-page charges.

## How do filters work?

Title inclusion matches any listed phrase, case-insensitively. Title exclusion removes a row when any excluded phrase matches. Empty arrays disable these filters. Numeric bounds use zero to disable the bound; missing values do not pass an active bound. Filtering happens before row billing but after fetching and parsing a paid page. The actor may inspect several pages to find the requested number of matching results.

## What are the source limitations?

This actor reads Zillow city search cards for sale and rental searches. It does not visit individual property-detail pages, retrieve owner contacts, compute valuations or provide historical transactions. Listings may contain property cards or rental buildings. A building has listing_type="building", a stable building ID, zpid=null and source unit_options; its scalar price, beds and currency can be null. Active numeric filters exclude missing scalar values and do not infer a whole building from its cheapest unit. Prices are source asking prices, not sold prices or totals including fees. Area is the listing card area in square feet. The source can cap visible search pages even when the reported total is much larger. Existing saved-search query parameters are preserved, but unsupported paths fail validation. A rejected or unrecognized Zillow response is retried at most twice through a fresh US residential proxy; only a successfully parsed replacement page is billed.

Public sources change over time and may temporarily refuse requests. These actors use bounded requests, response sizes and page counts; they do not promise complete historical coverage. For legal use, respect source terms and applicable law, and obtain rights required for downstream reuse. No separate source credentials, cookies or commercial data API key are requested.

## How do I call the API from Python, JavaScript or curl?

Python:

```python
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/zillow-property-search").call(run_input={'searchUrls': ['https://www.zillow.com/austin-tx/'], 'maxResultsPerSource': 3}, max_total_charge_usd=1)
rows = client.dataset(run["defaultDatasetId"]).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/zillow-property-search').call({"searchUrls": ["https://www.zillow.com/austin-tx/"], "maxResultsPerSource": 3}, { maxTotalChargeUsd: 1 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~zillow-property-search/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" -H 'Content-Type: application/json' \
  -d '{"searchUrls": ["https://www.zillow.com/austin-tx/"], "maxResultsPerSource": 3}'
```

The asynchronous endpoint returns a run record. Wait for completion before reading the dataset and SUMMARY. The same inputs can be used in n8n, Make and MCP clients. A monetary run option must not be passed as an invented actor-input field.

## FAQ: why did I receive fewer rows than requested?

Result caps are ceilings. Filters, source pagination, source errors, repeated records, monitoring and the monetary cap can all reduce delivery. Inspect per-source status in SUMMARY to identify the stopping reason. Do not increase the result limit alone if the page cap is the limiting factor.

### Can I export the data to a spreadsheet?

Yes. Apify datasets support CSV and Excel exports. Preserve IDs and observation timestamps when merging repeat runs into another system. Null values should remain missing rather than being displayed as measured zero values.
