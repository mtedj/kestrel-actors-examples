# TikTok Video Details - Views, Likes & Hashtags

TikTok Video Details helps agents collect views and hashtags. Read public TikTok videos by full video URL. One row per video: caption, author, date, views, likes, comments, shares, saves, hashtags and duration. Filter text, dates, views or likes; skip saved IDs or hashes for monitoring. No account feeds, keyword search, comments or media downloads.

Video-performance and campaign-monitoring agents checking known TikTok video links, current engagement counters and changed snapshots. This Actor reads public web data into structured JSON, CSV or Excel. It runs on Apify and can be called through its API, an MCP client, n8n, Make or a saved Task. It is an independent tool, not an official product of the source platform, and it does not require source-account login credentials.

## TikTok Video Details scraper for AI agents: which input answers which request?

Use this Actor when the requested data and input mode match the contract below. A source check is a successfully parsed public response, not an assurance that every requested filter will match. The main output fields are `text, author_username, published_at, views, likes, comments, shares, saves, duration_seconds, hashtags`. Views and hashtags are observations from the source; absent fields remain null.

| Request | Input JSON |
| --- | --- |
| Get a small useful sample | `{"videoUrls": ["https://www.tiktok.com/@apifytech/video/7398101551744552225", "https://www.tiktok.com/@scout2015/video/6718335390845095173"], "maxResults": 3, "maxSources": 2}` |
| Apply the supported filters | `{"videoUrls": ["https://www.tiktok.com/@apifytech/video/7398101551744552225", "https://www.tiktok.com/@scout2015/video/6718335390845095173"], "maxResults": 3, "maxSources": 2, "minViews": 1, "minLikes": 1}` |
| Keep only previously unseen records | Add `excludeIds` with actual prior dataset `id` values |
| Keep changed snapshots for repeat monitoring | Add `excludeContentHashes` with actual prior hashes, without excluding their IDs |
| Bound cost | Set the Apify run option `maxTotalChargeUsd`; it is not Actor input |

Do not use this Actor for unsupported discovery, account access, full-history exports or fields not declared here. Full https://www.tiktok.com/@username/video/ID URLs only. No short links, numeric IDs alone, photo posts, profile feeds, keyword/hashtag discovery, comments, private videos or downloads. Views and engagement are public source counters at collection time, not independently audited measurements. Caption languages indicate advertised subtitle tracks; the Actor does not fetch caption files, transcribe speech or deliver transcript text. Music metadata is descriptive and confers no licence to use the audio.

## TikTok Video Details: how do I start?

1. Enter the example input below, or replace the public source targets with your own supported values.
2. Start the run with a small result limit and an explicit maximum cost in the Apify run options.
3. Read both the dataset and the `SUMMARY` key-value record. A successful run can contain fewer results than requested because filters and source coverage still apply.
4. Save IDs and hashes in your workflow if later runs should suppress duplicates or unchanged observations.

```json
{
  "videoUrls": [
    "https://www.tiktok.com/@apifytech/video/7398101551744552225",
    "https://www.tiktok.com/@scout2015/video/6718335390845095173"
  ],
  "maxResults": 3,
  "maxSources": 2
}
```

Inputs are processed in their listed order. Duplicate inputs collapse before source work. `maxResults` is a global paid-row limit after filters and exclusions; it is not a per-target limit. `maxSources` bounds attempted targets, including unsuccessful ones. The spending cap is checked before every source and before row charging. Increasing a result limit cannot create records that the public response does not expose.

## TikTok Video Details: what does each input control?

