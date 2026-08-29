import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/tripadvisor-reviews-scraper').call({
    hotelNames: ['Memmo Alfama Lisbon', 'The Lumiares Lisbon'],
    sinceDate: '30 days',
    includeTranslated: false,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter(r => r.type === 'review');
console.log(reviews.length, 'reviews;', reviews.filter(r => r.response).length, 'answered by the hotel');
