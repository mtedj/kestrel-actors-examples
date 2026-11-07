# Website Screenshot - PNG, Mobile Viewports & 网页截图

Website Screenshot provides png and downloads for automated workflows, with JSON export, repeat monitoring and bounded pay-per-result delivery. Capture visual evidence, website QA samples and competitor landing-page snapshots in automated workflows.

## Website Screenshot: scope and source behavior

Uses headless Chromium. width and height specify CSS viewport pixels, not a real device profile; mobile-sized viewports do not emulate touch, device sensors or a mobile user agent. fullPage=true captures the page height up to 12,000 pixels and reports height_capped when clipped. A bounded one-second settling period follows DOMContentLoaded; this is not a guarantee every asynchronous widget has loaded. Public GET requests are fetched through a validating network layer; POST requests, WebSockets, service workers, private addresses, more than 120 requests and oversized assets are blocked. blocked_requests exposes degraded capture. No credentials, cookie upload, custom scripts, form submissions or challenge solving are supported.

This is an independent Kestrel utility. It is not an official product of the source, registry, browser vendor or document library. It accepts the documented inputs and returns observed or extracted data with source references. It does not create source accounts, buy data subscriptions, send messages, alter websites or submit forms. The exact supported operation matters more than a generic promise to handle every possible agent request.

## Website Screenshot for AI agents: which input answers which request?

Use this Actor when the requested output matches the scope above. Read the input schema before constructing a call. Required target values are explicit lists, while optional settings have documented defaults. A run with omitted target fields uses the demonstration values; production callers should always send their intended targets. A source account or source API key is not required for the supported operation.

| Request | Input approach |
| --- | --- |
| Try the documented example | Use the small JSON sample below. |
| Process a batch | Put up to 100 targets in `startUrls`. |
| Return at most three paid results | Set `maxResults` to 3. |
| Skip previously delivered identities | Copy previous `id` values into `excludeIds`. |
| Skip previously seen snapshots | Copy previous `content_hash` values into `excludeContentHashes`. |
| Limit spending | Set `maxTotalChargeUsd` in the Apify run options, outside input JSON. |

```json
{
  "startUrls": [
    "https://example.com"
  ],
  "width": 1440,
  "height": 900,
  "fullPage": true,
  "maxResults": 3
}
```

The example is a small test, not a promise of a fixed row count. A document may contain empty pages, a website may display no email address, or an image may have no recognizable text. Valid empty extractions are distinguished from upstream errors. Keep the free summary alongside the dataset so your agent can explain what actually happened.

## PNG inputs and limits

| Input | Behavior |
| --- | --- |
| `startUrls` | Public HTTP(S) website URLs, e.g. ["https://example.com"]. Up to 100. No credentials or private-network URLs. One target may yield multiple contacts only in Email Finder. |
| `width` | Viewport width in CSS pixels, 320–1920. Default 1440. Example: 390 for a mobile-sized page, without mobile device emulation. |
| `height` | Viewport height in CSS pixels, 320–1080. Default 900. Used for viewport screenshots; full-page screenshots can be taller. |
| `fullPage` | true (default) captures the full page up to 12,000 pixels tall; false captures the viewport. One screenshot price either way; height_capped reports clipping. |
| `maxResults` | Maximum paid rows across the run, 1–1000, default 20. Example: 3 for a sample. Exclusions and empty results apply before the cap. |
| `excludeIds` | Prior output id values to skip before billing, up to 5,000. Empty [] disables. Suppresses that identity even if content changed. |
| `excludeContentHashes` | Prior output content_hash values (64 lowercase hex characters), up to 5,000. Empty [] disables. Matching snapshots are skipped before billing. |

All fields reject incompatible types. Boolean values must be JSON booleans, not strings. Lists contain strings rather than nested request objects. Unknown property names fail validation to catch misspelled agent inputs early. Duplicate target strings are removed within a run. Domain names are normalized before deduplication. Exclusion lists are optional and bounded so a single run cannot grow without limit.

The overall result limit applies after exclusions. A qualifying result removed by an exclusion does not consume that result allowance. Source page limits, download limits and processing limits remain independent: excluding an old result does not refund the work needed to discover it. A request for twenty rows can therefore finish with fewer than twenty rows without indicating a bug.

## Downloads output and download contract

One paid row represents one **screenshot**. The principal observed row fields are shown below. Optional source fields can be missing or null; consumers should not invent replacements. The output remains structured JSON even when a downloadable file is also produced.

| Field | Meaning |
| --- | --- |
| `source_url` | source url |
| `title` | title |
| `viewport_width` | viewport width |
| `viewport_height` | viewport height |
| `full_page` | full page |
| `height_capped` | height capped |
| `blocked_requests` | blocked requests |
| `id` | Stable identity within this Actor and target scope. |
| `content_hash` | SHA-256 of the normalized result for comparison. |
| `fetched_at` | UTC extraction or observation time. |

