# kestrel/tiktok-profile-details | input checked against build 1.0.3 on 2026-11-11.
# Install: python -m pip install 'apify-client>=3.1,<4'
# Paid sample: $0.25 event-charge ceiling; may stop before completing the input.
# Change the sample targets before use. APIFY_TOKEN comes from your environment.
import json
import os
import sys
from datetime import timedelta
from urllib.request import Request, urlopen
from apify_client import ApifyClient

run_input = json.loads("{\n    \"usernames\": [\n        \"tiktok\"\n    ],\n    \"maxResults\": 3,\n    \"maxSources\": 3\n}")
token = os.environ["APIFY_TOKEN"]
# Start once: SDK3 HTTP retries could repeat a start after a lost response.
request = Request(
    "https://api.apify.com/v2/acts/kestrel~tiktok-profile-details/runs?timeout=300&restartOnError=false&maxTotalChargeUsd=0.25",
    data=json.dumps(run_input).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST",
)
with urlopen(request, timeout=60) as response:
    run_id = json.load(response)["data"]["id"]
print(f"Run {run_id} started; preserve this ID if a later request fails.", file=sys.stderr)
# SDK retries are safe here: polling and dataset retrieval only read existing data.
client = ApifyClient(token)
run = client.run(run_id).wait_for_finish(wait_duration=timedelta(seconds=360))
if run is None:
    raise RuntimeError("No run returned. Inspect Apify Console before starting another run.")
print(f"Run {run.id}: {run.status}; inspect its status, logs and summary.", file=sys.stderr)
# SDK 3 returns a typed Run object, not a dictionary. Keep all row types and nulls.
for item in client.dataset(run.default_dataset_id).iterate_items(clean=False):
    print(json.dumps(item, ensure_ascii=False))
if run.status != "SUCCEEDED":
    raise SystemExit("Run did not succeed; exported rows may be partial. Do not retry blindly.")
