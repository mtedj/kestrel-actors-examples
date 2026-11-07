# Google Hotels Prices Scraper & API - OTA Rates, Hotel Details

Google Hotels prices scraper for exact dates and guests: the lowest nightly rate and the stay total for every hotel in a search, then every booking site's rate for each hotel — Booking.com, Expedia, Agoda, Hotels.com, Trip.com and the hotel's official site — with free-cancellation flags and deep links. Run it once for a price check, on a schedule for hotel price tracking and rate parity, or with a date sweep to build a price calendar and your own hotel price history. No Google API key, no login, no browser: it reads the same public Google Hotels results any visitor sees, through Apify's proxies, and returns clean JSON.

**You pay only for priced rows.** Sold-out hotels, empty searches and status rows cost nothing, and the price per row is stated on this page and identical on every plan.

## Google 酒店价格、酒店比价与 OTA 房价：中文调用与语言设置

查询城市或具体酒店的指定入住日期，获得酒店价格、税费与可订状态。需要多渠道比价时开启 includeOffers；只需要酒店行时关闭，避免多余的报价行费用。

language 设置显示语言；country 是搜索者市场，不是酒店所在地；currency 独立设置币种。中文界面示例 language="zh-CN"；不要因为目的地在中国就自动改变搜索市场。

| 调用需求 | 参数与结果约定 |
|---|---|
| 小规模验证 | 使用下面 JSON；先检查结果和状态，再提高上限 |
| 语言与市场 | 按上面的真实字段选择，不要把中文说明当成自动翻译承诺 |
| 费用控制 | maxTotalChargeUsd 是 Apify 运行选项，不是输入 JSON 字段；按定价页的计费事件设置上限 |
| 数据完整性 | 检查状态行和 SUMMARY；空结果、来源错误与完整数据集是不同情况 |

```json
{
  "queries": [
    "hotels in Lisbon"
  ],
  "checkIn": "30 days",
  "checkOut": "32 days",
  "adults": 2,
  "currency": "USD",
  "maxHotels": 1,
  "includeOffers": false,
  "offerLevel": "sources",
  "sweepDays": 1,
  "language": "zh-CN",
  "includeDetails": false,
  "sessions": 1
}
```

Hotelpreise / prix des hôtels / precios de hoteles：使用同一组日期、人数和币种比较价格。

This localized quick start uses the existing input contract. API users should send the JSON as actor input and set `maxTotalChargeUsd` separately in Apify run options. Source coverage and translation depend on the platform, not the language of this guide.

## What does Google Hotels Prices Scraper do?

Google Hotels is a metasearch engine: for a hotel and a stay it shows the rates of every booking site it knows and the hotel's own site. This scraper reads that comparison for the dates, occupancy, currency and market you choose and turns it into three kinds of rows:

