# PDF to Markdown - Text, Scanned OCR & PDF转Markdown

PDF to Markdown provides pages and ocr for automated workflows, with JSON export, repeat monitoring and bounded pay-per-result delivery. Ingest text-bearing documents into agent research, retrieval and knowledge-base pipelines with page references.

## PDF to Markdown: scope and source behavior

Each nonempty PDF page becomes a Markdown document headed with its page number. Default ocrMode=disabled extracts the digital text layer only. Set ocrMode=auto to recognize printed text on pages with no extractable text, using ocrLanguage=eng, chi_sim or eng+chi_sim. Language is explicit, not automatically detected. Auto mode retains digital text when any non-whitespace text exists; it does not OCR image regions on those pages or replace a poor existing text layer. Scanned OCR uses Tesseract at 150 DPI, bounded to 20 million rendered pixels per page. English and simplified Chinese are supported; handwriting, skew, tiny print and complex layouts may produce errors. The extraction field identifies digital_text_no_ocr or ocr_scanned_page, with ocr_language on OCR rows. It returns plain text in Markdown, not reconstructed tables, headings or images. Empty results are not billed; successful OCR pages use the same page price. A page exceeding 200,000 characters fails explicitly. Encrypted, malformed, oversized or timed-out documents fail explicitly. startPage is one-based. maxPagesPerDocument caps inspected pages including blank pages. Downloads are separate .md files per page.

This is an independent Kestrel utility. It is not an official product of the source, registry, browser vendor or document library. It accepts the documented inputs and returns observed or extracted data with source references. It does not create source accounts, buy data subscriptions, send messages, alter websites or submit forms. The exact supported operation matters more than a generic promise to handle every possible agent request.

## PDF to Markdown for AI agents: which input answers which request?

Use this Actor when the requested output matches the scope above. Read the input schema before constructing a call. Required target values are explicit lists, while optional settings have documented defaults. A run with omitted target fields uses the demonstration values; production callers should always send their intended targets. A source account or source API key is not required for the supported operation.

| Request | Input approach |
| --- | --- |
| Try the documented example | Use the small JSON sample below. |
| Process a batch | Put up to 100 targets in `documentUrls`. |
| Return at most three paid results | Set `maxResults` to 3. |
| Skip previously delivered identities | Copy previous `id` values into `excludeIds`. |
| Skip previously seen snapshots | Copy previous `content_hash` values into `excludeContentHashes`. |
| Limit spending | Set `maxTotalChargeUsd` in the Apify run options, outside input JSON. |

```json
{
  "documentUrls": [
    "https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf"
  ],
  "startPage": 1,
  "maxPagesPerDocument": 5,
  "ocrMode": "disabled",
  "ocrLanguage": "eng",
  "maxResults": 3
}
```

The example is a small test, not a promise of a fixed row count. A document may contain empty pages, a website may display no email address, or an image may have no recognizable text. Valid empty extractions are distinguished from upstream errors. Keep the free summary alongside the dataset so your agent can explain what actually happened.

## Pages inputs and limits

| Input | Behavior |
| --- | --- |
| `documentUrls` | Public PDF URLs. Up to 100, 12 MB each. One billed nonempty page. Default digital text; enable ocrMode=auto for scanned pages without text. Use ocrLanguage=chi_sim or eng+chi_sim for Chinese. |
| `startPage` | First PDF page to inspect, one-based, e.g. 2. Default 1. Pages before this are not inspected or billed. |
| `maxPagesPerDocument` | Maximum PDF pages inspected per document from startPage, 1–20; default 5. This is a scan cap, not a guaranteed row count. Pages without extracted text consume it but have no result fee. A delivered text-bearing page is billed even if it contains no tables; OCR pages with recognized text use the same page price. maxResults separately caps paid rows. |
| `ocrMode` | "disabled" (default) extracts digital PDF text only. "auto" applies printed-text OCR only to pages with no extractable text. Does not OCR images on text-bearing pages or repair bad text layers. One billed nonempty page, same price. 扫描PDF识别。 |
| `ocrLanguage` | "eng" (default), "chi_sim" for simplified Chinese, or "eng+chi_sim" for mixed printed text. Used only when ocrMode=auto needs OCR; not automatic language detection. 中文扫描件识别。 |
| `maxResults` | Maximum paid rows across the run, 1–1000, default 20. Example: 3 for a sample. Exclusions and empty results apply before the cap. |
| `excludeIds` | Prior output id values to skip before billing, up to 5,000. Empty [] disables. Suppresses that identity even if content changed. |
| `excludeContentHashes` | Prior output content_hash values (64 lowercase hex characters), up to 5,000. Empty [] disables. Matching snapshots are skipped before billing. |

