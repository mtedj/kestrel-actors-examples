import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<APIFY_TOKEN>' });
const run = await client.actor('kestrel/despegar-hotel-ratings').call({
    startUrls: ['https://www.despegar.com.ar/hoteles/h-265543/riu-cancun'], includeComments: true });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'hotel'));
