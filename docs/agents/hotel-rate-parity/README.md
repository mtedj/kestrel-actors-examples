# Hotel Rate Parity Checker — OTA Price Comparison

Hotel rate parity checker built on Google Hotels prices: for each property and stay you name, one row with every booking source Google lists side by side — Booking.com, Expedia, Hotels.com, Agoda, Trip.com, Vio.com, the property's official site — and the parity math already done: the cheapest and dearest source, the spread in percent, the direct rate, and which OTAs undercut it and by how much. It is an OTA price comparison and rate shopping tool for revenue managers, channel managers and owners, priced per row instead of per seat. Put it on a schedule and it becomes rate parity monitoring with a history you own. No API key, no login, no browser: it reads the same public comparison any traveller sees, through Apify's proxies, and returns clean JSON.

**You pay only for delivered parity rows.** Properties with no rates, names that do not resolve, duplicates, rows a filter removed and status rows cost nothing.

## 酒店比价、OTA 房价一致性与直订价格：中文调用与语言设置

对同一酒店、入住日期和人数比较 Google Hotels 展示的 OTA 与官网报价。minSpreadPct 只筛选达到差价阈值的结果。

country 是搜索者市场，language 控制可用的名称翻译，currency 控制报价币种。保持市场和币种一致；差价不自动证明违反合同条款。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "hotels": [
    "https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE"
  ],
  "checkIn": "30 days",
  "nights": 1,
  "currency": "USD",
  "sweepDays": 1,
  "language": "zh-CN",
  "sessions": 1
}
```

Parité tarifaire / paridad de tarifas / Ratenparität：同条件比较 OTA 与直订报价。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Hotel rate parity checker for AI agents: which input answers which request?

Use it when the user names one or more hotels and wants every booking site's rate for a stay side by side with the hotel's own rate, the gap, and who undercuts direct: "is anyone undercutting our direct rate for next weekend", "compare OTA rates for the Hyatt in Lisbon", "a parity report for our comp set every morning", "only the breaches over 5 %". Do not use it for a city search or hotels you cannot name (the [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices) searches places), for room-level parity (the same room type on every channel — the parent's `offerLevel: "rooms"`), for the cheapest date to stay over a window of dates (the [Hotel Price Tracker](https://apify.com/kestrel/hotel-price-tracker)), for reviews, or for more than 6 adults or one room.

| The user asks for | Input |
|---|---|
| Is anyone undercutting hotel X for a stay | `{"hotelNames": ["Hyatt Regency Lisbon"], "checkIn": "2026-11-14", "nights": 2}` then read `undercut_by` and `undercut_pct` |
| Every OTA's rate for hotel X side by side | the same input; the `sources` array, cheapest first, each with `price_nightly`, `price_total`, `free_cancellation`, `url` |
| A parity report for our comp set every morning | `{"hotels": ["<entity_id>", "<entity_id>"], "checkIn": "30 days", "nights": 1}` (entity ids from a first run by name) and an Apify schedule |
| Only stays with at least 5% cheapest-to-dearest spread | add `"minSpreadPct": 5`; this does not itself prove an OTA undercut of the official site |
| Only where an OTA is under the official site | keep `minSpreadPct` 0 and filter rows on `undercut_by` not empty (`spread_pct` measures cheapest vs dearest source, not direct) |
| The next week of check-in dates per hotel | `"sweepDays": 6` (7 stays per hotel, one row each) |
| A family stay, prices in pounds as a UK booker sees them | `"adults": 2, "childrenAges": [5, 9], "currency": "GBP", "country": "gb"` |
| A spending limit | the Apify run option `maxTotalChargeUsd`; hotels × (`sweepDays` + 1) bounds the rows ($0.01 each) |

One `parity` row per hotel and stay, $0.01, however many sources the row holds (4 to 36, about 18 on average, measured on 174 hotels with the same call). Hotels with no rate, rows under `minSpreadPct`, names that match nothing, duplicates and status rows are never billed. Measured on 2026-08-30 across 100 independent US hotels over 14 nights: 71 were undercut by at least one OTA on most nights where Google showed a direct rate, 18 by 20 % or more on average, mostly by wholesale resellers (Super.com, Vio.com, Etrip, Traveluro) rather than the major OTAs.

Rows come in two types. `parity`: `hotel_name`, `entity_id`, `check_in`, `check_out`, `nights`, `currency`, `sources` (array, cheapest first: `source`, `source_id`, `official`, `price_nightly`, `price_total`, `free_cancellation`, `url`), `n_sources`, `min_source`, `min_price`, `max_source`, `max_price`, `spread_pct`, `median_price`, `official_source`, `official_price`, `official_is_cheapest`, `undercut_by` (OTAs priced under the official site, cheapest first), `undercut_pct`, `fetched_at`; `stars`, `rating`, `reviews` are filled for hotels given by name, null for hotels given by URL. When Google lists no official site for the hotel that day, `official_source`, `official_price`, `official_is_cheapest` and `undercut_pct` are null and `undercut_by` is empty — and Google does not list it on every run: a null one day and a rate the next is Google's listing changing, not the hotel's rate, so confirm a missing direct rate on a second run before acting on it. `status`: one per hotel and stay with `status` `ok`, `filtered`, `no_rates`, `not_found`, `duplicate`, `unpaid` or `error`, never charged. An empty result is a `status` row that says why, not a failed run; the run's status message counts the rows and how many undercut the official site.

In other languages: Preisvergleich Hotelpreise, Ratenparität (DE); comparador de precios de hoteles, paridad tarifaria (ES); comparateur de prix d'hôtel, parité tarifaire (FR); comparação de preços de hotéis (PT).

### Flag a lower OTA quote without confusing missing evidence with parity

For an OTA quote at least 5% below direct, leave `minSpreadPct` at zero. That input measures the cheapest-to-dearest source spread, not the discount from the official site.

```json
{
  "actor": "kestrel/hotel-rate-parity",
  "input": {
    "hotelNames": ["Hyatt Regency Lisbon"],
    "checkIn": "2026-12-10",
    "nights": 3,
    "adults": 2,
    "currency": "EUR",
    "minSpreadPct": 0,
    "sweepDays": 0
  },
  "callOptions": {"maxTotalChargeUsd": 0.05, "timeout": 180},
  "waitSecs": 30
}
```

This `call-actor` envelope requests one hotel/stay: at most one $0.01 parity event plus a free status row. Poll `get-actor-run` if needed and fetch its default dataset with `get-dataset-items`. Validate the resolved `hotel_name`, `hotel_url` and `entity_id`; the name guard is a heuristic, not proof of identity. Reuse the verified `entity_id` in `hotels` on later runs.

Interpret `type: "parity"` rows as follows:

| Returned evidence | Interpretation |
|---|---|
| `official_price` is null | Direct comparison is unknown; an empty `undercut_by` does not mean parity passed. |
| Official price exists, `undercut_by` is nonempty, and `undercut_pct >= 5` | At least one returned OTA quote is 5% or more below the lowest returned direct quote. Inspect `sources` for the source and rate. |
| Official price exists and the condition above is false | No returned quote met that threshold; this is limited to the offers Google exposed for this request. |
| Status is `no_rates`, `not_found`, `filtered`, `unpaid` or `error` | No comparable delivered parity result; report the reason instead of declaring parity. |

These are per-source minimum quotes for the requested stay/party. The code does not join an identical room, meal plan, cancellation contract, payment timing or tax basis across channels. A source's `free_cancellation` value is an available indicator, not that full contract. Treat a lower quote as a lead to investigate, not a verified equivalent-rate violation. The Actor sends no notification itself; a downstream integration can act on qualified rows.

Each run uses its own dataset. Save the rows with `fetched_at` and the request context to build a history; fixed absolute dates compare the same stay, while relative dates compare a moving lead time.

## What does the rate parity checker return?

Google Hotels is a metasearch engine: for a property and a stay it shows the rate of every booking site it knows and the property's own site. The parent scraper of this actor returns that comparison as one row per source. This actor collapses it into what a parity check actually needs — **one `parity` row per property and stay**:

- `sources` — every source that carried a rate, cheapest first, each with its name, Google's `source_id`, an `official` flag, the nightly rate, the stay total, the free-cancellation flag and the booking link with your dates filled in (official sites: the booking engine URL).
- `min_source` / `min_price` and `max_source` / `max_price` — who is cheapest, who is dearest, and `spread_pct` between them. `median_price` shows where the market sits.
- `official_source` / `official_price` — the property's own listing when Google shows one, `official_is_cheapest`, the list of OTAs in `undercut_by`, and `undercut_pct`: how far the cheapest channel beats direct.
- Identity and context: `hotel_name`, `entity_id`, `hotel_url`, `check_in`, `check_out`, `nights`, `adults`, `children`, `currency`, `fetched_at`; for name lookups also `hotel_id`, `stars`, `rating` and `reviews`.

A `status` row per property and stay (never charged) says what happened: `ok`, `filtered`, `no_rates`, `not_found`, `duplicate`, `unpaid` or `error`.

## Rate parity monitoring on a schedule

Parity breaks quietly: a wholesaler feeds a bed bank, a bed bank feeds a metasearch, and by Friday an OTA is 8% under your direct rate for the weekend you were sure of. A rate parity checker is only useful if it runs every day, so this actor is built for schedules:

- **Relative dates.** `"checkIn": "30 days"` means "the stay 30 days from whenever this run starts", forever. No stale dates, no edited schedules.
- **A window per run.** `sweepDays: 6` checks the same length of stay on seven consecutive check-in dates — one parity row each — so a single scheduled run covers the week that matters for your pickup.
- **Spread filter.** `minSpreadPct: 5` delivers only stays whose cheapest-to-dearest spread reaches 5%. A filtered stay is not a verified parity pass; for an official-site undercut threshold, keep this filter at zero and qualify the direct-rate evidence downstream.
- **History you own.** Each run writes dated rows to its own dataset; combine saved datasets externally to build a history. Export to Sheets, BigQuery or a warehouse and the `undercut_pct` column over time is your parity violation report — and, read across properties, plain hotel price tracking and hotel price comparison for the set you named.

Pair the run with Apify's webhooks or an n8n, Make or Zapier flow and a breach becomes a Slack message with the property, the OTA, the gap and the booking link — see the integrations section below.

## OTA price comparison: the sources Google lists

Whatever Google Hotels shows for that property and market is what you get: Booking.com, Expedia, Hotels.com, Agoda, Trip.com, Priceline, Vio.com, Etrip, Super.com, KAYAK, Kiwi.com, eDreams, Bluepillow, Hostelworld, Vrbo, Holidu and dozens of regional OTAs, plus the official site. Two details matter for a clean OTA rate comparison:

- Sources are keyed by Google's `source_id`, not by name. A brand can appear twice for one property — its official listing (`official: true`) and its marketplace rate — and both are kept as separate entries in `sources`.
- Rates are the lowest rate each source offers for your occupancy and dates, in one currency, for one market. Set `country` to the market you sell in, because which sources Google lists differs by market, and compare like with like. Whether the displayed rate includes taxes follows the country of the proxy IP the request leaves from (pre-tax plus mandatory fees from a US IP, all-in from most others), not `country`.

The official site is identified by Google itself, not guessed from the name. When Google lists no official site the direct fields are `null` and the row still gives you the full OTA price comparison. Google does not list the official site on every run (measured: 8 of 14 nights one day, 14 of 14 the next for the same hotel), so treat a `null` direct rate as "not shown today" and confirm it on a second run before telling anyone their direct rate is missing.

## Hotel price monitoring for your competitive set

A revenue manager's comp set is a list of names, not tokens. `hotelNames` accepts names — `"Hyatt Regency Lisbon"`, `"Brown's Avenue Hotel Lisbon"` — and resolves each with one place search. The listing is kept only when its name shares at least two words and 60 % of the words you typed; otherwise the status row says `not_found` and nothing is billed. Google answers every search with *something*, so this guard is what stops a typo from turning into a paid row about a stranger. The guard counts every word you typed, so a city Google leaves out of the listing's name works against you ("Hotel Emma San Antonio" shares 1 of 3 words with "Hotel Emma"): write the name as Google lists it, and add the city only to a generic name. Name lookups also carry `stars`, `rating`, `reviews` and `hotel_id` from the listing, which URL lookups do not.

Once resolved, reuse the `entity_id` from the row in `hotels`: exact, one call per stay, and no search at all. That is the cheapest and most reliable way to run the same comp set every morning, and it is how hotel price monitoring should be wired after the first run.

## Input

| Field | Meaning |
|---|---|
| `hotels` | Google Hotels URLs (`…/travel/hotels/entity/ChkI…`) or bare entity tokens. Exact: one offers call per property and stay, no search, nothing unrelated billed. |
| `hotelNames` | Property names. One place search each; kept only when the listing's name matches most of your words (at least two). Add the city to a generic name. |
| `checkIn` | `YYYY-MM-DD`, or relative for schedules: `"30 days"`, `"6 weeks"`, `"+30d"`, `today`, `tomorrow`. Past check-ins are rejected before anything is fetched. |
| `nights` | Length of stay, 1–30. Check-out = check-in + nights. |
| `sweepDays` | Also check the same stay starting on each of the next N days (a week of check-in dates = `6`). |
| `adults`, `childrenAges` | Occupancy per room; rates scale with it exactly as on Google. |
| `currency`, `language`, `country` | One currency for every price; Google UI language (`hl`); market (`gl`) — the booker's country, which decides which booking sites Google lists. |
| `minSpreadPct` | 0 = every priced property. N = only properties whose cheapest-to-dearest spread is at least N%. This is not an official-site undercut filter. Dropped properties are never billed. |
| `proxyConfiguration` | Apify datacenter proxies work; keep the default. |
| `sessions`, `perIp` | Parallel proxy sessions and requests per second per IP (defaults 4 and 0.5). |

### Example: two properties, tonight plus 30 days, one night

```json
{ "hotels": ["https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE"], "checkIn": "30 days", "nights": 1, "adults": 2, "currency": "USD" }
```

### Example: a comp set by name, a week of check-in dates, breaches only

```json
{ "hotelNames": ["Hyatt Regency Lisbon", "Altis Grand Hotel Lisbon", "Brown's Avenue Hotel Lisbon"], "checkIn": "14 days", "nights": 2, "sweepDays": 6, "minSpreadPct": 5, "currency": "EUR", "country": "pt" }
```

### Example: a family occupancy in the market you sell in

```json
{ "hotels": ["ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE"], "checkIn": "2026-10-16", "nights": 3, "adults": 2, "childrenAges": [5, 9], "currency": "GBP", "country": "gb", "language": "en" }
```

## Output

`parity` row (the Console's **Rate parity** and **Undercut check** views show the same rows as tables; the dataset schema documents every field):

```json
{ "type": "parity", "query": "https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "hotel_name": "Brown's | Avenue Hotel", "entity_id": "ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "hotel_id": null, "hotel_url": "https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "stars": null, "rating": null, "reviews": null,
  "check_in": "2026-09-27", "check_out": "2026-09-29", "nights": 2, "adults": 2, "children": 0, "currency": "USD",
  "sources": [
    { "source": "Vio.com", "source_id": 2017, "official": false, "price_nightly": 377.39, "price_total": 754.78, "free_cancellation": null, "url": "https://www.vio.com/…" },
    { "source": "Brown's Avenue", "source_id": 12058, "official": true, "price_nightly": 488.46, "price_total": 976.92, "free_cancellation": null, "url": "https://be.synxis.com/?hotel=…&arrive=2026-09-27&depart=2026-09-29" },
    { "source": "Booking.com", "source_id": 184, "official": false, "price_nightly": 563.3, "price_total": 1126.61, "free_cancellation": null, "url": "https://www.booking.com/hotel/pt/browns-avenue.html?checkin=2026-09-27&checkout=2026-09-29" },
    { "source": "Expedia.com", "source_id": 232, "official": false, "price_nightly": 573.94, "price_total": 1147.88, "free_cancellation": null, "url": "https://www.expedia.com/…" }
  ],
  "n_sources": 4, "min_source": "Vio.com", "min_price": 377.39, "max_source": "Expedia.com", "max_price": 573.94, "spread_pct": 52.1, "median_price": 525.88,
  "official_source": "Brown's Avenue", "official_price": 488.46, "official_is_cheapest": false, "undercut_by": ["Vio.com"], "undercut_pct": 22.7,
  "fetched_at": "2026-08-29T06:15:42+00:00" }