All fields reject incompatible types. Boolean values must be JSON booleans, not strings. Lists contain strings rather than nested request objects. Unknown property names fail validation to catch misspelled agent inputs early. Duplicate target strings are removed within a run. Domain names are normalized before deduplication. Exclusion lists are optional and bounded so a single run cannot grow without limit.

The overall result limit applies after exclusions. A qualifying result removed by an exclusion does not consume that result allowance. Source page limits, download limits and processing limits remain independent: excluding an old result does not refund the work needed to discover it. A request for twenty rows can therefore finish with fewer than twenty rows without indicating a bug.

## OCR output and download contract

One paid row represents one **nonempty PDF page**. The principal observed row fields are shown below. Optional source fields can be missing or null; consumers should not invent replacements. The output remains structured JSON even when a downloadable file is also produced.

| Field | Meaning |
| --- | --- |
| `page` | page |
| `total_pages` | total pages |
| `source_url` | source url |
| `extraction` | extraction |
| `markdown` | markdown |
| `characters` | characters |
| `width` | width |
| `height` | height |
| `id` | Stable identity within this Actor and target scope. |
| `content_hash` | SHA-256 of the normalized result for comparison. |
| `fetched_at` | UTC extraction or observation time. |

```json
{
  "page": 1,
  "total_pages": 1,
  "source_url": "https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf",
  "extraction": "digital_text_no_ocr",
  "markdown": "# Page 1\n\nNICS Firearm Background Checks\nNovember - 2015\nPre-Pawn Redemption Returned/Disposition Rentals Private Sale Return to Seller - Private Sale\nState / Territory Permit Handgun Long Gun *Other **Multiple Admin Handgun Long Gun *Other Handgun Long Gun *Other Handgun Long Gun *Other Handgun Long Gun Handgun Long Gun *Other Handgun Long Gun *Other Totals\nAlabama 18,870 23,022 22,650 859 1,178 0 14 15 0 2,179 2,307 11 0 0 0 13 14 0 3 2 0 71,137\nAlaska 209 3,062 3,209 191 184 0 9 3 0 100 100 0 18 9 1 0 0 0 0 0 0 7,095\nArizona 2,303 12,382 9,041 707 618 0 5 3 0 1,273 648 4 76 8 1 9 6 1 1 1 0 27,087\nArkansas 3,298 6,359 11,611 168 376 0 12 6 1 922 2,275 1 0 0 0 6 12 1 0 0 0 25,048\nCalifornia 98452 41181 35007 4559 0 0 0 0 0 480 433 4 0 0 0 0 0 0 0 0 0 180116\nColorado 4,144 19,784 16,082 932 1,151 0 0 0 0 0 0 0 144 34 0 0 0 0 0 0 0 42,271\nConnecticut 9,631 11,594 5,072 134 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 26,438\nDelaware 204 2,152 2,424 65 72 0 3 4 0 17 12 0 0 0 0 59 24 0 4 0 0 5,040\nDistrict of Columbia 8 54 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 64\nFlorida 15,907 50,796 28,981 2,268 1,957 121 8 9 0 2,248 1,135 2 40 5 0 36 19 0 0 0 0 103,532\nGeorgia 14,111 16,635 15,227 448 758 0 10 14 0 1,772 1,796 4 0 0 0 10 9 1 0 0 0 50,795\nGuam 0 100 55 12 3 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 171\nHawaii 1,248 0 0 0 0 0 0 0 0 0 0 0 1 3 0 0 0 0 0 0 0 1,252\nIdaho 1,944 3,609 5,227 190 189 0 0 4 0 273 455 1 22 4 1 1 2 0 0 3 0 11,925\nIllinois 87,190 24,412 17,227 0 1,032 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 129,861\nIndiana 81,935 25,519 20,227 1,113 808 0 2 3 0 13 629 5 28 0 0 31 13 1 2 4 0 130,333\nIowa 8,785 267 4,596 27 4 37 0 1 0 0 71 0 4 2 0 0 0 0 0 0 0 13,794\nKansas 894 7,086 8,702 311 396 3 1 3 1 486 530 2 2 0 0 6 10 0 0 0 0 18,433\nKentucky 264,140 12,155 14,847 254 648 1 9 11 0 1,491 2,315 2 2 2 0 6 8 0 0 0 0 295,891\nLouisiana 1,945 14,708 17,368 697 793 0 5 11 2 884 1,323 3 0 0 0 1 10 1 0 1 0 37,752\nMaine 299 4,048 4,387 135 171 2 0 0 0 70 165 0 6 7 0 4 3 0 0 0 0 9,297\nMariana Islands 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\nMaryland 1,512 3,220 8,310 96 9 0 0 3 0 72 213 2 14 3 1 1 6 1 0 0 0 13,463\nMassachusetts 5,214 6,083 3,931 402 175 0 0 1 0 2 5 0 1 0 1 42 23 5 0 0 0 15,885\nMichigan 16,786 13,634 17,604 385 238 1,025 1 4 0 5 489 2 69 24 0 4 1 1 2 3 1 50,278\nMinnesota 18,939 9,373 14,173 486 330 0 1 2 0 176 512 0 8 11 0 2 6 0 0 2 2 44,023\nMississippi 618 9,785 13,191 267 523 9 28 20 0 1,171 1,874 1 0 0 0 6 6 3 2 0 0 27,504\nMissouri 5,884 21,135 22,852 1,004 1,060 0 11 16 0 1,131 1,754 3 99 11 4 33 25 6 0 3 0 55,031\nMontana 852 2,848 5,170 90 197 10 1 4 6 391 828 1 11 4 0 0 2 0 0 0 0 10,415\nNebraska 4,258 173 3,724 23 10 0 1 0 0 5 96 1 7 0 0 0 0 1 0 0 0 8,299\nNevada 1,543 4,889 3,272 193 287 0 0 0 0 284 163 0 1 0 0 0 0 0 0 0 0 10,632\nNew Hampshire 3,630 4,847 4,165 95 2 1 0 0 0 0 23 1 69 11 1 2 2 0 0 1 0 12,850\nNew Jersey 0 3,462 4,704 147 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8,313\nNew Mexico 829 5,247 4,974 334 277 0 2 3 1 397 618 1 33 0 0 0 4 0 1 0 0 12,721\nNew York 2,906 8,650 23,519 665 149 0 0 3 0 16 25 0 0 0 0 243 220 16 5 4 0 36,421\nNorth Carolina 22,469 1,370 20,107 576 202 0 16 25 0 1,771 2,644 7 0 0 0 2 26 1 1 0 0 49,217\nNorth Dakota 453 1,720 3,744 65 79 0 0 3 0 65 157 0 0 0 0 1 1 0 0 0 0 6,288\nOhio 9,338 34,878 31,817 1,392 1,483 0 24 16 1 1,228 1,389 4 0 0 0 21 22 1 1 0 1 81,616\nOklahoma 0 15,005 14,753 778 998 0 11 7 1 1,639 2,226 6 0 0 0 11 21 0 0 1 0 35,457\nOregon 35 13,586 11,832 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 25,453\nPennsylvania 24,136 62,752 16,297 0 0 58 0 0 0 0 0 0 446 147 0 0 0 0 0 0 0 103,836\nPuerto Rico 0 1,033 170 11 20 0 0 0 0 6 1 0 0 0 0 0 0 0 0 1 0 1,242\nRhode Island 0 954 932 57 135 0 0 0 0 3 4 0 0 0 0 12 2 1 1 0 0 2,101\nSouth Carolina 7,284 11,452 10,393 561 438 0 3 8 0 979 912 3 16 4 0 4 6 0 1 0 0 32,064\nSouth Dakota 819 2,765 5,484 143 151 0 0 1 0 123 239 0 0 0 0 1 1 0 0 0 0 9,727\nTennessee 9,509 28,815 24,023 0 1,300 0 0 0 0 0 0 0 17 1 5 0 0 0 0 0 0 63,670\nTexas 21,550 56,941 51,670 2,532 3,048 0 29 20 0 5,748 5,331 21 1 2 1 42 36 4 1 5 0 146,982\nUtah 10,429 4,314 5,857 195 262 0 0 1 0 209 285 1 140 58 21 0 0 0 0 0 0 21,772\nVermont 0 1,189 1,826 49 70 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 3,136\nVirgin Islands 93 13 2 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 109\nVirginia 622 24,052 22,348 974 0 0 0 0 0 0 0 0 10 4 0 0 0 0 0 0 0 48,010\nWashington 10,314 15,822 12,425 1,238 606 4 8 8 0 1,096 1,129 3 356 159 3 444 340 19 6 9 0 43,989\nWest Virginia 2,217 6,953 11,561 224 478 2 4 9 0 923 2,678 3 0 0 0 3 8 0 0 0 0 25,063\nWisconsin 5,867 13,700 17,759 458 45 0 0 3 0 124 513 3 15 20 4 10 15 1 0 3 1 38,541\nWyoming 383 1,745 2,372 87 104 1 0 4 0 132 184 0 0 0 0 1 2 0 0 2 0 5,017\nTotals 804,006 671,330 636,903 26,597 23,015 1,281 218 249 13 29,905 38,487 102 1,656 533 44 0 0 1,067 905 65 31 45 5 2,236,457\n*Refers to frames, receivers and other firearms that are not either handguns or long guns (rifles or shotguns), such as firearms having a pistol grip that expel a shotgun shell\nNOTES:\n**Multiple (multiple types of firearms selected)\nSome states may reflect lower than expected numbers for handgun checks based on varying state laws pertaining to handgun permits Since the permit check is done in place of the NICS check in most of the affected states, the low handgun statistics are often balanced out by a higher number of handgun permit checks\nDISCLAIMERS:\nThese statistics represent the number of firearm background checks initiated through the NICS They do not represent the number of firearms sold Based on varying state laws and purchase scenarios, a one-to-one correlation cannot be made between a firearm background check and a firearm sale\nPage 1 of 205\n",
  "characters": 5656,
  "width": 1008,
  "height": 612
}
```