- **`hotel` rows** — up to 200 hotels per place search (Google's results, paged) or exactly the properties you list: lowest nightly rate, stay total, deal note ("19% less than usual"), star class, rating and review count, coordinates, website, Google Maps link and the Google Hotels entity id.
- **`offer` rows** — for every priced hotel, each booking source's rate: nightly, total for the stay, free-cancellation flag and deadline, the source's link, and for official sites the booking-engine URL with your dates already filled in. Optionally every room type and rate.
- **`status` rows** — one per place or property and stay: how many hotels, how many priced, how many offers, any error. Never charged.

It is the data behind a Google Hotels price tracker, a hotel price monitoring workflow, a rate shopping tool or a rate parity check — without the SaaS subscription, and with the raw hotel price data in your own dataset.

## Google Hotels scraper for AI agents: which input answers which request?

Use it when the user wants hotel prices from Google Hotels for given dates: a city or area, a named hotel, or a list of hotels; one price per hotel or every booking site's rate; once or on a schedule. Do not use it for review text (it returns rating, review count, rating breakdown and review topics, not reviews), for flights, for stays of more than 6 adults or more than one room, or for a rate straight from one booking site's own pages: every rate is the one Google Hotels lists.

| The user asks for | Input |
|---|---|
| Hotel prices in a city for dates | `{"queries": ["hotels in Lisbon"], "checkIn": "2026-10-10", "checkOut": "2026-10-13", "includeOffers": false}` |
| The 30 cheapest 4-star and 5-star hotels | add `"maxHotels": 30, "sortBy": "lowest_price", "hotelClass": ["4", "5"]` |
| Pool, free cancellation, under 250 a night, rated 4.5+ | add `"amenities": ["pool"], "freeCancellation": true, "maxPrice": 250, "minRating": "4.5"` |
| Address, phone, amenities, photos of each hotel | add `"includeDetails": true` (no extra charge) |
| What each booking site charges for a named hotel, rate parity | `{"hotelNames": ["Hyatt Regency Lisbon"], "checkIn": "…", "checkOut": "…"}` (`includeOffers` is already true) |
| Every room type with its cancellation deadline | add `"offerLevel": "rooms"` |
| Which check-in day is cheapest, a price calendar | `"sweepDays": 13` with `"includeOffers": false` |
| Track prices daily without editing the input | `"checkIn": "30 days", "checkOut": "32 days"` and an Apify schedule |
| The same hotels every day | pass the `entity_id` values of a first run in `hotels` |
| Prices as a user in Japan sees them, names in Japanese | `"country": "jp", "language": "ja", "currency": "JPY"` |
| A family | `"adults": 2, "childrenAges": [5, 9]` |
| A spending limit | the Apify run option `maxTotalChargeUsd`; `maxHotels` and `maxOffersPerHotel` bound the rows |

`includeOffers` defaults to `true`, and it is where the bill is decided: a hotel row alone is one event, a hotel with every booking site's rate is about 19 (measured on 174 hotels: 18 offer rows on average, 4 to 36). Set it `false` whenever the user asks for one price per hotel. With `false` the hotel row still carries the lowest nightly rate, but not which site sells it: that is in the offer rows.

Rows come in three types. `hotel`: `name`, `nightly`, `total`, `total_base`, `taxes`, `fees`, `total_with_taxes`, `deal`, `stars`, `rating`, `reviews`, `lat`, `lng`, `entity_id`, `google_url`. `offer`: `source`, `official` (true for the hotel's own site, present only when Google lists it), `nightly`, `total`, `free_cancel`, `free_cancel_until`, `link`, and with `offerLevel: "rooms"` also `room` and `max_guests`. `status`: one per place or hotel and stay with `hotels`, `priced`, `offers`, `spread_km` and `error`, never charged. An empty result is a `status` row that says why, not a failed run. The actor returns rows, not conclusions: "which day is cheapest" is a group-by on `check_in` over the hotel rows.

## Google Hotels price tracking with your own data

Google's built-in hotel price tracking emails you when a price moves, but it picks the sources, keeps the history and gives you no export. Scheduling this scraper gives you the same signal as data you own:

- **Track a city or a shortlist daily.** Schedule the run (Apify Console → Schedules, or the API) with relative dates such as `"checkIn": "30 days", "checkOut": "32 days"`: every run prices the stay 30 days out, forever. Each run appends rows with `fetched_at`, so the dataset becomes your hotel price history.
- **Price alerts.** A Google Hotels price alert you control: connect the run to n8n, Make or Zapier through Apify's integrations and alert on `nightly` below a threshold, or on a specific `source` dropping below the official site.
- **Rate calendars.** `sweepDays: 6` prices the same length of stay for each of the next seven check-in days in one run — a price calendar per hotel, or "which weekend is cheapest".

Google Hotels' own price history and price alerts stay inside Google; this is how you get the numbers out.

## Rate parity and rate shopping for hotels

For revenue managers the `offer` rows are the point. One run answers, per property and stay: what is the official site charging, what is every OTA charging, which rate is refundable until when, and what is each source's stay total. That is a rate parity check across every channel Google lists, at the price of a few cents per hotel.

- Put your properties and your competitive set in `hotels` (Google Hotels URLs — find them on google.com/travel/hotels — or the `entity_id` from an earlier run). No search is needed: one offers call per property and stay.
- Use `offerLevel: "sources"` (default) for one row per source with its lowest rate — the rate shopping view — or `offerLevel: "rooms"` for every room type and rate.
- Sources are keyed by `source_id`, and the property's own listing carries `official: true`, so a parity breach is a one-line comparison: any row where `official` is false and `nightly` is below the official row.

The same rows serve a hotel competitor rate shopping tool, hotel price intelligence dashboards, OTA rate comparison and channel-manager checks.

## Input

| Field | Meaning |
|---|---|
| `queries` | Free-text places exactly as you would type them into Google Hotels: `"hotels in Lisbon"`, `"hotels near Times Square"`, `"5-star hotels Bangkok Sukhumvit"`. Google's results are paged 20 at a time; the scraper pages on until `maxHotels` distinct hotels. |
| `hotels` | Specific properties without a search: Google Hotels URLs (`…/travel/hotels/entity/ChkI…`) or entity tokens from an earlier run. One offers call per property and stay. |
| `hotelNames` | Specific properties by name: `"Hyatt Regency Lisbon"` (add the city), or a Google Maps place link. One lookup per name and run; a name nothing matches costs nothing and is reported in its `status` row, and only a property whose name matches yours is billed. These rows also carry star class, rating, reviews and coordinates. |
| `checkIn`, `checkOut` | `YYYY-MM-DD`, or relative to the run date for schedules: `"30 days"`, `"6 weeks"`, `"+30d"`, `today`, `tomorrow`. Nights = the difference. Past check-ins are rejected before anything is fetched. |
| `sweepDays` | Also price the same length of stay starting on each of the next N days (rate calendars). |
| `adults`, `childrenAges` | Occupancy per room; prices scale exactly as on Google. Up to 6 adults: Google Hotels prices no stay for a larger party (asked for 7 or more it returns no price and no booking site at all), so a scraper that accepts more can only return empty rows. |
| `currency`, `language`, `country` | Any ISO currency for every price; Google UI language (`hl`); market (`gl`) — prices and available sources differ by market. |
| `maxHotels` | Distinct hotels per place and stay, up to 200 (one list call per 20). |
| `sortBy` | Google Hotels' own sort for place searches: `relevance` (default), `lowest_price`, `highest_rating`, `most_reviewed`. With `maxHotels: 50` that is the 50 cheapest or the 50 best-rated hotels of a city. Google sorts prices on the basis of the country the request comes from — the pre-tax `total_base` from a US IP, the all-in `total_with_taxes` elsewhere — so re-sort on the field you compare on. |
| `freeCancellation` | Only hotels with a free-cancellation rate for your dates. Google then quotes the refundable rate where it has one. |
| `minPrice`, `maxPrice` | Nightly price range in your currency. Google filters on the price it displays (the `nightly` field), which is before taxes from a US IP and all-in from most other countries; filter again on `total_with_taxes` when the limit must include taxes. |
| `minRating` | `3.5`, `4.0` or `4.5` — minimum Google guest rating. |
| `hotelClass` | Star classes to keep, e.g. `["4", "5"]`. |
| `amenities` | Hotels that have all of: `free_wifi`, `free_breakfast`, `restaurant`, `bar`, `kid_friendly`, `pet_friendly`, `free_parking`, `parking`, `ev_charger`, `room_service`, `fitness_center`, `spa`, `pool`, `indoor_pool`, `outdoor_pool`, `air_conditioned`, `wheelchair_accessible`, `beach_access`, `all_inclusive`. |
| `specialOffers` | Only hotels Google marks as a deal for your dates; the `deal` field carries the note ("23% less than usual"). |
| `includeOffers` | Fetch every source's rate per hotel (one extra call per hotel). |
| `offerLevel` | `sources`: one row per source, lowest rate (about 18 rows per hotel, 4 to 36). `rooms`: every source × room × rate with room names and cancellation deadlines (about 50–100 rows per hotel). |
| `maxOffersPerHotel` | 0 = every source; N = only the N cheapest rows per hotel (cost control). |
| `includeDetails` | Adds what Google's property page says about each hotel: `address`, `phone`, `place_id` (Google Maps), `description_long`, `rating_breakdown` (5 to 1 stars), `review_aspects` (Service, Location, Breakfast… with positive and negative mention counts), `external_ratings` (Tripadvisor, Trip.com…), `amenities` and `amenities_unavailable` (about 120 of them, with notes such as `Wi-Fi (free)`, `Parking (extra charge)`, `Front desk (24 hour)`) and `photos`. One small extra call per hotel, **at no extra charge**. It also completes hotels given by URL with star class, rating and coordinates. |
| `proxyConfiguration` | Apify datacenter proxies work; keep the default. |
| `sessions`, `perIp` | Parallel proxy sessions and requests per second per IP (defaults 4 and 0.5). |

### Example: hotel prices in a city for a stay

```json
{ "queries": ["hotels in Lisbon"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "adults": 2, "currency": "USD", "maxHotels": 60 }
```

### Example: the 40 cheapest 4–5-star hotels rated 4.5+ with free cancellation

```json
{ "queries": ["hotels in Lisbon"], "checkIn": "30 days", "checkOut": "32 days", "maxHotels": 40, "sortBy": "lowest_price", "hotelClass": ["4", "5"], "minRating": "4.5", "freeCancellation": true, "maxPrice": 350, "includeOffers": false }
```

Filters are Google Hotels' own and are applied by Google before anything is fetched, so you pay only for hotels that match. They apply to place searches (`queries`); hotels you name in `hotels` or `hotelNames` are always returned.

### Example: hotel data with contact details, rating breakdown and review topics

```json
{ "queries": ["hotels in Lisbon"], "checkIn": "30 days", "checkOut": "32 days", "maxHotels": 50, "includeDetails": true, "includeOffers": false }
```

```json
{ "type": "hotel", "name": "Altis Grand Hotel", "stars": 5, "rating": 4.7, "reviews": 6419, "nightly": 172.45, "total": 344.9, "total_base": 344.9, "taxes": 38.6, "fees": 0, "total_with_taxes": 383.5,
  "address": "R. Castilho 11, 1269-072 Lisboa, Portugal", "phone": "+351 21 310 6000", "place_id": "ChIJmYhOlXAzGQ0RmcenLVMx37g", "website": "https://www.altishotels.com/altis-grand-hotel/",
  "rating_breakdown": [{ "stars": 5, "percent": 77, "reviews": 4811 }, { "stars": 4, "percent": 19, "reviews": 1221 }],
  "review_aspects": [{ "aspect": "Service", "mentions": 611, "positive": 568, "negative": 29, "score": 0.79 }, { "aspect": "Location", "mentions": 332, "positive": 308, "negative": 7, "score": 0.77 }],
  "external_ratings": [{ "source": "Tripadvisor", "rating": 4.3, "scale": 5, "reviews": 2082 }],
  "amenities": ["Wi-Fi (free)", "Indoor pool", "Spa", "Fitness center", "Restaurant", "Bar", "Room service (24 hour)", "Parking (extra charge)", "Pet-friendly (extra charge)", "Airport shuttle"], "amenities_unavailable": ["Outdoor pool"] }
```

The detail fields cost nothing extra: a hotel row is the same price with or without them. Amenity names are in English whatever `language` is set to; an amenity Google lists that this actor has no verified name for is left out, never guessed.

### Example: track named hotels, no URLs needed

```json
{ "hotelNames": ["Hyatt Regency Lisbon", "Altis Grand Hotel Lisbon"], "checkIn": "30 days", "checkOut": "32 days", "currency": "EUR" }
```

### Example: rate parity for your own properties, scheduled daily, always 30 days out

```json
{ "hotels": ["https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE"], "checkIn": "30 days", "checkOut": "32 days", "sweepDays": 6, "currency": "EUR", "offerLevel": "sources" }
```

### Example: cheapest weekend in the next two months for a family

```json
{ "queries": ["family hotels Orlando near Disney"], "checkIn": "2026-10-02", "checkOut": "2026-10-04", "sweepDays": 56, "adults": 2, "childrenAges": [5, 9], "currency": "USD", "maxHotels": 20, "includeOffers": false }
```

## Hotel prices in Asia-Pacific: Singapore, Hong Kong, China, Taiwan, Japan, Korea and Southeast Asia

Every market Google Hotels serves works the same way: set `country` (the market), `language` and `currency`, and search in any language. Prices, deal notes, star-class labels and free-cancellation dates come back as that market shows them, in the one currency you asked for. Checked on 2026-09-20 in all of the markets below — 20 of 20 hotels priced in each.

| Market | `country` | `language` | `currency` | Booking sites Google lists there (besides Booking.com, Agoda, Trip.com and the hotel's own site) |
|---|---|---|---|---|
| Singapore | `sg` | `en` or `zh-CN` | `SGD` | Klook, Wego, AirAsia MOVE, Skyscanner, hutchgo |
| Hong Kong | `hk` | `zh-HK` or `en` | `HKD` | Wego, hutchgo, Qantas Hotels |
| Mainland China | `cn` | `zh-CN` | `CNY` | Hotels.com, Expedia, Qantas Hotels |
| Taiwan | `tw` | `zh-TW` | `TWD` | ezTravel 易遊網, Lion Travel 雄獅旅遊, Klook |
| Japan | `jp` | `ja` | `JPY` | Expedia.co.jp, Wego |
| South Korea | `kr` | `ko` | `KRW` | Tripbtoz, Creatrip, Klook, Wego |
| Indonesia | `id` | `id` | `IDR` | AirAsia MOVE, KAYAK, Hotelscombined |
| Thailand | `th` | `th` | `THB` | Traveloka, Klook, Wego, EaseMyTrip |
| Malaysia | `my` | `ms` or `en` | `MYR` | Klook, Expedia, Qantas Hotels |
| Vietnam | `vn` | `vi` | `VND` | KAYAK, Hotelscombined, HomeToGo |

Queries and hotel names can be written in the local script: `"新加坡酒店"`, `"香港酒店"`, `"上海酒店"`, `"台北飯店"`, `"東京 ホテル"`, `"서울 호텔"`, `"hotel di Jakarta"`, `"โรงแรมในกรุงเทพ"`. `hotelNames` understands Chinese, Japanese, Korean and Thai names too — `"香港半島酒店"`, `"上海外滩华尔道夫酒店"`, `"パーク ハイアット 東京"`, `"서울신라호텔"` — and a name Google lists in another script (`"台北君悅酒店"` → Grand Hyatt Taipei) is matched as well.

### Example: Singapore hotels in SGD, cheapest 4–5-star first

```json
{ "queries": ["hotels in Singapore"], "country": "sg", "language": "en", "currency": "SGD", "checkIn": "30 days", "checkOut": "32 days", "maxHotels": 40, "hotelClass": ["4", "5"], "sortBy": "lowest_price" }
```

### Example: Hong Kong hotels in HKD, in Traditional Chinese

```json
{ "queries": ["香港酒店"], "hotelNames": ["香港半島酒店"], "country": "hk", "language": "zh-HK", "currency": "HKD", "checkIn": "30 days", "checkOut": "32 days", "maxHotels": 40 }
```

### Example: rate parity for hotels in Shanghai, Tokyo and Seoul, every source, daily

```json
{ "hotelNames": ["上海外滩华尔道夫酒店", "Park Hyatt Tokyo", "서울신라호텔"], "currency": "USD", "checkIn": "30 days", "checkOut": "31 days", "offerLevel": "sources" }
```

### 简体中文 — 谷歌酒店价格爬虫

谷歌酒店（Google Hotels）价格爬虫：按入住日期和人数抓取酒店价格，包括每晚最低价、整段住宿总价，以及 Booking.com、Agoda、携程 Trip.com、Klook 和酒店官网等每个预订网站的报价，并标明是否可免费取消。适用于酒店价格监控、酒店比价、价格追踪和渠道价格一致性（rate parity）检查。支持中文搜索词和中文酒店名称，支持人民币（CNY）、新加坡元（SGD）、港币（HKD）等币种，无需 API 密钥，按实际获得的价格数据付费。

### 繁體中文 — Google 飯店價格爬蟲

Google 飯店（Google Hotels）價格爬蟲：依入住日期與人數擷取飯店與酒店價格，包含每晚最低價、整段住宿總價，以及 Booking.com、Agoda、Trip.com、Klook、易遊網、雄獅旅遊和飯店官網等各訂房網站的報價與免費取消條件。適用於酒店價格監控、飯店比價、價格追蹤與通路價格一致性檢查。支援中文搜尋與中文酒店名稱，支援港幣（HKD）、新台幣（TWD）、新加坡幣（SGD）。

### 日本語 — Google ホテル料金スクレイパー

Google ホテルの料金を日付と人数を指定して取得します。1泊あたりの最安値、滞在合計、Booking.com・Agoda・Trip.com・Expedia・公式サイトなど予約サイトごとの料金と無料キャンセルの有無を出力。ホテル料金の監視、料金比較、価格追跡、レートパリティの確認に。日本語の検索語とホテル名、日本円（JPY）に対応。

### 한국어 — 구글 호텔 가격 스크레이퍼

구글 호텔(Google Hotels)에서 날짜와 인원에 맞는 호텔 가격을 수집합니다. 1박 최저가, 총 숙박 요금, Booking.com·아고다·Trip.com·공식 홈페이지 등 예약 사이트별 요금과 무료 취소 여부를 제공합니다. 호텔 가격 모니터링, 가격 비교, 가격 추적에 적합하며 한국어 검색어와 호텔 이름, 원화(KRW)를 지원합니다.

### Bahasa Indonesia, ไทย, Tiếng Việt

Harga hotel dari Google Hotels untuk tanggal dan jumlah tamu tertentu: harga termurah per malam, total menginap, dan harga tiap situs pemesanan (Agoda, Trip.com, Booking.com, AirAsia MOVE) — untuk memantau harga hotel dan membandingkan harga hotel, dalam Rupiah (IDR) atau Ringgit (MYR). ราคาโรงแรมจาก Google Hotels ตามวันที่เข้าพัก: ราคาต่ำสุดต่อคืนและราคาจากทุกเว็บไซต์จองโรงแรม สำหรับเปรียบเทียบราคาโรงแรมและติดตามราคาโรงแรมเป็นเงินบาท (THB). Giá khách sạn từ Google Hotels theo ngày lưu trú: giá thấp nhất mỗi đêm và giá của từng trang đặt phòng, để so sánh giá khách sạn và theo dõi giá khách sạn bằng đồng (VND).

## Output

`hotel` row (the Console's **Hotels** and **Offers by source** views show the same rows as tables; the dataset schema documents every field):

```json
{ "type": "hotel", "query": "hotels in Lisbon", "check_in": "2026-10-03", "check_out": "2026-10-06", "nights": 3, "adults": 2, "children": 0, "currency": "USD",
  "rank": 1, "name": "The Central House Lisbon Baixa", "hotel_id": "10088532857338925820", "entity_id": "ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE",
  "stars": 2, "class_label": "2-star hotel", "rating": 4.3, "reviews": 727, "lat": 38.7131, "lng": -9.1368, "types": ["hostel"],
  "nightly": 81.81, "nightly_display": "$82", "total": 245, "total_display": "$245", "deal": "19% less than usual", "source": null,
  "website": "https://www.thecentralhousegroup.com/", "maps_url": "https://maps.google.com/?cid=3848859359889388291", "thumbnail": "https://lh3.googleusercontent.com/gps-cs-s/…",
  "google_url": "https://www.google.com/travel/hotels/entity/ChkIg-b2ismUj7M1Gg0vZy8xMWg3MThreGg1EAE", "total_results": 15000, "fetched_at": "2026-08-25T14:03:11+00:00" }
```

`offer` row (one per source with `offerLevel: "sources"`; per room and rate with `"rooms"`):

```json
{ "type": "offer", "name": "Hyatt Regency Lisbon", "entity_id": "ChoI4cjBy-KGurGyARoNL2cvMTFtdnFfdncydhAB", "check_in": "2026-10-03", "check_out": "2026-10-06", "nights": 3, "adults": 2, "children": 0, "currency": "USD",
  "source": "Booking.com", "source_id": 184, "official": false, "room": null, "nightly": 569.35, "total": 1708.05, "max_guests": null,
  "free_cancel": null, "free_cancel_until": null, "link": "https://www.google.com/travel/lodging/clk?pc=…", "partner_url": "https://www.booking.com/hotel/pt/hyatt-regency-lisbon.html?checkin=2026-10-03&checkout=2026-10-06…", "lowest": true, "fetched_at": "2026-08-25T14:03:14+00:00" }
```

Room-level rows carry the free-cancellation deadline three ways: `free_cancel_until` as Google words it ("Oct 25", "26. Okt.", "10月22日"), `free_cancel_until_date` as an ISO date (2026-10-25) and `free_cancel_until_time` ("11:59 PM"). The date is derived only where the wording cannot be misread — English, German, French, Spanish, Italian, Portuguese, Dutch, Chinese and Japanese — and left empty otherwise. Rows with `"lowest": true` are each source's cheapest rate; official-site rows carry the hotel's booking engine URL with your dates in `partner_url`. A source is keyed by `source_id` — a name such as Holidu or Booking.com can appear twice for one property when Google lists both its official listing (`official: true`) and its marketplace rate. Properties given in `hotels` are answered from their offers page: the `hotel` row carries name, headline nightly rate and stay total; star class, rating and coordinates come from place searches only.

`status` row (never charged):

```json
{ "type": "status", "query": "hotels in Lisbon", "hotel": null, "check_in": "2026-10-03", "check_out": "2026-10-06", "hotels": 25, "priced": 24, "offers": 310, "duplicates": 0, "offer_errors": 0, "error": null, "fetched_at": "2026-08-25T14:03:20+00:00" }
```

## How much does it cost?

Pay per event, only for priced rows: a `hotel` row (a hotel with a price for your dates) and an `offer` row (one source's rate). Sold-out hotels, empty searches and `status` rows are free, and a hotel and stay is billed once per run even when overlapping searches return it twice. A city search of 60 hotels with source-level offers is a few hundred rows; a daily parity check of ten properties with seven check-in days is about 70 hotel rows plus their offers. Apify's platform usage for a run of that size is a fraction of a cent — the runs above cost $0.001–$0.003 in compute. The exact per-row prices are on this page's pricing tab, and `maxOffersPerHotel` caps the offer rows when you only need the cheapest few sources.

## Google Hotels API or scraper: how this compares

Google has no public Google Hotels API for reading prices: its Hotel APIs (Hotel Prices, Hotel Ads, Book on Google) are partner feeds for hotels that *send* prices to Google. Reading prices back means a scraper or a SERP API vendor.

- **SerpApi Google Hotels API, DataForSEO, SearchApi, Bright Data** sell a Google hotel price API per search. They return the search page; per-source rates and room-level offers usually need a second product or are not exposed, and you pay per search whether or not it had results.
- **This scraper** returns hotels *and* every source's rate as flat rows, bills per priced row, handles paging to 200 hotels, occupancy including children's ages, any currency and market, relative dates for schedules, and property mode for your own hotels. It runs inside Apify, so scheduling, storage, webhooks and integrations come with it.
- **Writing your own with Python** ("scrape google hotels", "scrape hotel prices", "web scraping hotel prices"): Google Hotels renders prices through internal RPC calls, not HTML, and the payload formats change. The point of this actor is that someone keeps that working and reports failures as `status` rows instead of silent zeros.

### How it compares with the other Google Hotels scrapers on the Store

Read from the input schemas and public run statistics of the 12 other Google Hotels actors on Apify Store on 2026-09-20:

| What to check | This actor | The 12 others |
|---|---|---|
| Relative dates (`"30 days"`), so a schedule never goes stale | Yes | 0 of 12 |
| Hotels by name, no URL or token to look up | Yes — also in Chinese, Japanese, Korean and Thai | 3 of 12 |
| The same stay across many check-in dates in one run | Yes (`sweepDays`, up to 60) | 2 of 12 |
| Google's free-cancellation filter | Yes | 1 of 12 |
| Google's own sort (price, rating, reviews), held across pages | Yes | 5 of 12 |
| Children's ages, which change the price | Yes | 3 of 12 |
| Runs that succeeded over the last 30 days | 410 of 412 (99.5%) | from 55% to 100%; 3 of 12 below 90% |

Two things no schema shows, so check them on any scraper you try. **Complete rate ladders:** about one proxy IP in eight gets a cut-down answer from Google — 6 or 7 booking sites instead of 20 to 26, with the lowest rate wrong; this actor recognises those answers, retires the IP and asks again. **Complete result pages:** Google's page tokens belong to the IP that issued them, so a scraper that spreads one search over several proxies can silently skip hotels; this actor keeps each search on one session.

If you searched for "Google Hotels API free" or a hotel price comparison API: there is a free tier on Apify, no API key from Google is needed, and empty results are never charged. As a hotel rates API it is one POST with the dates and a dataset of rows back.

## How to use it from Python, JavaScript, curl, n8n, Make or an AI agent

Run it from the Apify Console with the form, or programmatically. Replace `<TOKEN>` with your Apify API token.

Python:

```python
from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/google-hotels-prices").call(run_input={
    "queries": ["hotels in Lisbon"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "adults": 2, "currency": "USD", "maxHotels": 40})
rows = list(client.dataset(run["defaultDatasetId"]).iterate_items())
hotels = [r for r in rows if r["type"] == "hotel"]; offers = [r for r in rows if r["type"] == "offer"]
cheapest = min((h for h in hotels if h["nightly"]), key=lambda h: h["nightly"])
print(cheapest["name"], cheapest["nightly_display"], cheapest["total_display"])
```

JavaScript / Node.js:

```javascript
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/google-hotels-prices').call({ hotels: ['https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE'], checkIn: '30 days', checkOut: '32 days', currency: 'EUR' });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const official = Math.min(...items.filter(x => x.type === 'offer' && x.official).map(x => x.nightly));
const parityBreaches = items.filter(o => o.type === 'offer' && !o.official && o.nightly < official);
console.log(parityBreaches.map(o => [o.name, o.source, o.nightly]));
```

curl:

```bash
curl -X POST "https://api.apify.com/v2/acts/kestrel~google-hotels-prices/run-sync-get-dataset-items?token=<TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"queries": ["hotels in Lisbon"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "maxHotels": 20, "includeOffers": false}'
```

- **n8n, Make, Zapier**: use the Apify node/app with this actor's id, or a webhook on run finished, then read the dataset — a hotel price tracker or alert flow is three nodes.
- **AI agents and MCP**: the actor is available through the Apify MCP server and Apify AI; the README, input schema and flat row types are written so an agent can ask "hotels in Lisbon under $150 from Oct 3 to 6 with free cancellation" and filter the rows.
- **Google Sheets, BigQuery, Airtable**: export the dataset from the run page or through Apify's integrations.

## Is it legal to scrape Google Hotels prices?

The scraper reads publicly displayed prices — the same figures any visitor sees without logging in — and stores no personal data: rows describe hotels, sources and rates, not people. Collecting public pricing for analysis and monitoring is common practice in the hotel industry (every rate shopping tool does it), but terms of service and local law differ; check that your use complies, and use the data for your own analysis rather than republishing it as Google's.

## Limits and honest notes

- A place search pages through Google's ranking 20 at a time up to `maxHotels` (200); neighbourhood or landmark queries add coverage beyond that.
- Prices are what Google Hotels shows for the market (`country`) and currency you choose; whether taxes and fees are included follows Google's display rules for that market. The `total` is the stay total Google shows.
- Sources per hotel vary by market and day: 18 on average, 4 to 36, measured on 174 hotels in September 2026; room level averages about 65 rows per hotel and reaches about 150. Sold-out hotels appear as `hotel` rows without a price and are not charged.
- Google changes its internal formats occasionally; a daily canary run watches for that, the actor is rebuilt within days, and every run reports `status` rows so a failure is visible rather than a silent zero.
- **Google never fails a place search.** An unrecognised or misspelt place is silently matched to somewhere else and answered with real hotels, which are delivered and billed like any other row. There is no signal in Google's response that says "I did not find that place", and a fuzzy-matched nonsense string can return a cluster as tight as a genuine region, so this cannot be detected reliably enough to refuse the run without also breaking legitimate broad searches like `"Portugal"` or `"California"`. Each place `status` row therefore carries `spread_km` — the median distance of the returned hotels from their centre. A city is single digits, a region tens, a country a few hundred; anything in the thousands almost certainly did not resolve. Above 500km the run logs a warning. Pass an exact place name or a Google Hotels entity URL when it matters, and check `spread_km` and each hotel's `lat`/`lng` before trusting a run.

## FAQ

### Does it need a Google Hotels API key or a Google account?

No. There is no public Google Hotels API for reading prices; the scraper uses the public results page through Apify's proxies. No login, cookies or API key.

### Can I get hotel price history and price alerts from Google Hotels?

Google's own tracker keeps history and alerts inside Google. Schedule this scraper (daily, with relative dates) and every run appends dated rows to your dataset — that is your price history — and an Apify integration (n8n, Make, Zapier, webhook) turns a drop into an alert.

### How is this different from Google's "Track hotel prices" feature?

Google's feature emails you about the listings it chooses to watch and does not let you pick sources or export data. This scraper returns every source's rate for the exact dates, occupancy and currency you set, as rows you own.

### Which booking sites are covered?

Whatever Google Hotels lists for that property and market: Booking.com, Expedia, Hotels.com, Agoda, Trip.com, Priceline, Kayak, eDreams, Vio.com, the official site and dozens of regional OTAs. The `source` name and `source_id` come straight from Google.

### Does it include taxes and fees?

It tells you exactly. Every hotel row from a place search carries Google's own breakdown of the stay: `total_base`, `taxes`, `fees` (service charges, resort fees) and `total_with_taxes`, where `total_base + taxes + fees = total_with_taxes` — checked on 2026-09-20 on 120 hotels in six markets (US, UK, Germany, Singapore, Japan, UAE). The `nightly` and `total` fields are what Google *displays*, and that follows the country of the IP the request comes from, not the market you ask for: from a US IP Google displays the price before taxes but with mandatory fees included (`total_base + fees`), from most other countries the all-in price. So the same hotel can show $221 or $253 for the same stay depending on the proxy. Compare on `total_with_taxes` (or `total_base`) and the proxy stops mattering.

### How many hotels can one run return?

Up to 200 per place search, or as many properties as you list in `hotels`, times the number of stays (`sweepDays`). A run stops cleanly when it reaches the spending limit you set on the run.

### Why do prices differ from what I see in my browser?

Google prices depend on market, currency, occupancy, dates and sometimes the device. Match `country`, `currency`, `adults`, `childrenAges` and the dates, and compare the `total` for the stay rather than a headline nightly figure.

### Can I use it as a hotel price scraper for Booking.com or Expedia specifically?

Yes for prices: each `offer` row names its source, so filtering `source == "Booking.com"` gives you Booking.com's rate per hotel and stay, and likewise for Expedia, Agoda or Hotels.com — without scraping each site separately. For reviews or room descriptions use a Booking.com scraper or Expedia scraper built for that site.

### Is there a free tier?

Yes: Apify's free plan covers small runs, and this scraper never charges for a run that returns no priced rows.

Last verified working: 2026-08-29.


## Ready-made runs

Each link opens this actor with the input already filled in — press Start and it runs. Every one is capped, so what it bills is on the page before you run it. What each returns is spelled out at [mtedj.github.io/kestrel-actors-examples/recipes.html](https://mtedj.github.io/kestrel-actors-examples/recipes.html).

- [Hotel Price History by Date (Google Hotels)](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-history-by-date)
- [OTA Rate Comparison: Booking vs Expedia](https://apify.com/kestrel/google-hotels-prices/examples/ota-rate-comparison-booking-expedia)
- [Hotel Price Data by Room Type and Source](https://apify.com/kestrel/google-hotels-prices/examples/hotel-room-rates-by-room-type)
- [Scrape Google Hotels Prices for a City](https://apify.com/kestrel/google-hotels-prices/examples/scrape-google-hotels-prices-for-a-city)
- [Hotel Price Monitoring for a Comp Set](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-monitoring-comp-set)
- [Google Hotels API Alternative, No SERP Key](https://apify.com/kestrel/google-hotels-prices/examples/google-hotels-api-alternative)
- [Scrape Hotel Prices for a Family Room](https://apify.com/kestrel/google-hotels-prices/examples/scrape-hotel-prices-for-a-family-room)
- [Hotel Price Tracking: Weekend vs Weekday](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-tracking-weekend-vs-weekday)
- [Hotel Rates API for the German Market](https://apify.com/kestrel/google-hotels-prices/examples/hotel-rates-api-for-the-german-market)
- [Hotel Price Intelligence: 5-Star Dubai](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-intelligence-five-star-dubai)
- [Scrape Hotel Prices Near a Landmark](https://apify.com/kestrel/google-hotels-prices/examples/scrape-hotel-prices-near-a-landmark)
- [Hotel Price Scraper for 7-Night Stays](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-scraper-for-7-night-stays)
- [Hotel Price Comparison API for Group Rates](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-comparison-api-group-rates)
- [Web Scraping Hotel Prices in Tokyo (JPY)](https://apify.com/kestrel/google-hotels-prices/examples/web-scraping-hotel-prices-in-tokyo-jpy)
- [Singapore Hotel Prices in SGD (Google Hotels)](https://apify.com/kestrel/google-hotels-prices/examples/scrape-hotel-prices-in-singapore-sgd)
- [Hong Kong Hotel Prices in HKD, in Chinese (香港酒店)](https://apify.com/kestrel/google-hotels-prices/examples/hong-kong-hotel-price-data-hkd-chinese)
- [Shanghai Hotel Prices in CNY (上海酒店价格)](https://apify.com/kestrel/google-hotels-prices/examples/scrape-hotel-prices-in-shanghai-cny-chinese)
- [Hotels with Free Cancellation, 4.5+ Rated, by Price](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-scraper-free-cancellation-filter)
- [Rate Parity for Hotels by Name, No URLs Needed](https://apify.com/kestrel/google-hotels-prices/examples/rate-parity-for-hotels-by-name)
- [Hotel Data: Address, Phone, Rating Breakdown & Prices](https://apify.com/kestrel/google-hotels-prices/examples/hotel-price-data-with-address-phone-ratings)

## Related scrapers

Hotel prices are one side of a trip. These read the rest of it, and they share the same row shape, the same pay-per-delivered-row billing and the same scheduling story:

- **[Agoda Prices Scraper](https://apify.com/kestrel/agoda-prices-scraper)** — the same stay priced on Agoda, by destination or property, for a second channel in a rate comparison.
- **[Booking.com Scraper — Hotel Prices](https://apify.com/kestrel/booking-prices-scraper)** — the same stay priced on Booking.com itself, by destination or property, no browser.
- **[Hotel Price Tracker](https://apify.com/kestrel/hotel-price-tracker)** — only want the lowest rate per property and check-in date, cheap enough to run every morning? It runs the same engine and bills one row per property and date over a window of up to 60 dates, ranked, with a `maxPrice` alert that filters before billing.
- **[Hotel Rate Parity Checker](https://apify.com/kestrel/hotel-rate-parity)** — the same comparison as one row per property and stay with the parity math done: cheapest and dearest source, spread, and which OTAs undercut the official site by how much.
- **[Google Flights Scraper](https://apify.com/kestrel/google-flights-prices)** — airfare for a route and date, with a cheapest-day sweep.
- **[Airbnb Scraper](https://apify.com/kestrel/airbnb-prices-calendar)** — Airbnb prices, availability calendars and occupancy.
- **[Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper)** — every guest review of an Airbnb listing, with translations.
- **[Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper)** — Agoda hotel reviews with separate positives and negatives.

All of them bill per delivered row, never charge for rows a filter or a spending limit removed, and write an Apify dataset you can export to CSV, Excel or JSON.
