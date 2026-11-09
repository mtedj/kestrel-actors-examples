# Apple App Store Apps - Search, Ratings & Versions

Apple App Store Apps provides structured ratings and versions for research workflows. Search Apple App Store apps by keywords or numeric app IDs across country storefronts. One row per app and country: developer, rating, rating count, version, price, currency and URL. Filter rating, free or paid apps and developer names; skip saved IDs or hashes for app research and monitoring.

App research, competitor monitoring and release-tracking agents comparing storefront-specific app metadata. This independent community Actor is maintained by kestrel and is not affiliated with or endorsed by the source platform. API use requires an Apify token. No source-site password, account cookies or additional paid API key is required.

## Apple App Store Apps for AI agents: which input answers which request?

Apple public software search and app lookup metadata, with no account login. Search has one response per query/country, up to searchLimit requested records; Apple may return fewer or cap coverage. There is no pagination, complete market inventory, keyword search-volume metric, download count, revenue estimate, review text or historical version archive. App price is the upfront storefront price, not subscription or in-app purchase pricing. Countries select storefronts, not developer locations. Ratings and availability vary by country. Missing source fields stay null. A source error is never fabricated into an empty successful result. Filtering selects from the provided targets or returned search records; it does not expand the underlying source coverage.

| Request | Input or action |
|---|---|
| First small sample | `{"queries": ["budget planner"], "countries": ["US"], "maxResults": 3, "maxSources": 1}` |
| Apply useful filters | `{"queries": ["budget planner"], "countries": ["US"], "maxResults": 3, "maxSources": 1, "minRating": 4, "priceType": "free"}` |
| Keep only unseen identities | Supply prior dataset `id` values in `excludeIds`. |
| Keep new or changed observations | Supply prior `content_hash` values in `excludeContentHashes`; do not exclude their IDs too. |
| Repeat monitoring tomorrow | Save an Apify Task, schedule it and carry history in your own workflow. |
| Cap dollar spend | Set `maxTotalChargeUsd` in Apify run options, outside input JSON. |

## Apple App Store Apps: how do I make the first call?

```json
{
  "queries": [
    "budget planner"
  ],
  "countries": [
    "US"
  ],
  "maxResults": 3,
  "maxSources": 1
}
```

`maxResults` is a global paid-row cap across the whole run, after filters, deduplication and exclusions. Earlier targets can fill the cap and leave later targets unvisited. It is not a guarantee that enough matching records exist. Use separate runs if every target must receive an independent quota. `maxSources` caps attempted source targets, including unsuccessful attempts. A source is one profile, Page or company, or one App Store query/ID and country combination. Duplicate targets collapse before collection.

## Apple App Store Apps: inputs, filters and limits

