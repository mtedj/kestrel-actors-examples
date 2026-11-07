# TripAdvisor Restaurant Reviews Scraper — Diner Reviews, Ratings

This **TripAdvisor restaurant reviews scraper** turns any restaurant or attraction page into structured rows: 1-5 bubbles, the full text, the diner's food / service / value / atmosphere sub-ratings, the visit date, the tips they left for the next guest, their photos and the owner's reply. Point it at **tripadvisor restaurant reviews** by URL, by location id or by name, pick your languages, and you get clean **restaurant reviews** and **attraction reviews** as a dataset, a CSV, an Excel file or a JSON API response. It is a **restaurant reviews scraper** built for restaurant groups, franchises, delivery platforms, POS and reputation vendors and city tourism boards — the people who need **diner reviews** at scale rather than one page at a time.

No browser, no login, no GraphQL keys, no CAPTCHA solving. The actor reads the same server-rendered pages a diner sees, through Apify's residential proxy, and pays for itself per review row delivered.

**Last verified working: 2026-10-02.**

Scraping hotels instead? Use the sibling listing, [TripAdvisor Reviews Scraper (hotels)](https://apify.com/kestrel/tripadvisor-reviews-scraper) — it covers `Hotel_Review` pages with the six hotel sub-ratings. This actor deliberately refuses hotel ids and tells you where to send them.

## TripAdvisor 餐厅评论、景点评价与店主回复：中文调用与语言设置

按餐厅或景点名称、URL 或 ID 获取评论、分项评分及店主回复。餐厅和景点字段可能不同。

languages=["zh"] 选择中文站点；includeTranslated=false 排除机器翻译。2026-10-16 实测中文站点未返回可用页面，当前不承诺中文采集可用；下面示例使用英文站点。每个语言单独计费，不应把不同语言版本当成不同顾客。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "startUrls": [
    "https://www.tripadvisor.com/Restaurant_Review-g189158-d2703366-Reviews-Cervejaria_Ramiro-Lisbon_Lisbon_District_Central_Portugal.html"
  ],
  "locationType": "any",
  "languages": [
    "en"
  ],
  "maxReviewsPerLocation": 1,
  "includeTranslated": false,
  "sessions": 1
}
```

Avis restaurants / recensioni ristoranti / opiniones restaurantes：原文与翻译分别处理。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## TripAdvisor scraper for AI agents: which input answers which request?

Use it when the user wants the reviews of specific restaurants or attractions on TripAdvisor — by name, URL or location id — with the bubble rating, text, the food/service/value/atmosphere ratings, visit date, trip type, the diner's tips, photos and the owner's reply, once or on a schedule, in one or several languages. Do not use it to list the restaurants of a city (it takes places, not a destination search), for hotel reviews (hotel URLs and ids are refused free of charge: use kestrel/tripadvisor-reviews-scraper), or for menus and prices beyond the free location row's menu link and price band.

| The user asks for | Input |
|---|---|
| Reviews of a restaurant by name | `{"restaurantNames": ["Cervejaria Ramiro, Lisbon"]}` — the newest 100 English reviews, at most $0.50 |
| Reviews of an attraction, museum or tour | `{"restaurantNames": ["Oceanário de Lisboa"]}` or an Attraction_Review URL in `startUrls`; `locationType` "any" (the default) accepts both |
| Reviews by URL | `{"startUrls": ["https://www.tripadvisor.com/Restaurant_Review-g189158-d2703366-Reviews-Cervejaria_Ramiro-Lisbon.html"]}` |
| Every review the place has | add `"maxReviewsPerLocation": 0` |
| Only negative reviews, a complaints feed for a restaurant group | add `"maxRating": 2, "maxReviewsPerLocation": 0` (filtered reviews are free; the cap is applied before the filter) |
| Only new reviews since the last run, review monitoring | add `"sinceDate": "2 days"` and an Apify schedule |
| Restaurants only, skip attractions | add `"locationType": "restaurant"` |
| Italian reviews as written by Italian diners | add `"languages": ["it"], "includeTranslated": false` |
| Rating, review count, cuisine, price band, menu link, hours, phone, address | already in the free `location` row (`includeLocationRow` defaults to true) |
| The same places every day | pass the `location_id` values of a first run in `locationIds` |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `maxReviewsPerLocation` bounds the rows per place and language |

Rows come in three types. `review` (billed, $0.005): `review_id`, `rating`, `title`, `text`, `sub_ratings` (food, service, value, atmosphere — restaurants only; attractions carry none), `language`, `original_language`, `translated`, `review_date`, `visit_date`, `trip_type`, `tips`, `helpful_votes`, `reviewer_name`, `reviewer_username`, `reviewer_hometown`, `reviewer_contributions`, `photos`, `response`, `response_date`, `url`, `location_name`, `location_type`. `location` (free, one per place and language): `location_type`, `rating`, `review_count`, `rating_counts`, `reviews_by_language`, `sub_ratings`, `ranking`, `cuisines`, `price_range`, `dish_tags`, `category_tags`, `address`, `city`, `latitude`, `longitude`, `phone`, `email`, `website`, `menu_url`, `hours`, `open_now`, `permanently_closed`. `status` (free, one per place and language): `status` is `ok`, `no_reviews`, `not_found`, `wrong_type`, `duplicate` or `error`, with `reviews`, `filtered`, `pages`, `total` and `error`. A place with no reviews, an unknown id, a hotel id or a name that matches nothing is a `status` row that says why — never a charge and never a failed run; a blocked or throttled source fails the run so it is not mistaken for "no reviews". `maxReviewsPerLocation` is applied to the reviews read (newest first) before the filters, so 100 with `maxRating: 2` delivers the low-rated reviews among the newest 100: for a complete complaints list set it to 0 or use `sinceDate`.

**Restaurant reviews in other languages.** `languages` picks the country site, so one run can return avis restaurant (tripadvisor.fr), recensioni ristorante (tripadvisor.it), opiniones de restaurantes (tripadvisor.es), Restaurant-Bewertungen (tripadvisor.de) and avaliações de restaurantes (tripadvisor.com.br): 30 country sites, 24 languages, each row saying which language it was written in.

## TripAdvisor restaurant reviews: what every run gives you

Three kinds of row share one dataset, so a single run answers both "what did people say" and "what is this place".

| Row | What it is | Price |
| --- | --- | --- |
| `review` | One diner or visitor review with everything TripAdvisor publishes about it | $0.005 |
| `location` | The restaurant or attraction itself: rating, ranking, cuisines, price band, address, hours | free |
| `status` | One line per location and language saying what happened | free |

A run that delivers 1,000 reviews costs $5.00, with compute and proxy included. Reviews you filter out before billing — by rating, by date, by trip type, by "must have text" — cost nothing at all.

### What is in a review row?

Every review row carries `review_id`, `location_id`, `location_name`, `location_type`, `language`, `original_language`, `translated`, `title`, `text`, `rating`, `sub_ratings`, `review_date`, `created_date`, `visit_date`, `trip_type`, `tips`, `helpful_votes`, `reviewer_name`, `reviewer_username`, `reviewer_verified`, `reviewer_contributions`, `reviewer_helpful_votes`, `reviewer_hometown`, `photos`, `photo_count`, `response`, `response_date`, `response_id`, `url`, `location_url`, `target` and `fetched_at`.

The two fields that make this different from a generic review dump:

- **`sub_ratings`** — on a restaurant review these are the four bubbles the diner actually gave: `food`, `service`, `value`, `atmosphere`. That is the whole point of **restaurant sub-ratings**: a 3-bubble review that scores food 5 and service 1 is a staffing problem, not a kitchen problem, and only the sub-ratings tell you which. Attraction reviews carry none — TripAdvisor does not ask for them.
- **`tips`** — the short note a reviewer leaves for the next guest ("ask for the terrace", "come hungry"). It is the most operational sentence in the whole review and almost nobody extracts it.

`visit_date` is the month of the meal or the visit, which is usually earlier than `review_date`; `trip_type` is `FAMILY`, `COUPLES`, `SOLO`, `BUSINESS` or `FRIENDS`. TripAdvisor no longer publishes a meal type (breakfast / lunch / dinner) on restaurant reviews, so trip type is the visit context that actually exists in the payload — we do not invent one.

### What is in a location row?

`location_id`, `geo_id`, `location_name`, `location_type`, `url`, `rating`, `review_count`, `rating_counts`, `reviews_by_language`, `sub_ratings`, `ranking`, `ranking_position`, `ranking_of`, `ranking_category`, `cuisines`, `price_range`, `category_tags`, `dish_tags`, `address`, `city`, `state`, `postal_code`, `country_code`, `latitude`, `longitude`, `phone`, `email`, `website`, `menu_url`, `accepts_reservations`, `open_now`, `hours`, `permanently_closed`, `description`, `neighborhoods`, `reviews_listed`, `reviews_fetched`, `language`, `fetched_at`.

`dish_tags` is the list of dishes and topics TripAdvisor itself mines out of the review corpus — for Cervejaria Ramiro in Lisbon that is `["clams", "seafood", "tiger prawns", "percebes", "worth the wait", "long wait"]`. It is a free menu-and-complaint summary in a dozen words. `category_tags` is the equivalent for attractions (`["Points of Interest & Landmarks", "Cooking Classes"]`), `ranking` is the sentence `#735 of 6,596 Restaurants in Lisbon` with `ranking_position`, `ranking_of` and `ranking_category` broken out, and `sub_ratings` here is the location's four dining averages rather than one diner's opinion.

