# Google Patents - Search, Inventors, Assignees & 专利

Google Patents provides inventors and assignees for structured research, JSON export and repeat monitoring. Search Google Patents by keywords and patent office. One row per patent: title, inventor, assignee, filing/publication dates, snippet, source and PDF link when available. Free text filters and ID/hash exclusions. 专利检索。 Search metadata; no full claims or legal opinion.

Last verified working: 2026-10-17. Independent community Actor maintained by kestrel; not affiliated with or endorsed by the source platform.

## Google Patents: when should an AI agent use it?

R&D and competitive-intelligence agents monitoring inventions and assignees. Use this Actor when the required data fields and target identifiers match the input contract below. It returns structured source observations that can be cited, filtered, saved and compared. It does not add invented values to fill gaps. A missing source field remains empty or null. Source identity, collection time and a content hash accompany every delivered record.

Uses the public Google Patents search interface. Search results contain metadata and a short search snippet, not the complete abstract or claims. PDF links are returned only when supplied by the source; files are not downloaded. The country input is a patent-office publication prefix such as US or CN, not the inventor nationality. Each source page contains up to ten records. Results can contain multiple publications from the same family; identity is the publication number, not family identity.

## Google Patents: how do I make the first call?

Start with a small target set and a low result limit. The following input is a real working example. Replace the example target with the employer, search query, company identifier or application you actually want to inspect. Keep the initial page budget small until the returned schema meets your downstream requirements.

```json
{
  "searchQueries": [
    "solar battery"
  ],
  "country": "",
  "maxResults": 5,
  "maxPages": 1
}
```

The default result limit is twenty across the entire run, not twenty per target. This distinction matters when several targets share one input. Targets are visited in input order and later targets may not be reached after the result or charge cap is met. Use separate runs if each target needs an independent guaranteed budget. Source availability may still prevent any particular target from returning data.

## Google Patents: which input answers which request?

| User request | Input approach |
| --- | --- |
| Inspect a small sample | Use the working JSON above with `maxResults: 5` and `maxPages: 1`. |
| Collect more results | Increase `maxResults` and `maxPages` within their allowed ranges. Neither guarantees a count. |
| Include a particular phrase | Set `includeKeywords` to a list of phrases. Matching is OR, case insensitive, inside fetched text. |
| Return only new records | Supply previously saved row IDs in `excludeIds`. Changed records with those IDs are also skipped. |
| Return changed snapshots | Supply previous `content_hash` values in `excludeContentHashes`. Real content changes remain eligible. |
| Cap spending | Set `maxTotalChargeUsd` on the Apify run request, outside the Actor input. |
| Export to a spreadsheet | Download the dataset as CSV or JSON after the run finishes. Preserve the original JSON for nested fields. |

```json
{
  "searchQueries": [
    "solar battery"
  ],
  "country": "",
  "maxResults": 2,
  "maxPages": 1
}
```

## What are the input fields?

| Input | Default | Meaning |
| --- | --- | --- |
| `searchQueries` | `["solar battery"]` | One or more keyword search strings, e.g. ["solar battery"]. One page budget per query. Results are deduplicated by id across queries before billing. |
| `country` | `""` | Patent publication office, e.g. "US" or "CN". Empty means all offices. Not inventor nationality. Free source filter plus output-prefix validation. |
| `maxResults` | `20` | Maximum paid rows across the entire run, after filters and exclusions. Example: 20. May return fewer when source pages end or maxPages is reached. |
| `maxPages` | `3` | Maximum source pages per target, 1–20; default 3. Up to 10 patent publications per source page per query. No publication-date filter is built in. Filters are free; maxResults can be lower than this scan budget. |
| `includeKeywords` | `[]` | Case-insensitive OR substring filter on title and snippet. Example: ["battery"]. Empty [] disables it. Applied before billing inside the page budget; not a semantic classifier or additional source search. |
| `excludeIds` | `[]` | Copy prior output id values here to skip before billing. id is the publication number, e.g. US12352469B2. Empty [] disables it. This also suppresses changes to existing IDs. |
| `excludeContentHashes` | `[]` | SHA-256 content_hash values from previous output to skip unchanged snapshots before billing. Example: copy returned hashes. Empty [] disables it. Changed counters or content can produce a new paid snapshot. |

