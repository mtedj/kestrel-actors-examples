# Google News - Articles, Headlines & Keyword Search

Google news returns headlines and articles from public keyword search RSS feeds for research and automation. It produces structured JSON that an agent can use without parsing a web page. Start with a small input, inspect a few rows, and then increase the result limit. The output has a stable identifier, source provenance and a fetch timestamp so another step can store, compare or cite the result.

Last verified working: 2026-10-16.


## Google News RSS API for agent workflows

Use this independent Apify actor to retrieve the public data documented below. It is not an official platform API or an account-management API. Pass the documented input JSON, keep result limits small for the first call, and use Apify run option `maxTotalChargeUsd` for the charge cap.

## 谷歌新闻搜索与采集：简体中文和繁體中文

通过关键词搜索 **Google News（谷歌新闻）**，返回新闻标题、媒体来源、发布时间和 Google News 链接。支持简体中文 `zh-CN` 与繁體中文 `zh-TW`。这是 **RSS 新闻元数据采集**，不返回新闻全文，不解析原始文章直链，也不保证完整历史覆盖。Google News 是数据源；本工具不绕过用户所在地的网络访问限制。

| 中文需求 | 正确输入或结果字段 |
|---|---|
| 简体中文人工智能新闻 | `queries: ["人工智能"]`，`language: "zh-CN"`，`country: "CN"` |
| 繁體中文人工智慧新聞 | `queries: ["人工智慧"]`，`language: "zh-TW"`，`country: "TW"` |
| 最多返回 3 条新闻 | `maxArticlesPerQuery: 3`，`maxResults: 3` |
| 只要指定媒体 | `publisherDomains: ["bbc.com"]`；域名不含 `https://` |
| 每天跳过已采集新闻 | 外部保存 `article_id`，下次通过 `excludeArticleIds` 传入 |
| 精确筛选某一天（UTC） | 当日设为 `sinceDate`，次日设为 `untilDate`；后者不包含在范围内 |

```json
{"queries":["人工智能"],"language":"zh-CN","country":"CN","maxArticlesPerQuery":3,"maxResults":3}
```

```json
{"queries":["人工智慧"],"language":"zh-TW","country":"TW","maxArticlesPerQuery":3,"maxResults":3}
```

`country` 与 `language` 选择新闻版本，不表示每条新闻发生在该地区，也不翻译标题。输出保留原文：一个 `type="article"` 行包含 `article_id`、`title`、`publisher`、`publisher_url`、`publisher_domain`、`published_at` 和 `google_news_url`。`publisher_url` 是媒体主页；`feed_description` 是 RSS 摘要元数据，不能当作新闻全文。

费用为 **每 1,000 条新闻 $1**；3 条最多 $0.003。无启动费，过滤、排除、重复、空结果和状态行不计新闻费用。过滤先于结果上限。金额上限使用 Apify 运行选项 `maxTotalChargeUsd`，不是输入字段。外部工作流负责调度和保存 ID；检查 `SUMMARY` 及 `type="status"` 以区分无结果与失败。

