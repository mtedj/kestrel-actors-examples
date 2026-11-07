# Flight Price Tracker — Cheapest Day to Fly & Airfare Alerts

A **flight price tracker** that reads Google Flights and returns the cheapest fare for every departure day in your window — one row per route and day, with the airline, stops, times and duration behind that price. Run it once to see the **cheapest day to fly**; schedule it and you have **airfare price tracking** you own, with a `maxPrice` line that turns any run into a **flight price alert**. No API key, no login, no browser.

It is a different product from an itinerary scraper. An itinerary scraper bills every fare Google lists for a day (usually 10–35). This bills **one row per day**, so a 30-day window on a route is 30 rows — cheap enough to run every morning.

Last verified working: 2026-10-19.

## 机票价格追踪、便宜机票与降价筛选：中文调用与语言设置

按航线扫描多个出发日期，返回每个日期的最低可见票价。maxPrice 仅筛选低于阈值的结果；每日定时运行和通知由外部工作流安排。

market 表示搜索者市场，currency 单独选择币种。没有 language 输入，结果按英文读取；历史需要自行保存每次运行的快照。

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
  "days": 1,
  "currency": "EUR",
  "market": "pt",
  "sessions": 1
}
```

Vuelos baratos / günstige Flüge：比较相同市场、舱位和乘客条件。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## Google Flights price tracker for AI agents: which input answers which request?

Use it when the user wants the cheapest fare per departure day on a route: the cheapest day to fly in a window, cheapest flights by date, a fare line to watch (`maxPrice`), or a daily schedule that builds flight price history. One row per route and day is the whole output. Do not use it when the user wants every itinerary of a day (airline comparison, the second-cheapest option, children or infants in the party): use [Google Flights Scraper](https://apify.com/kestrel/google-flights-prices), which bills per itinerary. It does not send notifications itself (connect the run to n8n, Make, Zapier or an Apify webhook), does not diff against the previous run, and reads what Google Flights lists, in English.

| The user asks for | Input |
|---|---|
| Cheapest day to fly LIS-LHR in the next two weeks | `{"routes": ["LIS-LHR"], "departDate": "tomorrow", "days": 14}` |
| A month of fares, a price calendar | `"days": 30` |
| Cheapest week-long round trip | add `"tripLengthDays": 7` (`price` = both legs, `round_trip_total: true`) |
| Cheapest nonstop per day | add `"maxStops": "nonstop"` |
| Business class | add `"seat": "business"` |
| Two adults | add `"adults": 2` (`price` is the total for both) |
| Alert me when it drops under 400 | add `"maxPrice": 400` and schedule the run: only days at or under 400 come back, and nothing is billed otherwise |
| Prices in euros as seen from Portugal | add `"currency": "EUR", "market": "pt"` |
| Track daily, build price history | `"departDate": "30 days"` with an Apify schedule: every run prices the next `days` days from 30 days out |
| Several routes | `"routes": ["JFK-LHR", "EWR-LHR"]` (each gets its own ranking and `status` row) |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `days` × routes bounds the rows |

`days` decides the bill: one search and at most one billed row per route and day (default 14). `maxPrice` filters before billing and the `status` row still reports the window's `cheapest` and `cheapest_date`, so an alert run that finds nothing costs nothing and still says how far off the line the market is.

Rows come in two types. `fare`: `route`, `depart_date`, `return_date`, `trip`, `price` (total for all adults), `currency`, `round_trip_total`, `airline`, `airlines`, `stops`, `depart_time`, `arrive_time`, `duration`, `duration_minutes`, `layovers`, `layover_airports`, `overnight_layover`, `co2_kg`, `google_url`, `itineraries_seen` (how many fares Google listed that day), `rank_in_window` (1 = the cheapest day of the window for that route; ties go to the earlier day) and `cheapest_in_window` (`true` on exactly one day per route), plus `fetched_at`. `status`: one per route with `days_searched`, `fares`, `filtered`, `no_results`, `errors`, `cheapest`, `cheapest_date`, `status` (`ok`, `no_results`, `error`) and `error`, never charged. A day Google lists nothing for is counted in `no_results`, not a failed run; a day priced in another currency counts as an error and is not billed. An input the actor cannot act on (a past date, a route that is not two airport codes) ends the run with the reason on the run card and nothing charged.

## What does the flight price tracker do?

You give it routes, a first departure day and a window length. For each route it searches every day in the window, keeps the cheapest itinerary of each day, ranks the days, and delivers:

- **`fare` rows** — one per route and departure day: `price` for all passengers, `airline` and `airlines`, `stops`, `depart_time` / `arrive_time`, `duration` and `duration_minutes`, every `layover`, `co2_kg`, the `google_url` that reproduces the search, `itineraries_seen` (how many fares Google listed that day), and two ranking fields: `rank_in_window` (1 = the cheapest day of the window) and `cheapest_in_window` (`true` on exactly one day per route).
- **`status` rows** — one per route: `days_searched`, `fares` delivered, `filtered` (days over `maxPrice`), `no_results`, `errors`, the window's `cheapest` fare and its `cheapest_date`. Never charged.

Round trips are priced the way Google shows them: set `tripLengthDays` and every day becomes a round trip returning that many days later, with `price` as the **total for both legs** and `round_trip_total: true`.

## Cheapest day to fly, one row per day

The question most people bring to Google Flights is not "what is the fare" but "which day should I leave". Google answers it with a calendar you have to read by eye. This answers it as data: the `fare` row with `cheapest_in_window: true` is the day, and `rank_in_window` orders the rest — so "the three cheapest departures in October" is a filter on one column, not a spreadsheet exercise.

A seven-day window on one route is seven searches and at most seven rows. A month is 30. Two routes over a month is 60 rows, and the two `status` rows tell you which route and day won overall. Sort by `price`, or by `depart_date` to see the shape of the month; every row also says what it beat, in `itineraries_seen`.

The ranking is computed over the whole window **before** any `maxPrice` filter, so a filtered run still tells you that the day you kept was, say, the second-cheapest of the month.

## Airfare price tracking on a schedule

Google's own tracker emails you when a fare moves, on the routes and dates it chooses, and keeps the history to itself. Scheduling this run gives you the same signal as rows you keep:

- Every row carries `fetched_at`, so a **flight price history** for your routes falls out of the dataset — one series per route and departure day, growing by one point per run.
- Relative dates (`"30 days"`, `"6 weeks"`) mean a scheduled run always looks the same distance ahead. It never goes stale, and it never prices a day that has passed.
- The window moves with the calendar, so yesterday's rank 1 can be compared with today's: that is **flight price monitoring** for a route, not a one-off snapshot.
- The `status` rows give you a one-line summary per route per run — `cheapest` and `cheapest_date` — which is usually all a daily message needs.

At one row per day, the arithmetic of tracking is simple: a daily run on three routes over a 30-day window is 90 rows a day, about 2,700 a month. The price per row is on this page's pricing tab; the compute behind a run that size is a fraction of a cent.

## Flight price alerts: maxPrice filters before billing

Set `maxPrice` and the run delivers only the days whose cheapest fare is at or under that number. Days over the line are dropped **before** billing — an alert run that finds nothing costs nothing, and the `status` row still tells you how many days were `filtered` and what the window's `cheapest` was, so you can see how far off the line you are.

That makes a **flight price drop alert** a two-node automation: schedule the run with `maxPrice`, and send a message when the dataset has any `fare` row. You do not need to store the previous price or diff anything — the filter is the comparison. Because you keep every row, the alert can be smarter than Google's: "nonstop under 400 on any of these three routes, any day next month" is one input.

```json
{ "routes": ["JFK-LHR", "EWR-LHR"], "departDate": "14 days", "days": 30, "maxStops": "nonstop", "maxPrice": 400, "currency": "USD" }
```

Nothing under 400? Zero fare rows, zero charge, two `status` rows with the real minimum in `cheapest`.

## Google Flights price tracker vs this actor

Google's tracker, Hopper, Kayak alerts and the airline apps all do one thing well: tell *you* when *their* pick of dates moves. What none of them gives you is the table — every day, with the fare and the itinerary behind it, in a format you can join, chart, or feed to an automation. The comparison in practice:

| | Google's price tracking | This actor |
| --- | --- | --- |
| Which days | The dates you saved, or Google's suggestion | Every day of a window you set, 1–60 days |
| Output | An email | A dataset row per day: price, airline, stops, times, rank |
| History | Google keeps it | You keep it — `fetched_at` on every row |
| Alert condition | Google decides what counts as a drop | Your `maxPrice`, per route, with stops and cabin filters |
| Integration | None | Apify API, n8n, Make, Zapier, MCP for AI agents |
| Cost | Free, unexportable | Per delivered row, nothing for empty or filtered days |

If what you want is **cheap flights** on a route as a one-off, Google's page is fine. If you want to **track flight prices** across dates over weeks, feed them to a sheet or a bot, or watch a line and act when a fare crosses it, that needs rows, and rows are what this returns.

## Input

| Field | What it does |
| --- | --- |
| `routes` | Routes as airport codes, one per line: `LIS-LHR`, `JFK-LAX`. Google's city codes work too — `NYC-LON` searches every New York and London airport. Written `LIS-LHR`, `lis > lhr` or `JFK to LAX`, all the same. |
| `departDate` | The first day of the window: `2026-10-05`, or relative so schedules never go stale: `30 days`, `6 weeks`, `tomorrow`. Past dates are rejected. |
| `days` | How many consecutive departure days to price, 1–60. One search and at most one billed row per day. Default 14. |
| `tripLengthDays` | `0` = one-way. `N` = every day is a round trip returning N days after departure, priced for both legs. |
| `seat` | `economy`, `premium_economy`, `business`, `first`. |
| `adults` | Up to 9. Prices are the total for everyone travelling. |
| `maxStops` | `any`, `nonstop`, `one_or_fewer`, `two_or_fewer` — applied before picking the day's cheapest fare. |
| `maxPrice` | `0` = deliver every day. `N` = deliver only days at or under N in `currency`; the rest are dropped before billing. |
| `currency` | Any ISO code for every price, e.g. `USD`, `EUR`, `GBP`. |
| `market` | Two-letter country code for the Google market (`gl`). Fares and airlines differ by market. |
| `sessions`, `perIp` | Parallel proxy sessions and the pace of each. Leave alone unless a run is throttled. |
| `proxyConfiguration` | Apify Proxy. Required — Google blocks datacentre traffic that is not rotated. |

### Example: the cheapest day to fly in the next month, two routes

```json
{ "routes": ["LIS-LHR", "LIS-CDG"], "departDate": "tomorrow", "days": 30, "currency": "EUR", "market": "pt" }
```

### Example: a daily nonstop business-class watch, week-long round trips

```json
{ "routes": ["JFK-LHR"], "departDate": "14 days", "days": 21, "tripLengthDays": 7, "seat": "business", "maxStops": "nonstop" }
```

### Example: an alert line for a family of four

```json
{ "routes": ["LHR-JFK"], "departDate": "45 days", "days": 14, "adults": 4, "maxPrice": 1800, "currency": "GBP", "market": "gb" }
```

## Output

One `fare` row per route and day:

```json
{
  "type": "fare", "route": "LIS-LHR", "origin": "LIS", "destination": "LHR", "trip": "one_way",
  "depart_date": "2026-10-05", "return_date": null, "seat": "economy", "adults": 1, "currency": "USD",
  "price": 127, "price_display": "127 US dollars", "round_trip_total": false,
  "airline": "Tap Air Portugal", "airlines": ["Tap Air Portugal"], "stops": 0,
  "depart_time": "8:00 PM", "arrive_time": "10:55 PM", "depart_day": "Monday, October 5", "arrive_day": "Monday, October 5",
  "duration": "2 hr 55 min", "duration_minutes": 175,
  "layovers": null, "layover_airports": null, "overnight_layover": false, "co2_kg": 123,
  "google_url": "https://www.google.com/travel/flights?tfs=...",
  "itineraries_seen": 12, "cheapest_in_window": true, "rank_in_window": 1,
  "fetched_at": "2026-08-29T06:25:14+00:00"
}
```

A day whose cheapest fare has a connection carries it:

```json
{
  "stops": 1, "duration_minutes": 785,
  "layovers": [{ "index": 1, "of": 1, "minutes": 550, "airport": "Aéroport de Paris-Charles de Gaulle", "city": "Paris" }],
  "layover_airports": ["Aéroport de Paris-Charles de Gaulle"]
}
```

And one `status` row per route:

```json
{
  "type": "status", "route": "LIS-LHR", "trip": "one_way", "seat": "economy", "currency": "USD",
  "depart_date": "2026-10-05", "return_date": null,
  "days_searched": 7, "fares": 7, "filtered": 0, "no_results": 0, "errors": 0,
  "cheapest": 127, "cheapest_date": "2026-10-05", "status": "ok", "error": null,
  "fetched_at": "2026-08-29T06:25:20+00:00"
}
```

`duration_minutes` exists so you can sort without parsing `"13 hr 5 min"`; `rank_in_window` and `cheapest_in_window` exist so you never have to compute the minimum yourself. The dataset has three views in the Console — *Overview*, *Cheapest fare by day* and *Run status* — and exports to CSV, Excel or JSON.

## How much does it cost?

Pay per event, one event per **delivered** `fare` row — at most one per route and departure day. Days on which Google lists nothing, days dropped by `maxPrice`, failed days and `status` rows are free, and nothing a spending limit refused is ever delivered.

Some worked sizes at the listed per-row price:

- One route, 7 days: 7 rows.
- One route, 30 days: 30 rows.
- Three routes, 30 days, daily for a month: 90 rows a run, about 2,700 a month.
- An alert run with `maxPrice` that finds nothing: 0 rows, $0 charged; compute and proxy are included in the event price.

The verified runs behind this listing used $0.0002–$0.003 of platform compute each. Exact per-row pricing is on this page's pricing tab.

## How to use it from Python, JavaScript, curl, n8n, Make or an AI agent

Run it and read the dataset. In **Python**:

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("kestrel/flight-price-tracker").call(run_input={
    "routes": ["LIS-LHR"], "departDate": "30 days", "days": 14, "currency": "EUR",
})
for row in client.dataset(run["defaultDatasetId"]).iterate_items():
    if row["type"] == "fare":
        print(row["rank_in_window"], row["depart_date"], row["price"], row["airline"], row["stops"])
```

