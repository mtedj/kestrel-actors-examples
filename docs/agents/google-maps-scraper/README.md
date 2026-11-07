# Google Maps Scraper — Leads, Emails, Phone Numbers & Contacts

A Google Maps scraper built for lead lists. Give it search terms and locations and it returns one flat row per business — name, category, full address in parts, coordinates, phone, website, rating, review count, reviews per star, opening hours, claimed and closed status — and, if you ask, the emails and social links found on each business's own website. Use it as a Google Maps extractor for plain Google Maps data, as a source of Google Maps leads and local business leads, or as a Google Maps email extractor when you need Google Maps emails for outreach. It is priced the way reviewers of other actors keep asking for:

- **$0.004 per place, details included.** No add-on for details, no charge per filter, no start fee.
- **$0.003 per contact — only when one is found.** A place with no website, an unreachable website or a website with nothing on it costs $0 extra.
- **Every filter is free and runs before billing.** A place your filters reject is never charged. The status row tells you how many each filter removed.
- **Only confirmed charges are delivered.** Rows are charged immediately before being written. Billing failures stop the run, and spending limits stop new work.

**Last verified working: 2026-09-21.**

## 谷歌地图商家数据、联系方式与潜在客户：中文调用与语言设置

按关键词与地点获取商家名称、地址、电话、网站和营业时间。enrichContacts 可读取商家网站公开联系方式，费用规则与普通商家行不同，调用前查看定价。

