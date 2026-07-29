import requests

from config import KEYWORDS
from scrapers.hasbro import get_jobs


print("Downloading Hasbro jobs...\n")

jobs = get_jobs()

print(f"Downloaded {len(jobs)} Hasbro jobs.\n")

matches = 0

for job in jobs:

    title = job["title"]
    title_lower = title.lower()

    matched = False

    for keyword in KEYWORDS:
        if keyword.lower() in title_lower:
            matched = True
            break

    if matched:
        matches += 1

        print("=" * 60)
        print(f"Company : {job['company']}")
        print(f"Title   : {job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL     : {job['url']}")
        print()

print("=" * 60)
print(f"Found {matches} matching Concept Artist jobs.")