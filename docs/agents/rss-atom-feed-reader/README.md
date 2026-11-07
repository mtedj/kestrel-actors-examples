# RSS Feed Reader

Read RSS and Atom sources with a feed reader that returns structured article metadata and publisher-supplied text. Each record includes a stable identifier, title, link, author, dates, categories and source address. This is useful for release monitoring, news intake and routing new entries into downstream workflows without opening a browser or obtaining a separate source API key.

## RSS inputs: which request maps to which JSON?

Use this actor for exact public RSS 2.0 or Atom 1.0 addresses. It reads entries already present in those documents. It does not search the web, discover feeds from homepages, retrieve an archive, or visit article pages to expand shortened descriptions.

| Request | Input |
| --- | --- |
| First three Python blog entries | `{"feedUrls":["https://blog.python.org/feeds/posts/default?alt=rss"],"maxResults":3}` |
| Recent CPython release entries | `{"feedUrls":["https://github.com/python/cpython/releases.atom"],"sinceDate":"2026-10-01"}` |
| Titles mentioning a phrase | Pass `titleKeywords`, such as `["release","security"]` |
| Only IDs not delivered before | Pass the earlier dataset's `id` values in `excludeIds` |

For an AI agent or MCP client, put the source addresses in `feedUrls`. `maxTotalChargeUsd` belongs to the Apify run options rather than this input object. Feed checks that return no matching entries are still charged when the source was successfully parsed.

## Atom and RSS: how do I start with a small sample?

```json
{"feedUrls":["https://blog.python.org/feeds/posts/default?alt=rss"],"maxResults":3,"maxItemsPerFeed":3}
```

`feedUrls` accepts 1–50 public addresses. Duplicated input addresses are requested once. The default `maxResults` is 100 entries across the entire run, with a maximum of 5,000. `maxItemsPerFeed` defaults to 100 and accepts up to 1,000 matching entries from each source. The global cap can stop processing before later sources are checked.

Entries remain in the publisher's order. The actor does not sort all sources into a global timeline. If your workflow needs a timeline, sort the returned dataset by the available publication or update timestamp. A cap is a maximum; the publisher may supply fewer entries than requested.

## Feed reader output: what is included in a record?

Each dataset entry has `type="entry"`. Its `id` is a deterministic hash of the final source address and the publisher's entry identifier, with link or content-based fallbacks when no identifier exists. `source_id` retains the original GUID or Atom ID when supplied. `feed_url` and `feed_title` identify the source.

`title`, `url`, `text`, `author`, `published_at`, `updated_at` and `categories` contain the available metadata. HTML markup in supplied descriptions is removed and entities are decoded. Text is limited to 100,000 characters per entry. Missing fields remain null or an empty category list. Publication and update timestamps are normalized to UTC, and `fetched_at` records retrieval time.

```json
{"type":"entry","id":"example-id","source_id":"post-123","feed_url":"https://example.com/feed.xml","feed_title":"Example","title":"Release announcement","url":"https://example.com/releases/123","text":"Publisher supplied description.","author":"Editorial team","published_at":"2026-10-29T12:00:00+00:00","updated_at":null,"categories":["Releases"],"fetched_at":"2026-10-30T00:00:00+00:00"}
```

This is an illustrative record. Text completeness depends on what the publisher includes. A summary-only source produces summary text; the actor never claims to have downloaded the linked article.

## Filtering: how do I keep only matching or new entries?

`titleKeywords` defaults to `[]`, which keeps all titles. Phrases are case-insensitive literal substring matches combined with OR. For example, `["security","release"]` keeps either term. Different filters combine with AND. There is no full-text or regular-expression search input.

`sinceDate` is empty by default. Supply an ISO date or timestamp for an inclusive UTC lower bound. Publication time is used when available; otherwise update time is used. If both are missing or invalid, an entry is excluded when a cutoff is set. Without a cutoff the actor can return undated entries.

