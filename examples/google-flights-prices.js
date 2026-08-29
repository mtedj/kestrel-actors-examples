import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/google-flights-prices').call({
    routes: ['JFK-LHR'], departDate: '14 days', seat: 'business', maxStops: 'nonstop',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'flight').map((i) => [i.price, i.airline]));
