import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/app-store-reviews-scraper').call({
    appNames: ['Duolingo'], countries: ['us'], sort: 'most_critical', maxRating: 2, maxReviewsPerApp: 300,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const complaints = items.filter(r => r.type === 'review');
console.log(complaints.length, 'low-star reviews');