### What is in a status row?

`target`, `location_id`, `location_name`, `location_type`, `language`, `status`, `reviews`, `filtered`, `pages`, `total`, `duplicates`, `error`, `fetched_at`. The `status` value is one of `ok`, `no_reviews`, `not_found`, `wrong_type`, `duplicate` or `error`. Nothing is ever silently dropped: if a page was refused, you get `error` with the reason, never a quiet "no reviews".

## Scrape TripAdvisor restaurants by URL, by id or by name

Give the actor at least one of three things.

**`startUrls`** — restaurant or attraction pages on any TripAdvisor domain. The geo id and the slug do not have to be correct; the numeric `d<id>` is what counts, so a shortened URL still works. `ShowUserReviews` deep links work too, because they carry the same id.

```json
{
  "startUrls": [
    "https://www.tripadvisor.com/Restaurant_Review-g189158-d2703366-Reviews-Cervejaria_Ramiro-Lisbon_Lisbon_District_Central_Portugal.html",
    "https://www.tripadvisor.com/Attraction_Review-g189158-d3214902-Reviews-Time_Out_Market_Lisboa-Lisbon.html"
  ],
  "maxReviewsPerLocation": 200,
  "languages": ["en"]
}
```

**`locationIds`** — the numeric ids after `d`, with or without the `d`. This is the fastest path because it skips every lookup, and it is what an earlier run's `location_id` column hands you. Pulling **restaurant reviews by location id** is the normal shape of a scheduled job: resolve names once, store the ids, then run on ids forever.