Document conversion, OCR, website Markdown and screenshots include `download_url`, `artifact_key`, `artifact_bytes` and `artifact_sha256` when a file is delivered. Those fields identify a file in the run's Apify key-value store. Do not remove the signature query parameter from a generated download URL. The generated link includes a record-specific signature for downloading without an Apify token. Files remain available only while the store and record are retained. Export important artifacts into your own storage rather than treating a run as a permanent archive.

Email, DNS, registration and weather rows are dataset records and do not create a separate file download. Use Apify dataset export to obtain JSON or CSV where useful. Nested values such as tables, words, entities and forecasts are better preserved as JSON than flattened CSV. A download does not contain more coverage than the associated row; a PDF page workbook, for example, does not silently include unprocessed document pages.

## What does a successful run mean?

A successful run means the requested bounded work finished without a reported target error. It does not guarantee complete website coverage, perfect OCR, a reachable mailbox, future weather accuracy or a registry field that the source did not provide. Each product's limitations are specified in the scope section. Callers should verify a representative output before placing it into a consequential downstream workflow.

The free `SUMMARY` record contains `status`, `rows`, `excluded`, `targets_attempted`, `targets_requested`, `stop_reason`, `errors`, `artifacts` and `coverage`. It also reports `source_http_requests` (including redirects and failed connection attempts), `source_downloaded_bytes` (decoded response bytes) and `dns_cache_hits` for workload inspection. These counters exclude Apify storage traffic and system DNS resolution. The row count is the number delivered into the paid dataset. The artifact list contains file keys only for successfully delivered file-bearing rows. A budget or result limit can stop the run before every requested target is attempted.

