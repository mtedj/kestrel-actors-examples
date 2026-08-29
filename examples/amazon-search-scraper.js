import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-search-scraper').call({
    categories: ['electronics'], chart: 'new_releases', pages: 1,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'product').map((p) => [p.rank, p.asin, p.title]));
