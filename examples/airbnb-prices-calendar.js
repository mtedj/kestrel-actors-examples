import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/airbnb-prices-calendar').call({ listingIds: ['11562247'], checkIn: '30 days', checkOut: '33 days', includeDetails: true, calendarMonths: 12 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter(r => r.type === 'calendar').map(r => [r.id, r.occupancy_90, r.next_available]));
