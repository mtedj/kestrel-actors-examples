# Free Hotel Review Checker — Hotel Reputation, Rating Comparison

The free hotel review checker answers one question in one run: what does the internet actually say about this hotel? Give it a name, get back the hotel ratings and the review count that Google Hotels, Tripadvisor, Booking.com, Agoda, Hostelworld and Despegar publish for it, each on its own scale and again on a shared 0–5 scale, plus the Tripadvisor ranking sentence and whatever sub-scores each site gives away. It is a hotel reputation checker for people who need the numbers before they need the guest reviews — an online reputation snapshot, not a review dump. One run is the fastest way to check hotel reviews across every major booking channel at once, because the six hotel review sites are read in parallel and reported in one shape.

Last verified working: 2026-10-17.

## 酒店口碑、评分比较与评价平台检查：中文调用与语言设置

免费比较多个平台的酒店评分、评论数量及规范化评分。输出评分汇总，不是每个平台完整评论正文。

language 影响可用的名称和排名文本；country 是查询市场，不是酒店所在地。不同平台评分分制应使用规范化字段比较。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "hotelNames": [
    "Altis Grand Hotel, Lisbon"
  ],
  "sources": [
    "google"
  ],
  "language": "de",
  "country": "de",
  "sessions": 1
}
```

Hotelbewertungen vergleichen / e-réputation hôtel：用于评分对比，再按需获取评论正文。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Hotel review checker for AI agents: which input answers which request?

Use it when the user wants to know how a hotel is rated — the score, review count, star rating, ranking and sub-scores — on Google Hotels, Tripadvisor, Booking.com, Agoda, Hostelworld and Despegar, side by side, or to compare a hotel with its competitors (a comp set of up to 10 hotels). It is free: nothing is ever charged. Do not use it for review text (it returns ratings and counts, never a review; every row's `reviews_scraper` names the paid per-site scraper that does), for prices, or for more than 10 hotels in one run.

| The user asks for | Input |
|---|---|
| How is hotel X rated across review sites | `{"hotelNames": ["Altis Grand Hotel, Lisbon"]}` |
| Compare my hotel with its competitors, a comp set | `{"hotelNames": ["Altis Grand Hotel, Lisbon", "Memmo Alfama Hotel, Lisbon", "Hyatt Regency Lisbon"]}` (up to 10) |
| Only Tripadvisor and Booking.com | add `"sources": ["tripadvisor", "booking"]` |
| Include Hostelworld or Despegar | put the property URL in `startUrls` (no name search on those two) |
| The whole picture from one Booking.com or Tripadvisor URL | `{"startUrls": ["https://www.booking.com/hotel/pt/memmo-alfama.html"]}` — the URL's site answers first, its name is searched on the others |
| Names and ranking sentence in German, as seen from Germany | add `"language": "de", "country": "de"` |
| The review text behind the numbers | not this actor: run the `reviews_scraper` named on each row |

Rows come in three types. `reputation` (one per hotel per site): `source`, `source_label`, `source_url`, `hotel_name`, `rating` on the site's own scale (`rating_scale`: Google and Tripadvisor 5, Booking.com, Agoda and Despegar 10, Hostelworld 100), `rating_5` (the same score on a shared 0-5 scale), `review_count`, `ranking`, `ranking_position`, `ranking_of` (Tripadvisor only), `sub_scores` (Tripadvisor's six, Hostelworld's seven, Despegar's six; null elsewhere), `stars`, `city`, `country`, `matched_by`, `matched_confidence`, `reviews_scraper`. `summary` (one per hotel): `sources_checked`, `sources_found`, `sources_missing`, `rating_mean_5`, `rating_best_source`, `rating_best_5`, `rating_worst_source`, `rating_worst_5`, `rating_spread_5`, `review_total`, `ratings_by_source`, `review_counts_by_source`. `status` (one per hotel per site): `ok`, `not_found` (no property matched the name well enough — the best match score is in `error`), `unsupported` (Hostelworld or Despegar asked for by name), `skipped` (beyond the 10-hotel cap) or `error` (the site refused or broke), always with a reason. A hotel a site does not list is a `status` row, never a guessed match and never a failed run.

**Hotel ratings in other languages.** `language` picks the Tripadvisor country site and the locale of Google Hotels, Booking.com and Agoda, so Hotel Bewertungen (de), avis d'hôtel (fr), opiniones de hoteles (es), recensioni di hotel (it) and avaliações de hotéis (pt) come back with the same scores and localized names.

## What this hotel review checker does — and what it does not

**It does:** resolve a hotel on up to six hotel review sites, read exactly one aggregate page or API answer per site, and return one row per hotel per site with the hotel review score, the review count, the ranking and the cheap sub-scores. It then adds one cross-source summary row that puts every score on the same 0–5 scale and tells you how far apart the sites are about the same building.

**It does not** return review text. No guest sentences, no titles, no owner replies, no dates, no reviewer countries. That is a deliberate split. Reading one aggregate per site is cheap enough to give away; reading thousands of reviews per site is not. When a row shows you that Tripadvisor holds 1,977 reviews and Booking.com holds 894, the `reviews_scraper` column on that same row names the actor that will hand you those reviews in full. See **Related scrapers** below.

Everything here is free. There is no pay-per-event pricing on this actor, no charged row type, and no code path that calls a billing API. You pay Apify for the platform time and proxy traffic a run consumes, exactly as you would for any free actor, and nothing else.

## Hotel ratings on six review sites, side by side

| Site | Scale | What one request returns | Resolves a plain name? |
|---|---|---|---|
| Google Hotels | 0–5 | rating, review count, star class | yes |
| Tripadvisor | 0–5 | rating, review count, **ranking sentence**, six sub-scores | yes |
| Booking.com | 0–10 | rating, review count, star class, city | yes |
| Agoda | 0–10 | rating, review count, star class, city | yes |
| Hostelworld | 0–100 | rating, total ratings, **seven sub-scores** | no — URL only |
| Despegar | 0–10 | rating, review count, **six category scores** | no — URL only |

Put side by side like this, the table is the quickest way to compare hotel ratings across channels: a Tripadvisor rating of 4.3 out of 5 and a Booking.com score of 9.3 out of 10 are the same opinion, and `rating_5` says so in one column. Hotel reviews are counted differently by every site too, which is why the count travels with the score.

Hostelworld and Despegar have no public property search that can be trusted with a name, so they are read from a property URL you supply in `startUrls`. Everything else is found from the name alone, through each site's own autocomplete or typeahead.

Two of the six sites refuse datacenter IP ranges outright: Tripadvisor and Despegar are always fetched through Apify's residential group, whatever `proxyConfiguration` says. The other four are served from datacenter ranges, which is what the default configuration uses. If the account has no residential access the run logs a warning and falls back to the configured proxy rather than failing.

## Review count, ranking and sub-scores: what each site gives away

A rating on its own is close to meaningless — 9.3 on Booking.com and 4.7 on Google Hotels are the same opinion in different clothes. Three things make the number usable, and this actor collects all three where the site publishes them for free:

- **`review_count`** — 4.8 from eleven guests is not 4.8 from eleven thousand. Every site's own count is reported as it stands; no site's hotel review count is copied onto another.
- **`ranking`** — Tripadvisor is the only one of the six that publishes a position: `"#33 of 372 hotels in Lisbon"`, split out as `ranking_position` and `ranking_of` so you can compute a percentile.
- **`sub_scores`** — Tripadvisor gives cleanliness, location, rooms, service, sleep quality and value; Hostelworld gives seven (value, safety, location, staff, atmosphere, cleanliness, facilities); Despegar gives six category scores. Google Hotels, Booking.com and Agoda publish none on the cheap path, so those rows carry `null` and the paid scrapers named on the row carry the detail.

## What one run returns

Three row types share one dataset, distinguished by `type`.

`type: "reputation"` — one row per hotel per site:

```json
{
  "type": "reputation",
  "query": "Altis Grand Hotel, Lisbon",
  "hotel": "Altis Grand Hotel, Lisbon",
  "source": "tripadvisor",
  "source_label": "Tripadvisor",
  "source_id": "228423",
  "source_url": "https://www.tripadvisor.com/Hotel_Review-g189158-d228423-Reviews-Altis_Grand_Hotel.html",
  "hotel_name": "Altis Grand Hotel",
  "rating": 4.3,
  "rating_scale": 5,
  "rating_5": 4.3,
  "review_count": 1977,
  "ranking": "#33 of 372 hotels in Lisbon",
  "ranking_position": 33,
  "ranking_of": 372,
  "sub_scores": {"cleanliness": 4.5, "location": 4.7, "rooms": 4.2, "service": 4.4, "sleep_quality": 4.3, "value": 4.1},
  "stars": 5,
  "city": "Lisbon",
  "country": "PT",
  "matched_by": "name",
  "matched_confidence": 1.0,
  "reviews_scraper": "https://apify.com/kestrel/tripadvisor-reviews-scraper",
  "fetched_at": "2026-08-29T09:14:02+00:00"
}
```

`type: "summary"` — one row per hotel, across every site checked:

```json
{
  "type": "summary",
  "hotel": "Altis Grand Hotel, Lisbon",
  "sources_checked": ["agoda", "booking", "google", "tripadvisor"],
  "sources_found": ["agoda", "booking", "google", "tripadvisor"],
  "sources_missing": [],
  "rating_mean_5": 4.31,
  "rating_best_source": "google",
  "rating_best_5": 4.7,
  "rating_worst_source": "tripadvisor",
  "rating_worst_5": 3.1,
  "rating_spread_5": 1.6,
  "review_total": 8790,
  "ratings_by_source": {"google": 4.7, "tripadvisor": 3.1, "booking": 4.65, "agoda": 4.45},
  "review_counts_by_source": {"google": 6377, "tripadvisor": 384, "booking": 894, "agoda": 1135}
}
```

`type: "status"` — one row per hotel per site, including the sites that found nothing. `status` is `ok`, `not_found`, `unsupported`, `skipped` or `error`, and `error` always says why. A site that refuses the request is reported as `error`; a site that genuinely has no such property is `not_found`. The two are never merged, because a silent zero in a reputation report is worse than a loud failure.

## Output fields

| Field | Meaning |
|---|---|
| `type` | `reputation`, `summary` or `status` |
| `query` | the text the row was resolved from |
| `hotel` | the run's label for the hotel, the same on every row of that hotel |
| `source` | `google`, `tripadvisor`, `booking`, `agoda`, `hostelworld`, `despegar` |
| `source_label` | the site's own name |
| `source_id` | the property's id on that site |
| `source_url` | the property page on that site |
| `hotel_name` | the property name as that site spells it |
| `rating` | the headline score on the site's own scale |
| `rating_scale` | 5, 10 or 100 |
| `rating_5` | the same score converted to 0–5 |
| `review_count` | reviews or ratings that site counts |
| `ranking`, `ranking_position`, `ranking_of` | the ranking sentence and its two numbers |
| `sub_scores` | the category scores the site publishes free |
| `stars` | hotel star rating (the property's class) where the site states one |
| `city`, `country` | as that site files the property |
| `matched_by` | `url` or `name` |
| `matched_confidence` | 0–1, how sure the name match is |
| `reviews_scraper` | the actor that returns the full review text for this site |
| `sources_checked`, `sources_found`, `sources_missing` | summary rows |
| `rating_mean_5` | mean of every site's score on the 0–5 scale |
| `rating_best_source`, `rating_best_5` | the kindest site and its score |
| `rating_worst_source`, `rating_worst_5` | the harshest site and its score |
| `rating_spread_5` | best minus worst |
| `review_total` | every review count added up |
| `ratings_by_source`, `review_counts_by_source` | the per-site maps |
| `status`, `error` | status rows |
| `fetched_at` | UTC timestamp of the request |

The dataset schema ships nine views: an overview, one per site, the cross-source summary and the status list, so the Output tab is readable without exporting anything.

## How do I check a hotel by name?

Put one hotel per line in `hotelNames`, ideally as `Name, City`:

```json
{
  "hotelNames": ["Altis Grand Hotel, Lisbon", "Memmo Alfama, Lisbon"],
  "sources": [],
  "language": "en",
  "country": "us"
}
```

The part before the comma is what the name match is scored against; the city is passed to each site's search to disambiguate. An empty `sources` means "every site that can find this target", which for a name is Google Hotels, Tripadvisor, Booking.com and Agoda.

## How do I check a hotel by URL?

Put the property page in `startUrls`. Any of the six sites is accepted, and the URL's own site is read first — the name it returns is then what the other sites are searched by, so one URL gives you the whole cross-source picture:

```json
{
  "hotelNames": [],
  "startUrls": [
    "https://www.hostelworld.com/hostels/p/15529/home-lisbon-hostel/",
    "https://www.booking.com/hotel/pt/memmo-alfama.html",
    "https://www.despegar.com.ar/hoteles/h-265543/riu-cancun-cancun"
  ],
  "sources": ["hostelworld", "booking", "tripadvisor", "agoda"]
}
```

This is also the only way to reach Hostelworld and Despegar. Ask for either of them with a bare name and the status row says `unsupported` and tells you to supply a URL — it does not guess.

## Input reference

| Input | Default | What it does |
|---|---|---|
| `hotelNames` | `[]` | hotel names, one per line, ideally `Name, City` |
| `startUrls` | `[]` | property pages on any of the six sites |
| `sources` | `[]` | which sites to check; empty means every site that can resolve the target |
| `language` | `en` | two-letter code; picks the Tripadvisor domain and the locale the others answer in |
| `country` | `us` | two-letter market; sets Google's market, the Booking.com and Agoda locale suffix, and the Despegar country domain |
| `sessions` | `2` | proxy sessions per site's client |
| `perIp` | `1` | requests per second per session |
| `proxyConfiguration` | Apify Proxy | datacenter is enough for four of the six sites |

## Free run limits: what does the cap mean?

Because there is nothing to bill, the work has to be bounded somewhere, and it is bounded in two places:

1. **Ten hotels per run.** Targets beyond the tenth are never fetched. Each one gets a `status` row with `status: "skipped"` and an `error` that says so, and the run's status message counts them. Split a bigger list across runs, or schedule them.
2. **At most one lookup request and one aggregate request per site per hotel.** There is no paging anywhere in this actor. A full six-site check of one hotel is at most twelve HTTP requests, and usually fewer — Google Hotels answers the lookup and the aggregate in a single call, and a property URL skips the lookup entirely.

That ceiling is what makes the actor safe to give away, and it is also why it cannot return review text: the text lives behind pages this actor never turns.

## How accurate is the name match?

A wrong match is worse than a missing one, so every name lookup passes two guards.

First, each site's own guard. Tripadvisor's typeahead answer is only accepted when the returned name shares at least half the query's words — that endpoint will happily answer a random hotel for nonsense. Booking.com's autocomplete hit must be `dest_type: hotel`, and a Booking URL's country code must match the hit's. Despegar's canonical id on the page is compared with the id that was requested before anything is reported.

Second, a uniform word-overlap score: `matched_confidence` is the share of the query's meaningful words that the matched property name carries, ignoring filler like "hotel" and "the". Anything below 0.6 is refused, and the status row records the score that failed, e.g. `"Booking.com has no property matching 'Altis Belem Hotel and Spa, Lisbon' (best name match 0.33)"`. A property URL is an exact identity, so `matched_by` is `url` and `matched_confidence` is `1.0`.

## Reputation management: reading the spread

`rating_spread_5` is the most useful number this actor produces and it takes one glance. A tight spread — under about 0.3 — means the sites agree and the score is real. A wide spread usually means one of three things:

- **A different audience.** Hostelworld scores a property the way backpackers do; Booking.com scores it the way business travellers do. A hostel with 4.9 on Hostelworld and 3.9 on Google Hotels is not broken.
- **A stale or thin sample.** Check `review_counts_by_source`. One site holding 60 reviews against another's 6,000 explains most gaps.
- **A real problem on one channel.** This is the case that matters for reputation management. When counts are comparable and the scores are not, the harsh site is where the complaints are — and that is the site whose review text is worth buying.

Run it on your comp set as well as your own property and the same three columns become a hotel rating comparison across the market — a review score comparison you can hand to a revenue manager without any further work, and a tidy pile of hotel review data for anything downstream. Scheduled weekly, it becomes review monitoring: `rating_5` and `review_count` per site per week is the whole time series, and hotel reputation monitoring is mostly that plus an alert on a drop.

## Related scrapers — where the review text lives

Every reputation row names its site's scraper in `reviews_scraper`. The full set:

- **Tripadvisor Reviews Scraper** — https://apify.com/kestrel/tripadvisor-reviews-scraper — bubbles, title, text, six sub-ratings, trip type, stay date, photos, management response, 40+ language domains.
- **Booking.com Reviews Scraper** — https://apify.com/kestrel/booking-reviews-scraper — 1–10 score, what the guest liked and disliked, room, stay dates, traveller type, nationality, property reply.
- **Agoda Reviews Scraper** — https://apify.com/kestrel/agoda-reviews-scraper — 0–10 rating, title, comment, positives and negatives, stay dates, reviewer country, provider.
- **Hostelworld Reviews Scraper** — https://apify.com/kestrel/hostelworld-reviews-scraper — 0–100 score with seven sub-ratings, group type, age band, trip type, nationality, owner reply.
- **Despegar Hotel Ratings** — https://apify.com/kestrel/despegar-hotel-ratings — the 0–10 score, six category scores, Despegar's own written summary and the comments the page carries.
- **Google Hotels Prices** — https://apify.com/kestrel/google-hotels-prices — every booking source's rate for a stay, per room, with the partner deep links.

None of them is a free hotel review scraper — they read the text, and reading text costs money. None of them is required to use this one, either. The point of a review aggregator is to tell you where to look first; buy the deep read only for the site that turned out to matter.

## Integrations: n8n, Make, MCP and AI agents

The dataset is plain JSON, so the usual paths all work: the Apify n8n node, the Apify Make app, the Apify MCP server for an AI agent that needs a hotel review api it can call mid-conversation, and scheduled runs with a webhook on finish. Because the actor is free, an agent can call it speculatively — that is the point of shipping free hotel data — and only escalate to a paid per-site scraper when `rating_spread_5` or `review_count` says it is worth it.

## Using the results from Python, JavaScript and curl

Start a run and read the dataset with curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~hotel-reputation-checker/runs?token=$APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"hotelNames":["Altis Grand Hotel, Lisbon"]}'

curl "https://api.apify.com/v2/datasets/<DATASET_ID>/items?token=$APIFY_TOKEN&format=csv" > reputation.csv
```

