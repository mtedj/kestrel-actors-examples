import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/agoda-reviews-scraper').call({
    hotelIds: ['63820'], maxReviewsPerHotel: 200, reviewsSort: 'most_recent',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'reviews');
