import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/tripadvisor-restaurant-reviews').call({
    startUrls: ['https://www.tripadvisor.com/Restaurant_Review-g35805-d429386-Reviews-The_Cheesecake_Factory-Chicago_Illinois.html'],
    maxReviewsPerLocation: 100,
    sinceDate: '90 days',
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
const reviews = items.filter((i) => i.type === 'review');
console.log(reviews.length, 'reviews,', reviews.filter((r) => r.response).length, 'answered by the owner');