```json
{
  "locationIds": ["2703366", "d429386", "3214902"],
  "locationType": "any",
  "maxReviewsPerLocation": 100
}
```

**`restaurantNames`** — names resolved through TripAdvisor's own typeahead. Include the city ("Cervejaria Ramiro Lisbon"), because the endpoint answers *something* for every query, including nonsense. A hit must share at least half of the words you typed or it is rejected, so a typo comes back as an `error` row instead of a random bistro in another country. The resolved `location_name` and `location_type` are in the output so you can audit every match.

```json
{
  "restaurantNames": ["Cervejaria Ramiro Lisbon", "The Cheesecake Factory Chicago"],
  "locationType": "restaurant",
  "maxReviewsPerLocation": 50
}
```

You can mix all three. A URL, its id and its name resolve to one location and are billed once; the extra targets come back as `duplicate` status rows so nothing looks lost.

## Which restaurants and attractions does it cover?

`locationType` decides what the run accepts:

- `restaurant` — only `Restaurant_Review` pages. Anything else is reported and not charged.
- `attraction` — only `Attraction_Review` pages, for **tripadvisor attractions**: museums, markets, tours, landmarks, walking areas, classes.
- `any` (default) — both.

Because TripAdvisor canonicalises by id, a bare location id resolves to the right page on its own, and the actor reads the family off the page rather than guessing. If a target turns out to be the other family — or a hotel — you get a `wrong_type` status row that names what it actually is, after a single page read, and nothing is charged. Hotel ids are pointed at [the hotel sibling](https://apify.com/kestrel/tripadvisor-reviews-scraper) by name in the `error` field.

That check matters more than it sounds. "Time Out Market Lisboa" exists twice on TripAdvisor — once as a restaurant (`d10769801`) and once as an attraction (`d3214902`) — with different review counts. Being told which one you hit is the difference between a report and a guess.

## How many reviews can I pull, and what does it cost?

`maxReviewsPerLocation` is the main cost control. `0` means every review the site lists for that location in that language; a number means the newest N. TripAdvisor lists **15 reviews per page on a restaurant** and 10 on an attraction, newest first, and the actor reads the page-size straight off the page's own paging links — so no page is fetched twice and none is skipped.

Rough sizing for **bulk restaurant reviews**: a busy city-centre restaurant has 2,000-12,000 reviews in English alone, an attraction like a famous food market can pass 25,000, and each page is around a megabyte of residential proxy traffic. Start with 100-200 per location, look at the `total` column in the status rows, then decide.

| Goal | Input |
| --- | --- |
| Latest 50 per restaurant | `maxReviewsPerLocation: 50` |
| Everything, once | `maxReviewsPerLocation: 0` |
| Daily top-up | `maxReviewsPerLocation: 0`, `sinceDate: "2 days"` |
| Complaints only | `maxRating: 2`, `requireText: true` |

Billing is per delivered `review` row at $0.005. Locations with no reviews, unknown ids, wrong-family ids, duplicate targets and filtered-out reviews are all free, and the actor never delivers a row it could not charge for.

## How do I get only the reviews I care about?

Every filter runs **before billing**, so a complaints feed costs a fraction of a full pull.

- **`maxRating`** — keep only reviews at or below N bubbles. `maxRating: 2` is the classic **tripadvisor negative restaurant reviews** feed; combine it with `requireText: true` and you have a queue of real, actionable **restaurant customer feedback** with the `response` field already telling you whether anyone replied.
- **`tripTypes`** — `family`, `couples`, `solo`, `business`, `friends`. A steakhouse that scores badly with `family` and well with `business` has a menu problem, not a service problem.
- **`sinceDate`** — `YYYY-MM-DD` or a relative string (`"30 days"`, `"2 weeks"`, `"6 months"`) so a schedule never goes stale. Pages come newest first, so the walk stops as soon as an entire page predates the cut: a daily job reads one or two pages per restaurant.
- **`requireText`** — drop rating-only reviews.
- **`includeTranslated`** — see the next section.
- **`includeLocationRow`** — set it to `false` if you only want review rows.

## How do I scrape restaurant reviews in multiple languages?

Each TripAdvisor domain serves the reviews in its own language, machine translations included, and `languages` maps to domains: `en` is tripadvisor.com, `de` is tripadvisor.de, `pt` is tripadvisor.com.br, and so on across `en-gb`, `en-au`, `en-ca`, `en-in`, `en-ie`, `en-sg`, `fr`, `es`, `it`, `nl`, `ja`, `zh`, `ru`, `sv`, `da`, `no`, `fi`, `pl`, `tr`, `el`, `ko`, `th`, `vi`, `id`, `cs`, `hu` and `he` — 30 sites in all.

The counts differ per domain, which is exactly why this matters. Cervejaria Ramiro lists 4,860 reviews on tripadvisor.com and 2,252 on tripadvisor.de. One location and one language is one job, and the same review can arrive once per language as a translation. Two knobs control that:

- `translated: true` on a row means the text you are reading is a machine translation; `original_language` says what it was written in.
- `includeTranslated: false` keeps only reviews written natively in that site's language — the right setting when you want **restaurant reviews in multiple languages** without counting the same meal five times.

```json
{
  "locationIds": ["2703366"],
  "languages": ["en", "de", "fr", "pt"],
  "includeTranslated": false,
  "maxReviewsPerLocation": 0
}
```

## How do I call it from Python, JavaScript or curl?

Run it from the Console, on a schedule, or from code with your Apify token. The dataset is available as JSON, CSV, Excel, XML or RSS, so "**download tripadvisor restaurant reviews**" can be one HTTP call, and a **tripadvisor restaurant reviews csv** is one query string away.

**Python**

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/tripadvisor-restaurant-reviews").call(run_input={
    "locationIds": ["2703366"],
    "locationType": "restaurant",
    "languages": ["en"],
    "maxReviewsPerLocation": 200,
    "maxRating": 3,
    "requireText": True,
})

