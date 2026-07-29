import requests


def get_jobs():

    url = "https://api.smartrecruiters.com/v1/companies/PeopleCanFly/postings"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("content", []):

        jobs.append({
            "company": "People Can Fly",
            "title": job.get("name", ""),
            "url": job.get("ref", ""),
            "location": job.get("location", {}).get("city", "Unknown")
        })

    return jobs