In **JavaScript** (Node):

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/flight-price-tracker').call({
    routes: ['JFK-LHR'], departDate: '14 days', days: 21, tripLengthDays: 7, maxStops: 'nonstop',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const best = items.find((i) => i.type === 'fare' && i.cheapest_in_window);
console.log(best.depart_date, best.price, best.airline);
```

With **curl**, synchronously, getting the dataset straight back:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~flight-price-tracker/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"routes":["LIS-LHR"],"departDate":"30 days","days":7,"maxPrice":150,"currency":"EUR"}'
```

For **n8n** and **Make** (and Zapier), the whole alert is three steps: a Schedule trigger, an HTTP Request to the `run-sync-get-dataset-items` URL above with the JSON body, and a message step that fires when the returned array has any row with `type: "fare"`. With `maxPrice` set, an empty array means "nothing under the line today". Map `depart_date`, `price`, `airline` and `google_url` into the message and the recipient can book from it.

For **AI agents**, the actor is callable over Apify's MCP server, so an agent asked "when is it cheapest to fly Lisbon to London next month" can run it and read the `cheapest_in_window` row back with no glue code.

## Is it legal to track prices from Google Flights?

This reads the same public result page a visitor sees, with no login and no account, and it collects **no personal data** — a fare is a price, an airline and two timestamps. In the EU and the US, reading public pages that contain no personal data is broadly accepted, and *hiQ v. LinkedIn* is the usual reference point for public data specifically.