for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] != "review":
        continue
    subs = row["sub_ratings"] or {}
    print(row["rating"], subs.get("food"), subs.get("service"), row["review_date"], row["title"])
```

**JavaScript / Node.js**

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/tripadvisor-restaurant-reviews').call({
    startUrls: ['https://www.tripadvisor.com/Restaurant_Review-g35805-d429386-Reviews-The_Cheesecake_Factory-Chicago_Illinois.html'],
    maxReviewsPerLocation: 100,
    sinceDate: '90 days',
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter((i) => i.type === 'review');
console.log(reviews.length, 'reviews,', reviews.filter((r) => r.response).length, 'answered by the owner');
```

**curl** — start a run and wait for it, then pull the dataset as CSV:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~tripadvisor-restaurant-reviews/run-sync-get-dataset-items?token=$APIFY_TOKEN&format=csv" \
  -H 'Content-Type: application/json' \
  -d '{"locationIds":["2703366"],"maxReviewsPerLocation":50,"languages":["en"]}' \
  -o restaurant-reviews.csv
```

## Can I use it with n8n, Make or an AI agent?

Yes, and none of it needs custom code.

- **n8n** — the Apify node runs the actor and hands the dataset to the next step. A common shape: run nightly with `sinceDate: "2 days"`, filter `rating <= 2`, post each one to Slack with the `text`, the `sub_ratings` and the `url`.
- **Make** (Integromat) — the Apify modules do the same with a visual scenario; map `location_name`, `rating` and `text` straight into Google Sheets, Airtable or a helpdesk ticket.
- **MCP / AI agents** — Apify actors are exposed over MCP, so an agent can call this one as a tool and reason over the returned **restaurant review data** ("summarise what changed in the last month at these five locations"). The `SUMMARY` record in the key-value store gives the agent the run's own counts to check its work.
- **Zapier, Airbyte, plain webhooks** — any of them can trigger a run and read the dataset over the REST API.

## Restaurant reputation monitoring: tracking a location over time

**Restaurant reputation monitoring** is a schedule plus two fields. Set up a daily or weekly run with `sinceDate: "7 days"` and `maxReviewsPerLocation: 0` so each run reads only the new pages, then watch:

1. **`rating` and `rating_counts` on the location row.** The overall bubble score moves slowly; the distribution moves first. A jump in `1` and `2` counts two weeks before the average moves is your early warning.
2. **`response` and `response_date` on review rows.** The share of bad reviews with a **restaurant owner response**, and the median days to answer, is the single most fixable reputation metric in the industry — and it is the one nobody measures because it needs exactly this data.

Add `ranking_position` from the location row and you have the third axis: where the restaurant sits against the whole city (`#735 of 6,596 Restaurants in Lisbon`), which is the number a franchise owner actually cares about. Because the same run can cover a whole list of ids, **restaurant competitor reviews** come from the same job: put your locations and your rivals' in one `locationIds` array and compare `sub_ratings`, `dish_tags` and reply rates side by side.

