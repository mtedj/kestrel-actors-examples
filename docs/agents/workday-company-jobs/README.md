# Workday Jobs - Careers, Descriptions & 招聘职位

Workday Jobs provides careers and descriptions for structured research, JSON export and repeat monitoring. Collect Workday jobs from company career URLs with keyword search. One row per job: title, company, location, requisition ID, description and apply URL. Free location/text filters and ID/hash exclusions. 招聘职位。 Public employer boards; no global company discovery.

Last verified working: 2026-10-17. Independent community Actor maintained by kestrel; not affiliated with or endorsed by the source platform.

## Workday Jobs: when should an AI agent use it?

Recruiting and sales agents checking target employers daily. Use this Actor when the required data fields and target identifiers match the input contract below. It returns structured source observations that can be cited, filtered, saved and compared. It does not add invented values to fill gaps. A missing source field remains empty or null. Source identity, collection time and a content hash accompany every delivered record.

Accepts HTTPS career-board URLs on tenant.wdN.myworkdayjobs.com. A locale segment such as en-US is optional. Individual job URLs are rejected. Keyword search runs inside each employer board. Description fetching is on by default and included in the job price; set includeDescriptions=false for faster listing-only runs. Salary is not extracted into a structured field. Employer boards can cap their visible result sets; no complete global jobs database is promised.

## Workday Jobs: how do I make the first call?

Start with a small target set and a low result limit. The following input is a real working example. Replace the example target with the employer, search query, company identifier or application you actually want to inspect. Keep the initial page budget small until the returned schema meets your downstream requirements.

```json
{
  "careerUrls": [
    "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"
  ],
  "searchQuery": "",
  "includeDescriptions": true,
  "locationContains": "",
  "maxResults": 5,
  "maxPages": 1
}
```

The default result limit is twenty across the entire run, not twenty per target. This distinction matters when several targets share one input. Targets are visited in input order and later targets may not be reached after the result or charge cap is met. Use separate runs if each target needs an independent guaranteed budget. Source availability may still prevent any particular target from returning data.

