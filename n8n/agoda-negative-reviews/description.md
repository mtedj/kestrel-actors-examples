Hotel reviews monitoring on autopilot: every morning this workflow pulls the latest Agoda reviews for your hotels, keeps only new ones scoring 6/10 or less, logs them to a Google Sheet and posts each to Slack — guest feedback alerts the same day. It calls the [Agoda Reviews Scraper](https://apify.com/kestrel/agoda-reviews-scraper) Apify actor through a core HTTP Request node — n8n Cloud or self-hosted.

## Who is this for

Hotel general managers, reputation and revenue managers, and agencies watching a portfolio who want Agoda complaints in Slack, with a running log.

## How it works

1. **Run daily at 08:00** — Schedule trigger.
2. **Run Agoda reviews** — HTTP POST to the actor's run-sync endpoint: 50 most recent reviews per hotel, delivered only if ≤ 6/10 and written.
3. **Keep new reviews** — Code node keeps `type = review` rows, drops `review_id`s seen before (workflow static data, max 5,000 ids), newest first, text trimmed to 300 characters.
4. **Any new?** — IF.
5. **Append to Google Sheets** — one row per review; columns are listed in the sticky note.
6. **Post to Slack** — one message per review.
7. **No new complaints** — NoOp.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in *Run Agoda reviews*.
2. Replace the example `hotelIds` with your Agoda hotel ids, or use `hotelNames: ["Park Hyatt Tokyo"]`.
3. Connect `Slack account` in *Post to Slack* and `Google Sheets account` in *Append to Google Sheets*; add a header row with the columns from the sticky note.

## How to customize

- `maxRating: 0` delivers every review; `maxRating: 4` only the worst.
- Remove `requireText` to include score-only reviews.
- Set `locale` for translations; swap Slack for Email, Teams or Telegram.

## Cost

$0.005 per delivered review; hotel and status rows are free, and reviews above 6/10 or without text are filtered before billing. Worst case 50 × $0.005 = $0.25 per hotel per day; typically 0–3 complaints, so ten hotels cost a few cents a day. The verification run delivered 1 review = $0.005.