| Field | Meaning, example and billing effect |
| --- | --- |
| `videoUrls` | Required full TikTok video URLs, e.g. ["https://www.tiktok.com/@apifytech/video/7398101551744552225"]. Up to 100. No short links, profile URLs, numeric IDs alone or photo posts. Each valid video check costs a source fee plus its delivered-row fee. No comments or media downloads. |
| `maxResults` | Maximum paid rows across the ENTIRE run after filters, exclusions and deduplication; default 20, range 1–1000. Earlier targets can fill it. Set maxTotalChargeUsd in Apify run options for a dollar cap, not inside input JSON. A result cap does not expand source coverage. |
| `minViews` | Minimum public view count, e.g. 1000; 0 disables. Missing views fail an active threshold. Instagram often omits views even for reels; leave 0 when views are not required. Filters supplied URLs before maxResults. No filter fee; valid checks remain paid. |
| `minLikes` | Minimum public like count, e.g. 100; 0 disables. Hidden or missing likes fail an active threshold. Filters supplied posts/videos before maxResults, without discovering new URLs. No filter fee; valid source checks remain paid. |
| `publishedAfter` | Optional ISO date/time, e.g. "2026-11-01T00:00:00Z"; "" disables. Keeps social posts/videos published at or after it. Date-only values use midnight UTC. Filters supplied URLs only, without discovering posts or reducing the source fee. Applied before maxResults. |
| `textContains` | Optional case-insensitive OR phrases, e.g. ["python", "developer"]. Matches title, caption/snippet/description, author, company or developer fields when present. [] disables. Filters before maxResults. Skipped rows have no row fee; valid source checks are paid. |
| `maxSources` | Maximum attempted source targets across the run; default 20, range 1–100. One post/video URL, Indeed query/location/country, or Play query-or-ID/country counts as one. Failed targets count toward this limit but have no event fee. Valid filtered sources are paid; retries add no source fee. |
| `excludeIds` | Prior dataset id values, e.g. [] on a first run; up to 5,000. Skips identities even when changed. For Google Play use the full app:country:language id. Excluded rows are free but valid checks are paid. Keep history in your workflow; no automatic persistence. |
| `excludeContentHashes` | Prior content_hash values, e.g. [] initially; up to 5,000 SHA-256 hashes. Skips unchanged observations while allowing updates. Do not also exclude IDs when changes matter. Time, search position, image URLs and relative-date labels do not affect hashes. Valid source checks remain paid; no stored history. |

Unknown input properties fail validation instead of being silently ignored. No arbitrary source host can be requested. URL inputs must match the supported public platform paths. For keyword inputs, the Actor constructs a fixed source URL; it never visits a result's external website or an arbitrary destination supplied through a record.

## What does each output row contain?

Declared row fields: `id, type, platform, title, text, url, author_username, author_name, author_verified, published_at, views, likes, comments, shares, saves, duration_seconds, width, height, hashtags, music_title, music_author, original_sound, caption_languages, image_url, source_url, content_hash, fetched_at`.

One dataset row represents one delivered video. Its `id` identifies the source entity; `source_url` records the fetched public document; `fetched_at` is the UTC observation time. `content_hash` represents the normalized record for caller-managed comparison. The following example projects factual fields from an observed public source response. Text, captions and image URLs are omitted from this documentation example; the runtime returns the declared fields when available. The hash belongs to the original full observation.

```json
{
  "id": "7398101551744552225",
  "type": "video",
  "platform": "tiktok",
  "url": "https://www.tiktok.com/@apifytech/video/7398101551744552225",
  "author_username": "apifytech",
  "author_name": "Apify",
  "author_verified": false,
  "published_at": "2024-08-01T09:32:32+00:00",
  "views": 595,
  "likes": 21,
  "comments": 0,
  "shares": 1,
  "saves": 1,
  "duration_seconds": 23,
  "width": 576,
  "height": 1024,
  "hashtags": [
    "data",
    "webscraping",
    "techtiktok",
    "job",
    "automation"
  ],
  "music_title": "original sound",
  "music_author": "Apify",
  "original_sound": true,
  "caption_languages": [
    "eng-US"
  ],
  "source_url": "https://www.tiktok.com/@apifytech/video/7398101551744552225",
  "content_hash": "ed99ff9d14978da50c83c1abbb608cd658a0b589be69e315331241db07117d1f",
  "fetched_at": "2026-11-11T05:35:48.162104+00:00"
}
```

Null means the field was not exposed or could not be confirmed from the public response. It does not mean zero, false, no activity or no commercial value. Counts and prices can change between runs. Do not infer private-account data, complete historical coverage, a verified employer policy, exact downloads or earned revenue from these records. Field-specific source limits are described above.

`SUMMARY` records attempted and successfully checked sources, request counts, found and delivered rows, filters, duplicates, charged events, per-target outcomes, source errors and spending-limit flags. It is not a paid dataset row. A valid response with no matching rows can succeed with an empty dataset. A blocked page, login redirect, missing expected data or unavailable target is an error, not a fabricated empty result. If every attempted source fails, the run fails. Partial success retains useful rows and records each failing target.

## What does a run cost, and how do I cap spending?

- Source checked: **$0.002 per valid source**, or $2 per 1,000 checks.
- Delivered video: **$0.002 per row**, or $2 per 1,000 rows, plus checked-source fees.
- No start fee. Proxy and compute are included in the event prices.