All names are case sensitive. Unknown fields fail validation rather than being silently ignored. Supply arrays for list inputs and numeric integers for limits. Strings such as "20" are not interchangeable with the integer 20. Empty filter arrays disable those filters, while a required target array must contain at least one usable target. Validation happens before collection and does not create charged output rows.

## What does one output row contain?

One row is one patent snapshot. Nested lists and objects belong to that row and do not create additional billing events. The sample below shows the shape of real source data. Values are examples from the verification run and will change as the source changes.

```json
{
  "id": "CN112383088B",
  "title": "Combined heat and power system of optical storage micro-grid in office and …",
  "snippet": "The invention discloses a combined heat and power supply system of photovoltaic storage micro-grid in office places and its coordinated scheduling control method. Considering various energy supply and demand conditions among photovoltaic arrays, batteries, heat storage devices, heating devices and …",
  "inventor": "赵建勇",
  "assignee": "浙江大学",
  "priority_date": "2020-11-02",
  "filing_date": "2020-11-02",
  "publication_date": "2023-04-28",
  "grant_date": "2023-04-28",
  "language": "en",
  "country": "CN",
  "patent_url": "https://patents.google.com/patent/CN112383088B",
  "pdf_url": "https://patentimages.storage.googleapis.com/62/32/83/ca666ded8e21fd/CN112383088B.pdf",
  "source_url": "https://patents.google.com/xhr/query?url=q%3Dsolar%2Bbattery%26num%3D10%26page%3D0&exp=",
  "content_hash": "b308486ef8105448279809ffd9324d1bca4712af9992b1e383f27b2d92f1fbee",
  "fetched_at": "2026-10-17T05:00:18.140267+00:00"
}
```

| Field | Meaning |
| --- | --- |
| `id` | Id; copied or normalized from the public source. |
| `title` | Title; copied or normalized from the public source. |
| `snippet` | Snippet; copied or normalized from the public source. |
| `inventor` | Inventor; copied or normalized from the public source. |
| `assignee` | Assignee; copied or normalized from the public source. |
| `priority_date` | Priority date; copied or normalized from the public source. |
| `filing_date` | Filing date; copied or normalized from the public source. |
| `publication_date` | Publication date; copied or normalized from the public source. |
| `grant_date` | Grant date; copied or normalized from the public source. |
| `language` | Language; copied or normalized from the public source. |
| `country` | Country; copied or normalized from the public source. |
| `patent_url` | Patent url; copied or normalized from the public source. |
| `pdf_url` | Pdf url; copied or normalized from the public source. |
| `source_url` | Source url; copied or normalized from the public source. |
| `content_hash` | Content hash; copied or normalized from the public source. |
| `fetched_at` | Fetched at; copied or normalized from the public source. |

The `source_url` field identifies the public endpoint or page used to obtain the observation. Human-readable item links are separate fields when the source exposes them. The `fetched_at` timestamp records collection time in UTC. It is not the original publication time and should not be used as one. A `content_hash` is a SHA-256 digest of the normalized content; it is intended for snapshot comparison rather than authentication or proof that the source has never changed.

## How do filters and page limits interact?

Collection is deliberately bounded. The Actor requests a source page, normalizes its records, removes duplicates, applies exclusions and text or source-specific filters, and then sends eligible rows to the paid dataset. A record removed by a filter does not consume the result limit or create a billing event. However, reading a page still consumes the page budget. If all rows on the allowed pages fail your filter, the result can correctly be empty.

