"""Minimal example: run the builtin-jobs-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "maxItems": 50,
    "includeDescription": True,
}

run = client.actor("bibian/builtin-jobs-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    location = item.get("city") or ("Remote" if item.get("isRemote") else "-")
    print(f"{item['title']} | {item.get('companyName')} | {location} | {item.get('salaryMin')}-{item.get('salaryMax')}")
print(f"{count} results")
