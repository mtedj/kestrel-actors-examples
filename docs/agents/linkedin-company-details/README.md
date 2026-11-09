# LinkedIn Companies - Industry, Size & Websites

LinkedIn Companies provides structured industry and size for research workflows. Read public LinkedIn company pages by company URL or slug. One row per company: industry, size band, headquarters, website, followers and description. Filter industry, size or text; skip saved IDs or hashes for monitoring. Company details only, without employee lists or email enrichment.

Company-enrichment and market-research agents with an existing list of public LinkedIn organization URLs. This independent community Actor is maintained by kestrel and is not affiliated with or endorsed by the source platform. API use requires an Apify token. No source-site password, account cookies or additional paid API key is required.

## LinkedIn Companies for AI agents: which input answers which request?

Public organization pages only. Supply named /company/ URLs or slugs, not numeric IDs, personal profiles or search URLs. Industry and size filters select from the supplied companies; they do not search LinkedIn for new companies. linkedin_members_count counts LinkedIn profiles associated with the organization and is not payroll headcount. company_size is the published band. No employees, founder lookup, email addresses, revenue estimates or jobs. Missing source fields stay null. A source error is never fabricated into an empty successful result. Filtering selects from the provided targets or returned search records; it does not expand the underlying source coverage.

| Request | Input or action |
|---|---|
| First small sample | `{"companyUrls": ["https://www.linkedin.com/company/google/", "https://www.linkedin.com/company/apify/"], "maxResults": 3, "maxSources": 2}` |
| Apply useful filters | `{"companyUrls": ["https://www.linkedin.com/company/google/", "https://www.linkedin.com/company/apify/"], "maxResults": 3, "maxSources": 2, "hasWebsite": "yes", "minFollowers": 1000}` |
| Keep only unseen identities | Supply prior dataset `id` values in `excludeIds`. |
| Keep new or changed observations | Supply prior `content_hash` values in `excludeContentHashes`; do not exclude their IDs too. |
| Repeat monitoring tomorrow | Save an Apify Task, schedule it and carry history in your own workflow. |
| Cap dollar spend | Set `maxTotalChargeUsd` in Apify run options, outside input JSON. |

## LinkedIn Companies: how do I make the first call?

```json
{
  "companyUrls": [
    "https://www.linkedin.com/company/google/",
    "https://www.linkedin.com/company/apify/"
  ],
  "maxResults": 3,
  "maxSources": 2
}
```

`maxResults` is a global paid-row cap across the whole run, after filters, deduplication and exclusions. Earlier targets can fill the cap and leave later targets unvisited. It is not a guarantee that enough matching records exist. Use separate runs if every target must receive an independent quota. `maxSources` caps attempted source targets, including unsuccessful attempts. A source is one profile, Page or company, or one App Store query/ID and country combination. Duplicate targets collapse before collection.

## LinkedIn Companies: inputs, filters and limits

| Field | Meaning |
|---|---|
| `companyUrls` | Required named LinkedIn /company/ URLs or slugs, e.g. ["https://www.linkedin.com/company/apify/"]. Up to 100. No personal profiles, numeric IDs or search URLs. Industry/size filters apply only to these supplied companies. Each valid company check has a source fee plus a fee for its delivered row. |
| `maxResults` | Maximum paid rows across the ENTIRE run after filters, deduplication and exclusions. Default 20; range 1–1000. Earlier targets can fill it. Set maxTotalChargeUsd in Apify run options for a dollar cap, not inside this input JSON. |
| `minFollowers` | Minimum profile/Page/company follower count, e.g. 1000. 0 disables. Missing values fail an active filter; source-rounded values remain approximate. Filters before maxResults. No extra filter fee; successfully checked sources are paid. |
| `industries` | Optional exact case-insensitive industry labels, e.g. ["Software Development"]. Copy labels from a first run; [] disables. Filters supplied company URLs only, not a company-discovery query. Applied before maxResults; checked-source fees still apply. |
| `companySizes` | Optional exact case-insensitive published size bands, e.g. ["51-200 employees"]. Copy actual company_size labels from a first run; [] disables. Not an exact payroll headcount or LinkedIn search. Filters before maxResults; checked-source fees apply. |
| `textContains` | Optional case-insensitive OR phrases, e.g. ["software", "education"]. Matches name, bio/description, industry or category when present. [] disables. Applied before maxResults; skipped rows have no row fee, but successful source checks are paid. |
| `hasWebsite` | "any" (default) keeps all. "yes" keeps rows with a published website/bio link; "no" keeps rows without one. The link is not fetched or verified for reachability. App Store uses sellerUrl. Filters before maxResults; no filter fee, source checks remain paid. |
| `maxSources` | Maximum source targets attempted across the run, default 20; range 1–100. One profile/Page/company or one app query/ID and country is one source. Failed attempts count toward this limit but have no source fee. Valid empty/filtered sources are paid. No extra filter fee. |
| `excludeIds` | Prior dataset id values, e.g. [] initially; up to 5,000. Skips identities even when they changed. App IDs include country, e.g. "310633997:DE". Excluded rows are free, source checks are paid. Keep history in your workflow; no automatic persistence. |
| `excludeContentHashes` | Prior content_hash values, e.g. [] initially; up to 5,000 SHA-256 values. Skips unchanged observations but allows changed fields through. Time, query, position and image URL are excluded from the hash. Do not also exclude IDs when changes matter. Source checks remain paid; no stored history. |

Unknown input fields, unsupported URLs and invalid bounds fail before source requests. Missing numeric fields fail an active positive threshold. Text lists are case-insensitive OR filters; empty lists disable them. All optional filters are free to apply, but the successful checks needed to inspect source records are paid. A filter that leaves no rows does not imply a free run. Check the source-check counter as well as the delivered-row counter.