```

`status` row (never charged):

```json
{ "type": "status", "query": "Brown's Avenue Hotel Lisbon", "hotel_name": "Brown's | Avenue Hotel", "entity_id": "ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE", "check_in": "2026-09-27", "check_out": "2026-09-29", "status": "ok", "n_sources": 4, "spread_pct": 52.1, "filtered": false, "error": null, "fetched_at": "2026-08-29T06:15:42+00:00" }
```

A run also writes a `SUMMARY` record to its key-value store: parity rows delivered, how many undercut their official site, filtered, no rates, not found, duplicates, errors, charged events and HTTP stats.

## How is the parity math calculated?

Everything is computed from the nightly rate of each source's lowest offer for your occupancy (when a source shows only a stay total, nightly = total ÷ nights). Using the row above:

- **Spread**: (max − min) ÷ min × 100 = (573.94 − 377.39) ÷ 377.39 × 100 = **52.1%**. This is the size of the gap across the whole distribution, official site included, and it is what `minSpreadPct` filters on.
- **Official is cheapest**: the official rate is 488.46 and the cheapest source is 377.39, so **false**. A tie counts as parity (half a cent tolerance), and an official rate that *is* the minimum makes `undercut_by` empty and `undercut_pct` 0.
- **Undercut by**: every non-official source below 488.46 — here only **Vio.com**. Cheapest first, so the first name is your worst offender.
- **Undercut %**: (official − min) ÷ official × 100 = (488.46 − 377.39) ÷ 488.46 × 100 = **22.7%**: the discount a guest gets for not booking direct.
- **Median**: the middle of the four nightly rates, **525.88** — a quick read on whether one outlier or the whole market has moved.

When Google lists no official site, `official_price`, `official_is_cheapest` and `undercut_pct` are `null` and `undercut_by` is empty; spread, min, max and median still describe the OTA market.

## How much does it cost?

Pay per event: one `parity` event per delivered parity row, at the price on this page's pricing tab. A comp set of ten properties checked over seven check-in dates is 70 rows; the same run with `minSpreadPct` set delivers and bills only rows meeting the cheapest-to-dearest spread threshold. That filter does not establish a direct-price undercut or equivalent-room violation. Properties with no rates for the stay, names that do not resolve, a property listed twice, rows removed by the filter, rows the spending limit refused and `status` rows are all free, and a property and stay is billed once per run. Apify's platform usage for such a run is a fraction of a cent: name lookups take one search each, every property and stay takes one offers call.

Compared with the parent [Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices), which bills one row per source, a parity row is one event for the whole comparison — usually cheaper per property, and already in the shape a rate shopper wants.

## Google Hotels prices vs rate shopping tools: how this compares

- **Rate shopping tools for hotels** — the hotel rate shopper and parity monitor SaaS sold per property per month, the competitor rate shopping and hotel price intelligence suites — shop the same public sources, add dashboards and alerts, and charge a seat or a property licence. This actor gives you the rows and the math for cents, and the dashboard is whatever you already use — a sheet, Metabase, Looker, a Slack channel.
- **SERP APIs** (SerpApi, DataForSEO, Bright Data) return Google's search page per query; per-source rates are usually a second product, there is no parity math, and you pay per search whether or not it had results.
- **Channel managers** know your own rates, not the OTAs' displayed prices after wholesaler and bed-bank markups. A channel manager rate check against what a guest actually sees needs a metasearch read, which is what this is.
- **Building it yourself**: Google Hotels renders prices through internal RPC calls, not HTML, and the payload changes. The point of this actor is that someone keeps that working and reports failures as `status` rows instead of silent zeros.

There is no public Google Hotels API for reading prices; Google's own hotel APIs are feeds for properties that *send* rates to Google. Reading them back is a scraper, and this one is watched by a daily canary run.

## How to use it from Python, JavaScript, curl, n8n, Make or an AI agent

Run it from the Apify Console with the form, or programmatically. Replace `<TOKEN>` with your Apify API token.

Python — observed direct-price undercuts to stdout, for further comparison of terms:

```python
from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/hotel-rate-parity").call(run_input={
    "hotelNames": ["Hyatt Regency Lisbon", "Altis Grand Hotel Lisbon"], "checkIn": "30 days", "nights": 2, "sweepDays": 6, "currency": "EUR", "country": "pt"})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "parity"]
