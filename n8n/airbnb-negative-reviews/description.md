Airbnb guest reviews, watched for you: every morning this workflow fetches the newest reviews for your listings, keeps only new ones rated 3 stars or less, appends them to a Google Sheet and posts each to Slack, flagged *unanswered* until the host replies — short-term rental review notifications for the bad ones only. It calls the [Airbnb Reviews Scraper](https://apify.com/kestrel/airbnb-reviews-scraper) Apify actor through a core HTTP Request node — n8n Cloud or self-hosted.

## Who is this for

Hosts, co-hosts and property managers with many listings who want to answer low-star reviews fast and keep a log.

## How it works

1. **Run daily at 08:00** — Schedule trigger.
2. **Run Airbnb reviews** — HTTP POST to the actor's run-sync endpoint: 50 most recent reviews per listing, delivered only if ≤ 3★.
3. **Keep new reviews** — Code node keeps `type = review` rows, drops `review_id`s seen before (workflow static data, max 5,000 ids), newest first, text trimmed to 300 characters, `reply_status` unanswered/replied.
4. **Any new?** — IF.
5. **Append to Google Sheets** — one row per review; columns are listed in the sticky note.
6. **Post to Slack** — one message per review.
7. **No new complaints** — NoOp.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in *Run Airbnb reviews*.
2. Replace the example `listingIds` with your listing ids.
3. Connect `Slack account` in *Post to Slack* and `Google Sheets account` in *Append to Google Sheets*; add a header row with the columns from the sticky note.

## How to customize

- Watch a whole market: `locationQueries: ["Lisbon, Portugal"], maxListingsPerQuery: 50` instead of `listingIds`.
- `minRating: 0` delivers every review; `minRating: 2` only 1–2★.
- Swap Slack for Email, Teams or Telegram.

## Cost

$0.005 per delivered review; listing and status rows are free, and reviews above 3★ are filtered before billing. Worst case 50 × $0.005 = $0.25 per listing per day; low-star reviews are rare, so a run usually costs cents. The verification run over two listings delivered 3 reviews = $0.015.