language 控制来源分类、营业时间和描述语言；country 用于地点歧义和电话格式，不是自动翻译服务。中文搜索词可以用于目标地点；先限制 maxPlacesPerSearch。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "searches": [
    "coffee shop"
  ],
  "locations": [
    "Austin, TX"
  ],
  "maxPlacesPerSearch": 1,
  "maxPlacesTotal": 1,
  "maxCrawledPlacesPerSearch": 1,
  "language": "zh-CN",
  "enrichContacts": false,
  "sessions": 1
}
```

Google Maps entreprises / negocios / Firmen：只把来源实际返回的联系方式交付给下游。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Google Maps scraper for AI agents: which input answers which request?

Built to be called by an AI agent (Claude, ChatGPT, or any MCP client through the Apify MCP server) as well as by people. One call, one flat table back, no API key for Google, no login, and the cost is known before the run: `maxPlacesPerSearch` × $0.004, plus $0.003 for each place where a contact is actually found.

Use this actor when the task is to **find local businesses** (any category, any country) and get their **phone numbers, websites, addresses, ratings, opening hours, emails or social media contacts**. Do not use it for review text, photos or popular times — it does not return them (for the reviews of known places use `kestrel/google-maps-reviews-scraper`).

| The user asks for | Input |
| --- | --- |
| "dentists in Austin with phone numbers" | `{"searches": ["dentist"], "locations": ["Austin, TX"], "maxPlacesPerSearch": 50}` |
| "…with emails" / "contact details" / "social media" | add `"enrichContacts": true` |
| "only businesses that have an email" | add `"onlyWithEmail": true` |
| "businesses without a website" | add `"hasWebsite": "no", "hasPhone": "yes"` |
| "unclaimed" Google Business Profiles | add `"isClaimed": "no"` |
| "low rated" / "bad reviews" businesses | add `"maxRating": 3.9, "minReviews": 20` |
| "top rated" / "established" businesses | add `"minRating": 4.5, "minReviews": 100` |
| "places newly seen since the previous run" (scheduled) | add `"onlyNew": true, "monitorKey": "my-list"` |
| "every restaurant in the city", more than ~200 places | add `"fullCoverage": true` and raise `maxPlacesPerSearch` |
| "details / phone / email for this place" (URL, place ID or CID known) | `{"startUrls": ["ChIJ…"], "enrichContacts": true}` |
| several categories × several cities | `"searches": ["plumber", "electrician"], "locations": ["Tulsa, OK", "Norman, OK"]` |

What comes back: rows with `type: "place"` (the data — `name`, `category`, `phone`, `phone_international`, `website`, `address`, `city`, `postal_code`, `country_code`, `lat`, `lng`, `rating`, `review_count`, `opening_hours`, `place_id`, `google_maps_url`, `lead_flags`, and with enrichment `email_primary`, `emails`, `facebook`, `instagram`, `linkedin`, `whatsapp`) and one free `type: "status"` row per search that says how many places were found, filtered, delivered and charged — read it to explain a short or empty result to the user instead of guessing. An unknown location or an empty search is a successful run that costs $0.

## Google Maps scraper output: what is in a row?

One row per place, always the same columns in the same order, so CSV and Excel exports are never ragged. Fill rates were measured on 870 places from 12 cities in 6 countries on 2026-09-21.

| Field | What it is | Filled |
| --- | --- | --- |
| `place_id`, `cid`, `feature_id`, `google_maps_url` | The stable place id (`ChIJ…`), the CID from `?cid=` links, the feature id, and a link that opens the place | 100% |
| `name`, `category`, `categories` | Business name, primary category and every category, in the language you ask for | 100% |
| `search_term`, `search_location`, `rank` | Which search returned the place and where it stood in the list | 100% |
| `address`, `street`, `city`, `state`, `postal_code`, `country_code`, `neighborhood` | The one-line address and its parts. `state` and `neighborhood` exist only where the country uses them | 100 / 99.8 / 91 / 66 / 91 / 100 / 76% |
| `lat`, `lng`, `plus_code`, `distance_km_from_center`, `timezone` | Coordinates, the global plus code, kilometres from the centre of your location or area, IANA timezone | 100% |
| `phone`, `phone_international` | Local format and `+1 512-…` format | 95% |
| `website`, `domain` | The website on the listing and its host | 83% |
| `rating`, `review_count`, `reviews_per_star` | Stars, number of reviews, and the 1★–5★ histogram | 100% |
| `is_closed_permanently`, `is_closed_temporarily`, `is_claimed` | Closed flags, and whether the listing has an owner (`false` = "Claim this business") | 100% |
| `opening_hours`, `open_now` | `{"monday": "8 AM–5 PM", …}` and whether it was open when fetched | 99% |
| `description`, `attributes` | The short description and the attributes listed as present (accessibility, amenities, service options) | 31% / 86% |
| `booking_url`, `menu_url`, `image_url`, `photo_count`, `price_level` | Reservation link, menu link, cover photo, photo count. `price_level` and `menu_url` are in the schema but the search answer did not carry them in any of the 870 places — expect null | 24 / 0 / 99.8 / 99 / 0% |
| `has_website`, `has_email`, `lead_flags` | Free lead helpers: `lead_flags` is any of `no_website`, `low_rating` (< 4.0), `few_reviews` (< 10), `unclaimed` | 100% |
| `fetched_at` | UTC timestamp | 100% |

With `enrichContacts` on, every place row also carries: `emails` (each with `type` — `named` or `role` such as info@ — and the `source_url` it was read from), `email_primary`, `phones_from_site`, `contact_page_url`, `facebook`, `instagram`, `linkedin`, `x`, `youtube`, `tiktok`, `whatsapp` and `enrichment_status`.

A second row type, `status`, is written once per search and is **always free**: `search_term`, `search_location`, `target`, `status` (`ok` / `no_results` / `unknown_location` / `limit` / `error`), `requested`, `found`, `filtered`, `filtered_by` (how many each filter removed), `duplicates`, `already_seen`, `delivered`, `charged`, `contacts_found`, `pages`, `grid_cells`, `coverage_note`, `note` and `error`. `delivered` always equals `charged`.

## Google Maps leads by city: how do I get them?

Cross `searches` with `locations`. Each term is searched in every location; `maxPlacesPerSearch` caps what is delivered (and charged) per pair and `maxPlacesTotal` caps the whole run.

```json
{
  "searches": ["dentist", "orthodontist"],
  "locations": ["Austin, TX", "Round Rock, TX"],
  "maxPlacesPerSearch": 100,
  "enrichContacts": true
}
```

A place that turns up under two searches is delivered and billed once — de-duplication is by place id across every search and grid cell in the run. A full phrase that already says where, such as `"pubs near Prague 2"`, works as a search term on its own; leave `locations` empty.

`language` sets the language of categories, hours and descriptions (`en`, `de`, `fr`, `pt-BR`, `ja` …) and `country` the country to assume for ambiguous names (`us`, `de`, `jp` …). The release test covers the United States, Germany, France, Brazil, India, Japan and the UAE.

## Google Maps emails: how does contact enrichment work, and what does it find?

Turn on `enrichContacts`. For each place with a website the actor reads the home page and then the most promising contact, about, team and imprint pages — up to `maxPagesPerSite` (default 5), because the address is usually not on the home page. It collects emails (including Cloudflare-protected and `name [at] domain` ones), `tel:` numbers, Facebook, Instagram, LinkedIn, X, YouTube, TikTok and WhatsApp links.

Measured on 200 places sampled across the 12 test cities on 2026-09-21:

| Outcome | Places | Charged |
| --- | --- | --- |
| Contact found (email or social link) | 102 (51%) | $0.003 each |
| … of which with at least one email | 67 (34% of all places, 41% of places that have a website) | |
| Website read, nothing on it | 21 | $0 |
| Website unreachable or refusing crawlers | 25 | $0 |
| The "website" is itself a social profile | 16 | $0 |
| No website on the listing | 36 | $0 |

So expect an email for roughly one place in three, not for every place — and pay for the ones you get. An address on somebody else's domain that is not even a `mailto:` link (the web agency's, a booking widget's, the template's) is left out rather than passed off as the business's email. Emails are not verified over SMTP.

The crawler identifies itself, honours `robots.txt`, reads at most one page per second per site, gives each page a 10-second timeout and reads HTML only.

`onlyWithEmail` delivers and bills only places where an email was found on the business website. The cap counts delivered places after filters, and the run reads further down the result list toward that cap. It may return fewer when there are not enough matches. Emails are extracted, not verified for deliverability.

For up to 50 dentists in Austin with an email, use:

```json
{
  "searches": ["dentist"],
  "locations": ["Austin, TX"],
  "maxPlacesPerSearch": 50,
  "onlyWithEmail": true
}
```

Each delivered place costs $0.004 base + $0.003 contact = **$0.007**. If 50 places are delivered, the cost is **$0.35**; 20 cost $0.14. Places with no email are omitted and free. Set `maxTotalChargeUsd: 0.35` separately in Apify run options if that is your budget; it is not an Actor input. A social link without an email is enough for the contact event in general enrichment mode, but not for an email-only row. Phone-only website findings do not trigger a contact fee.

## Scrape Google Maps for businesses without a website

The prospecting list web and marketing agencies ask for: places with a phone but no website.

```json
{
  "searches": ["plumber", "electrician", "roofer"],
  "locations": ["Tulsa, OK"],
  "hasWebsite": "no",
  "hasPhone": "yes",
  "skipClosed": true,
  "maxPlacesPerSearch": 50
}
```

`hasWebsite`, `hasPhone` and `isClaimed` take `any`, `yes` or `no` (`"isClaimed": "no"` keeps only listings Google still offers to "Claim this business"). The places that do have a website are counted under `filtered_by.has_website` in the status row and cost nothing.

## Google Maps data for reputation work: how do I find low rated businesses?

```json
{
  "searches": ["restaurant"],
  "locations": ["Lyon"],
  "language": "fr",
  "country": "fr",
  "maxRating": 3.9,
  "minReviews": 20,
  "maxPlacesPerSearch": 50
}
```

`minRating` / `maxRating` filter on stars and `minReviews` / `maxReviews` on the review count (0 = no limit). A place whose rating or count is unknown never passes a filter that needs it: nobody should pay for a row that cannot be shown to match. The Google Maps review count is on every row, `reviews_per_star` gives the 1★–5★ split, and `lead_flags` marks `low_rating`, `few_reviews` and `unclaimed` on every row for free.

More filters, all free: `categoriesInclude` / `categoriesExclude` match words against the place's own categories (the fix for "two thirds of my leads were off-industry and I was still charged"); `nameContains` / `nameExcludes` match the name; `excludePlaceIds` skips ids you already have and `excludeDatasetId` skips every `place_id` in an earlier dataset of this actor.

## Can I monitor for new businesses on Google Maps?

```json
{
  "searches": ["bakery"],
  "locations": ["Boulder, CO"],
  "maxPlacesPerSearch": 200,
  "onlyNew": true,
  "monitorKey": "boulder-bakeries"
}
```

With `onlyNew`, a run delivers and charges only places that earlier runs with the same `monitorKey` have not delivered; everything else is counted under `already_seen`. These are newly seen listings, not businesses confirmed newly opened: this actor does not verify opening dates. Schedule it weekly and each run is the delta. Only delivered places are remembered, so a place a spending limit cut off comes back next time. Use one `monitorKey` per list.

One honest caveat. Maps re-ranks and rotates the tail of every result list between requests: asked six times in a row, "bakery Boulder, CO" returned 111–129 places each time, 138 distinct, 90 in all six. The actor asks an exhausted list twice and merges the answers, which covers 93–99% of the union, but a repeat run can still surface a few places the previous run was never shown. They are new to you and are delivered as new; nothing is ever delivered twice.

## How do I use my own Google Maps URLs, place ids or CIDs?

Paste them into `startUrls`: search URLs (`google.com/maps/search/…`, read from the map position in the URL), place URLs (`google.com/maps/place/…`), short links (`maps.app.goo.gl/…`), a Google Maps place id (`ChIJ…`), a feature id or a CID.

```json
{
  "startUrls": [
    "ChIJb5gBC-u0RIYRHkntaUcdJGs",
    "https://maps.google.com/?cid=7720327853776914718",
    "https://www.google.com/maps/search/ramen/@35.658,139.7016,15z"
  ],
  "maxPlacesPerSearch": 40
}
```

A place gives one full row. The first two lines above are the same business pasted two ways — it is delivered once. An id Maps does not know is reported in a free status row.

If you are moving from another Google Maps actor, a saved input pastes unchanged: `searchStringsArray`, `locationQuery`, `maxCrawledPlacesPerSearch` and `countryCode` are accepted as aliases of `searches`, `locations`, `maxPlacesPerSearch` and `country`.

## Searching an area: circle, bounding box or polygon

Instead of `locations`, give `latitude` and `longitude` with `radiusKm`, or a `boundingBox`, or a `polygon`:

```json
{
  "searches": ["zahnarzt"],
  "latitude": "52.52",
  "longitude": "13.405",
  "radiusKm": 2,
  "withinRadiusOnly": true,
  "language": "de",
  "country": "de"
}
```

Maps ranks by prominence as well as distance, so a well-known place slightly outside your circle can appear. `withinRadiusOnly` drops anything outside the circle, box or polygon **before billing** — the answer to "results far outside my radius". `distance_km_from_center` is on every row either way. A `boundingBox` is `{"south": …, "west": …, "north": …, "east": …}`; a `polygon` is a list of `[latitude, longitude]` points.

## FAQ: how many places can one search return, and what is full coverage?

A single Maps query lists a limited number of places and then stops — in our measurements between about 120 and 220, depending on the query. When that happens and you asked for more, the status row carries a `coverage_note` saying how many were listed.

`fullCoverage` goes past it: the area is split into a grid, every cell is searched separately from the centre outwards, and the results are merged. It works with `locations` (the area is looked up) or with a circle, box or polygon. `gridCellKm` sets the cell size (0 = automatic) and `maxGridCells` bounds the number of cells (default 64). In the release test a 3 km circle in central Austin returned 260 places for "cafe" through 9 cells, where single queries in the same city stopped between 203 and 222. Every place is still delivered and billed once, however many cells it appears in.

### What happens with a small town, or a location that does not exist?

Every location is looked up first. If Maps does not know it, that search ends with `status: unknown_location`, a note, and **no charge** — and if it was the only search, the run still ends as a success with the explanation on the run card. This matters more than it sounds: asked for "plumber Zzqqxwv Nowhereville", Maps answers with twenty real plumbers near whatever IP asked, as if nothing were wrong. The actor never passes those off as your town.

Since October 2026 Google also answers a misspelt or made-up location with a business whose name merely resembles it, near the IP that asked ("Zzqqxwv Nowhereville" became a bar called Nowhere in Manhattan). The actor reads Google's own place type off the answer and refuses anything that is not a town, postcode, district, region or country, or a landmark spelled as you typed it: those searches end as a free `unknown_location` status row. Bare ambiguous names ("Springfield", "Bali", "Marais") are refused the same way — add the state or country.

A real small town never comes back as a silent zero either. If the typed query returns nothing, or returns places centred far from the looked-up town, the actor searches again around the town's centre and says so in the `note`.

### What if Google throttles or blocks a request?

A consent page, a captcha or an empty shell is never read as "no more places". The request is retried on a fresh proxy session; if the search still fails it becomes an `error` row, not an empty success. There is one more thing the actor handles quietly: about half of all answers arrive with every review count stripped. Those are asked again, so `review_count` is filled on 100% of rows in the release test rather than on half of them.

### Does it work outside the United States?

Yes, by default. The release gate runs 12 cities in the US, Germany, France, Brazil, India, Japan and the UAE and requires at least 60 places from 4 pages in each; on 2026-09-21 every city returned between 67 and 77.

### Is the same search the same twice?

Mostly, and the README will not pretend otherwise: Maps re-ranks per request, so two identical runs capped at 80 places shared 68–77 of them in our tests. Set the cap above what Maps lists, or use `fullCoverage`, when you need the complete set rather than the top of it.

### Is it legal to scrape Google Maps?

The actor reads publicly visible business listings — the same information anyone sees on the map without logging in — and the public pages of business websites, with `robots.txt` honoured. Business contact details are generally not personal data, but some listings belong to sole traders, and emails can be personal data under the GDPR and similar laws. You are responsible for having a lawful basis for how you use what you collect, for honouring opt-outs, and for following the anti-spam rules where your recipients live. If in doubt, ask a lawyer.

## Pricing: what does a run cost?

| Event | Price | When |
| --- | --- | --- |
| `place` | $0.004 | One place row delivered, all details included |
| `contact-found` | $0.003 | Only when enrichment is on **and** an email or social link was read off that place's own website |
| Filters, status rows, duplicates, already-seen places, failed or empty searches, unknown locations, start | $0 | Always |

Worked example: 1,000 places with enrichment on, 380 contacts found → 1,000 × $0.004 + 380 × $0.003 = **$5.14**. Without enrichment the same list is $4.00.

Your spending limit is checked before starting another search, fetching more pages or crawling a website. Searches already in flight may finish. Optional enrichment reserves the base place fees first and skips contacts the remaining budget cannot cover (`enrichment_status: "spending_limit_reached"`). Email-only mode requires enough budget for both the place and contact events before doing work. A billing failure fails the run; if the base place charge succeeded but its contact charge failed, the paid base row is delivered with contacts removed and `enrichment_status: "billing_error"`. Charges and dataset writes are separate platform operations, so an abrupt interruption between them can leave a charged row unwritten. There are no hidden free-tier caps.

## Speed and proxy settings

Apify datacenter proxies work for Maps and are the default in `proxyConfiguration`; residential is not needed. `sessions` is the number of proxy sessions used in parallel (default 6) and `perIp` the requests per second per session (default 1). Measured on 2026-09-21: the 20-place example takes about 20 seconds, 260 places through a 9-cell grid about a minute, and 40 places with enrichment under two minutes — reading websites politely is the slow part. A filter that very few places pass (say, restaurants rated under 4.0) makes the run read the whole result list, which takes a couple of minutes per search.

## Google Maps API alternative: run it from Python, JavaScript or curl

Python:

```python
from apify_client import ApifyClient

