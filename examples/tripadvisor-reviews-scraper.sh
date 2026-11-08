#!/usr/bin/env bash
# kestrel/tripadvisor-reviews-scraper | input checked against build 1.2.5 on 2026-11-08.
# Requires bash, curl and jq. Paid sample: $0.25 event-charge ceiling; may stop before completing the input.
# Change the sample targets before use. APIFY_TOKEN comes from your environment.
set -euo pipefail
: "${APIFY_TOKEN:?Set APIFY_TOKEN in your environment}"
api='https://api.apify.com/v2'
# Start once. A failed network response is not permission to start another paid run.
run=$(curl --silent --show-error --fail-with-body --max-time 60     -H "Authorization: Bearer $APIFY_TOKEN" -H 'Content-Type: application/json'     --data-binary @- "$api/acts/kestrel~tripadvisor-reviews-scraper/runs?timeout=300&restartOnError=false&maxTotalChargeUsd=0.25" <<'INPUT'
{
    "startUrls": [
        "https://www.tripadvisor.com/Hotel_Review-g189158-d4509998-Reviews-Memmo_Alfama_Hotel-Lisbon_Lisbon_District_Central_Portugal.html"
    ],
    "languages": [
        "en"
    ],
    "maxReviewsPerHotel": 3
}
INPUT
)
run_id=$(jq -er '.data.id' <<<"$run")
printf 'Run %s started; preserve this ID if a later request fails.\n' "$run_id" >&2
deadline=$((SECONDS + 360))
while true; do
    status=$(jq -er '.data.status' <<<"$run")
    case "$status" in SUCCEEDED|FAILED|TIMED-OUT|ABORTED) break ;; esac
    if (( SECONDS >= deadline )); then
        printf 'Run %s is still %s; inspect it in Apify Console. Do not start a duplicate.\n' "$run_id" "$status" >&2
        exit 2
    fi
    sleep 2
    run=$(curl --silent --show-error --fail-with-body --max-time 60         -H "Authorization: Bearer $APIFY_TOKEN" "$api/actor-runs/$run_id?waitForFinish=5")
done
printf 'Run %s: %s; inspect its status, logs and summary.\n' "$run_id" "$status" >&2
dataset_id=$(jq -er '.data.defaultDatasetId' <<<"$run")
offset=0
while true; do
    rows=$(curl --silent --show-error --fail-with-body --max-time 60         -H "Authorization: Bearer $APIFY_TOKEN"         "$api/datasets/$dataset_id/items?format=json&clean=false&offset=$offset&limit=100")
    jq -c '.[]' <<<"$rows"
    count=$(jq 'length' <<<"$rows")
    offset=$((offset + count))
    if (( count < 100 )); then break; fi
done
if [[ "$status" != SUCCEEDED ]]; then
    printf 'Exported rows may be partial; do not retry blindly.\n' >&2
    exit 1
fi