The text filter searches the documented returned text fields. It is a substring check, not a semantic classifier. A phrase that is related in meaning but not present literally will not match. Conversely, a matching substring does not prove relevance to your business question. Use the upstream search inputs to narrow retrieval first, then use `includeKeywords` as a precise final constraint. This separation makes filtering behavior predictable and avoids charging for an undocumented AI interpretation.

If you request one hundred results but permit only a page containing ten eligible items, ten is the expected output. Increasing the result cap alone cannot create source coverage. A page cap, interrupted source request, changing feed or restricted upstream search can each limit what the run observes. The free summary records which sources and pages were visited so an agent can explain those limits instead of describing the output as exhaustive.

## How much does this Actor cost?

The price is **$5 per 1,000 delivered patent rows**, or **$0.005 per row**. There is no Actor start fee. Proxy and compute are included in the event price. Filtered records, within-run duplicates, excluded IDs, unchanged excluded hashes and failures that produce no delivered rows do not generate a row charge. A run that delivers valid rows before a later source error retains those paid rows.

For example, ten delivered rows cost $0.05; one hundred cost $0.5. These examples are event-price arithmetic, not a prediction of how many results a source will return. Set a maximum total charge on each run to make the desired ceiling explicit. The charging SDK stops delivery when the event budget is exhausted. Do not put the budget parameter inside the Actor input: it belongs to the run API options and will be rejected as an unknown input field.

## How can I call it from Python, JavaScript or curl?

The examples use an environment variable for your Apify token. Keep credentials out of shared notebooks, source control and public URLs. The synchronous dataset endpoint is convenient for small runs. Larger collections can use the asynchronous run endpoint and retrieve the resulting dataset after completion.

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("kestrel/google-patents-search").call(
    run_input={'searchQueries': ['solar battery'], 'country': '', 'maxResults': 5, 'maxPages': 1},
    max_total_charge_usd=0.10,
)
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
summary = client.key_value_store(run["defaultKeyValueStoreId"]).get_record("SUMMARY")
print(len(rows), summary)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/google-patents-search').call(
  {"searchQueries": ["solar battery"], "country": "", "maxResults": 5, "maxPages": 1},
  { maxTotalChargeUsd: 0.10 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const summary = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('SUMMARY');
console.log(items, summary);
```

```bash
curl --request POST \
  'https://api.apify.com/v2/acts/kestrel~google-patents-search/runs?maxTotalChargeUsd=0.10' \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"searchQueries": ["solar battery"], "country": "", "maxResults": 5, "maxPages": 1}'
