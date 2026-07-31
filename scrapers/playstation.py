import requests

def get_jobs():
    # PlayStation's global Greenhouse API endpoint covering all studios and corporate listings
    url = "https://boards-api.greenhouse.io/v1/boards/sonyinteractiveentertainmentglobal/jobs?content=true"
    
    jobs = []

    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        
        for job in data.get("jobs", []):
            title = job.get("title", "")
            location = job.get("location", {}).get("name", "Unknown")
            
            if title:
                jobs.append({
                    "company": "PlayStation",
                    "title": title.strip(),
                    "url": job.get("absolute_url", ""),
                    "location": location
                })
                
    except Exception as e:
        pass
        
    return jobs