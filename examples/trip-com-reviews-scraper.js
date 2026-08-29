import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/trip-com-reviews-scraper').call({
    startUrls: ['https://www.trip.com/hotels/lisbon-hotel-detail-2561632/valverde-hotel/'],
    maxReviewsPerHotel: 200,
    languages: ['English'],
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter((r) => r.type === 'review');
console.log(reviews.length, 'reviews; replied to:', reviews.filter((r) => r.response).length);