for r in sorted(rows, key=lambda r: -(r["undercut_pct"] or 0)):
    if r["undercut_by"]: print(r["hotel_name"], r["check_in"], f'{r["undercut_pct"]}% under direct via {r["undercut_by"][0]} ({r["min_price"]} vs {r["official_price"]} {r["currency"]})')
```

JavaScript / Node.js — observed direct-price undercuts of at least 5%, with unknown results kept distinct:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/hotel-rate-parity').call({ hotels: ['ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE'], checkIn: '30 days', nights: 1, minSpreadPct: 0 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const comparisons = items.filter(r => r.type === 'parity');
const lines = comparisons.filter(r => r.official_price != null && r.undercut_by.length && r.undercut_pct >= 5)
  .map(r => `${r.hotel_name} ${r.check_in}: ${r.min_source} ${r.min_price} vs direct ${r.official_price} (${r.undercut_pct}%) — verify room and rate terms`);
const unknown = !comparisons.length || comparisons.some(r => r.official_price == null || !r.sources.some(s => !s.official));
if (unknown) lines.push('Some comparisons lack direct/OTA evidence; parity unknown for those results');
console.log(lines.join('\n') || 'No observed OTA undercut of at least 5%; equivalent room and rate terms remain unverified');
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~hotel-rate-parity/run-sync-get-dataset-items?token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"hotels": ["ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE"], "checkIn": "30 days", "nights": 1, "currency": "USD"}'
```

