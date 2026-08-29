import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/ebay-search-scraper').call({
    queries: ['keycap set'],
    pages: 1,
    sortBy: 'price_low',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((r) => r.type === 'item').length, 'listings');
