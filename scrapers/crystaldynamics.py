import requests


def get_jobs():

    url = "https://boards-api.greenhouse.io/v1/boards/crystaldynamics/jobs?content=true"

    jobs = []

    response = requests.get(
        url,
        timeout=30
    )

    data = response.json()

    for job in data.get("jobs", []):

        jobs.append(
            {
                "company": "Crystal Dynamics",
                "title": job.get("title", ""),
                "location": job.get("location", {}).get("name", ""),
                "url": job.get("absolute_url", "")
            }
        )

    return jobs