import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/agoda-prices-scraper').call({
    hotelIds: ['6988894', '63820'], checkIn: '2026-10-10', nights: 3, adults: 2, currency: 'USD', calendarDays: 30,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const cheapest = items.filter(r => r.type === 'calendar' && r.cheapest_in_window);
console.log(cheapest.map(r => [r.hotel_name, r.check_in, r.price_nightly]));
