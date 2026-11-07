# Google Flights Scraper — Airfare Prices, Fares & Price Tracking

A **google flights scraper** that returns airfare prices straight from Google Flights for the routes, dates and cabin you ask for. Every itinerary comes back as one row: price, airline, departure and arrival times, duration, stops, every layover and the CO2 estimate — a **flight price scraper** and **flight price tracker** in one, with no **google flights api** key, no login and no browser.

Use it to watch **flight prices** on your routes, build **flight price history** nobody else will give you, or pull **airline ticket prices** across a whole month to find the cheapest departure day.

Last verified working: 2026-10-19.

## Google 机票价格、航班与票价查询：中文调用与语言设置

通过机场代码、出发日期和乘客人数获取航班价格。需要每天保存结果才能形成自己的价格历史；一次运行不会还原过去未采集的价格。

market 是搜索者市场，currency 是票价币种。当前结果按英文读取，没有 language 输入；不要传入 zh-CN 或虚构翻译功能。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "routes": [
    "LIS-LHR"
  ],
  "departDate": "30 days",
  "sweepDays": 1,
  "currency": "EUR",
  "market": "pt",
  "maxResultsPerSearch": 1,
  "sessions": 1
}
```

Precios de vuelos / prix des vols / Flugpreise：比较相同航线、舱位和日期。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Google Flights scraper for AI agents: which input answers which request?

Use it when the user wants flight prices from Google Flights for a route and dates: every itinerary Google lists (airline, times, stops, layovers, CO2) for one date, a round trip, a passenger mix or a cabin, or the same trip across a sweep of departure days. Do not use it for booking links per seller, flight numbers, aircraft types, baggage fees, multi-city trips, an airline filter, or fares from Skyscanner, Kayak or an airline's own site: it returns what Google Flights lists, read in English. For one row per day (the cheapest fare of each day, a tracker you schedule) use [Flight Price Tracker](https://apify.com/kestrel/flight-price-tracker) instead; this actor bills every itinerary of every search.

| The user asks for | Input |
|---|---|
| Flight prices on a route for a date | `{"routes": ["JFK-LHR"], "departDate": "2026-11-20"}` |
| Round trip fares | add `"returnDate": "2026-11-27"` (`price` = both legs, `round_trip_total: true`) |
| Nonstop only | add `"maxStops": "nonstop"` |
| Business class fares | add `"seat": "business"` |
| A family: 2 adults, 2 children | add `"adults": 2, "children": 2` (`price` is the total for all four) |
| A few Google-ranked options, a bounded run | add `"maxResultsPerSearch": 5`; these are not necessarily the five cheapest |
| Which departure day is cheapest, a price calendar | add `"sweepDays": 13` (14 departure days; sort `flight` rows by `price`, or read `cheapest` on each `status` row) |
| Prices in euros as seen from Germany | add `"currency": "EUR", "market": "de"` |
| Track a fare daily without editing the input | `"departDate": "30 days"` (and `"returnDate": "37 days"`) with an Apify schedule |
| Several routes at once | `"routes": ["JFK-LHR", "EWR-LHR", "BOS-LHR"]` (every route is searched for every date) |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `maxResultsPerSearch` bounds the rows per search |

`maxResultsPerSearch` defaults to `0` = every itinerary Google lists, usually 10 to 35 per route and date, and each one is billed; `sweepDays` multiplies the searches. A small `maxResultsPerSearch` buys a ranked sample. For a lowest-fare comparison, sort the delivered observations and state any cap or completeness limit.

Rows come in two types. `flight`: `route`, `depart_date`, `return_date`, `trip`, `rank` (Google's own order, 1 = its top pick), `price` (total for all passengers), `currency`, `round_trip_total`, `airline`, `airlines`, `stops`, `depart_time`, `arrive_time`, `depart_day`, `arrive_day`, `depart_airport`, `arrive_airport`, `duration`, `duration_minutes`, `layovers` (airport, city, minutes), `layover_airports`, `overnight_layover`, `co2_kg`, `emissions_vs_typical`, `google_url`, `fetched_at`. `status`: one per route and date with `searches`, `flights`, `duplicates`, `cheapest`, `status` (`ok`, `no_results`, `error`) and `error`, never charged. A search with no itineraries is a `status` row with `no_results`, not a failed run; a search Google priced in another currency is a `status` row with an error and no billed rows. An input the actor cannot act on (a past date, a route that is not two airport codes, more than 9 passengers) ends the run with the reason on the run card and nothing charged.

### Three cheapest returned options within a hard budget

`maxResultsPerSearch: 3` means Google's first three ranked results. It does not identify the three lowest fares. For a family search, retrieve the parsed results with `0`, then sort delivered `flight` rows numerically by `price` and take three. The price includes all requested passengers; with a return date it is the round-trip quote, not a per-leg or per-person amount.

```json
{
  "actor": "kestrel/google-flights-prices",
  "input": {
    "routes": ["LIS-LHR"],
    "departDate": "2026-12-10",
    "returnDate": "2026-12-17",
    "adults": 2,
    "children": 2,
    "maxStops": "nonstop",
    "currency": "EUR",
    "maxResultsPerSearch": 0,
    "sweepDays": 0
  },
  "callOptions": {"maxTotalChargeUsd": 0.10, "timeout": 180},
  "waitSecs": 30
}
```

Use this envelope with `call-actor`; pass only `input` in the Actor editor. Poll a running call with `get-actor-run`, then read the default dataset with `get-dataset-items`. A $0.10 cap funds at most 20 delivered flight events at $0.005 each; status rows are free. If more itineraries are available, the spending cap can truncate Google's ordered results. Inspect `SUMMARY.limit_hit` and status errors. Report the cheapest among the delivered observations; neither a capped response nor Google's page guarantees the market's absolute cheapest bookable fare.

`status.cheapest` is computed from the rows actually delivered for that route/date, not from unseen or unpaid results. For `sweepDays: 6`, group by route, `depart_date`, `return_date`, passenger mix, cabin and currency before taking daily minima: seven departure days mean seven searches and a potentially larger bill. The return shifts by the same number of days. For adult-only one-row-per-day comparisons, use Flight Price Tracker; that Actor has no child/infant input.

Each run creates its own dataset. Persist the observations externally to build history. Repeat absolute dates to monitor a fixed trip; relative dates keep a constant lead time and change the trip on every run. Notifications require a separate schedule/webhook/integration.

## What does the Google Flights scraper do?

You give it routes and dates. It gives you every itinerary Google lists, as structured rows.

- **`flight` rows** — one per itinerary: `price` for all passengers, `airline` and `airlines`, `stops`, `depart_time` / `arrive_time` and the days they fall on, `duration` and `duration_minutes`, every `layover` (airport, city, minutes), `overnight_layover`, `co2_kg`, `emissions_vs_typical`, and `google_url` — the exact Google Flights link that reproduces the search.
- **`status` rows** — one per route and date: how many itineraries were delivered, the cheapest price found, and the reason if a search failed. Never charged.

Round trips are priced the way Google shows them: one row per itinerary, `price` is the **total for both legs**, and `round_trip_total` is `true`.

## Flight price tracking with data you own

Google's own price tracking emails you when a fare moves. It picks the routes, keeps the history and gives you no export. Scheduling this **flight price monitoring** run gives you the same signal as data you control:

- Every row is timestamped with `fetched_at`, so a price series falls out of the dataset with no extra work.
- Relative dates (`"30 days"`) mean a scheduled run never goes stale — it always looks the same distance ahead.
- Connect the run to n8n, Make or Zapier and raise a **flight price alert** on `price` below your threshold, or on a nonstop appearing under a number you would actually pay.

## Cheapest day to fly, in one run

`sweepDays` prices the same trip departing on each of the next N days. One run answers "when should I fly" as data rather than a chart you have to squint at — the **cheapest day to fly** for a route, with the airline and duration attached to each day's best fare.

A seven-day sweep on one route is seven searches. A month is 30.

## Google Flights API or scraper: how this compares

There is no public **google flights api**. Google retired the QPX Express API, and the alternatives split into two camps:

- **Aggregator APIs** (Amadeus, Duffel, Kiwi/Tequila) sell fares from their own inventory. Good for booking, but the numbers differ from what a shopper sees on Google, and most require a commercial agreement.
- **SERP resellers** (SerpApi, SearchApi, DataForSEO) resell a Google Flights endpoint per search. They work, and they charge per search whether or not it returned anything useful.

This actor reads Google Flights directly and bills per **delivered itinerary row**, so an empty route costs nothing. If you want a **flight search api** shape, run it through Apify's API and treat the dataset as the response — the "How to use it" section below has the exact calls.

## Input

| Field | What it does |
| --- | --- |
| `routes` | Routes as airport codes, one per line: `LIS-LHR`, `JFK-LAX`. Google's city codes work too — `NYC-LON` searches every New York and London airport. Written `LIS-LHR`, `lis > lhr` or `JFK to LAX`, all the same. |
| `departDate` | `2026-10-05`, or relative so schedules never go stale: `30 days`, `6 weeks`, `tomorrow`. Past dates are rejected rather than silently priced for another day. |
| `returnDate` | Empty for one-way. With a date, rows are round trips priced for both legs. |
| `sweepDays` | `0` = just that date. `N` = also each of the next N departure days; a return date shifts with it, keeping the trip length. |
| `seat` | `economy`, `premium_economy`, `business`, `first`. |
| `adults`, `children`, `infantsSeat`, `infantsLap` | Up to 9 passengers per search. Prices are the total for everyone travelling. |
| `maxStops` | `any`, `nonstop`, `one_or_fewer`, `two_or_fewer`. |
| `maxResultsPerSearch` | `0` = every itinerary Google lists (usually 10–35). `N` = the N top-ranked only — the cost cap. |
| `currency` | Any ISO code for every price, e.g. `USD`, `EUR`, `GBP`. |
| `market` | Two-letter country code for the Google market (`gl`). Fares and airlines differ by market. |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. Required — Google blocks datacentre traffic that is not rotated. |

### Example: cheapest departure day across a week, two routes

```json
{ "routes": ["LIS-LHR", "LIS-CDG"], "departDate": "30 days", "sweepDays": 6, "currency": "EUR", "market": "pt" }
```

### Example: a daily nonstop business-class check on one route

```json
{ "routes": ["JFK-LHR"], "departDate": "14 days", "returnDate": "21 days", "seat": "business", "maxStops": "nonstop" }
```

### Example: a family of four, one way, cost-capped

```json
{ "routes": ["LHR-JFK"], "departDate": "45 days", "adults": 2, "children": 2, "maxResultsPerSearch": 10 }
```

## Output

One `flight` row per itinerary:

```json
{
  "type": "flight", "route": "LIS-LHR", "depart_date": "2026-10-05", "return_date": null, "trip": "one_way",
  "seat": "economy", "adults": 1, "currency": "USD", "rank": 1,
  "price": 127, "price_display": "127 US dollars", "round_trip_total": false,
  "airline": "Tap Air Portugal", "airlines": ["Tap Air Portugal"], "stops": 0,
  "depart_time": "8:00 PM", "arrive_time": "10:55 PM", "depart_day": "Monday, October 5",
  "depart_airport": "Humberto Delgado Airport", "arrive_airport": "Heathrow Airport",
  "origin": "LIS", "destination": "LHR", "duration": "2 hr 55 min", "duration_minutes": 175,
  "layovers": null, "layover_airports": null, "overnight_layover": false,
  "co2_kg": 123, "emissions_vs_typical": -7, "max_stops": null,
  "google_url": "https://www.google.com/travel/flights?tfs=..."
}
```

A one-stop itinerary carries its connections:

```json
{
  "stops": 1, "duration_minutes": 785,
  "layovers": [{ "index": 1, "of": 1, "minutes": 550, "airport": "Aéroport de Paris-Charles de Gaulle", "city": "Paris" }],
  "layover_airports": ["Aéroport de Paris-Charles de Gaulle"]
}
```

`duration_minutes` exists so you can sort and filter without parsing `"13 hr 5 min"`, and `rank` preserves Google's own ordering — its top pick is 1. The `status` rows carry `searches`, `flights`, `duplicates`, `cheapest`, `status` and any `error` for each route and date, plus `trip`, `seat` and `currency` so a row always says what it was priced for.

## How much does it cost?

Pay per event, one event per **delivered** itinerary row. Searches that return nothing, `status` rows and failed searches are free, and the same itinerary is billed once per run even when two overlapping searches return it — `NYC-LON` and `JFK-LHR` will not bill the same flight twice. `maxResultsPerSearch` caps the first rows in Google's order. Sort delivered prices for a lowest-fare comparison; a cap may exclude a cheaper itinerary.

A single route and date is typically 10–35 rows. A 7-day sweep on 3 routes is about 21 searches — a few hundred rows. Apify platform usage for a run that size is a fraction of a cent; the verified runs behind this listing cost $0.0002–$0.0026 each in compute. Exact per-row pricing is on this page's pricing tab.

## How to use it from Python, JavaScript, curl, n8n, Make or an AI agent

Run it and read the dataset. In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/google-flights-prices").call(run_input={
    "routes": ["LIS-LHR"], "departDate": "30 days", "sweepDays": 6, "currency": "EUR",
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "flight":
        print(row["depart_date"], row["price"], row["airline"], row["stops"])
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/google-flights-prices').call({
    routes: ['JFK-LHR'], departDate: '14 days', seat: 'business', maxStops: 'nonstop',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'flight').map((i) => [i.price, i.airline]));
```

