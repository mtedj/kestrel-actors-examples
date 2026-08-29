import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-reviews-scraper').call({
    asins: ['B0BSHF7WHW', 'https://www.amazon.co.uk/dp/B09G9FPHY6'],
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'product').map((p) => [p.marketplace, p.rating, p.ratings_count]));
