import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/hrs-reviews-scraper').call({
    startUrls: ['https://www.hrs.com/en/hotel/10520'],
    maxReviewsPerHotel: 100,
    proxyConfiguration: { useApifyProxy: true, apifyProxyGroups: ['RESIDENTIAL'] },
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter(r => r.type === 'review');
console.log(reviews.length, 'reviews;', reviews.filter(r => r.hotel_reply).length, 'answered by the hotel');