Status `no_matches` means no qualifying row was produced without a target failure. Status `error` means a failure with no valid delivered row, and `partial_error` means valid rows were delivered before or alongside a failure. Error states fail the Actor run so automation does not mistake an unavailable source for an empty result. Invalid inputs are reported as `invalid_input` before any target access.

## How much does it cost?

The event price is **$0.01 per delivered nonempty PDF page**, equivalent to **$10 per 1,000 rows**. Ten rows cost $0.1; one hundred cost $1. There is no Actor start fee. Compute and network access are included in the event price. Nested data and files described for a row are included in that row's price. Prose pages without tables are paid results when they contain extracted text; blank or empty-text pages have no result fee.

Within-run duplicates, excluded identities, excluded matching snapshots and empty extractions are free. Failures without delivered data produce no result charge. An invalid-syntax email is a valid diagnostic result and is billed as an email check; a DNS NXDOMAIN response and a registry not-found response are likewise useful observations, not failed requests. The Actor never charges a separate event for every nested word, cell, DNS record or forecast step.

Set `maxTotalChargeUsd` in Apify run options for a monetary ceiling. It is not an Actor input field. The charging manager is checked before starting a target and before delivering a result; delivery stops when no complete result event fits the remaining budget. Previously delivered rows remain available and retain their charges if a later target fails. Customer event prices and developer infrastructure costs are different figures; a test run's compute cost is not a customer revenue measurement.

