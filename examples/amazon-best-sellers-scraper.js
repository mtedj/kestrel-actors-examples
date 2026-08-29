import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-best-sellers-scraper').call({
    categories: ['kitchen'], chart: 'new_releases', pages: 1, maxResultsPerCategory: 20,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'product').map((p) => [p.rank, p.asin, p.title]));