这是独立的 Kestrel 工具，与 [Google News](https://news.google.com) 无隶属关系。


## Google news: what does it return?

Each article row contains a headline, publisher name, publisher homepage, publication timestamp and Google News link. The source is the public keyword search RSS feed. This is metadata retrieval: feed_description is the short feed text, often just a repeated headline and publisher, not the full article body. google_news_url opens a Google News link; publisher_url is a homepage, not a direct article URL. The actor does not resolve publisher article URLs, download articles, bypass paywalls or return sentiment scores. Each query exposes at most about 100 feed entries with no pagination. Date filters narrow retrieval and then enforce exact UTC bounds locally, but they do not produce an exhaustive historical archive. Publisher domains and country/language editions are supported. Source headlines are preserved, including publisher suffixes where Google includes them.

The actor separates records from diagnostics. A record has `type="article"` and is the only billable unit. A diagnostic has `type="status"`, identifies its `source`, and describes what happened during that source's retrieval. Read the `SUMMARY` record from the run's key-value store for totals. A successful platform run is not proof that every requested source had matches: inspect the diagnostic rows and the summary before declaring a research task complete.

## Google news for AI agents: which input answers which request?

Use this actor when the requested data matches the public source described above. Use the explicit input fields instead of constructing browser scripts. The target values identify what to search; the result limits bound the number of records delivered; filters narrow the matching records before charging. The actor does not interpret natural-language instructions outside the schema.

| User request | Input change |
|---|---|
| News about artificial intelligence | `queries: ["artificial intelligence"]` |
| Spanish edition | `language: "es"`, `country: "ES"` |
| Simplified Chinese news | `language: "zh-CN"`, `country: "CN"` |
| Traditional Chinese news | `language: "zh-TW"`, `country: "TW"` |
| A particular publisher | `publisherDomains: ["bbc.com"]` |
| Stories from one UTC day | `sinceDate: "2026-10-15"`, `untilDate: "2026-10-16"` |
| Newly observed articles on a repeat run | Save and pass `excludeArticleIds` |
| Full article bodies or direct publisher article URLs | Not supported; use a separate article retrieval tool |

The actor does not schedule itself, retain your earlier dataset as monitoring state, or send notifications. In a recurring workflow, store identifiers after each successful run and pass them in the exclusion field next time. If the user requests a complete historical archive or facts that the public source does not expose, explain the limitation before calling. Do not manufacture a target, fill a missing value from guesswork, or describe an empty result as evidence that no such record exists anywhere.

## Google news quick start

Paste this minimal example into the Input tab. It requests three records at most, so it is inexpensive to inspect. A smaller result is possible if the source is unavailable, has fewer records, or does not contain enough matches. The sample is a live public source, and its contents can change between runs.

```json
{
  "queries": [
    "artificial intelligence"
  ],
  "maxArticlesPerQuery": 3,
  "maxResults": 3
}
```

After the run, open Output or the default dataset. Retain rows where `type` equals `article` for downstream processing. Keep status rows in operational logs so failures remain visible. Download JSON when you need nested objects and arrays; CSV is useful for the flat columns but does not turn nested structures into a separate table automatically.

This example narrows the keyword search to a publisher domain. Matching articles may be fewer than the requested cap.

```json
{
  "queries": [
    "artificial intelligence"
  ],
  "maxArticlesPerQuery": 3,
  "maxResults": 3,
  "publisherDomains": [
    "bbc.com"
  ]
}
```

## Inputs and source limits

| Input | Contract |
|---|---|
| `queries` | Required: 1-10 keyword searches, e.g. ["artificial intelligence"]. Google operators such as quotes, OR and site: work in queries. Returns recent RSS metadata, not full article text or direct publisher article URLs. At most about 100 source entries per query; no exhaustive historical archive. |
| `maxArticlesPerQuery` | 20 by default; 1-100. Maximum matching articles per query AFTER dates, publishers and exclusions. Newest publication first within the returned feed; RSS may contain fewer matches and has no pagination. 10 articles cost $0.01. |
| `maxResults` | 100 by default. Maximum delivered article rows across all inputs, after filters and deduplication. Stops early even if sources remain. Free status rows do not count. Cost is at most maxResults × $0.001; use Apify run option maxTotalChargeUsd for a dollar cap. |
| `country` | "US" default. Two-letter Google News edition, not the location of every story. 中文示例: "CN" + language="zh-CN" (简体); "TW" + "zh-TW" (繁體). Keep US if no region is requested. country and language select a feed, not a translation. No extra charge. |
| `language` | "en" default. Feed language, not translation. For 简体中文 use "zh-CN" with country="CN"; for 繁體中文 use "zh-TW" with country="TW". "es" pairs with "ES". Keep en if unspecified. Some edition pairs may return few or no articles. No extra charge. |
| `sinceDate` | Empty = no lower date bound. "2026-10-01" includes publication dates on or after midnight UTC. Free filter before caps; entries without a publication date are excluded. Narrowing the query does not guarantee an exhaustive historical archive. |
| `untilDate` | Empty = no upper bound. "2026-10-16" excludes publication dates on/after midnight UTC on October 16; this bound is exclusive. Must be later than sinceDate. Free filter before caps. For all of October 15, use sinceDate="2026-10-15", untilDate="2026-10-16". |
| `publisherDomains` | ["reuters.com", "bbc.com"] keeps either publisher domain or its subdomains. Empty = any publisher. Bare domains only, no URLs. Narrows the Google query and filters source publisher metadata before billing. publisher_url is the publisher homepage, not the original article URL. |
| `excludeArticleIds` | article_id or google_news_url values from earlier output; up to 10000 strings. Empty = no exclusions. Duplicate IDs across queries are billed only once. Distinct publishers covering the same story remain separate articles. Save/pass IDs externally; the actor does not remember prior runs or schedule itself. |

Filters apply before delivered-record limits. This means a request for ten matches will not spend its entire output allowance on records that fail the filters. However, output limits and source coverage are different things. A source may return a bounded feed or a scanned portion of its catalog. The actor reports retrieval limits rather than silently claiming complete coverage. Raising the output cap cannot force an upstream source to expose more data than it actually returns.

Sources are processed in the order supplied. The total limit spans the whole run, and reaching it can leave later sources unprocessed. Check `sources_not_processed` in `SUMMARY` before assuming each target was visited. For an equal allocation across sources, use the per-source limit and choose a total limit large enough to accommodate the sum. The actor deduplicates repeated target strings before starting requests, and record identifiers are also deduplicated across the run.

## Output fields and stable identifiers

| Field | Meaning |
|---|---|
| `article_id` | Article id. |
| `title` | Title. |
| `publisher` | Publisher. |
| `publisher_url` | Publisher url. |
| `publisher_domain` | Publisher domain. |
| `google_news_url` | Google news url. |
| `published_at` | Published at. |
| `feed_description` | Feed description. |
| `query` | Query. |
| `language` | Language. |
| `country` | Country. |
| `type` | Type. |
| `content_hash` | Content hash. |
| `fetched_at` | Fetched at. |
| `source` | Source. |
| `status` | Status. |
| `rows` | Rows. |
| `source_rows` | Source rows. |
| `filtered` | Filtered. |
| `duplicates` | Duplicates. |
| `errors` | Errors. |
| `error` | Error. |
| `pages` | Pages. |
| `cap_reached` | Cap reached. |
| `currency_warning` | Currency warning. |

Every returned record also includes `content_hash` and `fetched_at`. The hash is a SHA-256 digest of normalized content, excluding the fetch timestamp and, for news, the query that happened to retrieve it. It is useful for comparing repeated observations of the same identifier. It is not a guarantee that the underlying source has never changed: an edit can occur between runs, and only observed versions are available. Treat the timestamp as the time this actor observed the record, not the original publication date.

Keep source-provided identifiers as strings. Large numeric product identifiers can exceed safe integer precision in some spreadsheet or JavaScript workflows. Converting them to floating point can produce false matches or broken exclusion lists. Use the stable identifier as a database key and keep the human-readable title as a separate attribute. If you compare data from several sources, preserve the source component of the key.

Some fields can be null or empty. Null means the source did not supply a usable value or the documented lookup was unavailable. An empty list means no entries were available for that field. Neither means that a missing fact has been verified false. Preserve these distinctions in downstream reports instead of replacing null values with zeros, invented dates, or a default currency.

## Pricing and maximum cost

The price is $1 per 1,000 delivered article records. Ten records cost $0.01. There is no start fee. Proxy and compute are included in the event price for callers. Free status rows do not count toward the bill or the `maxResults` input. Filters, excluded identifiers, duplicates, empty results, failed requests and invalid input do not generate billable record events.

Billing is tied to successfully persisted records through the Apify SDK. A partial run can deliver and charge for valid records before a later source fails. Those delivered records remain useful and are not discarded because another source is unavailable. The actor does not charge a failed request as though it had produced a record. Review the dataset and status rows together when reconciling a partial result.

Set the maximum total price using Apify's `maxTotalChargeUsd` run option. This is a platform option, not an input property, and must be passed outside the JSON input body when using the API. The actor stops when the SDK reports that the event charge limit has been reached. For predictable calls, use both the record limit and the dollar cap. A smaller cap can stop the run before the requested count is reached; it cannot guarantee that the source contains enough matching data.

## Status rows and error handling

A status row includes `source`, `status`, `rows`, `source_rows`, `filtered`, `duplicates`, `errors`, `error`, `pages`, `cap_reached` and `currency_warning`. `rows` is the number delivered for that source; `source_rows` counts the source entries inspected, before filtering and deduplication. Repeated pages may make the inspected count larger than the number of distinct entries. `filtered` and `duplicates` explain why inspected entries did not become paid output.

`ok` indicates that the retrieval completed without a reported error. `empty` means the public source returned no entries. `no_matches` means entries were inspected but none survived the filters or exclusions. `error` means the source failed before delivering records; `partial_error` means a failure occurred after some records were already delivered. The `error` message explains the failure without including credentials. If source errors prevent all delivery, the actor marks the run failed. If some useful records were delivered, inspect the error count and decide whether to retry the affected sources.

`budget_reached` means the dollar cap stopped output. `cap_reached=true` means a count or scan boundary was reached; it does not promise that all matching data was exhausted. Catalog runs may also report `scan_limit` or `repeated_page`. The former indicates the maximum page count was used. The latter prevents an upstream endpoint that repeats the same page from causing a long, unproductive loop. A run summary includes `rows`, `sources`, `errors`, `filtered`, `duplicates`, `http_requests`, `budget_reached`, `result_limit_reached` and `sources_not_processed`.

## API examples: curl, Python and JavaScript

Keep your Apify token in an environment variable or the platform's credential manager. Do not paste it into a public workflow, shared input example or repository. The token authenticates your call to Apify; the actor itself does not require a separate source API key. Replace the sample input with a JSON object that follows the schema, and retain the same dollar cap when testing changes.

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~google-news/runs?maxTotalChargeUsd=0.05' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"queries": ["artificial intelligence"], "maxArticlesPerQuery": 3, "maxResults": 3}'
```

The asynchronous REST endpoint returns a run object. Poll that run until it reaches a terminal state, then read its `defaultDatasetId` and `defaultKeyValueStoreId`. Do not assume that a successful HTTP response to the start request means the extraction itself has finished. The client libraries can wait for completion, which is often simpler for a short agent task.

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('kestrel/google-news').call(
    run_input={'queries': ['artificial intelligence'], 'maxArticlesPerQuery': 3, 'maxResults': 3},
    max_total_charge_usd=0.05,
)
for row in client.dataset(run['defaultDatasetId']).iterate_items():
    if row.get('type') == 'article':
        print(row)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/google-news').call(
  {"queries": ["artificial intelligence"], "maxArticlesPerQuery": 3, "maxResults": 3},
  { maxTotalChargeUsd: 0.05 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const records = items.filter(row => row.type === 'article');
console.log(records);
```

## Automation, MCP, n8n and Make

An AI agent using the Apify MCP server can search for the platform and data type, inspect this actor's schema, and run it with a bounded input. Field descriptions explain important distinctions at the point of use, including the per-source limit and the total cap. Ask the agent to inspect status rows before summarizing the results. This prevents a technically successful run with no matches from becoming an unsupported claim about the broader market.

In n8n or Make, connect the Apify run step to a dataset retrieval step. Filter the dataset by `type` before sending records to a spreadsheet, database or analysis model. For scheduled monitoring, create the schedule in your automation platform, store the identifiers there, and supply exclusions on subsequent calls. Keep separate handling for empty results and failures: an empty successful search may need no action, while a failed source might warrant a later retry with the same bounded input.

When a run is retried after partial delivery, pass the identifiers already saved so they are not billed again. The actor does not know whether your downstream database successfully committed those rows. Your workflow should save records and their identifiers together, or use an idempotent upsert keyed by the stable identifier. Avoid blindly retrying a large run immediately after a rate-limit response; a short delay and a smaller set of sources make it easier to determine whether the problem is temporary.

## FAQ: coverage, data quality and legal use

### Does this actor guarantee a complete dataset?

No. It reports what the public source exposes within the documented retrieval bounds. Source ordering, publication changes, feed limits and endpoint availability affect results. Inspect caps and status messages, and keep the input alongside the dataset for reproducibility. A small sample is appropriate for checking a workflow; it is not automatically representative of the entire source or market.

### Can it return information that is missing from the source?

No. It normalizes public records and preserves missing values. It does not infer stock quantities, reconstruct a historical archive, generate article bodies, or estimate facts the source did not provide. If an analysis needs additional evidence, treat that as a separate retrieval task rather than treating a nullable field as a model prompt to invent an answer.

### Can I rerun the same search tomorrow?

Yes. Use an external schedule and retain your previous identifiers if you want only newly observed records. A new observation is not necessarily a new publication: the actor may not have seen an older record previously. If you want to observe changes to known records, do not exclude those identifiers; compare their content hashes and preserve both versions with their fetch timestamps.

### Why did the run return fewer records than requested?

The source may contain fewer matches, filters or exclusions may remove entries, a source boundary may stop scanning, or the dollar cap may be smaller than the requested result cost. Status rows distinguish these situations. Increasing the count does not fix a blocked source. Check the error or cap first, then change the input that addresses that specific condition.

### How should I handle an unavailable source?

Keep the diagnostic with the failed target and timestamp. Retry only that target after checking whether the public endpoint is accessible. A storefront may disable its public feed, and a news query may temporarily return an error. The actor does not bypass passwords, log in to private systems or promise access to every source. Successful sources can still be processed and retained independently.

### Is the output suitable for legal or commercial reuse?

The actor accesses public information, but public access does not grant unrestricted rights to republish source content. Check the source's applicable terms and your intended use. Preserve attribution and source links, minimize copied content when publishing summaries, and handle any downstream personal information appropriately. The actor is a retrieval tool and does not determine the legal status of a particular reuse.