For groups and franchises, the natural cadence is: full historical pull once (`maxReviewsPerLocation: 0`), then a daily top-up. Store `review_id` as the primary key — it is stable — and upsert.

## Restaurant review data: what teams build with it

- **Menu intelligence.** `dish_tags` plus the review `text` tells you which dishes people name, and `sub_ratings.food` tells you whether they liked them. Run it across every competitor in a postcode and you have the local menu landscape.
- **Service analytics.** `sub_ratings.service` against `visit_date` and `trip_type` isolates the shifts and the audiences where service slips.
- **Delivery and POS platforms.** Enrich merchant profiles with `rating`, `review_count`, `cuisines`, `price_range`, `hours`, `open_now` and `permanently_closed` — the last one quietly removes dead listings from a marketplace.
- **Tourism boards and destination marketing.** `attraction reviews` with `category_tags`, `ranking_category` and `reviews_by_language` show which nationalities visit what, which is the whole job.
- **Sentiment and LLM pipelines.** Every row is flat JSON with the text, the language and the bubble score already attached, so it drops straight into an embedding or classification step.
- **Lead generation.** The location row carries `phone`, `email`, `website` and `address` where TripAdvisor publishes them — a list of restaurants under 4.0 bubbles in a city is a qualified list for a reputation product.