client = ApifyClient("<APIFY_TOKEN>")
run = client.actor("kestrel/google-maps-scraper").call(run_input={
    "searches": ["coffee shop"], "locations": ["Austin, TX"], "maxPlacesPerSearch": 50, "enrichContacts": True})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "place": print(row["name"], row["phone"], row["email_primary"])
```

JavaScript (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<APIFY_TOKEN>' });
const run = await client.actor('kestrel/google-maps-scraper').call({
  searches: ['coffee shop'], locations: ['Austin, TX'], maxPlacesPerSearch: 50, hasWebsite: 'no' });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((r) => r.type === 'place').map((r) => [r.name, r.phone]));
```

curl, synchronous, straight to CSV:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~google-maps-scraper/run-sync-get-dataset-items?token=<APIFY_TOKEN>&format=csv" \
  -H "Content-Type: application/json" \
  -d '{"searches":["coffee shop"],"locations":["Austin, TX"],"maxPlacesPerSearch":20}'
```

That last call is also the shortest route from Google Maps to CSV. Compared with the official Places API there is no per-field billing, no 60-result ceiling per query, and the emails and social links are not something that API offers at all — which is why people look for a Google Places API alternative for lead generation in the first place.

## Google Maps lead generation in n8n, Make and AI agents

- **n8n** — use the Apify node (or an HTTP Request node with the curl call above): *Run actor and get dataset* → filter `type = place` → your CRM, Google Sheets or an email tool. With `onlyNew` and a schedule trigger, each execution passes on only the new leads. People searching for a Google Maps scraper n8n workflow usually want exactly this loop.
- **Make** — the Apify app's *Run an Actor* module followed by *Get Dataset Items*; map `name`, `phone_international`, `email_primary` and `lead_flags` into the next module.
- **AI agents (MCP)** — through the Apify MCP server an agent can call this actor as a tool: "find 30 dentists in Austin without a website" becomes one run with `hasWebsite: "no"`. The flat row and the `lead_flags` column are there so a model does not have to interpret nested data.
- **Zapier, Google Sheets, webhooks** — any Apify integration works; the dataset exports as JSON, CSV, Excel or an RSS feed.

## What this Google places scraper does not do

Said plainly, so nobody finds out from a bill:

- **Review text.** This actor returns the rating, the review count and the per-star histogram, not the reviews themselves.
- **Photos and popular times.** One cover image URL and the photo count only.
- **Email verification.** Addresses are read off websites; they are not checked over SMTP.
- **Person-level leads.** No names and job titles from bought databases — that data is the source of the worst reviews in this category. The Google Maps business data here is what the business itself publishes.
- **Google Maps phone numbers for places that list none.** About 5% of places have no phone on their listing; `phones_from_site` sometimes fills the gap when enrichment is on.

## Support

Open an issue on the actor's Issues tab with the run id and what you expected; issues are answered personally and quickly, and a field you need is usually a small change. If a run fails because of the source rather than your input, it fails loudly on purpose — a daily canary runs this actor and checks both the places and the enrichment.
