# Clinical Trials - Studies, Sponsors & 临床试验

Clinical Trials provides studies and sponsors for structured research, JSON export and repeat monitoring. Search clinical trials on ClinicalTrials.gov by query and recruitment status. One row per study: title, sponsor, conditions, phase, enrollment, eligibility, locations and public study contacts. Free country/text filters and ID/hash exclusions. 临床试验。 Registry data, not medical advice.

Last verified working: 2026-10-17. Independent community Actor maintained by kestrel; not affiliated with or endorsed by the source platform.

## Clinical Trials: when should an AI agent use it?

Biotech research and trial-landscape agents monitoring sponsors and recruiting studies. Use this Actor when the required data fields and target identifiers match the input contract below. It returns structured source observations that can be cited, filtered, saved and compared. It does not add invented values to fill gaps. A missing source field remains empty or null. Source identity, collection time and a content hash accompany every delivered record.

Queries the official ClinicalTrials.gov API v2 and sorts by most recently posted update. Recruitment status filters are source status codes, not a guarantee that every site is currently accepting participants. Country filtering matches the listed study locations; it is independent of sponsor nationality. Public contacts are only the contact records submitted with a study and may be absent. Nested locations and contacts are included in the one study price. Registry records can be incomplete or outdated and do not establish treatment effectiveness.

## Clinical Trials: how do I make the first call?

Start with a small target set and a low result limit. The following input is a real working example. Replace the example target with the employer, search query, company identifier or application you actually want to inspect. Keep the initial page budget small until the returned schema meets your downstream requirements.

```json
{
  "searchQuery": "diabetes",
  "recruitmentStatus": "all",
  "countryContains": "",
  "maxResults": 5,
  "maxPages": 1
}
```

The default result limit is twenty across the entire run, not twenty per target. This distinction matters when several targets share one input. Targets are visited in input order and later targets may not be reached after the result or charge cap is met. Use separate runs if each target needs an independent guaranteed budget. Source availability may still prevent any particular target from returning data.

