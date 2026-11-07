# Shopify Products - Prices, Variants, SKUs & Availability

Shopify products returns prices and variants from public storefront catalogs for research and automation. It produces structured JSON that an agent can use without parsing a web page. Start with a small input, inspect a few rows, and then increase the result limit. The output has a stable identifier, source provenance and a fetch timestamp so another step can store, compare or cite the result.

Last verified working: 2026-10-16.


## Connect this Actor to your AI agent

[Open the MCP setup and small sample call](https://mtedj.github.io/kestrel-actors-examples/agents/shopify-products/) for this Actor, or [choose a related toolkit](https://mtedj.github.io/kestrel-actors-examples/agents/) for a larger workflow. The setup includes the input schema and current pricing events.

For a per-run dollar ceiling, use the hosted MCP `call-actor` tool with `callOptions.maxTotalChargeUsd` outside the Actor input. After the run finishes, retrieve the dataset with `get-dataset-items`; a run response is not the data itself. Check the live schema and pricing before a large or recurring run.

## Shopify product scraper API for agent workflows

Use this independent Apify actor to retrieve the public data documented below. It is not an official platform API or an account-management API. Pass the documented input JSON, keep result limits small for the first call, and use Apify run option `maxTotalChargeUsd` for the charge cap.

## Shopify 商品采集：价格、SKU、变体与库存状态

从已知店铺的公开商品目录获取 **Shopify 商品、产品价格、SKU、商品变体、图片和库存状态**，适合选品研究、竞品价格比较和 AI 智能体。`available` 仅表示至少一个变体可购买，**不提供精确库存数量**。不访问商家后台，不查找未知店铺，不读取订单或客户资料。

| 中文需求 | 正确参数或处理方式 |
|---|---|
| 采集一个店铺 | `storeUrls: ["https://www.allbirds.com"]` |
| 只保留可购买商品 | `onlyAvailable: true` |
| 最多返回 3 个商品 | `maxProductsPerStore: 3`，`maxResults: 3` |
| 只采集指定集合 | `collection: "all"`；使用店铺已有的集合 handle |
| 每天只获取新商品 | 外部保存 `product_key`，下次通过 `excludeProductIds` 传入 |
| 监控已有商品价格变化 | 不排除这些商品；定时重跑并在外部比较 `content_hash` 和价格 |

```json
{"storeUrls":["https://www.allbirds.com"],"maxProductsPerStore":3,"maxResults":3,"onlyAvailable":true}
```

一个 `type="product"` 行包含一个商品及其 `variants`、`price_min`、`price_max`、`currency`、`available`、`images` 和 `description_text`。变体不另计费。价格保留源币种；币种无法获取时为 `null`。商品名称和描述不自动翻译，关键词应使用店铺原文。

费用为 **每 1,000 个商品 $2**；3 个商品最多 $0.006。过滤、排除和去重先于计费及结果上限。无启动费；免费状态行、空结果和失败请求不按商品收费。金额上限使用 Apify 运行选项 `maxTotalChargeUsd`，不要将它放入输入 JSON。检查 `SUMMARY` 和 `type="status"`；公开目录关闭或访问失败会明确报告错误。历史价格和定时通知需要由外部工作流保存及执行。

这是独立的 Kestrel 工具，与 [Shopify](https://www.shopify.com) 无隶属关系。


## Shopify products: what does it return?

Each product row contains prices, currency, variants, SKUs, availability, images, vendor, tags and full product descriptions. All variants remain nested inside one product row; variants are not separately charged. Prices are decimal currency units from the public catalog, not cents. Currency is read from the storefront cart endpoint and remains null if that lookup fails. Availability means at least one variant is explicitly available; it does not provide inventory quantity. The public product catalog is paginated, up to 250 source products per page, with a maximum of 20 pages per store. Stores that disable or block the feed return an explicit error. Collection handles are supported. This actor does not discover stores, access admin data, place orders or track historical inventory. A feed may be incomplete for products with exceptionally large variant sets; the output contains all variants the public feed actually returns.

The actor separates records from diagnostics. A record has `type="product"` and is the only billable unit. A diagnostic has `type="status"`, identifies its `source`, and describes what happened during that source's retrieval. Read the `SUMMARY` record from the run's key-value store for totals. A successful platform run is not proof that every requested source had matches: inspect the diagnostic rows and the summary before declaring a research task complete.

## Shopify products for AI agents: which input answers which request?

Use this actor when the requested data matches the public source described above. Use the explicit input fields instead of constructing browser scripts. The target values identify what to search; the result limits bound the number of records delivered; filters narrow the matching records before charging. The actor does not interpret natural-language instructions outside the schema.

| User request | Input change |
|---|---|
| Products from one store | `storeUrls: ["https://www.allbirds.com"]` |
| Only available products | `onlyAvailable: true` |
| Match a title and vendor | `titleKeywords: ["runner"]`, `vendorKeywords: ["Allbirds"]` |
| Products in a collection | `collection: "shoes"` |
| New products since my last run | Save and pass `excludeProductIds` |
| Watch prices of known products | Rerun without exclusions and compare `content_hash`; no built-in price history |

The actor does not schedule itself, retain your earlier dataset as monitoring state, or send notifications. In a recurring workflow, store identifiers after each successful run and pass them in the exclusion field next time. If the user requests a complete historical archive or facts that the public source does not expose, explain the limitation before calling. Do not manufacture a target, fill a missing value from guesswork, or describe an empty result as evidence that no such record exists anywhere.

## Shopify products quick start

Paste this minimal example into the Input tab. It requests three records at most, so it is inexpensive to inspect. A smaller result is possible if the source is unavailable, has fewer records, or does not contain enough matches. The sample is a live public source, and its contents can change between runs.

```json
{
  "storeUrls": [
    "https://kith.com"
  ],
  "maxProductsPerStore": 3,
  "maxResults": 3
}
```

After the run, open Output or the default dataset. Retain rows where `type` equals `product` for downstream processing. Keep status rows in operational logs so failures remain visible. Download JSON when you need nested objects and arrays; CSV is useful for the flat columns but does not turn nested structures into a separate table automatically.

This example filters products to those with an available variant. All variants still appear in the delivered product.

```json
{
  "storeUrls": [
    "https://kith.com"
  ],
  "maxProductsPerStore": 3,
  "maxResults": 3,
  "onlyAvailable": true
}
```

## Inputs and source limits

| Input | Contract |
|---|---|
| `storeUrls` | Required: 1-10 public store homepage URLs, e.g. ["https://www.allbirds.com"]. HTTPS only; no paths or query strings. The public Shopify products.json feed must be enabled. No global store discovery, login or API key. One product with all its variants = one charged row. |
| `maxProductsPerStore` | 100 by default; 1-5000. Maximum matching products per store AFTER filters and exclusions, not variants. Source order; not sorted by newest. May return fewer if the catalog ends or maxPagesPerStore is reached. 10 products cost $0.02. |
| `maxResults` | 100 by default. Maximum delivered product rows across all inputs, after filters and deduplication. Stops early even if sources remain. Free status rows do not count. Cost is at most maxResults × $0.002; use Apify run option maxTotalChargeUsd for a dollar cap. |
| `onlyAvailable` | false (default) keeps all products. true keeps products with at least one variant explicitly available. All variants, including unavailable ones, stay in each returned product. Availability is a storefront flag, not an inventory quantity. Free filter before billing and caps. |
| `titleKeywords` | ["shoe", "runner"] keeps product titles containing either phrase, case insensitive. Empty = any title. Multiple title phrases use OR; combined with vendorKeywords and onlyAvailable using AND. Free filter before the product cap. |
| `vendorKeywords` | ["Nike"] keeps vendor names containing a phrase, case insensitive. Empty = all vendors. Multiple phrases use OR. Combined with titleKeywords and onlyAvailable using AND. Free filter before billing. |
| `collection` | Empty (default) scans the public catalog. A handle such as "shoes" scans /collections/shoes/products.json on every store. Pass the handle, not a URL. Unknown collections may be empty or fail. No extra charge. |
| `excludeProductIds` | Product IDs or full product_key values from previous output. Prefer product_key across multiple stores. Example ["www.allbirds.com:7340901859408"]. Up to 10000 strings. Exclusions are free and applied before caps. Save/pass IDs in your workflow; state and scheduling are external. |
| `maxPagesPerStore` | 5 by default; 1-20. Each public catalog page requests up to 250 products. Filtered and excluded rows still consume this scan allowance. Reaching it sets cap_reached=true and status=scan_limit; the run may have more matches outside the scanned pages. Requests themselves are not billed. |

Filters apply before delivered-record limits. This means a request for ten matches will not spend its entire output allowance on records that fail the filters. However, output limits and source coverage are different things. A source may return a bounded feed or a scanned portion of its catalog. The actor reports retrieval limits rather than silently claiming complete coverage. Raising the output cap cannot force an upstream source to expose more data than it actually returns.

Sources are processed in the order supplied. The total limit spans the whole run, and reaching it can leave later sources unprocessed. Check `sources_not_processed` in `SUMMARY` before assuming each target was visited. For an equal allocation across sources, use the per-source limit and choose a total limit large enough to accommodate the sum. The actor deduplicates repeated target strings before starting requests, and record identifiers are also deduplicated across the run.

## Output fields and stable identifiers

| Field | Meaning |
|---|---|
| `product_id` | Product id. |
| `product_key` | Product key. |
| `title` | Title. |
| `url` | Url. |
| `vendor` | Vendor. |
| `price_min` | Price min. |
| `price_max` | Price max. |
| `currency` | Currency. |
| `available` | Available. |
| `variants` | Variants. |
| `images` | Images. |
| `description_text` | Description text. |
| `store_url` | Store url. |
| `handle` | Handle. |
| `product_type` | Product type. |
| `tags` | Tags. |
| `description_html` | Description html. |
| `variant_count` | Variant count. |
| `options` | Options. |
| `published_at` | Published at. |
| `created_at` | Created at. |
| `updated_at` | Updated at. |
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

The price is $2 per 1,000 delivered product records. Ten records cost $0.02. There is no start fee. Proxy and compute are included in the event price for callers. Free status rows do not count toward the bill or the `maxResults` input. Filters, excluded identifiers, duplicates, empty results, failed requests and invalid input do not generate billable record events.

Billing is tied to successfully persisted records through the Apify SDK. A partial run can deliver and charge for valid records before a later source fails. Those delivered records remain useful and are not discarded because another source is unavailable. The actor does not charge a failed request as though it had produced a record. Review the dataset and status rows together when reconciling a partial result.

Set the maximum total price using Apify's `maxTotalChargeUsd` run option. This is a platform option, not an input property, and must be passed outside the JSON input body when using the API. The actor stops when the SDK reports that the event charge limit has been reached. For predictable calls, use both the record limit and the dollar cap. A smaller cap can stop the run before the requested count is reached; it cannot guarantee that the source contains enough matching data.

## Status rows and error handling

A status row includes `source`, `status`, `rows`, `source_rows`, `filtered`, `duplicates`, `errors`, `error`, `pages`, `cap_reached` and `currency_warning`. `rows` is the number delivered for that source; `source_rows` counts the source entries inspected, before filtering and deduplication. Repeated pages may make the inspected count larger than the number of distinct entries. `filtered` and `duplicates` explain why inspected entries did not become paid output.

`ok` indicates that the retrieval completed without a reported error. `empty` means the public source returned no entries. `no_matches` means entries were inspected but none survived the filters or exclusions. `error` means the source failed before delivering records; `partial_error` means a failure occurred after some records were already delivered. The `error` message explains the failure without including credentials. If source errors prevent all delivery, the actor marks the run failed. If some useful records were delivered, inspect the error count and decide whether to retry the affected sources.

`budget_reached` means the dollar cap stopped output. `cap_reached=true` means a count or scan boundary was reached; it does not promise that all matching data was exhausted. Catalog runs may also report `scan_limit` or `repeated_page`. The former indicates the maximum page count was used. The latter prevents an upstream endpoint that repeats the same page from causing a long, unproductive loop. A run summary includes `rows`, `sources`, `errors`, `filtered`, `duplicates`, `http_requests`, `budget_reached`, `result_limit_reached` and `sources_not_processed`.

## API examples: curl, Python and JavaScript

Keep your Apify token in an environment variable or the platform's credential manager. Do not paste it into a public workflow, shared input example or repository. The token authenticates your call to Apify; the actor itself does not require a separate source API key. Replace the sample input with a JSON object that follows the schema, and retain the same dollar cap when testing changes.

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~shopify-products/runs?maxTotalChargeUsd=0.05' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"storeUrls": ["https://kith.com"], "maxProductsPerStore": 3, "maxResults": 3}'
```

The asynchronous REST endpoint returns a run object. Poll that run until it reaches a terminal state, then read its `defaultDatasetId` and `defaultKeyValueStoreId`. Do not assume that a successful HTTP response to the start request means the extraction itself has finished. The client libraries can wait for completion, which is often simpler for a short agent task.

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ['APIFY_TOKEN'])
run = client.actor('kestrel/shopify-products').call(
    run_input={'storeUrls': ['https://kith.com'], 'maxProductsPerStore': 3, 'maxResults': 3},
    max_total_charge_usd=0.05,
)
for row in client.dataset(run['defaultDatasetId']).iterate_items():
    if row.get('type') == 'product':
        print(row)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/shopify-products').call(
  {"storeUrls": ["https://kith.com"], "maxProductsPerStore": 3, "maxResults": 3},
  { maxTotalChargeUsd: 0.05 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const records = items.filter(row => row.type === 'product');
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
