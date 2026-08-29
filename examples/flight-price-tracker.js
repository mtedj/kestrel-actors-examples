import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/flight-price-tracker').call({
    routes: ['JFK-LHR'], departDate: '14 days', days: 21, tripLengthDays: 7, maxStops: 'nonstop',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const best = items.find((i) => i.type === 'fare' && i.cheapest_in_window);
console.log(best.depart_date, best.price, best.airline);