`excludeIds` defaults to `[]`. Supply identifiers saved from a previous dataset to suppress already delivered entries before output caps are applied. State is not stored automatically between executions. Your scheduler or integration must retain identifiers and pass them in again. Because identity includes the source address, the same article syndicated through two different feeds can appear twice. A publisher changing an entry's identifier or redirect destination can also produce a new ID.

## Pricing: what does checking a source cost?

Each successfully parsed feed costs **$0.0025**, or **$2.50 per 1,000 checks**. There is no per-entry fee and no startup fee. Compute and data transfer are included. One source returning 100 entries costs the same as one source returning three entries.

A valid empty source, or a successful check where every item is excluded by filters or known IDs, still incurs the check fee. Invalid input, HTTP failures, malformed XML, unsupported document types and duplicate input addresses are not charged. Successful sources remain billable if a different source fails later in the run.

Checking ten feeds every day for 30 days would cost **$0.75** if all ten are successfully parsed on every run. This is event-price arithmetic, not a claim that a source will always be available or contain useful new entries. Processing can stop earlier if the global row cap is reached.

Set `maxTotalChargeUsd` as an **Apify run option**. The actor checks remaining allowance before requesting another source, then charges only after parsing succeeds. When no further check can be charged, it stops making source requests. Use input caps alongside the monetary cap for predictable processing scope.

## Limits: which formats and source sizes work?

This release supports RSS 2.0 and Atom 1.0 XML, including common content and author namespaces. It does not support RSS 1.0/RDF, JSON Feed, HTML pages or authenticated sources. A document must be at most 8 MB after decompression. Requests and redirects have bounded timeouts, and processing never follows article links.

Public HTTP and HTTPS on standard ports are accepted. Embedded credentials, private addresses and private network DNS results are rejected, including after redirects. XML DTDs and external entities are unsupported. Blocked sources are reported as errors rather than retried through a paid proxy.

## API and workflow integrations

Use Apify Console schedules, n8n, Make, the API or MCP. For recurring monitoring, retain each delivered `id`, pass saved identifiers into the next run, and send the resulting new entries to your own downstream workflow. This actor does not send messages or create schedules by itself.

Python:

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("kestrel/rss-atom-feed-reader").call(
    run_input={"feedUrls": ["https://blog.python.org/feeds/posts/default?alt=rss"], "maxResults": 3},
    max_total_charge_usd=0.10,
)
print(list(client.dataset(run["defaultDatasetId"]).iterate_items()))
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/rss-atom-feed-reader').call(
  { feedUrls: ['https://blog.python.org/feeds/posts/default?alt=rss'], maxResults: 3 },
  { maxTotalChargeUsd: 0.10 }
);
console.log((await client.dataset(run.defaultDatasetId).listItems()).items);
```

curl:

```bash
curl 'https://api.apify.com/v2/acts/kestrel~rss-atom-feed-reader/run-sync-get-dataset-items?maxTotalChargeUsd=0.10' \
  -H "Authorization: Bearer $APIFY_TOKEN" -H 'Content-Type: application/json' \
  -d '{"feedUrls":["https://blog.python.org/feeds/posts/default?alt=rss"],"maxResults":3}'
```

## FAQ: where do failures and partial results appear?

The default key-value store contains a `SUMMARY` record with source counts, delivered rows, filtering counts, errors and the stop reason. Source errors are kept out of the article dataset. If every attempted source fails, the run fails explicitly. When at least one source succeeds, its valid rows remain available and errors identify the unsuccessful sources. A valid source with zero matching entries is a successful check.

### Can it retrieve older articles missing from the feed?

No. Publishers control retention. Use an archive or a dedicated crawler for entries no longer present in the supplied document.

### Are there legal or access requirements?

Use sources you are authorized to access and respect applicable terms and laws. Public syndication does not automatically allow unrestricted content republication. The actor does not log in, bypass access challenges or fetch private network resources.

Last verified working: 2026-10-30. See the changelog for tested release behavior.
