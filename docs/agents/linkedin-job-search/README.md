# LinkedIn Jobs - Job Descriptions & New Jobs

LinkedIn Jobs collects job descriptions with new jobs for repeatable business research. Search LinkedIn jobs by keyword and location. One row per job: title, company, location, posted date, URL and available salary text. Optional job descriptions; company, title and date filters. Monitor new jobs across runs. Parsed pages are billed even when filters or monitoring leave no rows. Export results as JSON, CSV or Excel, or connect a saved task to an existing workflow. This actor is independent of the source platform. Last verified working: 2026-10-30.

## LinkedIn Jobs for AI agents: which input answers which request?

Use this actor for the public search records described below. Read both pricing events before estimating a run: a successful page check can cost money even when it returns no matching or changed rows. Result counts alone do not describe the complete bill.

| Request | Input |
|---|---|
| Small first sample | `{"queries": ["data engineer"], "maxResultsPerSource": 3}` |
| Repeated monitoring | `{"queries": ["data engineer"], "maxResultsPerSource": 3, "onlyNew": true, "monitorKey": "daily-watch"}` |
| Apply the main optional features | `{"queries": ["data engineer"], "maxResultsPerSource": 3, "includeDetails": true, "companies": ["Microsoft"], "postedWithinDays": 7}` |
| Exclude records already stored elsewhere | Add `excludeIds` using exact output `id` values. |
| Cap spend | Set `maxTotalChargeUsd: 1` in Apify run options, outside the input JSON. |

## LinkedIn Jobs input: how do I start?

```json
{
  "queries": [
    "data engineer"
  ],
  "maxResultsPerSource": 3
}
```

Each source runs sequentially. `maxResultsPerSource` limits delivered matches after filters, monitoring and deduplication. `maxPagesPerSource` separately limits source search pages. Asking for fifty rows does not guarantee that fifty matches are available. When a page contains fewer than the requested rows, the actor follows recognized source pagination until it reaches a limit or the source ends.

| Field | Meaning |
|---|---|
| `queries` | Search keywords, for example ["data engineer"]. Up to 20 queries. Each query has independent page and delivered-result limits. No separate source account or API key required. |
| `maxResultsPerSource` | Maximum delivered job rows per query, after filters, monitoring and cross-query deduplication. Default 50; maximum 1000. IDs are LinkedIn job IDs, so different jobs at the same company or linkedin.com can all be returned. The same job appearing in several queries is delivered once across the run. Source availability and page caps can leave fewer rows. |
| `location` | Location passed to LinkedIn public search, for example "United States" or "London". Default United States. Source search can include nearby locations; this is not an exact city filter. |
| `includeDetails` | true fetches full public description, seniority, employment type, job function and industries when available. Charges $0.004 per delivered enriched job instead of $0.001 for a listing-only job. Failed descriptions are skipped with an error and no job fee. Page fees still apply. |
| `companies` | Keep company names containing any phrase, case-insensitive, for example ["Microsoft"]. Empty means all. Applied to visible search results before job billing; it does not discover a company directory. |
| `postedWithinDays` | Keep jobs whose source posted_date is within this number of UTC calendar days, for example 7. Zero disables it. Missing dates do not pass an active filter. This filters inspected pages; it does not guarantee every recent job. |
| `onlyNew` | true emits job IDs not previously delivered. First run delivers the baseline; use the same monitorKey later. Successful unchanged checks still pay page fees. Default false. |
| `titleContains` | Keep titles containing any phrase, case-insensitive, for example ["engineer"]. Empty disables it. Applied before row billing; parsed pages are still billed. |
| `titleExcludes` | Drop titles containing any phrase, case-insensitive, for example ["senior"]. Empty disables it. Filtered rows have no row fee; parsed pages still carry their fee. |
| `monitorKey` | Persistent history name, for example "daily-watch". Use 1–60 letters, digits, underscores or hyphens. Use the same targets, filters and name for repeat runs. Keeps the latest 50,000 delivered IDs. Do not overlap runs sharing this name. |
| `excludeIds` | Skip exact output id values. Up to 10,000. Useful for external deduplication; excluded rows have no row fee, but parsed pages are billed. |
| `maxPagesPerSource` | Safety cap on parsed pages per search, for example 5. Default 5, maximum 20. Each parsed page costs $0.005, including filtered or unchanged checks. Both this cap and maxResultsPerSource apply. |

## LinkedIn Jobs output: what is a result row?

One row is one job. Main keys: `id`, `job_id`, `title`, `url`, `company`, `company_url`, `location`, `posted_date`, `posted_text`, `salary_text`, `logo_url`, `description`, `seniority`, `employment_type`, `job_function`, `industries`, `query`, `search_location`, `source_url`, `fetched_at`, `change`. Missing source values stay null. Use `id` for deduplication and keep `fetched_at` to distinguish an observation time from source posting dates. The source URL records the search page used for that observation.