With **curl**, synchronously, getting the dataset straight back:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~google-flights-prices/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"routes":["LIS-LHR"],"departDate":"30 days","maxResultsPerSearch":10}'
```

For **n8n**, **Make** and Zapier, use Apify's integration: add the actor as a step, paste the same JSON as the input, and map `price`, `airline` and `depart_date` into your filter or alert. For **AI agents**, the actor is callable over Apify's MCP server, so an agent can ask for a route and dates and read the rows back without any glue code.

## Is it legal to scrape Google Flights prices?

This reads the same publicly available result page a visitor sees, with no login and no account, and it collects **no personal data** — an itinerary is a price, an airline and two timestamps. In the EU and the US, scraping public pages that contain no personal data is broadly accepted, and *hiQ v. LinkedIn* is the usual reference point for public data specifically.

That is not the whole story, and you should know the rest: Google's Terms of Service discourage automated access, so this is a terms question rather than a criminal one, and the risk sits with the operator of the run. Facts such as prices are not copyrightable, but a database can attract *sui generis* protection in the EU, so do not redistribute the raw dataset as a product. If you are unsure how any of this applies to your use, ask a lawyer — this is not legal advice.

## Limits and honest notes

- **Google's list is what you get.** This does not book, hold or price seats directly with airlines, and it does not see fares that only appear after login or in a corporate channel.
- **Results are read in English.** The parser reads Google's own English accessibility labels, which is why there is no language input. `currency` and `market` still control the fares themselves — those are the two that change prices.
- **Prices include what Google shows.** Taxes and carrier fees as Google presents them; baggage and seat fees are not in the number.
- **Round-trip prices are the trip total**, not per leg. `round_trip_total` marks them so you never mix the two.
- **A currency swap fails the run** rather than billing rows priced in something you did not ask for — some markets ignore `curr`.
- **Google renders every itinerary twice** on its own page. The run de-duplicates before billing, so you are never charged for its markup.

## FAQ

### Does it need a Google Flights API key or a Google account?

No. There is no public **google flights api** to hold a key for, and this uses none. No login, no cookies, no browser — it builds the same `tfs` query parameter Google puts in its own URLs and reads the page Google returns.

### Can I get flight price history from Google Flights?

Not retroactively — Google does not publish history, and neither can this. What you can do is *build* it: schedule a run daily with a relative `departDate`, and every row lands timestamped. Two weeks of that is two weeks of **flight price history** for your routes that is yours to keep.

### How do I find the cheapest day to fly?

Set `sweepDays`. `{"departDate": "30 days", "sweepDays": 29}` prices the same trip departing on each of the next 30 days; sort the `flight` rows by `price` and the answer is the top row. The `status` row for each date also carries `cheapest`, if you only want the daily minimum.

### Can I set a flight price alert?

Yes, outside the actor. Schedule the run, connect it to n8n, Make or Zapier through Apify's integrations, and fire when `price` drops below your threshold. Because you keep every row, your alert can be smarter than Google's — "nonstop under $400 on any of these three routes", for example.

### Does it support round trips and multi-city?

Round trips yes: set `returnDate` and every row prices both legs. Multi-city is not exposed as an input in this version — run each leg as its own one-way route if you need one.

### Which cabins and passenger mixes work?

`economy`, `premium_economy`, `business` and `first`, and up to nine passengers across adults, children, infants in a seat and infants on a lap. Business and first return a genuinely different, smaller market — in testing JFK–LHR economy started at $282 and business at $1,469 on the same day.

### Why do prices differ from what I see in my browser?

Three usual reasons: your `market` differs from your browser's country, your `currency` differs, or the fare simply moved — airline pricing changes through the day. Set `market` and `currency` explicitly and re-run to compare like for like; each row also carries the `google_url` that reproduces the exact search.

### How many itineraries does one search return?

Usually 10–35 for a route and date, which is what Google itself lists. `maxResultsPerSearch` can reduce the number delivered and billed, but takes Google's first ranked rows, not necessarily the cheapest. Sort the delivered rows and report any cap or incomplete coverage.

### Can I use it as an airfare scraper for Skyscanner or Kayak specifically?

No — it reads Google Flights. That said, Google aggregates most of the same carriers and online travel agents those sites do, so for **airfare price tracking** the numbers are usually comparable, and you get them from one source with one schedule.

### Is there a free tier?

Empty searches, failed searches and `status` rows are always free, so a run that finds nothing has no event charge; compute is included in the event price. Paid rows start only when an itinerary is actually delivered. Apify's free plan includes monthly platform credit you can spend here.

## Google Flights vs Skyscanner, Kayak and Momondo

People searching for a **skyscanner scraper** or a **kayak scraper** usually want the same thing: **cheap flights** on a route, as data. Those meta-search sites and Google Flights draw on largely the same carriers and online travel agents, so for tracking purposes the numbers move together.

Where they differ is access. Skyscanner's public data is behind an approval process, Kayak's affiliate feed is partner-only, and both are aggressive about automated traffic. Google Flights is the one surface that renders a complete, comparable result set to an ordinary request — which is why this is a **google flights data** source rather than a Skyscanner one.

If you need a **flight data api** shape rather than a dataset, call the actor through Apify's API synchronously (the curl example above) and treat the returned rows as your response body. You get a **flight search api** without operating a scraper yourself, and a **flight scraper without api key** in the sense that matters: there is no key to apply for, because there is no public Google Flights API to hold one for.

### Round trip, nonstop and premium fares

- **Round trip flight prices** come back as one row per itinerary with the trip total in `price` and `round_trip_total: true` — set `returnDate` and every row prices both legs.
- **Nonstop flight search** is `maxStops: "nonstop"`. This was verified live: JFK–LAX with the filter returned 31 itineraries, every one of them nonstop.
- **Business class fares** and first are a different, smaller market. Set `seat` and compare — do not assume a fixed multiple of economy.

### Multi-city trips

There is no **multi city flight scraper** mode in this version. Google's own multi-city builder takes an arbitrary list of legs, and exposing that safely needs a different input shape than routes plus dates. Until it exists, run each leg as its own one-way route and join the rows on your side — the per-leg prices are the same ones Google would use to build the itinerary.

### Is there a free Google Flights API?

No. People searching **google flights api free** are usually finding either the retired QPX Express service, an unofficial GitHub wrapper that breaks whenever Google changes its page, or a SERP reseller with a small free tier. This actor is the third option's shape without the per-search billing: you pay for delivered itinerary rows, and a route that returns nothing costs nothing.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Business Class Fares from Google Flights](https://apify.com/kestrel/google-flights-prices/examples/business-class-fares)
- [Cheapest Day to Fly: 14-Day Calendar](https://apify.com/kestrel/google-flights-prices/examples/cheapest-day-to-fly-calendar)
- [Google Flights API Free Alternative](https://apify.com/kestrel/google-flights-prices/examples/google-flights-api-alternative)
- [Nonstop Flight Search on One Route](https://apify.com/kestrel/google-flights-prices/examples/nonstop-flight-search-on-one-route)
- [Flight Prices for a Family of Four](https://apify.com/kestrel/google-flights-prices/examples/flight-prices-for-a-family-of-four)
- [Scrape Google Flights for 5 One-Way Routes](https://apify.com/kestrel/google-flights-prices/examples/scrape-google-flights-for-5-one-way-routes)
- [Airline Ticket Prices in Premium Economy](https://apify.com/kestrel/google-flights-prices/examples/airline-ticket-prices-in-premium-economy)
- [Google Flights Data for the German Market](https://apify.com/kestrel/google-flights-prices/examples/google-flights-data-for-the-german-market)
- [Flight Data API: Who Flies a Route](https://apify.com/kestrel/google-flights-prices/examples/flight-data-api-who-flies-a-route)
- [Cheap Flights from Three London Airports](https://apify.com/kestrel/google-flights-prices/examples/cheap-flights-from-three-london-airports)
- [Flight Price Monitoring on a Schedule](https://apify.com/kestrel/google-flights-prices/examples/flight-price-monitoring-on-a-schedule)

## Related scrapers

Flights are one side of a trip. These read the rest of it, and they share the same row shape, the same pay-per-delivered-row billing and the same scheduling story:

- **[Flight Price Tracker](https://apify.com/kestrel/flight-price-tracker)** — only want the cheapest fare per day, cheap enough to run every morning? It runs the same engine and bills one row per route and departure day, with a `maxPrice` alert line that filters before billing.
- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site’s rate for a stay.
- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — Airbnb prices, availability calendars and occupancy.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing, with translations.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
