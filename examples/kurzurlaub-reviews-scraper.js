import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('kestrel/kurzurlaub-reviews-scraper').call({
    startUrls: ['https://www.kurzurlaub.de/hotel/rhein_lahn_taunus/hachenburg/parkhotel-hachenburg.html'],
    maxReviewsPerHotel: 200,
    sinceDate: '90 days',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
const ratings = items.filter((r) => r.type === 'review');
console.log(ratings.length, 'ratings; with a comment:', ratings.filter((r) => r.text).length);