## Is scraping TripAdvisor legal?

Scraping publicly available pages is broadly lawful in the EU and the US, and this actor only ever reads pages that any visitor can open without logging in — there is no account, no paywall and no access control involved. That said, we are not lawyers and this is not legal advice.

Two things are worth your own review. First, review text is copyrighted by the person who wrote it, so republishing reviews verbatim is a different question from analysing them; aggregate, quote briefly, or link back. Second, reviewer names, handles and hometowns are personal data under the GDPR: if you keep them, you need a lawful basis, a retention policy and a way to honour deletion requests. Many teams simply drop `reviewer_name`, `reviewer_username` and `reviewer_hometown` on ingest and keep the ratings and text — the actor gives you the fields so that you can make that choice, not because you have to keep them.

Also check TripAdvisor's terms for your particular use case, and do not use the output to build a service that impersonates or passes itself off as TripAdvisor.

## Why not just use the TripAdvisor API?

The official Content API returns up to five reviews per location and requires an approved key, a partner agreement and per-call billing. That is enough to show a widget and nowhere near enough to analyse a restaurant. This actor exists because the useful data is on the page and the API will not give it to you — it is **tripadvisor reviews without api** keys, approvals or quotas, with the full review history, the sub-ratings, the tips and the owner replies that the API omits entirely.

Nor does it need a browser. The reviews are inlined in the page's own hydration state, so one HTTP request per 15 reviews is the whole mechanism: fast, cheap and stable.

## Why does it need a residential proxy?

TripAdvisor is behind a bot gate that fingerprints the TLS handshake. Every datacenter IP range is refused outright, and every Chrome-shaped client is challenged, whatever the IP. A residential IP with a Firefox fingerprint is served normally at about one page per second per IP — which is what this actor does, through Apify Proxy's `RESIDENTIAL` group.

That is why `proxyConfiguration` defaults to residential and why you should leave it alone. If a page is refused anyway, the actor rotates that session's IP and retries with backoff; only after the retries are exhausted does it report `status: "error"` with the reason. A refusal is never reported as "no reviews" — that distinction is the difference between a monitoring pipeline you can trust and one that quietly goes blind.

