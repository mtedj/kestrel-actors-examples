import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/indeed-company-reviews').call({
    companies: ['Google'],
    countries: ['all'],
    maxReviewsPerCompany: 1000,
    sinceDate: '90 days',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.filter((i) => i.type === 'review').length, 'employee reviews');
