import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/google-play-reviews-scraper').call({
    appIds: ['com.spotify.music'], languages: ['en'], countries: ['us', 'gb'],
    sort: 'most_recent', sinceDate: '7 days', maxReviewsPerApp: 500,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter(r => r.type === 'review');
console.log(reviews.length, 'new reviews this week;', reviews.filter(r => r.reply_text).length, 'answered');
