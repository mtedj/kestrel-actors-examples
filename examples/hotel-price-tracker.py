from apify_client import ApifyClient
client = ApifyClient("<TOKEN>")
run = client.actor("kestrel/hotel-price-tracker").call(run_input={
    "hotelNames": ["Hyatt Regency Lisbon", "Altis Grand Hotel Lisbon"], "checkIn": "30 days", "days": 14, "nights": 2, "currency": "EUR", "country": "pt"})
rows = [r for r in client.dataset(run["defaultDatasetId"]).iterate_items() if r["type"] == "rate" and r["cheapest_in_window"]]
for r in rows: print(r["hotel_name"], r["check_in"], r["price"], r["currency"], "at", r["source"], "direct" if r["official"] else f'(direct {r["official_price"]})', r["source_url"])
