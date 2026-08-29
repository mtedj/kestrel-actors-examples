import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_API_TOKEN>' });
const run = await client.actor('kestrel/trustpilot-reviews-scraper').call({
    companyDomains: ['www.monzo.com'],
    maxReviewsPerCompany: 100,
    minRating: 1,
    maxRating: 2,
    requireText: true,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'reviews');