- **n8n, Make, Zapier**: a Schedule trigger, an HTTP Request (or the Apify node) calling `run-sync-get-dataset-items` with the input above, a filter on `undercut_by` not empty, and a Slack, email or Sheets node — four nodes for a parity alert.
- **AI agents and MCP**: the actor is available through the Apify MCP server and Apify AI; the README, input schema and flat rows are written so an agent can answer "is anyone undercutting our direct rate for next weekend?" from one run.
- **Google Sheets, BigQuery, Airtable**: export the dataset from the run page or through Apify's integrations; `sources` is a nested array, so flatten it or keep the summary columns.

## Is it legal to check rate parity with scraped prices?

The actor reads publicly displayed prices — the same figures any visitor sees without logging in — and stores no personal data: rows describe properties, booking sources and rates, not people. Comparing public rates across channels is standard practice in the industry (it is what every rate shopping tool does), but terms of service and local law differ; check that your use complies, and use the data for your own analysis rather than republishing it as Google's.

## Limits and honest notes

- Rates are what Google Hotels displays for the market (`country`) and currency you choose. Proxy location can affect tax presentation. Keep the request context consistent and verify each source's taxes and fees before treating a difference as comparable; a shared market and currency do not prove identical rate terms.
- Sources per property vary by market and day: 4 to 36, about 18 on average (measured on 174 hotels with the same call). A property with a rate on only one source still gets a row (spread 0); a property with none gets a free `no_rates` status.
- Official-site detection is Google's. A few properties are listed under a marketplace brand (a property manager, a franchise engine) and carry no official flag; the row then has `official_price: null`. Google also drops the official listing on some runs and shows it again the next: confirm a missing direct rate on a second run.
- Google's comparison shows each source's lowest offer for the occupancy. Use the parent scraper with `offerLevel: "rooms"` to inspect room-level offers, then verify room, cancellation and other rate terms across channels; collecting room offers does not itself prove equivalence.
- Name lookups are guarded, not clairvoyant: a name matching a *different* property with the same words (two "Grand Hotel" in one city) resolves to Google's best match. Check the `entity_id` once, then switch to `hotels`.
- Google changes its internal formats occasionally; a daily canary run watches for that, the actor is rebuilt within days, and every run reports `status` rows so a failure is visible rather than a silent zero.

