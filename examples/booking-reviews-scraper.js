import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/booking-reviews-scraper').call({
    hotelNames: ['Memmo Alfama Lisbon'], maxReviewsPerHotel: 0, maxRating: 6, requireText: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const complaints = items.filter(r => r.type === 'review');
console.log(complaints.length, 'complaints;', complaints.filter(r => r.response).length, 'answered by the hotel');