## How do Python, JavaScript and curl integrations work?

The Python example uses apify-client 3.x and its typed Run object. Use an environment variable for the Apify token and the asynchronous run API for reliable orchestration. Start the run, wait for its terminal status, then read both the dataset and the free summary. Keep the run identifier in downstream records so an extraction can be traced to its inputs, build and status. Never paste credentials into target URLs.

```python
import os
from decimal import Decimal
from apify_client import ApifyClient
client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('kestrel/pdf-to-markdown-pages').call(
    run_input={'documentUrls': ['https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf'], 'startPage': 1, 'maxPagesPerDocument': 5, 'ocrMode': 'disabled', 'ocrLanguage': 'eng', 'maxResults': 3}, max_total_charge_usd=Decimal('0.10'))
rows = list(client.dataset(run.default_dataset_id).iterate_items())
summary = client.key_value_store(run.default_key_value_store_id).get_record('SUMMARY')
print(rows, summary)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({token: process.env.APIFY_TOKEN});
const run = await client.actor('kestrel/pdf-to-markdown-pages').call(
  {"documentUrls": ["https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf"], "startPage": 1, "maxPagesPerDocument": 5, "ocrMode": "disabled", "ocrLanguage": "eng", "maxResults": 3}, {maxTotalChargeUsd: 0.10});
const rows = await client.dataset(run.defaultDatasetId).listItems();
const summary = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('SUMMARY');
console.log(rows.items, summary);
```