## What is in the output?

One dataset row is one **company**. Main keys: `name, industry, company_size, headquarters, website, followers, linkedin_members_count`. Every row includes `id`, `url`, `source_url`, `content_hash` and `fetched_at`. The example below is a minimized public-source observation; long descriptions are excerpts and current values can differ.

```json
{
  "id": "10608457",
  "type": "company",
  "platform": "linkedin",
  "slug": "apify",
  "company_urn": "urn:li:organization:10608457",
  "name": "Apify",
  "url": "https://cz.linkedin.com/company/apify",
  "description": "Apify is the largest marketplace of trusted tools for AI. More than 100,000 Actors to automate your business. Get real-time",
  "industry": "Technology, Information and Internet",
  "company_size": "201-500 employees",
  "headquarters": "Prague",
  "organization_type": "Privately Held",
  "founded": null,
  "specialties": "Web scraping, Browser automation, AI agents, API integration, Data pipelines, No-code tools, Actor marketplace, and Developer platform",
  "linkedin_members_count": 274,
  "followers": 47484,
  "website": "https://apify.com/",
  "street_address": "Vodickova 704/36",
  "city": "Prague",
  "region": null,
  "postal_code": "11100",
  "country": "CZ",
  "image_url": null,
  "source_url": "https://www.linkedin.com/company/apify/",
  "content_hash": "27d6148582e8d0734e66be58610ad8b630803aff4b076b283424f6bfcdc0689b",
  "fetched_at": "2026-11-09T05:56:13.403502+00:00"
}
```

The key-value store's `SUMMARY` record gives attempted and checked sources, source requests, delivered/filtered/duplicate counts, charged events, per-target outcomes, errors and budget flags. Summary records are not paid dataset rows. A run with some useful sources and some failures reports partial success with errors in SUMMARY. When every attempted source fails, the run fails. A recognized empty App Store response is different from a blocked, redirected, private or unavailable source.

## What does it cost?

- **Source checked:** $0.002 per valid source ($2 per 1,000 checks).
- **Delivered company:** $0.002 per row ($2 per 1,000 rows), in addition to source checks.
- No start fee. Proxy and compute are included in these event prices.

One checked source returning one row costs **$0.004**. A valid source with no matching rows costs **$0.002**. Invalid input, blocked responses and failed source requests have no source or row fee. Duplicate, filtered and excluded records have no row fee. Requests used for a bounded retry are included in a successful source's fee. For App Store search, one query/country with three delivered apps costs the source fee plus three app fees; ID lookup can return at most one app in a country.

A conservative maximum before a monetary cap is `min(number of targets, maxSources) × 0.002 + maxResults × 0.002`. App Store targets equal countries multiplied by the combined number of unique queries and app IDs. The Actor requires room for a source check plus at least one row before fetching another target. A cap below **$0.004** does no source work. It stops when billing fails or the platform's event-charge limit is reached. Charging and dataset writes are separate operations; a delivery interruption can leave a charged row unwritten, which SUMMARY records explicitly.

## How does repeat monitoring work?

Save IDs, hashes and observation times in your workflow. `excludeIds` suppresses an identity even when its content changed; use it only for unseen-identity collection. `excludeContentHashes` suppresses unchanged observations and keeps changed fields eligible. For change monitoring, avoid passing both the old ID and its hash, because the ID exclusion would also hide the update. A new hash is a signal to compare relevant fields, not proof of a specific follower, price or version change.

Hashes omit collection time, query, position, image URLs and selected display labels. The Actor does not retain a previous dataset, calculate growth rates, create schedules or emit deletion events. Save an Apify Task or use your own scheduler, carry forward up to 5,000 hashes and avoid overlapping jobs that overwrite the same workflow state. A missing row can result from filters, access errors, coverage limits or a spending cap; it does not by itself prove an account or app disappeared.

## How do I call it through the API or MCP?

Python (apify-client 3.x):

```python
from decimal import Decimal
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/linkedin-company-details").call(run_input={'companyUrls': ['https://www.linkedin.com/company/google/', 'https://www.linkedin.com/company/apify/'], 'maxResults': 3, 'maxSources': 2}, max_total_charge_usd=Decimal("1"))
assert run is not None and run.status == "SUCCEEDED", run
rows = client.dataset(run.default_dataset_id).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/linkedin-company-details').call(
  {"companyUrls": ["https://www.linkedin.com/company/google/", "https://www.linkedin.com/company/apify/"], "maxResults": 3, "maxSources": 2}, { maxTotalChargeUsd: 1 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~linkedin-company-details/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"companyUrls": ["https://www.linkedin.com/company/google/", "https://www.linkedin.com/company/apify/"], "maxResults": 3, "maxSources": 2}'
```

The same input works through n8n and Make. The asynchronous API returns a run record; wait for completion before reading the dataset and SUMMARY. MCP clients can discover `kestrel/linkedin-company-details`, fetch its input schema and call it through Apify. Check the currently exposed tool schema for run options. If the MCP client lacks a monetary-cap option, use the Apify API for calls that require a dollar limit; do not invent an input named maxTotalChargeUsd.

## FAQ: why are there fewer rows than requested?

Check SUMMARY for filters, exclusions, duplicate IDs, source limits, failed requests and the spending cap. Increasing a result cap does not create more source records. Public access and layouts can change, and retries are bounded. The Actor never logs source-account credentials because none are supplied; source errors are summarized without proxy secrets. Returned website links are observations and are not fetched, so a URL can be stale or unavailable. JSON preserves nested lists; CSV or Excel export is available through Apify's dataset export. Respect source terms and applicable legal rights when using or sharing the observations.

Last verified working: 2026-11-09 (public-source probes; published builds also pass Apify cloud checks).