`sessions` sets how many residential IPs run in parallel (default 2) and `perIp` sets the pace of each (default 1 request/second). Raising `perIp` causes rotations, not speed. Leave both alone unless a run is visibly throttled.

## Which input fields are there, in full?

| Field | Type | Default | What it does |
| --- | --- | --- | --- |
| `startUrls` | array | `[]` | Restaurant or attraction review URLs on any TripAdvisor domain |
| `locationIds` | array | `[]` | Numeric location ids (`2703366` or `d2703366`) |
| `restaurantNames` | array | `[]` | Names resolved via TripAdvisor's typeahead, with a word-overlap guard |
| `locationType` | string | `any` | `restaurant`, `attraction` or `any`; anything else is a free `wrong_type` row |
| `languages` | array | `["en"]` | Which TripAdvisor domains to read; one per language |
| `maxReviewsPerLocation` | integer | `100` | `0` = everything; otherwise the newest N per location and language |
| `maxRating` | number | `0` | Keep only reviews at or below N bubbles; `0` keeps all |
| `tripTypes` | array | `[]` | `family`, `couples`, `solo`, `business`, `friends` |
| `sinceDate` | string | `""` | `YYYY-MM-DD` or `"30 days"`; stops paging once a page predates it |
| `requireText` | boolean | `false` | Drop rating-only reviews before billing |
| `includeTranslated` | boolean | `true` | Keep machine translations, or only natively written reviews |
| `includeLocationRow` | boolean | `true` | Emit the free location context row |
| `sessions` | integer | `2` | Parallel residential proxy sessions |
| `perIp` | number | `1` | Requests per second per session |
| `proxyConfiguration` | object | residential | Apify Proxy settings; `RESIDENTIAL` is required |

## Frequently asked questions

### How much does it cost to scrape 10,000 restaurant reviews?

$50 total — 10,000 delivered rows at $0.005, with compute and residential proxy traffic included. Filtered reviews are free, so a `maxRating: 2` run over the same restaurants costs a fraction of that because only the rows you keep are billed.

### Does it get every review, or only the first page?

Every one, if you ask for it. `maxReviewsPerLocation: 0` walks the whole list in steps of 15 (restaurants) or 10 (attractions) until TripAdvisor stops returning new ids. The `total` field in the status row tells you how many that domain lists, and `reviews_listed` on the location row repeats it, so you can always confirm you got them all.

### Can I scrape attraction reviews with the same run?

Yes. Attractions are first-class here: set `locationType` to `attraction` or leave it at `any` and mix restaurant and attraction targets freely. **Tripadvisor attraction reviews** come back with the same fields minus `sub_ratings` (attractions have none) and plus `category_tags` on the location row.

### What happens if I pass a hotel URL or a hotel id?

A hotel URL is rejected up front with a message pointing at [kestrel/tripadvisor-reviews-scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper). A hotel *id* cannot be recognised before it is fetched, so the actor reads one page, sees that it is a hotel, emits a free `wrong_type` status row naming the sibling actor, and stops. You are never charged for it and it is never scraped here.

### How fresh are the reviews?

They are read live at run time; `fetched_at` on every row is the UTC timestamp of the request. There is no cache and no stored snapshot, so a review published a minute ago appears in the next run.

### Can I get restaurant reviews with photos?

Yes — `photos` is an array of 1200 px image URLs and `photo_count` is the number of them. Roughly one review in five carries at least one photo, and food photos cluster in the reviews that also mention dishes.

### Does it handle restaurants that reply to reviews?

That is one of the strongest fields in the output. `response`, `response_date` and `response_id` carry the owner's or manager's reply. Some chains reply to essentially every review, which makes them a clean benchmark for how fast your own locations answer.

### Why do the review counts differ between TripAdvisor domains?

Because each domain lists a different set: natively written reviews in that language plus the machine translations TripAdvisor has produced for it. `review_count` on the location row is the global total across all languages; `total` in the status row and `reviews_listed` on the location row are what that one domain lists. `reviews_by_language` breaks the global number down per language so you can plan which domains to read.

