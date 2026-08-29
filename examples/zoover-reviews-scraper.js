import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/zoover-reviews-scraper').call({
    accommodationIds: ['91488', '83376'],
    sinceDate: '12 months',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'reviews');