## FAQ

### Does it need a Google Hotels API key or a Google account?

No. There is no public API for reading Google Hotels prices; the actor reads the public results through Apify's proxies. No login, cookies or API key.

### What is rate parity, in the terms this actor uses?

Rate parity compares the same room and rate terms across channels, including your own site. This row summarizes displayed source minima: `spread_pct` is the gap between cheapest and dearest, and `undercut_pct` is how far the cheapest OTA is below the official quote. Scan `undercut_by` for candidate gaps to investigate; `official_price` is the direct quote Google shows. The row does not verify identical room or rate terms, and an absent official quote leaves that comparison unknown.

### Can it run a rate parity check for my whole comp set every morning?

Yes: list the properties in `hotels` (or `hotelNames` for the first run), add `sweepDays` for the booking window, and schedule the actor in Apify Console. Save each run's separate dataset externally. Relative `checkIn` observes a moving lead time; absolute dates retain a fixed stay. `minSpreadPct` filters the source spread; keep it zero and qualify `official_price`, `undercut_by` and `undercut_pct` downstream for a direct-undercut alert.

### Why is the OTA cheaper than my official site?

Usually a wholesale or bed-bank rate resold on a metasearch-facing OTA, a member price shown to everyone by a listing site, or a stale rate on a channel you stopped updating. The `sources` array names the exact source and gives its booking link, so the trail starts from the row.