```json
{
  "source_url": "https://example.com/",
  "title": "Example Domain",
  "viewport_width": 1440,
  "viewport_height": 900,
  "full_page": true,
  "height_capped": false,
  "blocked_requests": 0
}
```

Document conversion, OCR, website Markdown and screenshots include `download_url`, `artifact_key`, `artifact_bytes` and `artifact_sha256` when a file is delivered. Those fields identify a file in the run's Apify key-value store. Do not remove the signature query parameter from a generated download URL. The generated link includes a record-specific signature for downloading without an Apify token. Files remain available only while the store and record are retained. Export important artifacts into your own storage rather than treating a run as a permanent archive.

Email, DNS, registration and weather rows are dataset records and do not create a separate file download. Use Apify dataset export to obtain JSON or CSV where useful. Nested values such as tables, words, entities and forecasts are better preserved as JSON than flattened CSV. A download does not contain more coverage than the associated row; a PDF page workbook, for example, does not silently include unprocessed document pages.

## What does a successful run mean?

A successful run means the requested bounded work finished without a reported target error. It does not guarantee complete website coverage, perfect OCR, a reachable mailbox, future weather accuracy or a registry field that the source did not provide. Each product's limitations are specified in the scope section. Callers should verify a representative output before placing it into a consequential downstream workflow.

The free `SUMMARY` record contains `status`, `rows`, `excluded`, `targets_attempted`, `targets_requested`, `stop_reason`, `errors`, `artifacts` and `coverage`. It also reports `source_http_requests` (including redirects and failed connection attempts), `source_downloaded_bytes` (decoded response bytes) and `dns_cache_hits` for workload inspection. These counters exclude Apify storage traffic and system DNS resolution. The row count is the number delivered into the paid dataset. The artifact list contains file keys only for successfully delivered file-bearing rows. A budget or result limit can stop the run before every requested target is attempted.

Status `no_matches` means no qualifying row was produced without a target failure. Status `error` means a failure with no valid delivered row, and `partial_error` means valid rows were delivered before or alongside a failure. Error states fail the Actor run so automation does not mistake an unavailable source for an empty result. Invalid inputs are reported as `invalid_input` before any target access.

## How much does it cost?

The event price is **$0.025 per delivered screenshot**, equivalent to **$25 per 1,000 rows**. Ten rows cost $0.25; one hundred cost $2.5. There is no Actor start fee. Compute and network access are included in the event price. Nested data and files described for a row are included in that row's price.

Within-run duplicates, excluded identities, excluded matching snapshots and empty extractions are free. Failures without delivered data produce no result charge. An invalid-syntax email is a valid diagnostic result and is billed as an email check; a DNS NXDOMAIN response and a registry not-found response are likewise useful observations, not failed requests. The Actor never charges a separate event for every nested word, cell, DNS record or forecast step.

Set `maxTotalChargeUsd` in Apify run options for a monetary ceiling. It is not an Actor input field. The charging manager is checked before starting a target and before delivering a result; delivery stops when no complete result event fits the remaining budget. Previously delivered rows remain available and retain their charges if a later target fails. Customer event prices and developer infrastructure costs are different figures; a test run's compute cost is not a customer revenue measurement.

## How do Python, JavaScript and curl integrations work?

The Python example uses apify-client 3.x and its typed Run object. Use an environment variable for the Apify token and the asynchronous run API for reliable orchestration. Start the run, wait for its terminal status, then read both the dataset and the free summary. Keep the run identifier in downstream records so an extraction can be traced to its inputs, build and status. Never paste credentials into target URLs.

```python
import os
from decimal import Decimal
from apify_client import ApifyClient
client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('kestrel/website-screenshot-capture').call(
    run_input={'startUrls': ['https://example.com'], 'width': 1440, 'height': 900, 'fullPage': True, 'maxResults': 3}, max_total_charge_usd=Decimal('0.10'))
rows = list(client.dataset(run.default_dataset_id).iterate_items())
summary = client.key_value_store(run.default_key_value_store_id).get_record('SUMMARY')
print(rows, summary)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({token: process.env.APIFY_TOKEN});
const run = await client.actor('kestrel/website-screenshot-capture').call(
  {"startUrls": ["https://example.com"], "width": 1440, "height": 900, "fullPage": true, "maxResults": 3}, {maxTotalChargeUsd: 0.10});
const rows = await client.dataset(run.defaultDatasetId).listItems();
const summary = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('SUMMARY');
console.log(rows.items, summary);
```

```bash
curl --request POST \
  'https://api.apify.com/v2/acts/kestrel~website-screenshot-capture/runs?maxTotalChargeUsd=0.10' \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"startUrls": ["https://example.com"], "width": 1440, "height": 900, "fullPage": true, "maxResults": 3}'
```

