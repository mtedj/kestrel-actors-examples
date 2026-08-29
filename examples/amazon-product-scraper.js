import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/amazon-product-scraper').call({
    asins: ['B09B8V1LZ3', 'https://www.amazon.co.uk/dp/B09B8V1LZ3'],
    proxyConfiguration: { useApifyProxy: true, apifyProxyGroups: ['RESIDENTIAL'] },
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.filter(r => r.type === 'product').map(r => ({ asin: r.asin, marketplace: r.marketplace, price: r.price_display, inStock: r.in_stock })));
