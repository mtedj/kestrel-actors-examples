import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/hotel-price-tracker').call({ hotels: ['ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE'], checkIn: '2026-10-09', days: 3, nights: 2, maxPrice: 300 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const hits = items.filter(r => r.type === 'rate').map(r => `${r.hotel_name} ${r.check_in}: ${r.price} ${r.currency} at ${r.source} ${r.source_url}`);
console.log(hits.join('\n') || 'nothing under target yet');
