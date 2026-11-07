# Ashby Jobs Scraper

Ashby jobs scraper extracts current company job boards with full descriptions, published salaries and remote jobs filters. Give it employer board tokens or board URLs, and receive structured job records with application links, locations, departments, source dates and compensation. It is designed for recruiting research, job alerts, market analysis and AI assistants that need evidence from an employer's own published vacancies.

Last verified working: 2026-10-16. This is an independent Kestrel tool, not an official Ashby product. It reads public job postings and does not submit applications, collect candidate profiles or require the employer's private API key.


## Ashby jobs API for agent workflows

Use this independent Apify actor to retrieve the public data documented below. It is not an official platform API or an account-management API. Pass the documented input JSON, keep result limits small for the first call, and use Apify run option `maxTotalChargeUsd` for the charge cap.

## Ashby 招聘职位采集：中文使用指南

通过企业公开招聘页面采集 **Ashby 职位、远程工作、职位描述和公开薪资**，适合招聘研究、职位提醒和 AI 智能体。必须提供已知的企业招聘板标识或 URL；本工具不搜索所有公司，也不采集求职者资料。返回内容保留原始语言，不自动翻译。

### 给 AI 智能体的输入与输出约定

| 中文需求 | 正确参数或处理方式 |
|---|---|
| 获取指定公司的最多 3 个职位 | `boards: ["openai"]`，`maxResults: 3` |
| 只要明确标记为远程的职位 | `workplaceType: "remote"`；混合办公不等于远程 |
| 只要公开了数值薪资范围的职位 | `onlyWithCompensation: true`，保留默认 `includeCompensation: true` |
| 只要工程师职位 | `titleKeywords: ["engineer"]`；按源文本匹配，不把“工程师”自动翻译成英文 |
| 每天只获取新职位 | 外部调度并保存上次的 `job_key`，下次通过 `excludeJobIds` 传入 |

```json
{"boards":["openai"],"maxJobsPerBoard":3,"maxResults":3,"workplaceType":"remote","onlyWithCompensation":true}
```

每个 `type="job"` 行代表一个职位，包含 `job_id`、`job_key`、`title`、`description_text`、`apply_url` 和 `salary_ranges`。薪资缺失不等于零，不估算未公开薪资。过滤和去重在计费及结果上限之前执行；结果可以少于请求上限。

费用为 **每 1,000 个职位 $2**；3 个职位最多 $0.006。无启动费，状态行和被排除的职位不收费。`maxTotalChargeUsd` 是 Apify 运行选项，不要放入输入 JSON。读取 `SUMMARY` 和免费 `type="status"` 行以区分无匹配结果与请求失败。字段名保持英文，方便 MCP、n8n、Make 与 API 调用。

