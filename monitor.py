from config import KEYWORDS

from scrapers.hasbro import get_jobs as get_hasbro_jobs
from scrapers.peoplecanfly import get_jobs as get_peoplecanfly_jobs
from scrapers.zenimax import get_jobs as get_zenimax_jobs


print("Downloading jobs...\n")


hasbro_jobs = get_hasbro_jobs()
print(f"Hasbro: {len(hasbro_jobs)} jobs")


peoplecanfly_jobs = get_peoplecanfly_jobs()
print(f"People Can Fly: {len(peoplecanfly_jobs)} jobs")


zenimax_jobs = get_zenimax_jobs()
print(f"ZeniMax: {len(zenimax_jobs)} jobs")


jobs = []

jobs.extend(hasbro_jobs)
jobs.extend(peoplecanfly_jobs)
jobs.extend(zenimax_jobs)


print(f"\nTotal jobs downloaded: {len(jobs)}\n")


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