```bash
curl --request POST \
  'https://api.apify.com/v2/acts/kestrel~pdf-to-markdown-pages/runs?maxTotalChargeUsd=0.10' \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"documentUrls": ["https://raw.githubusercontent.com/jsvine/pdfplumber/stable/examples/pdfs/background-checks.pdf"], "startPage": 1, "maxPagesPerDocument": 5, "ocrMode": "disabled", "ocrLanguage": "eng", "maxResults": 3}'
```

## How should repeat monitoring work?

Persist returned identities and hashes in your own database. On subsequent runs, supply the relevant exclusion list. An identity exclusion suppresses that target or page even if its content changes. A hash exclusion suppresses only a previously seen normalized state. Choose hashes for change monitoring and identities for one-time collection. The Actor does not maintain a hidden shared contact history across customers.

The hash is for comparison, not proof of authenticity. It excludes the observation timestamp and storage download URL. Screenshot image bytes contribute to their hash, so dynamic banners, animations or dates can make a new screenshot differ even when the site's main content is unchanged. DNS TTLs and evolving forecasts also make snapshots change. Use field-specific downstream comparisons when your business definition of change is narrower.

Batch related targets and choose a schedule that matches the source update cadence. A repeated run cannot force a registry, weather model or website to publish new information. Avoid retry loops on permanent input errors. A transient upstream failure can justify a later bounded retry, with exclusions for rows already delivered. There is no built-in notification, email sending or schedule creation; those actions belong to the calling workflow.

## How do n8n, Make and MCP agents use this?

Use an Apify connector or an HTTP request module to start the run and wait for completion. In n8n and Make, branch on the run status before iterating rows. Download file artifacts only when a row actually contains an artifact key. Store the summary on both successful and failed branches. This makes partial results usable without hiding unobserved targets.

An MCP agent should inspect the Actor details, choose literal input fields and begin with a small sample. It should quote observed values and source URLs, preserve units and page numbers, and describe source limitations when they affect the answer. A structured result is easier to use correctly than an undocumented text blob, but it still requires interpretation. Do not treat a confidence score as certainty or a missing field as a negative fact.

## How do I read scanned PDFs?

Set `ocrMode` to `auto` and choose `ocrLanguage`: `eng`, `chi_sim`, or `eng+chi_sim`. Only pages without extractable text use OCR. Digital pages keep their original text. Blank pages remain free; a delivered OCR page has the same price as a digital page. OCR does not reconstruct tables or recover image text on pages that already have a text layer.

扫描 PDF 转 Markdown：设置 `ocrMode=auto`，简体中文使用 `ocrLanguage=chi_sim`，中英混合使用 `eng+chi_sim`。仅对无可提取文本的页面进行 OCR；已有文本的页面保留数字文本。空白页免费，成功识别页按相同单价计费。请核对识别结果；不保证手写、倾斜或低清晰度文字。

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

本工具支持PDF 转 Markdown、文档提取、文本解析。输入参数名保持英文，便于 AI 智能体和 MCP 客户端正确调用。结果包含来源、采集时间、稳定标识和内容哈希。请先使用少量目标验证结果，再扩大批量任务。

每条实际交付的结果计费；重复、排除和空提取结果不收费。请在 Apify 运行选项设置 `maxTotalChargeUsd`，不要放进输入 JSON。`maxResults` 限制整个任务的付费结果数量。文件转换工具会提供下载链接和文件键，访问权限由 Apify 存储设置决定。

本工具不会编造缺失字段，也不保证源站完整覆盖。邮箱 DNS 检查不等于邮箱可投递验证；数字 PDF 提取不等于扫描件 OCR；天气预报不等于历史实测数据。失败任务与真正的空结果明确区分，请同时检查数据集及免费的 `SUMMARY`。

Source documentation: https://github.com/jsvine/pdfplumber

Last verified working: 2026-10-17