## Clinical Trials: which input answers which request?

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
  "searchQuery": "diabetes",
  "recruitmentStatus": "all",
  "countryContains": "",
  "maxResults": 2,
  "maxPages": 1
}
```

## What are the input fields?

| Input | Default | Meaning |
| --- | --- | --- |
| `searchQuery` | `"diabetes"` | Registry search query, e.g. "diabetes". Searches official study records; cannot be empty. Most recently updated studies first. No query fee. |
| `recruitmentStatus` | `"all"` | "all" or an official registry status, e.g. "RECRUITING". Filters studies, not individual site availability. No extra charge. |
| `countryContains` | `""` | Case-insensitive substring of study location country names, e.g. "China". Empty disables it. Not sponsor nationality. Free filter within maxPages. |
| `maxResults` | `20` | Maximum paid rows across the entire run, after filters and exclusions. Example: 20. May return fewer when source pages end or maxPages is reached. |
| `maxPages` | `3` | Maximum source pages per target, 1–20; default 3. Up to 50 studies per source page. Filters are free; maxResults can be lower than this scan budget. |
| `includeKeywords` | `[]` | Case-insensitive OR substring filter on title and summary. Example: ["battery"]. Empty [] disables it. Applied before billing inside the page budget; not a semantic classifier or additional source search. |
| `excludeIds` | `[]` | Copy prior output id values here to skip before billing. id is the NCT study identifier. Empty [] disables it. This also suppresses changes to existing IDs. |
| `excludeContentHashes` | `[]` | SHA-256 content_hash values from previous output to skip unchanged snapshots before billing. Example: copy returned hashes. Empty [] disables it. Changed counters or content can produce a new paid snapshot. |

All names are case sensitive. Unknown fields fail validation rather than being silently ignored. Supply arrays for list inputs and numeric integers for limits. Strings such as "20" are not interchangeable with the integer 20. Empty filter arrays disable those filters, while a required target array must contain at least one usable target. Validation happens before collection and does not create charged output rows.

## What does one output row contain?

One row is one study snapshot. Nested lists and objects belong to that row and do not create additional billing events. The sample below shows the shape of real source data. Values are examples from the verification run and will change as the source changes.

```json
{
  "id": "NCT04141878",
  "title": "Dementia and Diabetes Prevention Program",
  "official_title": "Dementia and Diabetes Prevention Program (DDPP)",
  "status": "RECRUITING",
  "last_updated": "2026-10-16",
  "start_date": "2021-05-26",
  "completion_date": "2027-06-27",
  "conditions": [
    "Diabetes",
    "Dementia"
  ],
  "interventions": [
    {
      "type": "BEHAVIORAL",
      "name": "Aerobic Exercise",
      "description": "Participants will follow a structured program that includes exercise 3 times per week for about 30 minutes each time. The type of aerobic exercise may vary, but will primarily focus on walking tutorials.",
      "armGroupLabels": [
        "Aerobic Exercise Group"
      ]
    },
    {
      "type": "BEHAVIORAL",
      "name": "Diet Skills",
      "description": "Participants will attend weekly classes focused on incorporating heart healthy foods into their existing diets. Calories will be restricted, and portion control will be taught with the goal of losing body weight. Hands-on skills will be taught for preparing healthy home-cooked meals by professional chefs.",
      "armGroupLabels": [
        "Diet Skills Group"
      ]
    }
  ],
  "phases": [
    "NA"
  ],
  "study_type": "INTERVENTIONAL",
  "enrollment": 400,
  "sponsor": "University of California, Davis",
  "summary": "This is a multicenter, randomized 2-arm clinical trial of two lifestyle interventions varying in intensity and format, in 400 older African American and non-Hispanic whites at increased risk of cognitive decline and dementia in the East San Francisco Bay Area. The trial will include two lifestyle interventions that differ in intensity and format:\n\n1. Aerobic Exercise (AEx) Intervention that involves aerobic activities with in-class walking workouts and tutorials and carried out at the East Oakland Sports Center (EOSC) and Tice Creek Fitness Center (TICE).\n2. Dietary counseling to support adherence to the Mediterranean-Diet Approaches to Stop Hypertension (DASH) Intervention for Neurodegenerative Delay (MIND) diet to encourage increased consumption of berries, green leafy and other vegetables, whole grains, nuts, fish, poultry, beans and olive oil, and to reduce consumption of fried/fast foods, red meat, whole fat cheese, sweets, butter and trans-fat margarines.",
  "eligibility": "Inclusion Criteria:\n\n* Sedentary (as per the Telephone Assessment of Physical Activity)\n* Poor diet (as per the MIND Diet Screener)\n* Cognitive function: absence of significant cognitive impairment as per the modified Telephone Interview for Cognitive Status (TICSm; age-, education-, and race-adjusted TICSm \\>32)\n* Lives in a region where the DDPP interventions will be delivered\n* Does not plan to travel outside of the home geographic area for more than 3 months over the course of the study\n* Free of physical disabilities that preclude participation in the study\n* Willing to complete all study-related activities for 32 weeks\n* Willing to be randomized to either lifestyle intervention group\n\nExclusion Criteria:\n\n* Age \\<60\n* Body Mass Index (BMI) \\>40\n* Any significant neurologic disease, including any form of dementia, Parkinson's disease, Huntington's disease, normal pressure hydrocephalus, brain tumor, progressive supranuclear palsy, seizure disorder, subdural hematoma, multiple sclerosis, or history of significant head trauma with persistent neurologic sequelae or known structural brain abnormalities\n* History of major depression within the last 12 months\n* History of bipolar disorder or schizophrenia as per Diagnostic and Statistical Manual of Mental Disorders (DSM) V criteria\n* History of alcohol or substance abuse or dependence within the past 2 years, as per DSM V criteria\n* Use of psychoactive medications within the last 3 months including tricyclic antidepressants, antipsychotics, mood-stabilizing psychotropic agents (e.g., lithium salts), psychostimulants, opiate analgesics, antiparkinsonian medications, anticonvulsant medications (except gabapentin and pregabalin for non-seizure indications), systemic corticosteroids, or medications with significant central anticholinergic activity; in the absence of major depression, stable dose use of selective serotonin reuptake inhibitors or serotonin and norepinephrine reuptake inhibitors are allowed\n* Health profiles that would jeopardize their safety to participate: (Screen failures will be referred immediately to a physician for medical examination): (1) Myocardial infarction or symptoms of unstable coronary artery disease (e.g., angina) in the last six months, (2) Uncontrolled hypertension within the past 6 months, (3) Morbid obesity (BMI\\<40), (4) History of clinically-evident stroke, (5) Clinically-significant infection within the past 30 days, (6) Significant pain or musculoskeletal disorder limiting the ability to participate safely, or (7) Clinically significant\n* Past or current use of insulin to treat type 2 diabetes\n* Serious diabetic event within 6 months of enrollment\n* Lung disease requiring either regular use of corticosteroids or the use of supplemental oxygen (inhaled steroids for asthma is permissible)\n* Renal disease\n* Clinically significant abnormalities in laboratory blood tests as per judgment of the Study Physician\n* History within the last 2 years of treatment for primary or recurrent malignant disease, excluding non-melanoma skin cancers, resected cutaneous squamous cell carcinoma in situ, basal cell carcinoma, cervical carcinoma in situ, or in situ prostate cancer with normal prostate-specific antigen post-treatment\n* History of hip fracture, joint replacement, or spinal surgery in the last 6 months\n* Currently receiving physical therapy or cardiopulmonary rehabilitation\n* History of a malabsorptive bariatric procedure (gastric bypass, biliopancreatic diversion); other bariatric procedures involving restriction (i.e., sleeve, band) are not exclusionary\n* For women: currently pregnant, pregnant within the past 6 months, or planning to become pregnant within the next 6 months\n* Currently incarcerated\n* Receiving hospice care\n* Adults unable to provide consent for participation\n* PI/Study Physician discretion regarding appropriateness of participation or concern about intervention adherence",
  "contacts": [
    {
      "name": "Andrea Alioto, PhD",
      "role": "CONTACT",
      "phone": "925-357-6515",
      "email": "agalioto@ucdavis.edu"
    },
    {
      "name": "David K Johnson, PhD",
      "role": "CONTACT",
      "phone": "785-342-2778",
      "email": "dkj@ucdavis.edu"
    }
  ],
  "locations": [
    {
      "facility": "University of California, Davis Alzheimer's Disease Center",
      "status": "RECRUITING",
      "city": "Walnut Creek",
      "state": "California",
      "zip": "94598",
      "country": "United States",
      "contacts": [
        {
          "name": "Andrea Alioto, PhD",
          "role": "CONTACT",
          "phone": "925-357-6515",
          "email": "agalioto@ucdavis.edu"
        },
        {
          "name": "David K Johnson, PhD",
          "role": "CONTACT",
          "phone": "785-342-2778",
          "email": "dkj@ucdavis.edu"
        },
        {
          "name": "David K Johnson, PhD",
          "role": "PRINCIPAL_INVESTIGATOR"
        }
      ],
      "geoPoint": {
        "lat": 37.90631,
        "lon": -122.06496
      }
    }
  ],
  "has_results": false,
  "study_url": "https://clinicaltrials.gov/study/NCT04141878",
  "source_url": "https://clinicaltrials.gov/api/v2/studies?query.term=diabetes&pageSize=50&format=json&sort=LastUpdatePostDate%3Adesc",
  "content_hash": "09c6eb82c09ca8baffb5ddbabc52486edf663eda1fc3b7f671265b378dae5a60",
  "fetched_at": "2026-10-17T05:00:20.519576+00:00"
}
```

| Field | Meaning |
| --- | --- |
| `id` | Id; copied or normalized from the public source. |
| `title` | Title; copied or normalized from the public source. |
| `official_title` | Official title; copied or normalized from the public source. |
| `status` | Status; copied or normalized from the public source. |
| `last_updated` | Last updated; copied or normalized from the public source. |
| `start_date` | Start date; copied or normalized from the public source. |
| `completion_date` | Completion date; copied or normalized from the public source. |
| `conditions` | Conditions; copied or normalized from the public source. |
| `interventions` | Interventions; copied or normalized from the public source. |
| `phases` | Phases; copied or normalized from the public source. |
| `study_type` | Study type; copied or normalized from the public source. |
| `enrollment` | Enrollment; copied or normalized from the public source. |
| `sponsor` | Sponsor; copied or normalized from the public source. |
| `summary` | Summary; copied or normalized from the public source. |
| `eligibility` | Eligibility; copied or normalized from the public source. |
| `contacts` | Contacts; copied or normalized from the public source. |
| `locations` | Locations; copied or normalized from the public source. |
| `has_results` | Has results; copied or normalized from the public source. |
| `study_url` | Study url; copied or normalized from the public source. |
| `source_url` | Source url; copied or normalized from the public source. |
| `content_hash` | Content hash; copied or normalized from the public source. |
| `fetched_at` | Fetched at; copied or normalized from the public source. |

The `source_url` field identifies the public endpoint or page used to obtain the observation. Human-readable item links are separate fields when the source exposes them. The `fetched_at` timestamp records collection time in UTC. It is not the original publication time and should not be used as one. A `content_hash` is a SHA-256 digest of the normalized content; it is intended for snapshot comparison rather than authentication or proof that the source has never changed.

## How do filters and page limits interact?

Collection is deliberately bounded. The Actor requests a source page, normalizes its records, removes duplicates, applies exclusions and text or source-specific filters, and then sends eligible rows to the paid dataset. A record removed by a filter does not consume the result limit or create a billing event. However, reading a page still consumes the page budget. If all rows on the allowed pages fail your filter, the result can correctly be empty.

The text filter searches the documented returned text fields. It is a substring check, not a semantic classifier. A phrase that is related in meaning but not present literally will not match. Conversely, a matching substring does not prove relevance to your business question. Use the upstream search inputs to narrow retrieval first, then use `includeKeywords` as a precise final constraint. This separation makes filtering behavior predictable and avoids charging for an undocumented AI interpretation.

If you request one hundred results but permit only a page containing ten eligible items, ten is the expected output. Increasing the result cap alone cannot create source coverage. A page cap, interrupted source request, changing feed or restricted upstream search can each limit what the run observes. The free summary records which sources and pages were visited so an agent can explain those limits instead of describing the output as exhaustive.

## How much does this Actor cost?

The price is **$5 per 1,000 delivered study rows**, or **$0.005 per row**. There is no Actor start fee. Proxy and compute are included in the event price. Filtered records, within-run duplicates, excluded IDs, unchanged excluded hashes and failures that produce no delivered rows do not generate a row charge. A run that delivers valid rows before a later source error retains those paid rows.

For example, ten delivered rows cost $0.05; one hundred cost $0.5. These examples are event-price arithmetic, not a prediction of how many results a source will return. Set a maximum total charge on each run to make the desired ceiling explicit. The charging SDK stops delivery when the event budget is exhausted. Do not put the budget parameter inside the Actor input: it belongs to the run API options and will be rejected as an unknown input field.

## How can I call it from Python, JavaScript or curl?

The examples use an environment variable for your Apify token. Keep credentials out of shared notebooks, source control and public URLs. The synchronous dataset endpoint is convenient for small runs. Larger collections can use the asynchronous run endpoint and retrieve the resulting dataset after completion.

```python
import os
from apify_client import ApifyClient
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("kestrel/clinical-trials-search").call(
    run_input={'searchQuery': 'diabetes', 'recruitmentStatus': 'all', 'countryContains': '', 'maxResults': 5, 'maxPages': 1},
    max_total_charge_usd=0.10,
)
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
summary = client.key_value_store(run["defaultKeyValueStoreId"]).get_record("SUMMARY")
print(len(rows), summary)
```

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/clinical-trials-search').call(
  {"searchQuery": "diabetes", "recruitmentStatus": "all", "countryContains": "", "maxResults": 5, "maxPages": 1},
  { maxTotalChargeUsd: 0.10 }
);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const summary = await client.keyValueStore(run.defaultKeyValueStoreId).getRecord('SUMMARY');
console.log(items, summary);
```