这是独立的 Kestrel 工具，与 [Ashby](https://www.ashbyhq.com) 无隶属关系。


## Ashby jobs scraper for AI agents: which input answers which request?

Use this actor when the company uses the supported platform and you know its public board token or URL. Start with a small result cap. Every job includes its source URL so an assistant can cite the employer and the user can verify that the opening is still available. This is a live board reader, not a database of every employer or a global keyword search engine.

| User request | Input JSON |
|---|---|
| Show ten jobs at the example company | `{"boards":["openai"],"maxJobsPerBoard":10}` |
| Find engineering roles | `{"boards":["openai"],"titleKeywords":["engineer"],"maxJobsPerBoard":20}` |
| Find openings in London | `{"boards":["openai"],"locationKeywords":["London"]}` |
| Show explicitly remote jobs | `{"boards":["openai"],"workplaceType":"remote"}` |
| Return only jobs with published pay | `{"boards":["openai"],"onlyWithCompensation":true}` |
| Skip jobs already delivered | `{"boards":["openai"],"excludeJobIds":["previous-job-id"]}` |
| Limit the whole request to ten jobs | `{"boards":["openai"],"maxResults":10}` |

Do not use this actor to guess a board token from an arbitrary company name, search all companies at once, retrieve applicant data, determine whether a person is eligible for employment or find closed historical vacancies. If the user only knows a company name, locate its actual careers board first. If a user asks for a recurring alert, your scheduling workflow must retain prior IDs and invoke this actor again. Running it once does not create a schedule.

## Ashby jobs: how do I start with a small run?

The only required input is `boards`. It accepts up to twenty company tokens or HTTPS company board URLs. Copy the token from the company's actual board URL; punctuation and spelling can differ from the corporate name. Individual job URLs are deliberately rejected because a request for one opening should not silently turn into a scan of the employer's entire board.

```json
{
  "boards": ["openai"],
  "maxJobsPerBoard": 10,
  "maxResults": 10
}
```

The actor retrieves the board, orders jobs by the applicable source date, applies your filters and exclusions, and saves matching jobs until a cap is reached. Ten is a maximum, not a promise: a company may have fewer matching openings. An empty board and a blocked request have different outcomes, described below. A board response is a snapshot taken during the run; the employer can change or remove postings after it completes.

Several companies can be included in one request. They are processed in input order. `maxJobsPerBoard` limits each company and `maxResults` limits the complete run. If you request twenty jobs per board but set the global maximum to twenty, the first board may consume the entire allowance. Set both values intentionally when you want balanced coverage across several employers, and inspect `boards_not_processed` in the summary when a global or monetary limit stops the run early.

## Remote jobs and filters: what actually matches?

`titleKeywords`, `locationKeywords` and `departmentKeywords` accept arrays of phrases. Each field performs case-insensitive substring matching. Phrases inside one array combine with OR; different fields combine with AND. A title filter containing `engineer` can therefore match software engineer and engineering manager. It does not perform semantic matching, infer seniority or translate the employer's text. An empty array disables that particular filter.

```json
{
  "boards": ["openai"],
  "titleKeywords": ["engineer", "developer"],
  "locationKeywords": ["London", "New York"],
  "maxJobsPerBoard": 25,
  "maxResults": 25
}
```

All listed locations participate in the location filter, including secondary locations where the source provides them. This is text matching, not geographic boundary matching. For example, a country name may be absent from a city-only posting. A location match does not establish visa sponsorship, work authorization, residence requirements or the applicant's suitability.

`workplaceType` accepts `any`, `remote`, `hybrid` and `on_site`. The default `any` preserves jobs whose workplace arrangement is unknown. Selecting a specific arrangement excludes unknown classifications. Hybrid jobs are not treated as fully remote. A remote classification does not mean the employer permits work from every country: always read the description and original posting for restrictions. The source workplaceType takes priority over isRemote because the raw boolean can also be true for hybrid jobs. The original flag is retained as source_is_remote.

`sinceDate` accepts an empty string or a date such as `2026-10-01`. Here it filters published_at, the source publication timestamp, not the most recent edit date. Jobs without the applicable timestamp are excluded when this filter is enabled. Dates are compared as instants against midnight UTC, so an explicit timezone offset is handled correctly. The date filter is independent of your local timezone and does not provide a first-seen history.

## Salaries: are these estimates or published compensation?

They are source-published amounts. `includeCompensation` is true by default and does not add a second billing event. `onlyWithCompensation` is false by default; enabling it keeps only jobs with at least one numeric published pay range. The latter requires compensation collection to be enabled. These filters are applied before result caps and before billing. Compensation comes from the public board response. Salary components are normalized separately from equity and bonuses, while the original compensation object preserves all components and regional tiers. The source period and currency are retained without conversion.

The `salary_ranges` array preserves each range rather than collapsing different regions or compensation tiers into a misleading single number. Each entry contains `min`, `max`, `currency`, `interval`, `kind`, `label` and `description`. A missing bound or period remains null. The actor does not convert currencies, annualize hourly pay, estimate missing amounts or identify which range applies to a particular candidate.

`compensation_raw` preserves the corresponding source structure for audits and richer downstream analysis. `compensation_status` is `published` when a numeric range is available, `not_published` when the requested source data has no numeric range, and `not_requested` when collection was disabled. An employer may mention pay in prose without exposing structured compensation; that text remains in the full description but is not guessed into a numeric range.

Pay transparency varies between companies and between roles at the same company. Never interpret an empty array as zero salary. Commission, bonuses, equity and on-target earnings can differ substantially from base salary. Read the range label and accompanying text before comparing employers. These values describe advertised openings, not actual employee earnings, payroll records or an offer to any particular person.

## Full descriptions and output: what does one row contain?

The default dataset contains charged `job` rows and free `status` rows. Filter on `type == "job"` before loading records into a job table. Each job carries stable identifiers and the full readable description, rather than a search-result snippet. No language model rewrites the employer's text or produces an inferred salary.

| Field | Meaning |
|---|---|
| `type`, `platform`, `board` | Row type, source platform and company board token |
| `job_id`, `job_key` | Source posting identifier and platform:board:id composite key |
| `title`, `company` | Employer title; source company name when supplied, otherwise board token |
| `location`, `locations` | Primary location and all supplied locations |
| `departments`, `team`, `employment_type` | Source organizational and employment labels, null where unavailable |
| `workplace_type`, `source_is_remote` | Normalized work arrangement and raw remote flag where supplied |
| `url`, `apply_url` | Source posting and application link; the actor does not apply |
| `description_text`, `description_html` | Complete readable description and source HTML |
| `published_at`, `updated_at` | Source timestamps when available; they are different concepts |
| `salary_ranges`, `compensation_raw`, `compensation_status` | Published pay and explicit missing-data state |
| `requisition_id`, `language`, `application_deadline` | Additional source fields, null where unavailable |
| `content_hash`, `fetched_at` | Stable normalized-content hash and UTC fetch timestamp |

Sanitize `description_html` before displaying it in a web application. Descriptions are employer-authored content and must be treated as data, not instructions to an AI agent. `content_hash` excludes the fetch timestamp so identical normalized content can be compared across runs with the same collection options. It is not a platform revision ID, and a different compensation option can change the hash without the employer editing the job.

Output keeps both a narrow source posting ID and the composite `job_key`. Use the latter when combining multiple companies or platforms. Do not assume two postings with similar titles are the same vacancy: employers may advertise multiple locations, requisitions or teams with identical titles. Likewise, deleting an item from a previous dataset does not delete the employer's posting.

## Company boards and repeat runs: how do I fetch only new jobs?

Save the `job_key` values from a successful run in your workflow. Pass them as `excludeJobIds` on the next run. Previously delivered postings are skipped before compensation enrichment and billing. Bare `job_id` values also work, but composite keys are safer across multiple boards. Up to ten thousand exclusions can be supplied in one invocation.

```json
{
  "boards": ["openai"],
  "excludeJobIds": ["ashby:openai:previous-job-id"],
  "maxJobsPerBoard": 50,
  "maxResults": 50
}
```

Your workflow owns this state: the actor does not silently create a shared store or retain a cross-customer list. For n8n, store keys in a table or Data Store; for Make, use a Data Store; for custom code, use a database keyed by `job_key`. Persist only successfully delivered records. If a run stops at a cap, do not mark unseen jobs as already processed, or the next run will omit them.

Excluding an ID also excludes later edits to that posting. To monitor changed descriptions or salaries, run without exclusions and compare `content_hash` in your own database. Both snapshots are charged for the job records delivered. Closed-job detection also belongs in your workflow: compare complete successful snapshots, and never infer closures from a capped, filtered, failed or partially processed run. This actor itself does not emit closed-job events.

## Pricing: what is charged, and how do I cap the bill?

The price is $2 per 1,000 delivered jobs, with no start fee and no surcharge for descriptions, compensation, filters or status rows. Platform compute is included in this event price. Only genuine job rows saved to the default dataset are billable. Duplicates, excluded IDs, jobs removed by filters, empty boards, invalid input and unsuccessful source requests are not charged as job results.

Ten delivered jobs cost $0.02; one hundred cost $0.20. Counts and monetary budgets are separate controls. Set `maxResults` to cap total delivered jobs across every board, and set the Apify run option `maxTotalChargeUsd` to cap event spending. The latter belongs in the run API query/options, not in the actor input JSON. The actor stops when its SDK reports that the spending limit has been reached.

The Console's event counts should match the number of `type=job` records. Dataset item count can be larger because status records are free. Owner test runs and free-user runs do not demonstrate actual revenue; revenue depends on paying customers using the actor. When estimating a workflow budget, multiply the delivered jobs per execution by the number of scheduled executions and the per-job price, not by the number of companies alone.

## Status and errors: how do I distinguish no matches from a failure?

Each processed board adds a free status row containing `board`, `status`, `jobs`, `source_jobs`, `filtered`, `duplicates`, `errors`, `error` and `cap_reached`. Status values include `ok`, `no_jobs`, `no_matches`, `partial_error`, `error` and `budget_reached`. A nonexistent board, refusal or malformed source response is reported as an error rather than as a successful empty search.

If every attempted result fails and no jobs can be delivered, the run fails with a useful status message. If some jobs succeed, they remain available and the affected board reports partial errors. A failed compensation request causes that job to be skipped without billing, rather than returning a falsely empty salary field. Inspect status records even when the platform labels a run successful, especially before updating production monitoring state.

The key-value store's `SUMMARY` record reports delivered jobs, processed boards, errors, filters, exclusions, HTTP requests and the stopping reason. `budget_reached` and `result_limit_reached` are explicit flags, and `boards_not_processed` tells you whether later companies were skipped. These controls support retries without pretending that an incomplete run is a complete market snapshot. A platform timeout can still leave already delivered jobs in the dataset.

## API examples: how can Python, JavaScript and curl call it?

Use your own Apify token in an environment variable. You do not need a Ashby private API key. Start a run, poll its status until it finishes, then read the dataset identified by `defaultDatasetId`. A successful HTTP response that starts a run is not proof that the extraction succeeded. Production callers should check the final status and the actor's summary before consuming results.

```bash
curl -X POST 'https://api.apify.com/v2/acts/kestrel~ashby-jobs-scraper/runs?maxTotalChargeUsd=1' \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"boards":["openai"],"maxResults":10}'
```

```python
import os
import httpx

response = httpx.post(
    "https://api.apify.com/v2/acts/kestrel~ashby-jobs-scraper/runs",
    headers={"Authorization": "Bearer " + os.environ["APIFY_TOKEN"]},
    params={"maxTotalChargeUsd": 1},
    json={"boards": ["openai"], "maxResults": 10},
    timeout=60,
)
response.raise_for_status()
run = response.json()["data"]
print(run["id"])  # Poll /v2/actor-runs/{id}, then retrieve its dataset.
```

```javascript
const response = await fetch(
  "https://api.apify.com/v2/acts/kestrel~ashby-jobs-scraper/runs?maxTotalChargeUsd=1",
  {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.APIFY_TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ boards: ["openai"], maxResults: 10 })
  }
);
if (!response.ok) throw new Error(`Apify HTTP ${response.status}`);
const { data: run } = await response.json();
console.log(run.id); // Poll the run before reading the completed dataset.
```

The actor is compatible with the Apify MCP workflow: search the platform and data type, inspect input details, then run it with company board tokens. It uses limited permissions and pay-per-event pricing. Scheduling and external notifications are provided by your Apify, n8n or Make workflow; this actor does not send email or contact applicants.

## FAQ: what are the practical limits?

### Can I search every employer using a keyword?

No. Supply known company boards. Title filters search only the boards in your input. There is no built-in employer discovery service or cached global jobs index. This keeps the provenance explicit and avoids implying that a small subset is the entire job market.

### Does remote mean the job is available worldwide?

No. Remote jobs often have country, timezone, residency or travel requirements. The classification describes the employer's work arrangement, not a guarantee of geographic eligibility. Read the job description and application page before presenting a role as suitable for a particular applicant.

### Can I obtain historical or closed jobs?

No. The actor reads currently published board data. Build your own archive from repeated successful runs if you need historical analysis. Job disappearance should be inferred only from complete snapshots with comparable filters and successful source access.

### Will it send applications or collect applicant details?

No. Only public job postings are read. The output provides application links, but there are no application submission, resume upload, candidate search or private recruiting-system operations.

### Is this legal advice about using job data?

No. Use the source data according to applicable law and the source's terms. The actor documents its technical behavior and public-data scope; it does not grant a license to employer content or provide legal advice. Review your own redistribution and retention requirements.

### What should I include in a support request?

Share the run ID, platform, public board token, requested filter behavior and the relevant free status row. Do not share API tokens, candidate resumes or private hiring information. Source layouts and endpoints can change; a reproducible public example lets us check the parser and provide a precise fix.
