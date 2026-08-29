---
name: google-hotels-prices
description: Get hotel prices from Google Hotels for exact dates, guests and currency — lowest nightly rate and stay total per hotel, plus every booking site's rate (Booking.com, Expedia, Agoda, official site) with free-cancellation flags and deep links. Use when a user asks for hotel prices, the cheapest hotels for dates, whether a hotel is cheaper on some site, rate parity, or a hotel price history. Runs the Apify actor kestrel/google-hotels-prices (needs APIFY_TOKEN).
---

# Google Hotels prices (Apify actor `kestrel/google-hotels-prices`)

## When to use
- "hotels in <place> from <date> to <date>", "cheapest hotel in …", "how much is <hotel> on <dates>", "is <hotel> cheaper on Booking or the official site", "track prices for …", "rate parity for my hotels".
- Not for reviews, room descriptions or bookings — use a site-specific tool for those.

## Call
POST `https://api.apify.com/v2/acts/kestrel~google-hotels-prices/run-sync-get-dataset-items?token=$APIFY_TOKEN` with JSON:
- place search: `{"queries": ["hotels in Lisbon"], "checkIn": "2026-10-03", "checkOut": "2026-10-06", "adults": 2, "childrenAges": [], "currency": "USD", "country": "us", "maxHotels": 20, "includeOffers": true, "offerLevel": "sources"}`
- specific hotels: `{"hotels": ["https://www.google.com/travel/hotels/entity/ChkI…"], "checkIn": "30 days", "checkOut": "32 days", "currency": "EUR"}`
Dates: `YYYY-MM-DD` or relative (`"30 days"`, `"6 weeks"`, `today`, `tomorrow`); check-in must be in the future. `sweepDays: N` prices N more consecutive check-in days. Set `includeOffers: false` when only the lowest price per hotel is needed (cheaper, faster).

## Read the rows
- `type == "hotel"`: `name`, `nightly` (number), `nightly_display`, `total` (stay total), `stars`, `rating`, `reviews`, `deal`, `lat`/`lng`, `entity_id`, `google_url`, `maps_url`. A hotel without `nightly` is sold out for those dates.
- `type == "offer"`: `source` (booking site, or the hotel's name when `official` is true), `source_id`, `nightly`, `total`, `free_cancel`, `free_cancel_until`, `link`, `partner_url` (booking engine with dates when official), `room` (only with `offerLevel: "rooms"`), `lowest`.
- `type == "status"`: `hotels`, `priced`, `offers`, `error` — report `error` to the user instead of guessing.

## Answering well
- Compare the stay `total`, not just `nightly`; state currency and dates.
- Cheapest: min `nightly` over hotel rows with a price. Parity breach: offer rows with `official == false` and `nightly` below the official row's `nightly`.
- Billing is per priced row; empty results cost nothing — it is fine to run a search that may return nothing.
