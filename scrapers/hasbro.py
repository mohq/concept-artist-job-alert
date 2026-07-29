import requests


def get_jobs():
    url = "https://boards-api.greenhouse.io/v1/boards/hasbro/jobs"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data["jobs"]:
        jobs.append({
            "company": "Hasbro",
            "title": job["title"],
            "url": job["absolute_url"],
            "location": job["location"]["name"]
                if job.get("location")
                else "Unknown"
        })

    return jobs