from config import KEYWORDS

from scrapers.hasbro import get_jobs as get_hasbro_jobs
from scrapers.peoplecanfly import get_jobs as get_peoplecanfly_jobs
from scrapers.zenimax import get_jobs as get_zenimax_jobs


SCRAPERS = [

    ("Hasbro", get_hasbro_jobs),

    ("People Can Fly", get_peoplecanfly_jobs),

    ("ZeniMax", get_zenimax_jobs),

]


print("Downloading jobs...\n")

jobs = []


for company_name, scraper in SCRAPERS:

    try:

        company_jobs = scraper()

        print(f"{company_name}: {len(company_jobs)} jobs")

        jobs.extend(company_jobs)

    except Exception as e:

        print(f"{company_name}: FAILED")
        print(f"Reason: {e}\n")


print(f"\nTotal jobs downloaded: {len(jobs)}\n")


matches = 0


for job in jobs:

    title = job["title"].lower()

    if any(keyword.lower() in title for keyword in KEYWORDS):

        matches += 1

        print("=" * 60)
        print(f"Company : {job['company']}")
        print(f"Title   : {job['title']}")
        print(f"Location: {job['location']}")
        print(f"URL     : {job['url']}")
        print()


print("=" * 60)
print(f"Found {matches} matching Concept Artist jobs.")