## Workday Jobs: which input answers which request?

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
  "careerUrls": [
    "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"
  ],
  "searchQuery": "",
  "includeDescriptions": true,
  "locationContains": "",
  "maxResults": 2,
  "maxPages": 1
}
```

## What are the input fields?

| Input | Default | Meaning |
| --- | --- | --- |
| `careerUrls` | `["https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"]` | Workday career-board URLs, e.g. ["https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"]. Only myworkdayjobs.com boards; individual job URLs rejected. One page budget per board. |
| `searchQuery` | `""` | Keyword search within supplied employer boards, e.g. "engineer". Empty means all visible board jobs. Does not discover employers. No query fee. |
| `includeDescriptions` | `true` | true (DEFAULT) fetches each Workday job detail; included in the same job price. Set false for a faster list with description=null. This does not change the per-row price. |
| `locationContains` | `""` | Optional case-insensitive substring in source location fields, e.g. "London". Empty disables it. Applied before billing; not a radius or geocoding search. |
| `maxResults` | `20` | Maximum paid rows across the entire run, after filters and exclusions. Example: 20. May return fewer when source pages end or maxPages is reached. |
| `maxPages` | `3` | Maximum source pages per target, 1–20; default 3. Up to 20 listings per page per employer board; descriptions add detail requests but no extra row fee. Filters are free; maxResults can be lower than this scan budget. |
| `includeKeywords` | `[]` | Case-insensitive OR substring filter on title and description (description only when included). Example: ["battery"]. Empty [] disables it. Applied before billing inside the page budget; not a semantic classifier or additional source search. |
| `excludeIds` | `[]` | Copy prior output id values here to skip before billing. id combines board hostname, site name and job path. Empty [] disables it. This also suppresses changes to existing IDs. |
| `excludeContentHashes` | `[]` | SHA-256 content_hash values from previous output to skip unchanged snapshots before billing. Example: copy returned hashes. Empty [] disables it. Changed counters or content can produce a new paid snapshot. |

All names are case sensitive. Unknown fields fail validation rather than being silently ignored. Supply arrays for list inputs and numeric integers for limits. Strings such as "20" are not interchangeable with the integer 20. Empty filter arrays disable those filters, while a required target array must contain at least one usable target. Validation happens before collection and does not create charged output rows.

## What does one output row contain?

One row is one job snapshot. Nested lists and objects belong to that row and do not create additional billing events. The sample below shows the shape of real source data. Values are examples from the verification run and will change as the source changes.

```json
{
  "id": "nvidia.wd5.myworkdayjobs.com:NVIDIAExternalCareerSite:/job/US-CA-Santa-Clara/Principal-Block-File-Storage-Software-Engineer--Linux---DGX-Cloud_JR2024421",
  "title": "Principal Block and File Storage Software Engineer, Linux - DGX Cloud",
  "company": "nvidia",
  "job_requisition_id": "JR2024421",
  "location": "US, CA, Santa Clara",
  "additional_locations": [],
  "posted_at": "2026-10-16",
  "posted_label": "Posted Today",
  "employment_type": "Full time",
  "remote_type": null,
  "description": "We are looking for a 100% hands-on  Storage Services Software engineer to join the block storage group. You will be a member of a team that builds the next-generation block storage capabilities and architects a proprietary distributed file system solution from its inception. You will work closely with a variety of teams and architects including the networking team, and external customers. You will take part in defining the software architecture and implementation of the most advanced storage services! Services that will need to meet extreme performance and scalability demands! We have crafted a team of extraordinary people stretching around the globe, whose mission is to push the frontiers of what is possible today and define the platform of tomorrow. At NVIDIA, we work, think and learn as a team. We thrive in a deeply strong environment, and we're passionate about a culture that demands innovation and the highest standards. The rewards are sweet and include collaborating with some of the smartest people in the industry, an aggressive compensation plan that rewards top performers, and the opportunity to work on products that transform the way people work and play. What you’ll be doing: 100% hands-on coding role in C language, Kernel and Userspace Access advanced AI tools and a token budget for code development provided by NVIDIA, the world's AI factory leader. Research, design, implement and test, new and existing, distributed storage services and features of NVIDIA’s block and file storage solution, in both Host and  DPU environments. Acquire understanding of the algorithms, the technicalities and the interaction with other components across NVIDIA’s block and file storage ecosystem. Analyze and solve challenging bugs and customer cases in large scale production systems, identifying issues in our or inbox the kernel modules and often in other components. Drive new solutions based on any issues that arise What we need to see: B.Sc., M.Sc.. in Computer Science, Electrical Engineering or related discipline (or equivalent experience).  15+ years of experience as a senior developer, preferably in the domains of storage, networking, and/or operating-systems Strong proficiency in C/C++ programming. Experience with Linux block subsystem, File system and IO stack, Experience with storage protocols and standards, especially NVMe  Comprehension of large and complexed systems| Proven professional experience in designing and developing distributed systems; advantage for experience in block and/or file storage and/or networking systems. Ability to work autonomously, with a proactive mindset and perseverance to solve day to day challenges.  Ability to quickly adapt to new technology and go deep into new areas Excellent communication skills and a collaborative mindset. Innovative approach, identifying opportunities to improve, accelerate, and reuse existing solutions. Knowledge of cloud computing concepts, including virtualization, scalability, and data management. Ways to Stand Out From the Crowd: Linux Kernel coding experience Linux Kernel internals knowledge including memory management, scheduling, etc. Linux File system experience NVIDIA has continuously reinvented itself over two decades. NVIDIA’s invention of the GPU in 1999 sparked the growth of the PC gaming market, redefined modern computer graphics, and revolutionized parallel computing. More recently, GPU deep learning ignited modern AI — the next era of computing — with the GPU acting as the brain of computers, robots, and self-driving cars that can perceive and understand the world. This is our life’s work — to amplify human imagination and intelligence. Your base salary will be determined based on your location, experience, and the pay of employees in similar positions. The base salary range is 272,000 USD - 431,250 USD. You will also be eligible for equity and benefits . Applications for this job will be accepted at least until October 20, 2026. This posting is for an existing vacancy. NVIDIA uses AI tools in its recruiting processes. NVIDIA is committed to fostering an inclusive work environment and proud to be an equal opportunity employer. As we highly value diversity in our current and future employees, we do not discriminate (including in our hiring and promotion practices) on the basis of race, religion, color, national origin, gender, gender expression, sexual orientation, age, marital status, veteran status, disability status or any other characteristic protected by law.",
  "job_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Principal-Block-File-Storage-Software-Engineer--Linux---DGX-Cloud_JR2024421",
  "apply_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Principal-Block-File-Storage-Software-Engineer--Linux---DGX-Cloud_JR2024421",
  "details_included": true,
  "source_url": "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Principal-Block-File-Storage-Software-Engineer--Linux---DGX-Cloud_JR2024421",
  "content_hash": "9d8c929d8dc5b528fdfc50480758cdd8d63664970edcfde2d1f414d2742ac565",
  "fetched_at": "2026-10-17T05:00:19.196091+00:00"
}
```

| Field | Meaning |
| --- | --- |
| `id` | Id; copied or normalized from the public source. |
| `title` | Title; copied or normalized from the public source. |
| `company` | Company; copied or normalized from the public source. |
| `job_requisition_id` | Job requisition id; copied or normalized from the public source. |
| `location` | Location; copied or normalized from the public source. |
| `additional_locations` | Additional locations; copied or normalized from the public source. |
| `posted_at` | Posted at; copied or normalized from the public source. |
| `posted_label` | Posted label; copied or normalized from the public source. |
| `employment_type` | Employment type; copied or normalized from the public source. |
| `remote_type` | Remote type; source value can be absent and is then null. |
| `description` | Description; copied or normalized from the public source. |
| `job_url` | Job url; copied or normalized from the public source. |
| `apply_url` | Apply url; copied or normalized from the public source. |
| `details_included` | Details included; copied or normalized from the public source. |
| `source_url` | Source url; copied or normalized from the public source. |
| `content_hash` | Content hash; copied or normalized from the public source. |
| `fetched_at` | Fetched at; copied or normalized from the public source. |

The `source_url` field identifies the public endpoint or page used to obtain the observation. Human-readable item links are separate fields when the source exposes them. The `fetched_at` timestamp records collection time in UTC. It is not the original publication time and should not be used as one. A `content_hash` is a SHA-256 digest of the normalized content; it is intended for snapshot comparison rather than authentication or proof that the source has never changed.

## How do filters and page limits interact?

Collection is deliberately bounded. The Actor requests a source page, normalizes its records, removes duplicates, applies exclusions and text or source-specific filters, and then sends eligible rows to the paid dataset. A record removed by a filter does not consume the result limit or create a billing event. However, reading a page still consumes the page budget. If all rows on the allowed pages fail your filter, the result can correctly be empty.

The text filter searches the documented returned text fields. It is a substring check, not a semantic classifier. A phrase that is related in meaning but not present literally will not match. Conversely, a matching substring does not prove relevance to your business question. Use the upstream search inputs to narrow retrieval first, then use `includeKeywords` as a precise final constraint. This separation makes filtering behavior predictable and avoids charging for an undocumented AI interpretation.

If you request one hundred results but permit only a page containing ten eligible items, ten is the expected output. Increasing the result cap alone cannot create source coverage. A page cap, interrupted source request, changing feed or restricted upstream search can each limit what the run observes. The free summary records which sources and pages were visited so an agent can explain those limits instead of describing the output as exhaustive.

## How much does this Actor cost?

The price is **$4 per 1,000 delivered job rows**, or **$0.004 per row**. There is no Actor start fee. Proxy and compute are included in the event price. Filtered records, within-run duplicates, excluded IDs, unchanged excluded hashes and failures that produce no delivered rows do not generate a row charge. A run that delivers valid rows before a later source error retains those paid rows.

For example, ten delivered rows cost $0.04; one hundred cost $0.4. These examples are event-price arithmetic, not a prediction of how many results a source will return. Set a maximum total charge on each run to make the desired ceiling explicit. The charging SDK stops delivery when the event budget is exhausted. Do not put the budget parameter inside the Actor input: it belongs to the run API options and will be rejected as an unknown input field.

## How can I call it from Python, JavaScript or curl?

The examples use an environment variable for your Apify token. Keep credentials out of shared notebooks, source control and public URLs. The synchronous dataset endpoint is convenient for small runs. Larger collections can use the asynchronous run endpoint and retrieve the resulting dataset after completion.

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("kestrel/workday-company-jobs").call(
    run_input={'careerUrls': ['https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite'], 'searchQuery': '', 'includeDescriptions': True, 'locationContains': '', 'maxResults': 5, 'maxPages': 1},
    max_total_charge_usd=0.10,
)
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
summary = client.key_value_store(run["defaultKeyValueStoreId"]).get_record("SUMMARY")
print(len(rows), summary)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/workday-company-jobs').call(
  {"careerUrls": ["https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"], "searchQuery": "", "includeDescriptions": true, "locationContains": "", "maxResults": 5, "maxPages": 1},
  { maxTotalChargeUsd: 0.10 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const summary = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('SUMMARY');
console.log(items, summary);
```

```bash
curl --request POST \
  'https://api.apify.com/v2/acts/kestrel~workday-company-jobs/runs?maxTotalChargeUsd=0.10' \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"careerUrls": ["https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"], "searchQuery": "", "includeDescriptions": true, "locationContains": "", "maxResults": 5, "maxPages": 1}'
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

本工具用于招聘职位、企业招聘、职位描述。输入参数名保持英文，说明和示例适合 AI 智能体调用。每条输出均包含来源链接、采集时间和内容哈希，方便核验及持续监测。

只对实际写入数据集的结果计费。筛选掉的结果、重复结果、排除的 ID 和未变化的哈希不计费。`maxResults` 是整个任务的结果上限；`maxPages` 限制每个目标的扫描页数。需要控制费用时，请在 Apify 运行参数中设置 `maxTotalChargeUsd`，不要放进输入 JSON。

源站拒绝访问与真正的空结果会明确区分。请检查免费的 `SUMMARY`，不要把未完整扫描的数据当作全量结果。原始字段缺失时保留空值，不编造内容。来源网站的标志仅用于识别数据来源，并不表示官方合作。

Source reference: https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite
