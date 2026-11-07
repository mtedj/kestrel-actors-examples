# Google Shopping Products - Prices, Merchants & Changes

Google Shopping collects products with prices for repeatable research and monitoring. Search Google Shopping products by keyword and country. One row per product offer: title, price, currency, merchant, rating and delivery text. Merchant and price filters; monitor price changes between runs. Parsed pages are billed even when filters or unchanged prices leave no rows. Export the dataset as JSON, CSV or Excel, or connect it to an existing automation. Last verified working: 2026-10-30.

## Google Shopping for AI agents: which input answers which request?

Use this actor when the customer needs the public records described here. Read the input fields and pricing events before setting a budget. A successful check can cost money without returning rows: parsed pages and delivered records are separate paid units. Do not use a result count alone to estimate the entire bill.

| Request | Input |
|---|---|
| First small sample | `{"queries": ["wireless headphones"], "maxResultsPerSource": 3}` |
| Repeat checks with persistent memory | `{"queries": ["wireless headphones"], "maxResultsPerSource": 3, "onlyNewOrChanged": true, "monitorKey": "daily-watch"}` |
| Apply numeric filters | `{"queries": ["wireless headphones"], "maxResultsPerSource": 3, "minPrice": 20, "maxPrice": 100, "titleExcludes": ["case"]}` |
| Skip records from another system | Add `excludeIds` using the exact returned `id` values. |
| Keep the bill below a dollar | Set `maxTotalChargeUsd: 1` in the Apify run options, outside the input JSON. |

## Google Shopping input: how do I start?

```json
{
  "queries": [
    "wireless headphones"
  ],
  "maxResultsPerSource": 3
}
```

Targets run sequentially. `maxResultsPerSource` limits delivered matches after filtering, exclusions and monitoring. `maxPagesPerSource` limits source reads, so requesting fifty matching rows does not guarantee fifty exist within the inspected pages. Both bounds apply separately to each query or channel. Duplicate rows are removed across the entire run.

| Field | Meaning |
|---|---|
| `queries` | Product keywords, for example ["wireless headphones"]. Up to 50 queries. Each successfully parsed page costs $0.015 and each delivered product costs $0.002. |
| `maxResultsPerSource` | Maximum rows delivered per query/channel after filters and monitoring, for example 50. A source can return fewer. Duplicates are removed across this run. |
| `country` | Search market: us (USD), gb (GBP), de/fr (EUR), ca (CAD) or au (AUD). For example "gb" requests UK offers. Currency is read from the displayed price; no currency conversion. Queries use English interface text. |
| `merchants` | Keep merchant names containing any entry, case-insensitive; for example ["Best Buy"]. Empty means any merchant. Filtering adds no fee; parsed pages still cost $0.015. |
| `minPrice` | Minimum numeric displayed price in that market, for example 20. Zero disables the bound. A source "from" price is compared by its displayed minimum, without shipping or tax. |
| `maxPrice` | Maximum numeric displayed price in that market, for example 100. Zero disables the bound. Filters run before row billing; parsed pages are still billed. |
| `onlyNewOrChanged` | true compares title/merchant product identity and price text/currency with previously delivered rows under monitorKey. First run delivers matches; later runs emit new or changed prices with previous_price. Default false. Unchanged checks still pay parsed-page fees. |
| `titleContains` | Keep titles containing at least one phrase, case-insensitive; for example ["wireless"] or ["math"]. Empty means any title. Applied before row billing; successful page checks are still billed. |
| `titleExcludes` | Drop titles containing any phrase, case-insensitive; for example ["case"] or ["trailer"]. Empty disables exclusions. Dropped rows are not billed; parsed pages are. |
| `monitorKey` | Name for persistent delivered-row history, for example "daily-competitors". Use 1–60 letters, digits, underscores or hyphens. Reuse with the same target list and filters; change it for a new baseline. Keeps the latest 50,000 delivered IDs. |
| `excludeIds` | Skip exact output id values, for example ["a-previous-id"]. Up to 10,000. An optional alternative to persistent monitoring; excluded rows are not billed but parsed pages are. |
| `maxPagesPerSource` | Safety cap on successful page reads per query/channel, for example 5. Maximum 50. Every parsed page costs $0.015, including filtered/unchanged pages. The result limit can stop sooner. Source pagination does not guarantee complete coverage. |

## Google Shopping output: what does one row contain?

One dataset row is one product. Main fields: `id`, `title`, `query`, `country`, `product_id`, `cluster_id`, `offer_id`, `merchant`, `price`, `price_text`, `currency`, `price_is_from`, `rating`, `reviews_text`, `delivery_text`, `source_url`, `google_product_url`, `change`, `previous_price`, `price_change`, `fetched_at`. Fields absent from the source remain null. The key-value store's `SUMMARY` record contains per-source status, parsed pages, found and delivered counts, filter counts, duplicates, monitoring exclusions, event counts, errors and the spending-limit flag. Summary information is not emitted as a paid result row.

The `id` is the recommended key for deduplication. Keep `fetched_at` with exported records so downstream dashboards can distinguish an observation time from the source's own timestamps. Null is different from zero: a missing price, view count or rating should not be displayed as a measured zero.

## How much does each run cost?

