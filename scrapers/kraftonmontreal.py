import requests

def get_jobs():
    url = "https://boards-api.greenhouse.io/v1/boards/studiokraftonboard/jobs?content=true"
    jobs = []

    try:
        response = requests.get(url, timeout=30)
        data = response.json()

        for job in data.get("jobs", []):
            jobs.append({
                "company": "Krafton Montreal",
                "title": job.get("title", ""),
                "location": job.get("location", {}).get("name", "Montreal, QC"),
                "url": job.get("absolute_url", "")
            })
    except Exception as e:
        pass

    return jobs