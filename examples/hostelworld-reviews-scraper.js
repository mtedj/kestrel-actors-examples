import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/hostelworld-reviews-scraper').call({
    startUrls: ['https://www.hostelworld.com/hostels/p/15529/home-lisbon-hostel/'],
    maxReviewsPerProperty: 0,
    maxRating: 70,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((r) => r.type === 'review').length);
