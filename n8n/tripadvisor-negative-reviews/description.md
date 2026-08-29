TripAdvisor review monitoring on autopilot: every morning this workflow reads the newest TripAdvisor reviews of your hotels, keeps the ones at 3 bubbles or less with a written text, logs them to a Google Sheet and posts the ones not seen yet to Slack. It calls the [TripAdvisor Reviews Scraper](https://apify.com/kestrel/tripadvisor-reviews-scraper) Apify actor through a core HTTP Request node — n8n Cloud or self-hosted.

## Who is this for

Hotel general managers, reputation managers, agencies with a portfolio.

## How it works

1. **Run daily at 08:00** — Schedule trigger.
2. **Run TripAdvisor reviews** — HTTP POST to the actor's run-sync endpoint; of the 40 newest per hotel only those at 3 bubbles or less with text are billed.
3. **Flag new reviews** — Code node keeps `type = review` rows and marks each `is_new` by comparing `review_id` with earlier runs (workflow static data, 5,000 ids).
4. **Log to Google Sheets** — every delivered review, matched on `review_id`, so a repeat updates its row instead of duplicating it, and a late management response lands in the same row.
5. **New review?** — IF on `is_new` → **Post to Slack**, one message per review; **Already alerted** (NoOp) for the rest.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in *Run TripAdvisor reviews*.
2. Replace the example `locationIds` with yours (the `d<number>` in a TripAdvisor hotel URL), or use `startUrls` / `hotelNames`.
3. Connect `Google Sheets account` and `Slack account`; the sheet's header row is in the sticky note.

## How to customize

- `maxRating: 2` for a 1–2 bubble feed, `0` for every review.
- `sinceDate: "7 days"` stops at the first page older than that.
- `languages: ["en", "de", "fr"]` reads the hotel on several TripAdvisor sites. Every filter runs before billing.

## Cost

$0.005 per delivered review; hotel and status rows are free; reviews above 3 bubbles or without text are never billed. Two hotels × 40 newest is at most $0.40 a day; the verification run read 40 per hotel and delivered 2 = $0.010.
