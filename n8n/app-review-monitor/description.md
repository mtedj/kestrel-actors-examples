An app review monitor for both stores at once: every morning it reads the newest App Store and Google Play reviews of your app, keeps the 1- and 2-star ones with words in them, drops what an earlier run reported and posts the rest to Slack with store, rating, version and country. It calls the [App Store Reviews Scraper](https://apify.com/kestrel/app-store-reviews-scraper) and [Google Play Reviews Scraper](https://apify.com/kestrel/google-play-reviews-scraper) through core HTTP Request nodes — n8n Cloud or self-hosted.

## Who is this for

Mobile product managers, support leads and indie developers who want angry reviews in the team channel.

## How it works

1. **Run daily at 08:00** — Schedule trigger.
2. **Run App Store reviews** — HTTP POST to the actor's run-sync endpoint: `appIds` (Apple's numeric id) and `countries`.
3. **Run Google Play reviews** — the same for the Android package name, plus `languages`.
4. **Merge both stores** — Merge (append).
5. **Keep new reviews** — Code node normalises both row shapes into one list (App Store rows carry `title` and `version`, Play rows `app_version`, `language`) and drops the `store|review_id` pairs seen before (static data, 5,000 keys).
6. **Any new?** — IF → **Post to Slack**, one message per review; **No new complaints** (NoOp) otherwise.

## Setup

1. Create a **Header Auth** credential named `Apify Header Auth` (name `Authorization`, value `Bearer <your Apify token>`) and select it in both HTTP Request nodes.
2. Replace the example apps: Apple's numeric id (after `/id` in a store URL) and the package name.
3. Connect `Slack account` in *Post to Slack* and pick the channel.

## How to customize

- Add storefronts and languages — reviews live per locale.
- `maxRating: 3`, or `sort: "most_critical"` on the App Store side.
- Watch one store: disable the other HTTP node, the Code node copes.

## Cost

$0.004 per delivered review on each side. `maxRating: 2`, `requireText` and `sinceDate` are applied before billing, so 3–5 star and star-only reviews cost nothing and a quiet day costs nothing. The verification run delivered 20 App Store + 7 Play reviews = $0.108; a normal app sees a handful a day.
