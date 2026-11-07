# YouTube Channel Videos - Uploads, Views & Duration

YouTube Channel Videos collects uploads with views for repeatable research and monitoring. List YouTube channel videos from handles, IDs or channel URLs. One row per upload: title, URL, views, video duration, thumbnail and published text. Filter titles, minimum views and duration; save only new videos. Parsed pages are billed even when filters or monitoring leave no rows. Export the dataset as JSON, CSV or Excel, or connect it to an existing automation. Last verified working: 2026-10-30.

## YouTube Channel Videos for AI agents: which input answers which request?

Use this actor when the customer needs the public records described here. Read the input fields and pricing events before setting a budget. A successful check can cost money without returning rows: parsed pages and delivered records are separate paid units. Do not use a result count alone to estimate the entire bill.

| Request | Input |
|---|---|
| First small sample | `{"channels": ["@3blue1brown"], "maxResultsPerSource": 3}` |
| Repeat checks with persistent memory | `{"channels": ["@3blue1brown"], "maxResultsPerSource": 3, "onlyNew": true, "monitorKey": "daily-watch"}` |
| Apply numeric filters | `{"channels": ["@3blue1brown"], "maxResultsPerSource": 3, "minViews": 100000, "minDurationSeconds": 300, "maxDurationSeconds": 3600}` |
| Skip records from another system | Add `excludeIds` using the exact returned `id` values. |
| Keep the bill below a dollar | Set `maxTotalChargeUsd: 1` in the Apify run options, outside the input JSON. |

## YouTube Channel Videos input: how do I start?

```json
{
  "channels": [
    "@3blue1brown"
  ],
  "maxResultsPerSource": 3
}
```

Targets run sequentially. `maxResultsPerSource` limits delivered matches after filtering, exclusions and monitoring. `maxPagesPerSource` limits source reads, so requesting fifty matching rows does not guarantee fifty exist within the inspected pages. Both bounds apply separately to each query or channel. Duplicate rows are removed across the entire run.

| Field | Meaning |
|---|---|
| `channels` | Public channel handles, UC IDs or HTTPS /@handle and /channel/UC… URLs, for example ["@3blue1brown"]. Up to 50 channels. Regular Videos tab only; Shorts/live tabs, video URLs and playlists are not accepted. Each parsed page costs $0.005 plus $0.001 per delivered video. |
| `maxResultsPerSource` | Maximum rows delivered per query/channel after filters and monitoring, for example 50. A source can return fewer. Duplicates are removed across this run. |
| `minViews` | Keep videos at or above this displayed view count, for example 100000. Zero disables it. YouTube rounds counts such as 2.6M; views_approximate marks these. Missing counts do not pass an active bound. |
| `minDurationSeconds` | Minimum video length in seconds, for example 300 for five minutes. Zero disables the bound. Missing/live durations do not pass an active bound. |
| `maxDurationSeconds` | Maximum video length in seconds, for example 1200 for twenty minutes. Zero disables the bound. Filtering adds no fee; parsed pages still cost $0.005. |
| `onlyNew` | true emits only video IDs not previously delivered under monitorKey. First run establishes the baseline by delivering matching videos. Later checks still pay parsed-page fees, even with no new uploads. Use a saved task and an Apify schedule. |
| `titleContains` | Keep titles containing at least one phrase, case-insensitive; for example ["wireless"] or ["math"]. Empty means any title. Applied before row billing; successful page checks are still billed. |
| `titleExcludes` | Drop titles containing any phrase, case-insensitive; for example ["case"] or ["trailer"]. Empty disables exclusions. Dropped rows are not billed; parsed pages are. |
| `monitorKey` | Name for persistent delivered-row history, for example "daily-competitors". Use 1–60 letters, digits, underscores or hyphens. Reuse with the same target list and filters; change it for a new baseline. Keeps the latest 50,000 delivered IDs. |
| `excludeIds` | Skip exact output id values, for example ["a-previous-id"]. Up to 10,000. An optional alternative to persistent monitoring; excluded rows are not billed but parsed pages are. |
| `maxPagesPerSource` | Safety cap on successful page reads per query/channel, for example 5. Maximum 50. Every parsed page costs $0.005, including filtered/unchanged pages. The result limit can stop sooner. Source pagination does not guarantee complete coverage. |

## YouTube Channel Videos output: what does one row contain?

One dataset row is one video. Main fields: `id`, `video_id`, `title`, `url`, `channel_id`, `channel_name`, `channel_url`, `views`, `views_text`, `views_approximate`, `duration_seconds`, `duration_text`, `published_text`, `thumbnail_url`, `fetched_at`. Fields absent from the source remain null. The key-value store's `SUMMARY` record contains per-source status, parsed pages, found and delivered counts, filter counts, duplicates, monitoring exclusions, event counts, errors and the spending-limit flag. Summary information is not emitted as a paid result row.

The `id` is the recommended key for deduplication. Keep `fetched_at` with exported records so downstream dashboards can distinguish an observation time from the source's own timestamps. Null is different from zero: a missing price, view count or rating should not be displayed as a measured zero.