## How should repeat monitoring work?

Persist returned identities and hashes in your own database. On subsequent runs, supply the relevant exclusion list. An identity exclusion suppresses that target or page even if its content changes. A hash exclusion suppresses only a previously seen normalized state. Choose hashes for change monitoring and identities for one-time collection. The Actor does not maintain a hidden shared contact history across customers.

The hash is for comparison, not proof of authenticity. It excludes the observation timestamp and storage download URL. Screenshot image bytes contribute to their hash, so dynamic banners, animations or dates can make a new screenshot differ even when the site's main content is unchanged. DNS TTLs and evolving forecasts also make snapshots change. Use field-specific downstream comparisons when your business definition of change is narrower.

Batch related targets and choose a schedule that matches the source update cadence. A repeated run cannot force a registry, weather model or website to publish new information. Avoid retry loops on permanent input errors. A transient upstream failure can justify a later bounded retry, with exclusions for rows already delivered. There is no built-in notification, email sending or schedule creation; those actions belong to the calling workflow.

## How do n8n, Make and MCP agents use this?

Use an Apify connector or an HTTP request module to start the run and wait for completion. In n8n and Make, branch on the run status before iterating rows. Download file artifacts only when a row actually contains an artifact key. Store the summary on both successful and failed branches. This makes partial results usable without hiding unobserved targets.

An MCP agent should inspect the Actor details, choose literal input fields and begin with a small sample. It should quote observed values and source URLs, preserve units and page numbers, and describe source limitations when they affect the answer. A structured result is easier to use correctly than an undocumented text blob, but it still requires interpretation. Do not treat a confidence score as certainty or a missing field as a negative fact.

## FAQ: common operational questions

### Does this accept authenticated sites or private-network URLs?

No. Only public HTTP(S) targets on standard ports are supported for website and document inputs. Embedded credentials, loopback, private, link-local and reserved addresses are rejected. DNS resolution is checked before connections, and redirects are revalidated. The screenshot browser routes public GET resources through the same bounded fetch layer. This protects the execution environment and keeps the supported input contract predictable.

### Does it translate or invent missing content?

No. Chinese discovery text helps users find the utility, while output values retain their source meaning. OCR language selection controls recognition, not translation. A missing field stays missing or null. Document extraction does not infer a table that was not detected, and website conversion does not summarize text with an LLM. Downstream agents can translate or analyze the output separately while retaining the original evidence.

### What happens with a large or malformed file?

Downloads are capped, and parsing takes place in a separate process with a wall-time limit. An oversized, encrypted or malformed document can fail explicitly. This is preferable to returning a silently incomplete conversion. The supported page and image limits are documented in the input descriptions and scope. Split large batches into smaller runs so one problematic target is easy to isolate and retry.

### Are results deterministic?

The same stable source and settings usually produce equivalent normalized text or structured data, but upstream pages and endpoints change. Browser screenshots also depend on timing, responsive layout, fonts and dynamic content. Workbook binary metadata can differ even when extracted table cells match; the comparison hash uses normalized cells rather than requiring byte-identical workbooks. Preserve both hashes and source references when building an audit trail.

### Can I claim completeness from an empty dataset?

No. Read the run status and summary first. A genuinely empty extraction, a scan cap and an upstream failure are different outcomes. An email-free starting page does not establish that a company has no email address. A PDF page without extractable text may be a scan. A missing registry object does not establish that a domain is available to buy. The utility reports the observed operation, not a broader unsupported conclusion.

### What legal and source-use considerations apply?

Use public data and documents for purposes you are authorized to pursue, and retain applicable source notices. Public availability does not remove copyright or database restrictions. Source names identify the tool or service used and do not imply endorsement. MET Norway data requires attribution and its license reference, which the forecast row includes. Registry notices are preserved. The utility does not grant rights over supplied documents or collected website content.

## 中文说明：输入、结果与费用

本工具支持网页截图、长截图、移动端网站截图。输入参数名保持英文，便于 AI 智能体和 MCP 客户端正确调用。结果包含来源、采集时间、稳定标识和内容哈希。请先使用少量目标验证结果，再扩大批量任务。

每条实际交付的结果计费；重复、排除和空提取结果不收费。请在 Apify 运行选项设置 `maxTotalChargeUsd`，不要放进输入 JSON。`maxResults` 限制整个任务的付费结果数量。文件转换工具会提供下载链接和文件键，访问权限由 Apify 存储设置决定。

本工具不会编造缺失字段，也不保证源站完整覆盖。邮箱 DNS 检查不等于邮箱可投递验证；数字 PDF 提取不等于扫描件 OCR；天气预报不等于历史实测数据。失败任务与真正的空结果明确区分，请同时检查数据集及免费的 `SUMMARY`。

Source documentation: https://playwright.dev/python/docs/screenshots

Last verified working: 2026-10-17