| Field | Meaning |
|---|---|
| `queries` | App Store search phrases, e.g. ["budget planner"]. Up to 20; any language. Provide queries, appIds or both. Each query/country combination is a separate paid source check. Search is bounded by searchLimit; no pagination or complete-inventory guarantee. |
| `appIds` | Numeric App Store IDs as strings, e.g. ["310633997"]. Up to 100. No URLs or bundle IDs. Provide appIds, queries or both. Each ID/country combination is a paid source check, including a valid not-found response. IDs are checked before keyword searches within each country. |
| `countries` | App Store storefront country codes, e.g. ["US"] (default) or ["DE", "JP"]. Not developer nationality. Supported: US, GB, CA, AU, DE, FR, JP, IN, AE, SG, BR, ES, IT. Each country multiplies source checks. Local currencies retained; no conversion. A row id combines app ID and country so the same app in two markets yields two rows. |
| `maxResults` | Maximum paid rows across the ENTIRE run after filters, deduplication and exclusions. Default 20; range 1–1000. Earlier targets can fill it. Set maxTotalChargeUsd in Apify run options for a dollar cap, not inside this input JSON. |
| `searchLimit` | Requested results in each App Store keyword response, e.g. 50 (default), range 1–200. Apple can return fewer. This is search depth before filters, not a per-query delivered-row cap. One source fee per valid response plus delivered-app fees; no pagination. Does not change ID lookups. |
| `minRating` | Minimum App Store rating from 0 to 5, e.g. 4.5. 0 disables. Missing ratings fail a positive threshold. Ratings are storefront-specific. Applied before maxResults; no extra filter fee, successful source checks still cost money. |
| `priceType` | "all" (default), "free" for upfront price 0, or "paid" for price greater than 0 in the local storefront currency. Missing prices fail an active filter. This does not classify subscription or in-app purchase costs. No filter fee; source checks remain paid. |
| `developerContains` | Optional case-insensitive OR phrases in the app developer name, e.g. ["Google"]. [] disables. Filters returned apps before maxResults; it is not a developer-catalog lookup. No extra filter fee; source checks are paid. |
| `textContains` | Optional case-insensitive OR phrases, e.g. ["software", "education"]. Matches name, bio/description, industry or category when present. [] disables. Applied before maxResults; skipped rows have no row fee, but successful source checks are paid. |
| `hasWebsite` | "any" (default) keeps all. "yes" keeps rows with a published website/bio link; "no" keeps rows without one. The link is not fetched or verified for reachability. App Store uses sellerUrl. Filters before maxResults; no filter fee, source checks remain paid. |
| `maxSources` | Maximum source targets attempted across the run, default 20; range 1–100. One profile/Page/company or one app query/ID and country is one source. Failed attempts count toward this limit but have no source fee. Valid empty/filtered sources are paid. No extra filter fee. |
| `excludeIds` | Prior dataset id values, e.g. [] initially; up to 5,000. Skips identities even when they changed. App IDs include country, e.g. "310633997:DE". Excluded rows are free, source checks are paid. Keep history in your workflow; no automatic persistence. |
| `excludeContentHashes` | Prior content_hash values, e.g. [] initially; up to 5,000 SHA-256 values. Skips unchanged observations but allows changed fields through. Time, query, position and image URL are excluded from the hash. Do not also exclude IDs when changes matter. Source checks remain paid; no stored history. |

Unknown input fields, unsupported URLs and invalid bounds fail before source requests. Missing numeric fields fail an active positive threshold. Text lists are case-insensitive OR filters; empty lists disable them. All optional filters are free to apply, but the successful checks needed to inspect source records are paid. A filter that leaves no rows does not imply a free run. Check the source-check counter as well as the delivered-row counter.

## What is in the output?

One dataset row is one **app** in one country storefront. Main keys: `app_id, country, name, developer, rating, rating_count, version, price, currency, url`. Every row includes `id`, `url`, `source_url`, `content_hash` and `fetched_at`. The example below is a minimized public-source observation; long descriptions are excerpts and current values can differ.

```json
{
  "id": "1621020173:US",
  "type": "app",
  "platform": "app_store",
  "app_id": "1621020173",
  "country": "US",
  "name": "Fleur - Budget Planner App",
  "url": "https://apps.apple.com/us/app/fleur-budget-planner-app/id1621020173?uo=4",
  "query": "budget planner",
  "position": 1,
  "developer": "Akash Jain",
  "developer_id": "1473155604",
  "developer_url": "https://apps.apple.com/us/developer/akash-jain/id1473155604?uo=4",
  "website": "https://fleur.app",
  "seller_name": "Akash Jain",
  "bundle_id": "com.fleurbudget",
  "description": "Fleur is a cute, aesthetic, and simple budget planner and expense tracker. Easily record your daily expenses and income, set",
  "price": 0,
  "currency": "USD",
  "rating": 4.80077,
  "rating_count": 13191,
  "current_version_rating": 4.80077,
  "current_version_rating_count": 13191,
  "version": "3.1.6",
  "released_at": "2022-05-22T07:00:00Z",
  "updated_at": "2026-10-28T08:47:15Z",
  "minimum_os_version": "15.0",
  "size_bytes": 109469696,
  "content_rating": "4+",
  "primary_genre": "Finance",
  "genres": [
    "Finance",
    "Productivity"
  ],
  "languages": [
    "BG",
    "HR",
    "CS",
    "DA",
    "NL",
    "EN",
    "FI",
    "FR",
    "DE",
    "HU",
    "ID",
    "IT",
    "JA",
    "KO",
    "LT",
    "MS",
    "NB",
    "PL",
    "PT",
    "RO",
    "RU",
    "ZH",
    "SK",
    "ES",
    "SV",
    "ZH",
    "TR",
    "UK"
  ],
  "image_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/74/fc/f8/74fcf890-bc07-cd0f-84c3-9f68384310cf/NewFleurSingleAppIcon-0-0-1x_U007epad-0-1-0-85-220.png/512x512bb.jpg",
  "source_url": "https://itunes.apple.com/search?term=budget+planner&entity=software&country=US&limit=20",
  "content_hash": "cfd3deced88a46b258b4a256cbea98414b2c84b932b7d355c6fd0f671eb7f1b1",
  "fetched_at": "2026-11-09T05:56:13.405610+00:00"
}
```

