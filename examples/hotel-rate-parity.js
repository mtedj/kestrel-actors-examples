import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/hotel-rate-parity').call({ hotels: ['ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE'], checkIn: '30 days', nights: 1, minSpreadPct: 5 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const lines = items.filter(r => r.type === 'parity' && r.undercut_by.length).map(r => `${r.hotel_name} ${r.check_in}: ${r.min_source} ${r.min_price} vs direct ${r.official_price} (${r.undercut_pct}%)`);
console.log(lines.join('\n') || 'in parity');