Python, printing the spread for each hotel:

```python
from apify_client import ApifyClient

client = ApifyClient("<APIFY_TOKEN>")
run = client.actor("kestrel/hotel-reputation-checker").call(
    run_input={"hotelNames": ["Altis Grand Hotel, Lisbon", "Memmo Alfama, Lisbon"]}
)
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "summary":
        print(row["hotel"], row["rating_mean_5"], "spread", row["rating_spread_5"], row["sources_missing"])
```

JavaScript (Node), collecting one site's scores:

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('kestrel/hotel-reputation-checker').call({
    startUrls: ['https://www.booking.com/hotel/pt/memmo-alfama.html'],
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'reputation').map((i) => [i.source_label, i.rating, i.review_count]));
```

## Is scraping hotel ratings legal?

This actor reads only what each site publishes to anonymous visitors: the aggregate score and review count on a public property page or in the public JSON that page itself calls. It sends no credentials, solves no login, and stores no personal data — there are no reviewer names here because there are no reviews here. Scraping public data is broadly lawful in the EU and the US, and the leading US case law on public web data points the same way, but the legal position depends on your jurisdiction and your purpose, so take your own advice before building a commercial product on it. Respect each site's terms, keep the request rate polite (the defaults are), and do not present another company's ratings as your own.

## FAQ

### Is this actor really free?

Yes. There is no pay-per-event pricing attached to it and no charging call in its code; the run summary records `charged: {}` on every path. Apify still meters the compute time and proxy traffic your run uses, as it does for every actor, free or not.

### Why is there no review text?

Because that is what the paid per-site scrapers are for, and because reading review text means paging — dozens of requests per hotel per site instead of one. Keeping this actor to a single aggregate request per site is what lets it be given away. The `reviews_scraper` column on every row tells you exactly where to go next.

### Why do the sites disagree about the same hotel?

Different audiences, different sample sizes, and different scales. Convert everything with `rating_5`, compare `review_counts_by_source`, then read `rating_spread_5`. A spread over about 0.8 with comparable counts is worth investigating.

### Can I check more than ten hotels?

Not in one run. The free-run cap keeps the eleventh and later targets unfetched and reports them as `skipped`. Split the list across runs or schedule them a few minutes apart; there is no charge either way.

### Which sites need residential proxies?

Tripadvisor and Despegar, always — both refuse datacenter ranges. Google Hotels, Booking.com, Agoda and Hostelworld are fine on the datacenter group that `proxyConfiguration` defaults to.

### What happens when a site cannot find the hotel?

You get a `status` row with `not_found` and an `error` explaining it, including the best name-match score when the failure was a weak match. No reputation row is written and nothing is invented. If a site refuses the request instead, the status is `error` — never a zero rating.

### Does it work in other languages and markets?

Yes. `language` picks the Tripadvisor domain (`de` → tripadvisor.de, `fr` → tripadvisor.fr, and so on) and the locale the other sites answer in; `country` sets Google's market, the Booking.com and Agoda locale suffix, and which Despegar country domain is used. The scores are the same everywhere; the names, cities and ranking sentence change.

### How often should I run it?

Weekly is enough for hotel reputation monitoring — aggregate scores move slowly. Daily makes sense only when you are watching a specific incident, and the run is small enough that it costs almost nothing either way.