The key-value store's `SUMMARY` record contains parsed pages, delivered rows, duplicates, filtered and unchanged rows, charge counts, per-source statuses and errors. It is not a paid dataset row. A source refusal or unknown layout is an error, not fabricated empty data. If there are errors and no rows can be delivered, the run fails. A partial run retains valid rows and records errors in SUMMARY. Check that record before assuming a successful partial run covered all inputs.

## How much does the actor cost?

A successfully parsed page costs **$0.005** ($5 per 1,000 pages). Each delivered job costs **$0.001** ($1 per 1,000 rows). With includeDetails=true, a job with a successful description costs $0.004 instead of $0.001; these two row events are mutually exclusive. A description failure skips that job and records an error, with no job fee. No start fee; proxy and compute are included.

One page and ten basic rows cost **$0.015**. One successfully parsed page with zero matches or zero changes costs **$0.005**. Failed source requests and unrecognized page responses have no page fee. Filtered, duplicate, excluded and unchanged rows have no row fee. Successfully parsed search pages retain their fee even if a later job-description request or destination-link resolution fails.

A conservative ceiling is `number_of_sources × (maxPagesPerSource × page_price + maxResultsPerSource × row_price)`. Use the enriched-job row price if descriptions are enabled. Set the monetary `maxTotalChargeUsd` run option for a hard charge cap. Work stops before requesting another page when the remaining budget cannot cover its page fee and one chosen row event. Billing failures stop subsequent work.

Charging, dataset writing and monitor-state writing are separate platform operations. An interruption between them can leave a charged row unwritten or a delivered row not remembered. Use event counters and SUMMARY to investigate interrupted runs. Monetary limits apply to charged events; page and result caps also bound source work.

## How do monitoring and schedules work?

```json
{
  "queries": [
    "data engineer"
  ],
  "maxResultsPerSource": 3,
  "onlyNew": true,
  "monitorKey": "daily-watch"
}
```

The first monitored run delivers the matching baseline. Later runs with the same monitor name suppress unchanged records already delivered. A job is new only if its ID has not previously been delivered; changed descriptions do not make it new.

History keeps the most recently delivered 50,000 IDs in a named key-value store under the account running the actor. Evicted older IDs may reappear. Reuse the same targets and filters; change monitorKey when starting an independent baseline. Overlapping runs sharing one key are not transactionally coordinated, so configure schedules without overlap. No schedule is created automatically: save an Apify task and add an Apify Schedule for daily or weekly execution. Unchanged checks still incur parsed-page charges.

## How do filters work?

Title inclusion matches any listed phrase, case-insensitively. Title exclusion removes a row when any excluded phrase matches. Empty arrays disable these filters. Numeric bounds use zero to disable the bound; missing values do not pass an active bound. Filtering happens before row billing but after fetching and parsing a paid page. The actor may inspect several pages to find the requested number of matching results.

## What are the source limitations?

This actor reads public LinkedIn guest job search, not logged-in member profiles or recruiter-only information. Job search currently supplies about ten cards per page; available volume and ordering can change. Location is a source search hint and can include nearby jobs. Descriptions require includeDetails=true. Salary text is returned only when the public card supplies it; no salary estimate, compensation normalization, employee emails, applicant data or application submission is included. Job types and seniority are source labels from optional details, not inferred from titles. A failed public search or description request gets at most one residential-proxy retry; failed attempts are not billed as successful events. Source duplicates may end pagination early. Empty job feeds can indicate the end of public results. This is not a promise of the full LinkedIn jobs database.

Public sources change over time and may temporarily refuse requests. These actors use bounded requests, response sizes and page counts; they do not promise complete historical coverage. For legal use, respect source terms and applicable law, and obtain rights required for downstream reuse. No separate source credentials, cookies or commercial data API key are requested.

## How do I call the API from Python, JavaScript or curl?

Python:

```python
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/linkedin-job-search").call(run_input={'queries': ['data engineer'], 'maxResultsPerSource': 3}, max_total_charge_usd=1)
rows = client.dataset(run["defaultDatasetId"]).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/linkedin-job-search').call({"queries": ["data engineer"], "maxResultsPerSource": 3}, { maxTotalChargeUsd: 1 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~linkedin-job-search/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" -H 'Content-Type: application/json' \
  -d '{"queries": ["data engineer"], "maxResultsPerSource": 3}'
```

The asynchronous endpoint returns a run record. Wait for completion before reading the dataset and SUMMARY. The same inputs can be used in n8n, Make and MCP clients. A monetary run option must not be passed as an invented actor-input field.

## FAQ: why did I receive fewer rows than requested?

Result caps are ceilings. Filters, source pagination, source errors, repeated records, monitoring and the monetary cap can all reduce delivery. Inspect per-source status in SUMMARY to identify the stopping reason. Do not increase the result limit alone if the page cap is the limiting factor.

### Can I export the data to a spreadsheet?

Yes. Apify datasets support CSV and Excel exports. Preserve IDs and observation timestamps when merging repeat runs into another system. Null values should remain missing rather than being displayed as measured zero values.