One valid source with one delivered row costs **$0.004**. One valid source with three rows costs **$0.008**. If all rows are filtered or excluded, the valid source check still costs **$0.002**. Blocked, unavailable and failed sources and invalid inputs have no event fee. Duplicates and filtered rows have no row fee. Bounded HTTP retries are included in the source fee rather than billed as additional checks.

The conservative maximum before a spending cap is `min(number of targets, maxSources) × 0.002 + maxResults × 0.002`. A social post or video URL is one target. An Indeed target is one keyword/location/country combination. A Google Play target is one keyword or package ID in one country. Countries multiply checks; multiple keywords and locations can multiply them further. The Actor needs room for one source check plus one row before starting another target. A cap below **$0.004** performs no source work.

The Actor stops at the platform's charge limit or a billing failure. Charging and dataset writes are separate operations: a delivery interruption can leave a charged row unwritten. Such a failure is recorded explicitly in SUMMARY and fails the run. A result limit is useful for volume control; the run option `maxTotalChargeUsd` provides the monetary limit. Do not place that option inside Actor input.

## How does repeat monitoring detect changes?

Save IDs, hashes and observation times in your own database, dataset or workflow. `excludeIds` keeps only new identities, even if an old entity changed. `excludeContentHashes` keeps changed observations eligible. Passing both a previous ID and its hash also suppresses updates to that ID, so use hashes alone when changes matter. The Actor does not silently reuse a previous dataset or create a schedule.

Hashes exclude collection time, search position, source URL, image URL and relative-date labels. A changed hash is a reason to compare relevant fields; it is not proof of a specific engagement, salary, rating or version change. Missing rows can reflect filters, access problems, bounded source coverage or a spending cap. They are not deletion events. A saved Apify Task or your scheduler can run the same inputs and carry forward up to 5,000 exclusions; avoid overlapping jobs that overwrite shared workflow history.

## How do I call the API or MCP tools?

Python using apify-client 3.x:

```python
from decimal import Decimal
from apify_client import ApifyClient
client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("kestrel/tiktok-video-details").call(run_input={'videoUrls': ['https://www.tiktok.com/@apifytech/video/7398101551744552225', 'https://www.tiktok.com/@scout2015/video/6718335390845095173'], 'maxResults': 3, 'maxSources': 2}, max_total_charge_usd=Decimal("0.20"))
assert run is not None and run.status == "SUCCEEDED", run
rows = client.dataset(run.default_dataset_id).list_items().items
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/tiktok-video-details').call(
  {"videoUrls": ["https://www.tiktok.com/@apifytech/video/7398101551744552225", "https://www.tiktok.com/@scout2015/video/6718335390845095173"], "maxResults": 3, "maxSources": 2}, { maxTotalChargeUsd: 0.20 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
```

curl starts an asynchronous run:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~tiktok-video-details/runs?maxTotalChargeUsd=0.20' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"videoUrls": ["https://www.tiktok.com/@apifytech/video/7398101551744552225", "https://www.tiktok.com/@scout2015/video/6718335390845095173"], "maxResults": 3, "maxSources": 2}'
```

Wait for completion before reading the dataset and SUMMARY. MCP clients can fetch the Actor details and call `kestrel/tiktok-video-details` using the same input. Inspect the live tool schema for monetary run options. If a dedicated MCP tool lacks a cost-cap option, use `call-actor` with `callOptions.maxTotalChargeUsd` or the Apify API. Do not invent a spending input that the schema does not expose.

## FAQ: why are results missing or fewer than requested?

Fewer rows than requested usually means source coverage, filters, duplicate identities, exclusions, failed targets or a cap. Check SUMMARY before increasing limits. These Actors use bounded requests and retries, without login cookies, CAPTCHA solving or browser automation. Source layout or access changes can cause a real failure; such responses are never presented as successful empty data. Retrying a failed target may help with a temporary network issue, but repeated failures should be investigated before scheduling large workloads.

Public links and metadata can become stale. The Actor returns observations, not a warranty of current availability or permission to republish media. Use the source platforms and their content under applicable legal rights. JSON preserves nested arrays; Apify offers CSV, Excel and other dataset exports. Google Play parsing uses the MIT-licensed google-play-scraper package, pinned to version 1.2.7; network access and failure handling remain bounded by this Actor.

Last verified working: 2026-11-11 (public-source probes). Public builds are released only after cloud validation of useful output, filters, exclusions, invalid inputs and spending caps.