### Which booking sites are compared?

Every source Google Hotels lists for that property and market — the big OTAs, metasearch resellers and regional sites — plus the official site when Google identifies one. Names and `source_id`s come straight from Google.

### Does the price include taxes and fees?

It is the nightly and total figure Google Hotels shows. Tax presentation can depend on proxy location. Verify source-level taxes, fees and rate terms before a like-for-like conclusion; the Actor compares displayed minima and does not prove those terms match.

### How is this different from the Google Hotels Prices Scraper?

Same data, different shape. The parent returns one row per source (and can go to room level); this one returns one row per property and stay with the comparison and the parity math done, filters on spread before billing, and accepts names. Use the parent when you need every source as its own row or room-level offers.

### Is there a free tier?

Yes: Apify's free plan covers small runs, and a run that delivers no parity rows costs nothing.

Last verified working: 2026-08-29.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Daily Parity Violation Report for Hotels](https://apify.com/kestrel/hotel-rate-parity/examples/parity-violation-report)
- [Direct Booking Rate Undercut Check](https://apify.com/kestrel/hotel-rate-parity/examples/direct-booking-rate-check)
- [Competitor Rate Shopping Without a Seat](https://apify.com/kestrel/hotel-rate-parity/examples/competitor-rate-shopping)
- [Rate Parity Check for a Single](https://apify.com/kestrel/hotel-rate-parity/examples/rate-parity-check-for-a-single-hotel)
- [Rate Parity Monitoring Across 30 Days](https://apify.com/kestrel/hotel-rate-parity/examples/rate-parity-monitoring-over-30-days)
- [Rate Parity Checker: Spreads Over 10%](https://apify.com/kestrel/hotel-rate-parity/examples/rate-parity-checker-spreads-over-10-percent)
- [Rate Audit on the German Market](https://apify.com/kestrel/hotel-rate-parity/examples/hotel-rate-audit-on-the-german-market)
- [Rate Shopping Tool for a Group](https://apify.com/kestrel/hotel-rate-parity/examples/rate-shopping-tool-for-a-hotel-group)
- [OTA Price Comparison for Weekend Stays](https://apify.com/kestrel/hotel-rate-parity/examples/ota-price-comparison-for-weekend-stays)
- [Price Comparison at Family Occupancy](https://apify.com/kestrel/hotel-rate-parity/examples/hotel-price-comparison-at-family-occupancy)
- [Rate Shopper for the UK Market](https://apify.com/kestrel/hotel-rate-parity/examples/hotel-rate-shopper-for-the-uk-market)
- [Google Hotels Rate Parity by Entity URL](https://apify.com/kestrel/hotel-rate-parity/examples/google-hotels-rate-parity-by-entity-url)

## Related scrapers

Rate parity is one question about a property. These answer the others, with the same pay-per-delivered-row billing and the same scheduling story:

- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — need every source as its own row, room-level offers, or a whole city search? That is the parent of this actor.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda guest reviews with separate positives and negatives.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing, with translations.
- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — Airbnb prices, availability calendars and occupancy.
- **[Google Flights Scraper](https://apify.com/kestrel/google-flights-prices)** — airfare for a route and date, with a cheapest-day sweep.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
