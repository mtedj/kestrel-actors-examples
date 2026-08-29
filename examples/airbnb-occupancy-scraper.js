import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/airbnb-occupancy-scraper').call({
    listingIds: ['17088279', '34832567'], months: 3, includeListingRow: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const r of items.filter((i) => i.type === 'occupancy')) console.log(r.name, r.month, r.occupancy_pct, r.rate_nightly, r.currency);