## How much does each run cost?

The parsed-page event costs **$0.005 per successful source page**, or $5 per 1,000 pages. Each delivered video costs **$0.001**, or $1 per 1,000 rows. No start fee; proxy and compute are included in these event prices.

For example, one page with ten delivered rows costs **$0.015**. One successfully parsed page with no matches or no changes costs **$0.005**. Failed requests and unrecognized responses are not charged. Rows removed by filters, deduplication, monitoring or `excludeIds` have no row charge; their successfully parsed pages still carry the page fee. For N sources, a conservative ceiling before the monetary cap is `N × (maxPagesPerSource × page_price + maxResultsPerSource × row_price)`.

The actor checks available budget before another page and requires enough room for its page fee plus at least one row. It charges only confirmed events and stops after a billing error. Charges and dataset writes are separate platform operations; an interruption between them can leave a charged row unwritten. Use the run's event counters and SUMMARY when investigating an interrupted run.

## How do repeat runs remember previous results?

```json
{
  "channels": [
    "@3blue1brown"
  ],
  "maxResultsPerSource": 3,
  "onlyNew": true,
  "monitorKey": "daily-watch"
}
```

With `onlyNew` enabled, the first run delivers the matching baseline. Later runs reuse the same `monitorKey` to suppress previously delivered records; changed view counts on an existing video do not make that video new. The actor stores the latest 50,000 delivered IDs in a named key-value store under the account running it. Older evicted IDs can reappear. Use separate monitor keys for separate target sets or filter definitions. Overlapping runs sharing a key are not transactionally coordinated; schedule each monitor so its runs do not overlap.

No schedule is created automatically. Save a task and configure an Apify Schedule for daily or weekly checks. A small result limit may cover only the newest visible portion of a source; increase page and result bounds when you need a larger baseline. Successful empty monitoring checks still incur parsed-page charges.

## How do title and numeric filters work?

```json
{
  "channels": [
    "@3blue1brown"
  ],
  "maxResultsPerSource": 3,
  "minViews": 100000,
  "minDurationSeconds": 300,
  "maxDurationSeconds": 3600
}
```

`titleContains` is an OR match: at least one listed phrase must appear, case-insensitively. `titleExcludes` removes a row if any phrase appears. An empty list disables that filter. Numeric bounds use zero to mean disabled. Missing values do not pass an active numeric filter. The actor continues through available pages until it reaches the delivered-result limit, the page limit, the source's end or the spending limit. No filter adds a separate fee.

## What are the source limitations?

This lists the regular public Videos tab, in the order YouTube supplies. It does not fetch Shorts or live tabs, comments, transcripts, likes, private videos or video files. It does not discover channels by keyword. View counts can be rounded: 2.6 million becomes 2600000 with `views_approximate: true`, not an exact count. `published_text` is the original relative label such as “13 days ago”; no exact upload timestamp or date filtering is promised. Scheduled/live entries may have no duration. Missing values stay null. A channel without a Videos tab can be a successful empty check.

Public sources can change layouts or temporarily refuse requests. A refusal or unrecognized response is recorded as an error, not fabricated data. If all sources fail, the run fails; a partial run retains successful results and reports other errors in SUMMARY. There is no promise of complete historical coverage or stable source ordering. For legal use, respect source terms and applicable law, and obtain any rights required to reuse content; this actor is independent of the source platform.

## How do I call the API from Python, JavaScript or curl?

Python:

```python
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/youtube-channel-videos").call(
    run_input={'channels': ['@3blue1brown'], 'maxResultsPerSource': 3}, max_total_charge_usd=1
)
rows = client.dataset(run["defaultDatasetId"]).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/youtube-channel-videos').call(
  {"channels": ["@3blue1brown"], "maxResultsPerSource": 3}, { maxTotalChargeUsd: 1 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~youtube-channel-videos/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"channels": ["@3blue1brown"], "maxResultsPerSource": 3}'
```

The asynchronous run endpoint returns a run record. Wait for it to finish, then read its default dataset and SUMMARY. The same inputs work in n8n and Make. MCP clients and AI agents can call the actor after reading its event prices; a monetary run option must not be passed as an invented input field.

## FAQ: does this require another account or API key?

Only your Apify account is required. The actor does not ask for source-site passwords, cookies or a separate commercial data API key. Collection uses public channel pages and their public pagination responses.

### Why did I receive fewer rows than requested?

Filters, duplicates, monitoring, source availability, page bounds or your spending limit can all reduce delivery. Check SUMMARY for the actual stop reason. `maxResultsPerSource` is a ceiling, not a guarantee.

### Can I export to a spreadsheet?

Yes. Use Apify's dataset export as CSV or Excel, or read JSON from the Dataset API. Keep IDs and observation timestamps in downstream files so repeat exports can be reconciled.

### Why was a check charged when there were no new rows?

A source page was successfully parsed. That page check is the paid work used to determine whether matching or new data exists. The row event is charged only for rows delivered; parsed-page fees still apply.
