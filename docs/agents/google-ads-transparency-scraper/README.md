# Google Ads Transparency Scraper

Google Ads Transparency Scraper collects competitor ads and ad copy from the public advertising library. Give it company domains or exact advertiser IDs and receive structured creative records, preview URLs, advertiser identities and source dates. Optional English OCR reads text from preview images, while explicit extraction statuses distinguish available copy from missing or approximate text. This is an independent Google Ads API alternative for research, not an official advertising management API.


## 谷歌广告透明度：广告素材采集与竞品广告监控

从 Google Ads Transparency Center 采集 **谷歌广告、广告素材、广告主、预览链接和展示日期**。按域名或准确的广告主 ID 查询；`onlyNewOrChanged` 可在重复运行时只交付新增或变化的素材。域名匹配可能包含代理商、经销商或提及该域名的广告，**不能证明广告归属**。需要精确归属范围时，应先确认广告主，再传入 `advertiserIds`。

| 中文需求 | 正确参数或处理方式 |
|---|---|
| 按网站发现相关广告 | `domains: ["shopify.com"]` |
| 只查询已确认的广告主 | `advertiserIds: ["实际的 AR 开头广告主 ID"]` |
| 最多返回 10 个素材 | `maxAdsPerSource: 10`，`maxResults: 10` |
| 只监控新增或变化素材 | `onlyNewOrChanged: true`，固定 `monitorKey: "shopify-cn-monitor"` |
| 不需要 OCR 文案 | `includeAdText: false` |
| 查看某地区展示的广告 | `region: "US"`；这是展示地区，不是广告主注册地 |

```json
{"domains":["shopify.com"],"maxAdsPerSource":10,"maxResults":10,"includeAdText":false,"onlyNewOrChanged":true,"monitorKey":"shopify-cn-monitor"}
```

首次使用某个监控键会建立基线并交付扫描到的素材；后续运行跳过未变化的素材。监控键绑定查询范围，改变域名、广告主或过滤条件时使用新的键。运行一次不会创建定时任务；每日调度由 Apify 或外部工作流负责。扫描及结果上限可能导致覆盖不完整，不能据此判断广告已停止投放。

一个 `type="ad"` 行包含 `advertiser_id`、`advertiser_name`、`creative_id`、`ad_url`、`format`、`first_shown`、`last_shown`、`preview_urls`、`ad_text`、`text_status` 和 `content_hash`。当前 OCR 面向英文，**不保证识别中文文案**；必须保留 `text_status`，不要把缺失文案当作空白广告。本工具不提供广告花费、点击、展示次数或受众画像。

费用为 **每 1,000 个已交付素材 $3**；10 个最多 $0.03。无启动费，英文 OCR 不另计费。被排除、重复、未变化的监控素材、空结果、失败详情和状态行不收费。使用 Apify 运行选项 `maxTotalChargeUsd` 设置金额上限，不能放在输入 JSON 中。