The key-value store's `SUMMARY` record gives attempted and checked sources, source requests, delivered/filtered/duplicate counts, charged events, per-target outcomes, errors and budget flags. Summary records are not paid dataset rows. A run with some useful sources and some failures reports partial success with errors in SUMMARY. When every attempted source fails, the run fails. A recognized empty App Store response is different from a blocked, redirected, private or unavailable source.

## What does it cost?

- **Source checked:** $0.002 per valid source ($2 per 1,000 checks).
- **Delivered app:** $0.0005 per row ($0.5 per 1,000 rows), in addition to source checks.
- No start fee. Proxy and compute are included in these event prices.

One checked source returning one row costs **$0.0025**. A valid source with no matching rows costs **$0.002**. Invalid input, blocked responses and failed source requests have no source or row fee. Duplicate, filtered and excluded records have no row fee. Requests used for a bounded retry are included in a successful source's fee. For App Store search, one query/country with three delivered apps costs the source fee plus three app fees; ID lookup can return at most one app in a country.

A conservative maximum before a monetary cap is `min(number of targets, maxSources) × 0.002 + maxResults × 0.0005`. App Store targets equal countries multiplied by the combined number of unique queries and app IDs. The Actor requires room for a source check plus at least one row before fetching another target. A cap below **$0.0025** does no source work. It stops when billing fails or the platform's event-charge limit is reached. Charging and dataset writes are separate operations; a delivery interruption can leave a charged row unwritten, which SUMMARY records explicitly.

## How does repeat monitoring work?

Save IDs, hashes and observation times in your workflow. `excludeIds` suppresses an identity even when its content changed; use it only for unseen-identity collection. `excludeContentHashes` suppresses unchanged observations and keeps changed fields eligible. For change monitoring, avoid passing both the old ID and its hash, because the ID exclusion would also hide the update. A new hash is a signal to compare relevant fields, not proof of a specific follower, price or version change.

Hashes omit collection time, query, position, image URLs and selected display labels. The Actor does not retain a previous dataset, calculate growth rates, create schedules or emit deletion events. Save an Apify Task or use your own scheduler, carry forward up to 5,000 hashes and avoid overlapping jobs that overwrite the same workflow state. A missing row can result from filters, access errors, coverage limits or a spending cap; it does not by itself prove an account or app disappeared.

## How do I call it through the API or MCP?

Python (apify-client 3.x):

```python
from decimal import Decimal
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/app-store-app-discovery").call(run_input={'queries': ['budget planner'], 'countries': ['US'], 'maxResults': 3, 'maxSources': 1}, max_total_charge_usd=Decimal("1"))
assert run is not None and run.status == "SUCCEEDED", run
rows = client.dataset(run.default_dataset_id).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/app-store-app-discovery').call(
  {"queries": ["budget planner"], "countries": ["US"], "maxResults": 3, "maxSources": 1}, { maxTotalChargeUsd: 1 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~app-store-app-discovery/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"queries": ["budget planner"], "countries": ["US"], "maxResults": 3, "maxSources": 1}'
```

The same input works through n8n and Make. The asynchronous API returns a run record; wait for completion before reading the dataset and SUMMARY. MCP clients can discover `kestrel/app-store-app-discovery`, fetch its input schema and call it through Apify. Check the currently exposed tool schema for run options. If the MCP client lacks a monetary-cap option, use the Apify API for calls that require a dollar limit; do not invent an input named maxTotalChargeUsd.

## FAQ: why are there fewer rows than requested?

Check SUMMARY for filters, exclusions, duplicate IDs, source limits, failed requests and the spending cap. Increasing a result cap does not create more source records. Public access and layouts can change, and retries are bounded. The Actor never logs source-account credentials because none are supplied; source errors are summarized without proxy secrets. Returned website links are observations and are not fetched, so a URL can be stale or unavailable. JSON preserves nested lists; CSV or Excel export is available through Apify's dataset export. Respect source terms and applicable legal rights when using or sharing the observations.

Last verified working: 2026-11-09 (public-source probes; published builds also pass Apify cloud checks).
