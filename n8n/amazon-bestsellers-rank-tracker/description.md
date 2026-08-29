An Amazon best sellers tracker in one workflow: every morning it pulls the Top 50 of a Best Sellers category, compares each product's rank with yesterday's, appends the chart to a Google Sheet (a daily Amazon rank tracking history) and posts to Slack when a product enters the top 10. It calls the [Amazon Best Sellers Scraper](https://apify.com/kestrel/amazon-best-sellers-scraper) Apify actor through a core HTTP Request node.

## Who is this for

Sellers and brand managers watching their category, product researchers hunting movers, agencies reporting chart positions.

## How it works

1. **Run daily at 06:00** — Schedule trigger.
2. **Run Amazon charts** — HTTP POST to the actor's run-sync endpoint: one Best Sellers page for `categories: ["electronics"]`, capped at 50, `fillRanks` on so ranks 1–50 have no gaps (Amazon renders only 30 of a page's 50 entries).
3. **Compute rank moves** — Code node keeps `type = product` rows, looks up yesterday's rank per `category|chart|asin` in workflow static data (max 5,000 keys) and adds previous_rank and change (`+3`, `-2`, `0`, `new`).
4. **Append to Google Sheets** — all 50 rows, every day.
5. **New in top 10?** — IF: `change = new` and `rank ≤ 10`. A list's first run only seeds the history.
6. **Post to Slack** — one message per new entry.
7. **Nothing new in top 10** — NoOp.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in *Run Amazon charts*.
2. Edit `categories` (the slug after `/gp/bestsellers/` in a Best Sellers URL) and `domain`.
3. Connect `Google Sheets account` in *Append to Google Sheets* (header row: the columns from the sticky note) and `Slack account` in *Post to Slack*.

## How to customize

- Top 100: `pages: 2, maxResultsPerCategory: 100` ($0.40).
- `chart: "new_releases"` for the newest products; several categories at once; other marketplaces via `domain`.

## Cost

$0.004 per product row; status rows are free. Top 50 = 50 × $0.004 = $0.20 per category per day, Top 100 = $0.40; the verification run delivered exactly 50 rows = $0.20.