```

## How should repeat monitoring work?

Save the dataset from the first run in your own database or storage. For a later run, copy relevant IDs or hashes into the exclusion input. The Actor does not retain a hidden shared customer history and does not silently update a database for you. Inputs are therefore reproducible, and different schedules can maintain their own state. The exclusion lists are bounded to five thousand entries each; partition large monitoring workloads by target or time period.

Choose the comparison that matches the question. IDs answer whether an entity has been observed before. Hashes answer whether this particular normalized snapshot has been observed before. Engagement counters, source text, dates or other returned fields may change a hash. That is useful when monitoring changing content, but it also means a popular record can be delivered again even though its identity is familiar. Keep old hashes if you want to suppress a previously seen state that later returns.

An item absent from a later bounded scan is not automatically deleted, closed, inactive or unavailable. It might be outside the scanned pages or displaced by newer results. A source error or exhausted page budget makes disappearance especially ambiguous. Treat absence as unknown unless your own workflow has independent evidence and sufficient complete coverage. The Actor never creates synthetic deletion events from missing results.

## What does the free SUMMARY record report?

After collection, read `SUMMARY` in the run key-value store. It includes `status`, paid `rows`, network `requests`, `observed` records, `duplicates`, `excluded`, `filtered`, per-source observations, `errors`, `budget_reached` and `result_limit_reached`. The coverage label is `bounded_scan`. A source page's `source_end` refers to that page stream only; it is not a claim that every requested target was visited or that a platform-wide database was fully collected.

A successful empty result uses `no_matches`. A source failure without delivered rows uses `error`; a failure after valid rows uses `partial_error`. Both source error states fail the run so automation can distinguish them from a genuine empty search. Invalid input is reported separately as `invalid_input` before source access. Read the summary together with the run status rather than treating dataset length alone as evidence of success.

## How do I connect n8n, Make or an MCP agent?

In n8n or Make, use an Apify integration or an HTTP request step to start the Actor, then wait for completion and read the dataset and summary. Store the run identifier with your downstream records so failures can be traced. An MCP agent should first inspect the input schema, choose the correct source identifiers and set a small maximum charge. It can then cite the returned item URLs in its answer and state the observed coverage limits.

For daily monitoring, create a schedule with the desired source inputs and a separate state store for exclusion values. The Actor itself does not create schedules, send notifications or change source accounts. Your workflow decides when to run and what constitutes a meaningful update. This makes it suitable for both interactive research and scheduled pipelines without coupling data collection to a particular notification channel.

## FAQ: what should I know before using the data?

### Does this require a source account or source API key?

No source account is required for the supported public endpoints. An Apify token is required when you call the Actor through the Apify API. Public availability can change, and a source may rate limit or refuse an otherwise valid request. Such refusals are reported explicitly. The Actor does not accept session cookies or credentials and does not attempt to solve source challenges.

### Is the output guaranteed to be complete?

No. Results are bounded by the source response, requested targets, page cap, result cap and maximum charge. Search relevance and source limits also affect coverage. Ask for a focused, verifiable slice first and increase the scope only after checking the records. Never infer whole-market counts from a small bounded sample without additional evidence.

### Can I retrieve historical data or reconstruct missing fields?

Only the historical records exposed through the documented source path are available. The Actor does not maintain an independent archive. Save dated snapshots if you need a time series of changing source content. Missing fields are not estimated from unrelated data, and the output should not be presented as containing information that the source did not supply.

### Why can the same input return different results?

The upstream source is live. New records can appear, old records can move between pages, metadata can be corrected and popularity counters can change. A deterministic hash makes comparisons easier but does not freeze the source. Use the collection timestamp and source link to keep observations attributable, and preserve run summaries when comparing successive collections.

### What should an agent do after a blocked or partial run?

Inspect the errors and keep already delivered valid rows separate from unobserved coverage. Do not describe an unavailable source as having zero records. A transient failure may justify a later retry with the same bounded inputs and exclusions for already delivered data. Repeated refusals should be surfaced to the user instead of triggering an unlimited retry loop.

### Are there legal or reuse considerations?

Use the returned public data for purposes consistent with applicable laws and source terms. Source branding identifies where data originates and does not imply endorsement. Published text, abstracts, images and linked documents can carry their own rights. A returned download link is not a transfer of ownership or a guarantee that every downstream use is permitted. This Actor provides data collection, not legal, medical or investment advice.

## 中文使用说明

本工具用于专利检索、发明人、申请人、专利PDF。输入参数名保持英文，说明和示例适合 AI 智能体调用。每条输出均包含来源链接、采集时间和内容哈希，方便核验及持续监测。

只对实际写入数据集的结果计费。筛选掉的结果、重复结果、排除的 ID 和未变化的哈希不计费。`maxResults` 是整个任务的结果上限；`maxPages` 限制每个目标的扫描页数。需要控制费用时，请在 Apify 运行参数中设置 `maxTotalChargeUsd`，不要放进输入 JSON。

源站拒绝访问与真正的空结果会明确区分。请检查免费的 `SUMMARY`，不要把未完整扫描的数据当作全量结果。原始字段缺失时保留空值，不编造内容。来源网站的标志仅用于识别数据来源，并不表示官方合作。

Source reference: https://support.google.com/faqs/answer/7049475?hl=en
