import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/aliexpress-reviews-scraper').call({
    productIds: ['1005006255429323'],
    maxReviewsPerProduct: 0,
    maxRating: 3,
    sort: 'lowest_rating',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'complaints');