```bash
curl --request POST \
  'https://api.apify.com/v2/acts/kestrel~clinical-trials-search/runs?maxTotalChargeUsd=0.10' \
  --header "Authorization: Bearer $APIFY_TOKEN" \
  --header 'Content-Type: application/json' \
  --data '{"searchQuery": "diabetes", "recruitmentStatus": "all", "countryContains": "", "maxResults": 5, "maxPages": 1}'
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

本工具用于临床试验、研究机构、招募状态。输入参数名保持英文，说明和示例适合 AI 智能体调用。每条输出均包含来源链接、采集时间和内容哈希，方便核验及持续监测。

只对实际写入数据集的结果计费。筛选掉的结果、重复结果、排除的 ID 和未变化的哈希不计费。`maxResults` 是整个任务的结果上限；`maxPages` 限制每个目标的扫描页数。需要控制费用时，请在 Apify 运行参数中设置 `maxTotalChargeUsd`，不要放进输入 JSON。

源站拒绝访问与真正的空结果会明确区分。请检查免费的 `SUMMARY`，不要把未完整扫描的数据当作全量结果。原始字段缺失时保留空值，不编造内容。来源网站的标志仅用于识别数据来源，并不表示官方合作。

Source reference: https://clinicaltrials.gov/data-api/api
