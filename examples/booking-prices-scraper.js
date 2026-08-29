import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/booking-prices-scraper').call({
    hotelIds: ['536251', '2251985'], checkIn: '30 days', nights: 1, adults: 2, currency: 'USD', includeRooms: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const hotels = items.filter(r => r.type === 'hotel');
console.log(hotels.map(h => [h.name, h.price_nightly, h.free_cancellation]));