The parsed-page event costs **$0.015 per successful source page**, or $15 per 1,000 pages. Each delivered product costs **$0.002**, or $2 per 1,000 rows. No start fee; proxy and compute are included in these event prices.

For example, one page with ten delivered rows costs **$0.035**. One successfully parsed page with no matches or no changes costs **$0.015**. Failed requests and unrecognized responses are not charged. Rows removed by filters, deduplication, monitoring or `excludeIds` have no row charge; their successfully parsed pages still carry the page fee. For N sources, a conservative ceiling before the monetary cap is `N × (maxPagesPerSource × page_price + maxResultsPerSource × row_price)`.

The actor checks available budget before another page and requires enough room for its page fee plus at least one row. It charges only confirmed events and stops after a billing error. Charges and dataset writes are separate platform operations; an interruption between them can leave a charged row unwritten. Use the run's event counters and SUMMARY when investigating an interrupted run.

## How do repeat runs remember previous results?

```json
{
  "queries": [
    "wireless headphones"
  ],
  "maxResultsPerSource": 3,
  "onlyNewOrChanged": true,
  "monitorKey": "daily-watch"
}
```

With `onlyNewOrChanged` enabled, the first run delivers the matching baseline. Later runs reuse the same `monitorKey` to suppress previously delivered records; changed price text or currency produces a new observation with previous_price and price_change. The actor stores the latest 50,000 delivered IDs in a named key-value store under the account running it. Older evicted IDs can reappear. Use separate monitor keys for separate target sets or filter definitions. Overlapping runs sharing a key are not transactionally coordinated; schedule each monitor so its runs do not overlap.

No schedule is created automatically. Save a task and configure an Apify Schedule for daily or weekly checks. A small result limit may cover only the newest visible portion of a source; increase page and result bounds when you need a larger baseline. Successful empty monitoring checks still incur parsed-page charges.

## How do title and numeric filters work?

```json
{
  "queries": [
    "wireless headphones"
  ],
  "maxResultsPerSource": 3,
  "minPrice": 20,
  "maxPrice": 100,
  "titleExcludes": [
    "case"
  ]
}
```

`titleContains` is an OR match: at least one listed phrase must appear, case-insensitively. `titleExcludes` removes a row if any phrase appears. An empty list disables that filter. Numeric bounds use zero to mean disabled. Missing values do not pass an active numeric filter. The actor continues through available pages until it reaches the delivered-result limit, the page limit, the source's end or the spending limit. No filter adds a separate fee.

## What are the source limitations?

This reads public Google Shopping cards, not merchant checkout pages. It does not download images, verify stock, return shipping-inclusive totals or promise every offer on the web. Sponsored placements outside the recognized product-card feed are excluded. Some cards show a starting price with a plus sign; `price_is_from` marks it. Ratings and merchant names can be missing. Currency is never converted. The Google product URL is constructed from the source cluster ID and Google may redirect it; `source_url` is the search page used for the observation. Google may vary cards by market, location, time and experiments. The ID combines market, source product identity and merchant; source identity changes can appear as a new offer.

Public sources can change layouts or temporarily refuse requests. A refusal or unrecognized response is recorded as an error, not fabricated data. If all sources fail, the run fails; a partial run retains successful results and reports other errors in SUMMARY. There is no promise of complete historical coverage or stable source ordering. For legal use, respect source terms and applicable law, and obtain any rights required to reuse content; this actor is independent of the source platform.

## How do I call the API from Python, JavaScript or curl?

Python:

```python
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/google-shopping-products").call(
    run_input={'queries': ['wireless headphones'], 'maxResultsPerSource': 3}, max_total_charge_usd=1
)
rows = client.dataset(run["defaultDatasetId"]).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/google-shopping-products').call(
  {"queries": ["wireless headphones"], "maxResultsPerSource": 3}, { maxTotalChargeUsd: 1 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~google-shopping-products/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"queries": ["wireless headphones"], "maxResultsPerSource": 3}'
```

The asynchronous run endpoint returns a run record. Wait for it to finish, then read its default dataset and SUMMARY. The same inputs work in n8n and Make. MCP clients and AI agents can call the actor after reading its event prices; a monetary run option must not be passed as an invented input field.

## FAQ: does this require another account or API key?

Only your Apify account is required. The actor does not ask for source-site passwords, cookies or a separate commercial data API key. Google SERP proxy access is supplied by the actor and included in the listed fees. Country targeting is preserved on every page. Pages with prices outside the requested market currency are discarded, with at most two retries. Only the successfully parsed replacement page is charged. If all three attempts return the wrong market, the source is reported as an error without a page or row fee.

### Why did I receive fewer rows than requested?

Filters, duplicates, monitoring, source availability, page bounds or your spending limit can all reduce delivery. Check SUMMARY for the actual stop reason. `maxResultsPerSource` is a ceiling, not a guarantee.

### Can I export to a spreadsheet?

Yes. Use Apify's dataset export as CSV or Excel, or read JSON from the Dataset API. Keep IDs and observation timestamps in downstream files so repeat exports can be reconciled.

### Why was a check charged when there were no new rows?

A source page was successfully parsed. That page check is the paid work used to determine whether matching or new data exists. The row event is charged only for rows delivered; parsed-page fees still apply.