### Can I run this on a schedule?

Yes — use Apify Schedules with a relative `sinceDate` so the input never goes stale, and the run reads only the new pages. Pair it with a webhook to push new rows into your warehouse as they land. This is the normal setup for ongoing **review monitoring** and it is cheap, because a top-up run reads one or two pages per location.

### Is there a limit on how many locations per run?

No hard limit. Practically, keep a run under an hour: with two sessions at one request per second, that is a few thousand pages. For very large fleets, split the list across several runs — they are independent, and `location_id` makes the results trivial to merge.

### What does `status: "no_reviews"` mean?

The location exists and was read, but the domain you asked for lists no reviews for it — a brand-new restaurant, or a language nobody has reviewed it in. It is a free row, and it is deliberately distinct from `error`, which means the page could not be read at all.

### Can I use the output commercially?

The actor is a tool; what you may do with the data depends on your use case, your jurisdiction and TripAdvisor's terms. Analysis, benchmarking and internal reporting are the normal uses. Verbatim republication of review text and retention of reviewer identities are the two areas where you should take your own legal advice — see the legality section above.

## How does it compare to other TripAdvisor scrapers?

Most listings on the Store are hotel scrapers that happen to accept a restaurant URL. This one is built around the restaurant page: it knows that a restaurant lists 15 reviews per page instead of 10 (getting that wrong silently re-serves page one and truncates your data), it extracts the four dining **restaurant ratings** rather than the six hotel ones, it pulls the diner's tips and the dish tags nobody else surfaces, and it tells you when a target is not the family you asked for instead of billing you for the wrong place.

It also charges for what it delivers. Filtered reviews, unknown ids, duplicate targets, wrong-family targets and empty locations are all free, and if your spending limit is reached mid-run the actor stops delivering rather than handing you rows it could not bill — the counts in the dataset and the counts on your invoice always agree. **Guest reviews** from other platforms live in the sibling actors: [Booking.com](https://apify.com/kestrel/booking-reviews-scraper), [Agoda](https://apify.com/kestrel/agoda-reviews-scraper), [Airbnb](https://apify.com/kestrel/airbnb-reviews-scraper), [Trustpilot](https://apify.com/kestrel/trustpilot-reviews-scraper), [Hostelworld](https://apify.com/kestrel/hostelworld-reviews-scraper) and [Trip.com](https://apify.com/kestrel/trip-com-reviews-scraper), plus [TripAdvisor hotels](https://apify.com/kestrel/tripadvisor-reviews-scraper).

## Support

Found a page shape this does not handle, or a field you need? Open an issue on the actor's Issues tab with the URL and the run id — that is the fastest way to get it fixed, and page shapes do change.

## Related scrapers

Restaurants are one side of TripAdvisor. These read the hotel side and the other places guests and customers talk, with the same row shape and the same pay-per-delivered-row billing:

- [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) — the same engine on hotels: six hotel sub-ratings instead of the four dining ones, trip type, photos and the management response, on 30 country sites in 24 languages.
- [Booking.com Reviews Scraper](https://apify.com/kestrel/booking-reviews-scraper) — Booking.com guest reviews with the liked and disliked text split out, filtered by language and keyword before billing — a `keyword` of breakfast or restaurant gives you the hotel-dining view.
- [Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper) — Agoda hotel reviews with separate positives and negatives and the hotel's reply, by hotel name, URL or id.
- [Trip.com Reviews Scraper](https://apify.com/kestrel/trip-com-reviews-scraper) — Trip.com and Ctrip hotel reviews with four sub-scores and the Chinese-language corpus no other OTA carries, for what Chinese visitors say about a destination.
- [Trustpilot Reviews Scraper](https://apify.com/kestrel/trustpilot-reviews-scraper) — company reviews and TrustScore for a restaurant group or delivery brand, past the 200-review wall an anonymous reader normally hits.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
