Booking.com price drop alerts for a hotel shortlist: every morning it re-prices the same properties for the same stay, compares each total with yesterday's and emails only the ones that got cheaper, with the old price, the new price and the saving. It calls the [Booking.com Prices Scraper](https://apify.com/kestrel/booking-prices-scraper) Apify actor through a core HTTP Request node — n8n Cloud or self-hosted, no database.

## Who is this for

Travellers with a shortlist, travel agents watching client stays, revenue managers on a comp set.

## How it works

1. **Run daily at 07:00** — Schedule trigger.
2. **Run Booking.com prices** — HTTP POST to the actor's run-sync endpoint: your `hotelIds`, a relative `checkIn` ("45 days"), `nights`, `adults`, `currency`. One `hotel` row per property.
3. **Compare with the last run** — Code node keys each property on `hotel_id|check_in`, reads its previous total from workflow static data (5,000 keys), computes `change_pct`, keeps drops of at least `DROP_PCT` (3 %) and counts the sold-out ones. One item out: a ready-to-send `subject`, `table` and `body`.
4. **Any price drops?** — IF → **Email the drops** (Gmail); **No drops today** (NoOp) otherwise.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in *Run Booking.com prices*.
2. Put your own `hotelIds` (Booking's numeric property ids, or `hotelNames` / `startUrls`) and dates in *Run Booking.com prices*.
3. Connect `Gmail account` in *Email the drops* and set the recipient. `DROP_PCT` in the Code node is the threshold.

## How to customize

- `locationQueries: ["Lisbon"]` + `maxHotelsPerQuery` watches a destination instead of a shortlist.
- `maxPrice` drops anything above budget before billing; `minStars`, `sortBy` and `rooms` shape the search; `includeRooms` adds room-level rates.
- Swap Gmail for Slack or Telegram; the text is preformatted.
- Booking serves session-dependent rates: raise `DROP_PCT` if the mail is chatty.

## Cost

$0.004 per priced property (+ $0.002 per room row with `includeRooms`); sold-out properties and status rows are free. The five-hotel shortlist here costs 4 × $0.004 = $0.016 a day (one was sold out, free), about $0.48 a month.