That is not the whole story: Google's Terms of Service discourage automated access, so this is a terms question rather than a criminal one, and the responsibility sits with the operator of the run. Prices are facts and facts are not copyrightable, but a database can attract *sui generis* protection in the EU, so do not redistribute the raw dataset as a product. If you are unsure how any of this applies to your use, ask a lawyer — this is not legal advice.

## Limits and honest notes

- **One row per day means one itinerary per day.** The row is the cheapest fare Google lists for that day under your cabin and stop filters. If you need every itinerary — to compare airlines on the same day, or to see the second-cheapest option — use the [Google Flights Scraper](https://apify.com/kestrel/google-flights-prices), which bills per itinerary instead.
- **Google's list is what you get.** Fares visible only after login, in corporate channels or on airline sites Google does not index are not in it.
- **Results are read in English.** The parser reads Google's English accessibility labels, which is why there is no language input; `currency` and `market` are the two inputs that change the fares themselves.
- **Prices include what Google shows** — taxes and carrier fees as Google presents them. Baggage and seat fees are not in the number.
- **A currency swap is an error, not a row.** Some markets ignore the requested currency; a day priced in another one is reported in `status` rather than billed.
- **The window is capped at 60 days** per run. For a longer horizon, run twice with different `departDate` values.
- **Ties go to the earlier day.** When two days share the lowest fare, the earlier departure takes rank 1.

## FAQ

### Does it need a Google Flights API key?

No. There is no public Google Flights API to hold a key for, and this uses none. No login, no cookies, no browser — it builds the same `tfs` query parameter Google puts in its own URLs and reads the page Google returns. If you want a **flight price tracking api** shape, call it synchronously through Apify's API (the curl example above) and treat the rows as the response.

### How do I find the cheapest day to fly on Google Flights?

Set `departDate` to the first day you could leave and `days` to how far you are flexible. The `fare` row with `cheapest_in_window: true` is the answer; `rank_in_window` orders the alternatives. The `status` row repeats it as `cheapest` and `cheapest_date` if you only want the headline. That is the **cheapest day to fly google flights** search, as one input and one column.

### Can I get flight price history?

Not retroactively — Google does not publish history, and neither can this. What you can do is *build* it: schedule a daily run with a relative `departDate`, and every row lands with `fetched_at`. Two weeks of that is two weeks of history per route and departure day that is yours to keep and chart — a **flight price calendar** over time, not just across dates.

### How do I set up Google Flights price alerts with it?

Set `maxPrice`, schedule the run, and send a message whenever the dataset contains a `fare` row. Because filtering happens before billing, a quiet day costs nothing. **Google flights price alerts** in their native form only cover the dates you saved; this covers every day of the window and any stop or cabin filter you set.

### Does it do round trips?

Yes. `tripLengthDays: 7` prices every day of the window as a week-long round trip; `price` is the total for both legs and `round_trip_total` is `true`. **Round trip flight prices** across a window are how most leisure searches actually look, and that is one input here.

### What about nonstop-only, or business class?

`maxStops: "nonstop"` restricts every day's search to nonstop itineraries before the cheapest is picked, so the row is the cheapest *nonstop* that day — a **nonstop flight search** per day rather than one that a cheap connection would otherwise win. `seat: "business"` prices **business class fares** the same way; expect a different, smaller market than economy rather than a fixed multiple of it.

### Why do prices differ from what I see in my browser?

Three usual reasons: your `market` differs from your browser's country, your `currency` differs, or the fare moved — airline pricing changes through the day. Set `market` and `currency` explicitly and re-run to compare like for like; each row carries the `google_url` that reproduces the exact search.

### How many routes and days can one run track?

Up to 60 days per route, any number of routes; each route is searched in parallel across `sessions`. A 30-day window on five routes is 150 searches and, with no filter, 150 rows. Larger horizons are two runs with different `departDate` values.

### Is it a scraper for Skyscanner or Kayak?

No — it reads Google Flights. Those sites and Google draw on largely the same carriers and online travel agents, so for **airline ticket prices** on a route the numbers move together and you get them from one source on one schedule. For the full itinerary list from the same source, the **google flights scraper** linked below is the sibling listing.

### Is there a free tier?

Empty days, filtered days, failed days and `status` rows are always free, and Apify's free plan includes monthly platform credit you can spend on the paid rows. A run that finds nothing under your `maxPrice` has no event charge; compute and proxy are included in the event price.

## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Cheapest Day to Fly in a 30-Day Window](https://apify.com/kestrel/flight-price-tracker/examples/cheapest-day-to-fly)
- [Price Drop Alert Under a Cap](https://apify.com/kestrel/flight-price-tracker/examples/flight-price-drop-alert)
- [Price History on a Daily Schedule](https://apify.com/kestrel/flight-price-tracker/examples/flight-price-history)
- [Price Calendar, 60 Days of Fares](https://apify.com/kestrel/flight-price-tracker/examples/flight-price-calendar-60-days-of-fares)
- [Nonstop Search Across a Month](https://apify.com/kestrel/flight-price-tracker/examples/nonstop-flight-search-across-a-month)
- [Business Class Fares by Departure Date](https://apify.com/kestrel/flight-price-tracker/examples/business-class-fares-by-departure-date)
- [Track Prices for Five Routes](https://apify.com/kestrel/flight-price-tracker/examples/track-flight-prices-for-five-routes)
- [Airline Ticket Prices for Four Adults](https://apify.com/kestrel/flight-price-tracker/examples/airline-ticket-prices-for-four-adults)
- [Airfare Price Tracking in the Indian Market](https://apify.com/kestrel/flight-price-tracker/examples/airfare-price-tracking-in-the-indian-market)
- [Cheapest Flights by Date for a Weekend](https://apify.com/kestrel/flight-price-tracker/examples/cheapest-flights-by-date-for-a-weekend)
- [Google Flights Price Tracker by Airport](https://apify.com/kestrel/flight-price-tracker/examples/google-flights-price-tracker-by-airport)

## Related scrapers

Need every itinerary, not just the cheapest? The **[Google Flights Scraper](https://apify.com/kestrel/google-flights-prices)** is the same engine billing per itinerary row — use it when you want to compare airlines and times on the same day; use this one when you want the **cheapest flights by date** across a window.

The rest of the trip, from the same publisher, with the same pay-per-delivered-row billing:

- **[Google Hotels Prices Scraper](https://apify.com/kestrel/google-hotels-prices)** — hotel prices and every booking site's rate for a stay, for the same dates you just priced the fare for.
- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — Airbnb prices, availability calendars and occupancy.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
