import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/airbnb-reviews-scraper').call({
    locationQueries: ['Lisbon, Portugal'], maxListingsPerQuery: 20, maxReviewsPerListing: 50,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'reviews');
