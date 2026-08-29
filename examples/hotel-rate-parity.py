from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/hotel-rate-parity").call(run_input={
    "hotelNames": ["Hyatt Regency Lisbon", "Altis Grand Hotel Lisbon"], "checkIn": "30 days", "nights": 2, "sweepDays": 6, "currency": "EUR", "country": "pt"})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "parity"]
for r in sorted(rows, key=lambda r: -(r["undercut_pct"] or 0)):
    if r["undercut_by"]: print(r["hotel_name"], r["check_in"], f'{r["undercut_pct"]}% under direct via {r["undercut_by"][0]} ({r["min_price"]} vs {r["official_price"]} {r["currency"]})')
