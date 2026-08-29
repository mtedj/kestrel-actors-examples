import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<TOKEN>' });
const run = await client.actor('kestrel/google-hotels-prices').call({ hotels: ['https://www.google.com/travel/hotels/entity/ChkIhLCQwvjO2IYWGg0vZy8xMXE0bTZieDkyEAE'], checkIn: '30 days', checkOut: '32 days', currency: 'EUR' });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const official = Math.min(...items.filter(x => x.type === 'offer' && x.official).map(x => x.nightly));
const parityBreaches = items.filter(o => o.type === 'offer' && !o.official && o.nightly < official);
console.log(parityBreaches.map(o => [o.name, o.source, o.nightly]));