这是独立的 Kestrel 研究工具，与 [Google Ads](https://ads.google.com) 无隶属关系，也不是广告投放管理 API。


## Google Ads scraper for AI agents: which input answers which request?

Use this actor when a marketing or research agent needs evidence about advertising creatives. It accepts a small list of domains directly, so an agent can begin with a company website instead of navigating a browser to find a library account. Domain matching is discovery, however, and it must not be confused with ownership. Ads returned for a website can belong to resellers, agencies, partners or unrelated advertisers whose creatives mention that domain. The record preserves the actual advertiser identity. Use those advertiser IDs for a second, more precise collection when the task asks for one legal entity's ads.

| Request | Input choice |
| --- | --- |
| Collect three example ads associated with Shopify | `domains: ["shopify.com"], maxResults: 3` |
| Collect only a particular advertiser account | `advertiserIds: ["AR01625195283841286145"]`, leave domains empty |
| Research ads shown in the United States | `region: "US"` |
| Collect creative images without OCR | `includeAdText: false` |
| Find ads with recent source activity dates | `lastShownAfter: "2026-10-01"` |
| Keep a repeat-run feed of new or changed creatives | `onlyNewOrChanged: true, monitorKey: "shopify-weekly"` |
| Avoid previously collected creative IDs | `excludeCreativeIds: ["CR02097857130550788097"]` |
| Limit the row charge to thirty cents | `maxResults: 100`, plus platform run option `maxTotalChargeUsd: 0.30` |

Do not use this actor to manage your own campaigns, retrieve your account's conversion reports, discover every advertiser bidding on a keyword, or estimate competitor ad spend. It does not expose private account metrics. It also does not automatically decide that a long-running creative is profitable. Publication dates, performance and financial outcomes are different facts.

## Google Ads creatives: what does one row contain?

A paid record has `type: "ad"`. The identity fields are `advertiser_id`, `advertiser_name` and `creative_id`. The source evidence link is `ad_url`, which opens the creative in the public library. `query_type` and `query` record the input that first delivered the ad. When several inputs return the same advertiser and creative pair, the actor emits it once and retains that first query as provenance. It does not expand a duplicate into a second billed record.

`attribution` is `domain_match_not_ownership` for domain discovery, or `advertiser_id` for exact account collection. `format` is the source classification: text, image, video or unknown. A text-format ad may still be exposed as an image preview rather than machine-readable copy. `first_shown` and `last_shown` are dates from search metadata, not independent observations that the ad was running at the instant of the scrape. `fetched_at` is the time this actor collected the record.

`preview_urls` contains up to fifty source preview or renderer URLs. `variants_count` reports the number of detail variants returned by the source, which may be larger than the number of unique preview URLs. `detail_status` is `ok` for delivered ad records: missing or mismatched creative details are skipped and reported as errors, without a paid ad row. These URLs can expire or become unavailable later, so retain your own permitted archival copies if your workflow needs durable media.

`ad_text` contains extracted text or null. `text_method` identifies approximate English OCR, renderer text, a combination, unavailable content or a request that omitted extraction. `text_status` is extracted, partial, unavailable, error or not_requested. Text extraction is best effort and does not promise a complete transcription of every variant. Only the first three supported previews are attempted. Video audio is not transcribed, and the actor does not download video streams.

`content_hash` fingerprints advertiser identity, creative identity, format and preview URLs. `change_type` is snapshot for ordinary collection, or new/updated for monitoring. The hash normalizes transient renderer callback IDs and signatures, and deliberately excludes serving dates and OCR output: changing activity timestamps and small OCR differences should not produce recurring false creative changes. A provider changing a preview URL can still count as an update, while a change behind an identical URL may not be detected.

## Google Ads monitoring: how do repeat runs work?

Monitoring stores fingerprints in a named key-value store belonging to the caller. Enable `onlyNewOrChanged` and provide `monitorKey`. The first run establishes a baseline by delivering and charging for the ads it finds. Subsequent runs skip fingerprints that match and deliver unseen or changed creatives. There is no separate monitoring fee, and unchanged records are not billed. Limits still apply: a large initial collection may require additional runs to fill in the baseline.

The key is bound to the domain list, advertiser list, region, format and date filters. A different collection scope must use a different key; the actor rejects a conflicting scope instead of silently comparing unrelated campaigns. Keep the same ordering of sources when reusing a key. Only delivered paid rows advance the cache, so hitting a budget cap does not mark undelivered ads as already processed. Checkpoints reduce replay after interruption, although an abrupt failure can still cause some previously delivered records to be emitted again. Downstream systems should upsert using advertiser and creative IDs.

The state retains up to fifty thousand fingerprints. Old entries can be evicted when the bound is exceeded and may later appear as new. Never schedule overlapping runs with the same monitor key: the storage is not a distributed transactional lock, and concurrent writers can overwrite progress. Create separate keys for independent workflows. The actor does not create schedules itself; configure recurrence through Apify schedules or your existing automation platform.

A missing creative is not evidence that an ad stopped. Search caps, pagination, regional visibility, source restrictions and temporary errors can all remove records from a particular sample. This release therefore never emits a stopped-ad classification. It provides collection coverage and leaves lifecycle conclusions to a workflow with independently adequate evidence.

## Google Ads input settings

### domains

Bare domains, e.g. ["shopify.com"]. At least one domain or advertiser ID is required; 20 sources total. Domain results can include resellers or other advertisers mentioning the domain. Ownership is NOT inferred. Use advertiserIds for an exact legal advertiser. No customer login needed.

### advertiserIds

Exact advertiser accounts, e.g. ["AR01625195283841286145"], from ad_url or advertiser_id in earlier results. Empty = use domains. Provide IDs instead of domains when you need only a specific legal advertiser; do not combine both for that request.

### maxAdsPerSource

Hard cap per domain or advertiser, even when maxResults is higher: default 20; range 1-1000. For 50 ads from one source, set this AND maxResults to 50. Counts delivered matches AFTER date/format filters, exclusions and monitoring. maxPagesPerSource bounds the scan; fewer matches are possible. 20 delivered ads cost $0.06.

### maxResults

For N ads from one source, set BOTH maxResults and maxAdsPerSource to N; the per-source default 20 still applies. Total paid ad cap across sources after deduplication/filters; default 100. Maximum charge = maxResults × $0.003. Set Apify run option maxTotalChargeUsd for a dollar ceiling (not input JSON). One free status row per visited source; skipped sources have none. Status rows do not count toward caps.

### includeAdText

true (DEFAULT) attempts English OCR or renderer text from up to 3 creative previews per ad; included in $0.003/ad. OCR is approximate, not a verified transcript. false = previews and metadata only, same price and faster. Check ad_text, text_method and text_status; missing text is null.

### region

"ALL" default means all regions. Country where ads were shown, not advertiser headquarters. Use "US", "GB", "DE", etc.; choose ALL if no region was requested. Source-side filter. Reported first_shown/last_shown are source search dates, not a spend or performance measure.

### adFormat

"all" default. "text", "image" or "video" filters Google’s format classification before caps/billing. A text ad may have only an image preview and require OCR. Does not filter by Search/YouTube platform; platform targeting is not a supported input.

### lastShownAfter

Empty = no lower bound. "2026-10-01" includes ads last shown on or after that UTC date, filtering returned search metadata before billing. This is NOT first-launch date or proof an ad is still running. Scan limits can leave additional matching ads unvisited.

### lastShownBefore

Empty = no upper bound. "2026-10-16" includes ads last shown on or before that UTC date. Inclusive and must be on/after lastShownAfter. No charge for filtered records. This is a source last-shown date, not a complete historical archive.

### onlyNewOrChanged

false default. true requires monitorKey: first run delivers baseline ads; later runs deliver unseen or changed creative-preview records. Unchanged rows are free. Serving-date changes alone do not count. Never reports stopped ads. Set an Apify schedule separately and avoid overlapping runs for the same key.

### monitorKey

Empty by default. With onlyNewOrChanged=true, use a stable key such as "shopify-weekly" (letters/digits/_/-; max 60). Stores up to 50000 paid creative fingerprints in your named storage. Same key requires identical sources/filters. Use a new key for a fresh baseline; do not run the same key concurrently.

### excludeCreativeIds

[] default. Skip creative_id values or advertiser_id:creative_id pairs from past output before billing, e.g. ["CR02097857130550788097"]. Maximum 10000. Useful for externally managed state. Distinct advertiser/creative pairs are deduplicated across the entire run.

### maxPagesPerSource

5 by default; 1-20 search pages, up to 100 source records per page. Scanning stops at this bound even if filters/monitoring deliver fewer ads than requested. No separate page fee. Raise for deeper scans; partial coverage is explicit in free status rows. This does not promise exhaustive historical coverage.

## Billing and cost limits

The price is **$0.003 per delivered ad**, or **$3 per 1,000 ads**. There is one billing event. No start fee applies, and compute and proxy costs used by this actor are included in that event price. Optional text extraction has no separate fee. Disabling it reduces processing time, not the advertised per-record price. For example, three delivered ads cost $0.009 and twenty delivered ads cost $0.06. Empty results, filtered records, excluded IDs, duplicates, unchanged monitored records and failed creative-detail lookups cost nothing under the actor's event pricing.

The row cap applies after filtering and deduplication. A request for one hundred ads does not guarantee that one hundred matches exist or that the scan budget can reach them. It does establish a maximum event charge of thirty cents. For an independent dollar limit, supply `maxTotalChargeUsd` as an Apify run option. This field is not part of the input JSON. The actor respects the SDK's event budget result and stops without continuing to emit paid rows after the ceiling.

Successful creative records with unavailable or imperfect OCR remain billable because they contain the requested creative details and previews. If verified verbatim copy is essential, inspect `text_status`, `text_method` and the original preview before using the text. Free extraction-status fields make this distinction machine-readable; the actor does not label an OCR guess as authoritative source text.

## Output coverage and error handling

Each visited source also produces a free `type: "status"` row. Its `query`, `query_type`, `rows`, `scanned`, `filtered`, `duplicates`, `unchanged` and `pages` explain what happened. `status` distinguishes completed collection from result_limit, source_limit, scan_limit, budget_reached, partial_error and error. `complete` is true only when pagination was exhausted without source errors; it is not a guarantee that the public library exposes all advertising activity. Sources not visited because the global cap was reached have no status row.

`errors` and `error` describe source failures without exposing credentials. Individual failed detail records are skipped; other records may still succeed. If source errors prevent every ad from being delivered, the run fails and leaves its summary for inspection. A successful empty query is different: it can complete with zero billed records and no errors. Blocked direct requests are retried through managed proxy routing when available; persistent failures remain explicit. Free status rows mean the dataset item count can exceed the paid ad count. Filter on `type == "ad"` before sending records into creative analysis or counting billable output.

The default key-value store also contains `SUMMARY`: paid row count, error count, budget state, per-source status records, request count, transferred response bytes and whether fallback proxy routing was used. These diagnostics help distinguish a narrow filter from a blocked source. They also make it possible to see that a scan stopped before exhaustion instead of treating a small sample as a comprehensive inventory.

## Examples for agents and automation

A minimal discovery request returns up to three ads, with text extraction attempted automatically:

```json
{"domains":["shopify.com"],"maxResults":3,"maxAdsPerSource":3}
```

For exact advertiser collection, use the identifier copied from a previous output record or library URL. This avoids claiming that all domain matches belong to the company you intended:

```json
{"advertiserIds":["AR01625195283841286145"],"region":"US","adFormat":"text","maxResults":10,"includeAdText":true}
```

A recurring workflow can reuse a named monitoring state. The first run is a billable baseline, not a free inventory operation:

```json
{"domains":["shopify.com"],"onlyNewOrChanged":true,"monitorKey":"shopify-weekly","maxResults":20,"maxPagesPerSource":2}
```

For manual incremental collection, pass known creative IDs without enabling persistent monitoring:

```json
{"domains":["shopify.com"],"excludeCreativeIds":["CR02097857130550788097"],"maxResults":5,"includeAdText":false}
```

The API supports the same input as the Console. This curl example uses an environment variable rather than embedding a secret in a saved command. The dollar cap belongs to the request options:

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~google-ads-transparency-scraper/run-sync-get-dataset-items?maxTotalChargeUsd=0.03&timeout=300' \
  -H "Authorization: Bearer $APIFY_TOKEN" -H 'Content-Type: application/json' \
  -d '{"domains":["shopify.com"],"maxResults":10}'
```

In Python, the Apify client can start the run and read the dataset. Preserve the summary and status records when troubleshooting, even if the downstream model receives only ads:

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('kestrel/google-ads-transparency-scraper').call(
    run_input={'domains':['shopify.com'], 'maxResults':10},
    max_total_charge_usd=0.03,
)
for item in client.dataset(run['defaultDatasetId']).iterate_items():
    if item.get('type') == 'ad':
        print(item['advertiser_name'], item['ad_text'], item['text_status'])
```

JavaScript applications can use a standard authenticated request. Long runs are better handled asynchronously by starting a run, polling its status and then reading its default dataset:

```javascript
const response = await fetch(
  'https://api.apify.com/v2/acts/kestrel~google-ads-transparency-scraper/run-sync-get-dataset-items?maxTotalChargeUsd=0.03',
  {method: 'POST', headers: {
    Authorization: `Bearer ${process.env.APIFY_TOKEN}`,
    'Content-Type': 'application/json'
  }, body: JSON.stringify({domains: ['shopify.com'], maxResults: 10})}
);
if (!response.ok) throw new Error(`Actor request failed: ${response.status}`);
const records = await response.json();
const ads = records.filter(row => row.type === 'ad');
```

## Integrations and practical workflows

An n8n or Make workflow can read a client list, call this actor with a small set of competitor domains, filter ad records and write them into a spreadsheet or database. Keep `advertiser_id` and `creative_id` as a compound primary key. Store `fetched_at` separately from source activity dates. An AI agent connected through Apify MCP can search for Google ads creatives or advertisers and call this actor with the same fields. It should first resolve advertiser identity when the request refers to a specific company rather than all ads matching a domain.

For a weekly creative brief, group ads by verified advertiser account and format, then provide the extracted text together with preview evidence to the analysis model. Require the model to distinguish observations from inferences. A repeated slogan or a long-running campaign can be described as a pattern; it does not prove return on ad spend, targeting strategy or audience demographics. Avoid interpreting an OCR error as a deliberate claim by the advertiser.

## FAQ

### Can I retrieve competitor spend or conversions?

No. The output does not contain private spend, clicks, conversions or campaign profitability. Do not derive those quantities from creative counts or elapsed time. This actor supplies creative evidence and publicly available source metadata.

### Does a domain match prove advertiser ownership?

No. The actual advertiser is preserved separately from the query. Multiple legal entities can advertise a brand, and other advertisers can mention the same domain. Review the account identity and then use exact advertiser IDs if a task requires attribution to one entity.

### Is the extracted ad copy exact?

Not necessarily. English OCR can misread characters, layouts and multilingual text. Unsupported previews can yield null text. The output exposes extraction methods and statuses so the caller can retain only suitable records or inspect the original creative. Audio transcription and translation are not supported.

### Why did I receive fewer ads than requested?

Possible reasons include limited source availability, regional filters, date bounds, exclusions, unchanged monitoring records and page limits. Inspect the free status rows before increasing limits. A row cap is a maximum, not a promise of sufficient supply.

### Does monitoring detect stopped ads?

No. Monitoring detects previously unseen or changed preview fingerprints among collected records. Absence from a bounded scrape cannot establish that a campaign stopped. Serving dates changing alone do not count as a creative update.

### Can I run this without a LinkedIn or Google Ads account?

Yes. The collector reads the public library without customer browser cookies or advertising-account access. It still requires an Apify account to run on the platform. Temporary source restrictions can occur and are surfaced as errors rather than fabricated empty results.

### What are the legal and source limitations?

This independent tool is not affiliated with or endorsed by Google. Public availability does not grant unrestricted rights to advertising artwork or brand assets. Use collected data in accordance with applicable laws, source conditions and your rights to retain or reuse creative material. The library is a public evidence source, not a complete private campaign archive.

Last verified working: 2026-11-06. Verification covers the release's documented sample inputs and checks; source behavior can change after release. Report a reproducible issue with your run link, expected record and input settings, without including API tokens or private credentials.
