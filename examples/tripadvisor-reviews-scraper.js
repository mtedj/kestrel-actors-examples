// kestrel/tripadvisor-reviews-scraper | input checked against build 1.2.5 on 2026-11-08.
// Install: npm install 'apify-client@^2'
// Paid sample: $0.25 event-charge ceiling; may stop before completing the input.
// Change the sample targets before use. APIFY_TOKEN comes from your environment.
const { ApifyClient } = require('apify-client');
const input = {
    "startUrls": [
        "https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon_Lisbon_District_Central_Portugal.html"
    ],
    "languages": [
        "en"
    ],
    "maxReviewsPerHotel": 3
};

async function main() {
    if (!process.env.APIFY_TOKEN) throw new Error('Set APIFY_TOKEN in your environment.');
    // Do not automatically repeat a paid start request after a network failure.
    const client = new ApifyClient({ token: process.env.APIFY_TOKEN, maxRetries: 0 });
    const run = await client.actor("kestrel/tripadvisor-reviews-scraper").call(input, {
        maxTotalChargeUsd: 0.25,
        timeout: 300, restartOnError: false, log: null,
    });
    if (!run) throw new Error('No run returned. Inspect Apify Console before another start.');
    console.error(`Run ${run.id}: ${run.status}; inspect its status, logs and summary.`);
    // Paginate and retain all row types, hidden fields and nulls.
    const dataset = client.dataset(run.defaultDatasetId);
    let offset = 0;
    while (true) {
        const { items } = await dataset.listItems({ offset, limit: 100, clean: false });
        for (const item of items) console.log(JSON.stringify(item));
        offset += items.length;
        if (items.length < 100) break;
    }
    if (run.status !== 'SUCCEEDED') {
        throw new Error('Run did not succeed; exported rows may be partial. Do not retry blindly.');
    }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
