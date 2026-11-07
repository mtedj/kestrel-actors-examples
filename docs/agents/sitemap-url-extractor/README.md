# Sitemap URL Extractor

Extract sitemap URLs and lastmod values from public XML documents, gzip files and nested indexes. Each delivered record identifies a page and the file that listed it, giving downstream workflows an auditable inventory for content discovery, SEO analysis or crawl preparation. No browser, proxy subscription or third-party API key is needed.

## Sitemap inputs: which request maps to which JSON?

Use this actor when you already know a site's published XML source address. It follows child indexes and produces deduplicated page records. It does not discover source addresses from homepages, crawl page content, verify page availability, or prove that a page is indexed by a search engine.

| Request | Input |
| --- | --- |
| First three Python documentation links | `{"sitemapUrls":["https://docs.python.org/sitemap.xml"],"maxResults":3}` |
| Product pages from a supplied source | `{"sitemapUrls":["https://example.com/sitemap.xml"],"urlContains":["/products/"],"maxResults":100}` |
| Recently declared changes | `{"sitemapUrls":["https://example.com/sitemap.xml"],"sinceDate":"2026-10-01"}` |
| Exclude previously delivered records | Pass earlier `id` values in `excludeIds` |

The example.com addresses illustrate input structure; replace them with a real source. The Python documentation example is a live source.

## URLs: how do I run a small first extraction?

```json
{"sitemapUrls":["https://docs.python.org/sitemap.xml"],"maxResults":3,"maxSources":2}
```

Supply 1–50 exact public source addresses in `sitemapUrls`. Duplicate inputs are processed once. `maxResults` defaults to 1,000 delivered records and accepts values up to 100,000. The global output cap applies after filtering and duplicate removal. If the source has fewer qualifying records, the actor returns fewer; a cap is a maximum rather than a promise of availability.

## Lastmod: what do the fields mean?

The dataset contains one `type="url"` record per unique page address. `url` is the declared location. `id` is a deterministic SHA-256 identifier derived from that location. `lastmod`, `changefreq` and `priority` preserve the publisher's values as strings or null. `sitemap_url` identifies the file supplying the record, and `fetched_at` records retrieval time in UTC.

These are publisher declarations, not measurements of actual page changes or search ranking. An omitted date stays null. A recent retrieval time does not establish that the page itself was recently modified. Duplicate page addresses across child files are delivered once; the first encountered record supplies the metadata.

```json
{"type":"url","id":"example-id","url":"https://example.com/products/a","lastmod":"2026-10-29","changefreq":null,"priority":"0.8","sitemap_url":"https://example.com/sitemap.xml","fetched_at":"2026-10-30T00:00:00+00:00"}
```

This row is illustrative. The source determines the actual metadata and timestamps.

## Filtering: how do dates and exclusions work?

`urlContains` defaults to an empty list, which keeps all addresses. Values such as `["/products/","/blog/"]` are literal, case-insensitive substring matches combined with OR. They are not regular expressions. Different filter fields combine with AND.

`sinceDate` defaults to an empty string. A supplied ISO date or timestamp is an inclusive UTC lower bound on the declared modification time. When a cutoff is present, missing or invalid modification dates are excluded. Without a cutoff those records remain eligible.

`excludeIds` accepts identifiers from earlier datasets. No monitoring state is automatically retained between runs. Your workflow must save identifiers and send them back on the next execution. Unchanged addresses remain the same identifier even if their metadata changes, so omit ID exclusion when your purpose is to inspect updated metadata for existing pages.

## Pricing: what does an empty run cost?

A successfully parsed file costs **$0.005**, including an index document. Each delivered page costs an additional **$0.0001**, or **$0.10 per 1,000 records**. One file yielding 1,000 records therefore costs **$0.105**. An index plus two child files yielding 1,000 unique records costs **$0.115**.

An empty valid file, or a valid file whose entries are all filtered or excluded, still incurs the parsing fee. This pays for the source check. Malformed XML, blocked requests, unsupported documents, duplicate sources and invalid input do not incur a parsing event. Filtered and duplicate records do not incur a URL event. There is no startup fee; compute and transfer are included in event prices.

Set `maxTotalChargeUsd` as an **Apify run option**, not an input property. The actor checks the remaining event allowance before requesting another source and before charging a page. A parsed file can consume the remaining allowance without leaving enough for a page; that file's parsing remains a completed billable operation. Already completed events remain charged when a later request fails.

## Limits: how much source data can be processed?

`maxSources` defaults to 30 and accepts 1–100 unique source attempts. Index files and failed attempts count against this operational cap, while only successful parses count toward the source fee. Children are traversed breadth first and repeated addresses are skipped, preventing index loops. Processing stops when either source, result or spending limits are reached.

Each download has an 8 MB decompressed limit, including gzip expansion, and a bounded request timeout. This is deliberately below the protocol's maximum file size. Split larger sources into smaller documents before using this actor. Redirects are bounded and every destination must be public HTTP or HTTPS on a standard port. Private network destinations and embedded credentials are rejected. XML DTDs and external entities are unsupported.

## API and workflow integrations

Use the Apify Console, schedules, API, n8n, Make or an MCP client. Scheduling is configured in Apify; this actor does not create schedules itself. Start with a small result cap and inspect the output before increasing it.

Python:

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("kestrel/sitemap-url-extractor").call(
    run_input={"sitemapUrls": ["https://docs.python.org/sitemap.xml"], "maxResults": 3},
    max_total_charge_usd=0.10,
)
print(list(client.dataset(run["defaultDatasetId"]).iterate_items()))
```

JavaScript:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/sitemap-url-extractor').call(
  { sitemapUrls: ['https://docs.python.org/sitemap.xml'], maxResults: 3 },
  { maxTotalChargeUsd: 0.10 }
);
console.log((await client.dataset(run.defaultDatasetId).listItems()).items);
```

curl:

```bash
curl 'https://api.apify.com/v2/acts/kestrel~sitemap-url-extractor/run-sync-get-dataset-items?maxTotalChargeUsd=0.10' \
  -H "Authorization: Bearer $APIFY_TOKEN" -H 'Content-Type: application/json' \
  -d '{"sitemapUrls":["https://docs.python.org/sitemap.xml"],"maxResults":3}'
```

## FAQ: how are errors and partial results reported?

Read the `SUMMARY` record in the default key-value store for row counts, attempted and parsed sources, exclusions, errors and the stop reason. Operational errors are kept there rather than inserted into the page dataset. A run in which every attempted source fails ends as failed. Mixed success preserves the valid records and lists the unsuccessful sources. A cap or an empty valid document is not a source failure.

### Can this discover every page on a website?

No. It extracts only addresses the supplied documents declare, within the configured bounds. Publishers can omit pages, and files can be stale. Use an additional crawler if you need link discovery or page content.

### Does it fetch the listed pages?

No. Only source files and their child indexes are fetched. Listed locations are output records, not crawl requests.

### Are there legal or access requirements?

Use public sources you are authorized to access and comply with applicable source terms and laws. Public availability does not grant an unrestricted right to republish content. The actor does not log in, solve challenges or retrieve private network resources.

Last verified working: 2026-10-30. See the changelog for tested release behavior.
