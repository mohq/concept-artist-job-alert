import requests

def get_jobs():

    # PlayStation's global Greenhouse API
    url = "https://boards-api.greenhouse.io/v1/boards/sonyinteractiveentertainmentglobal/jobs?content=true"
    
    jobs = []

    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        
        for job in data.get("jobs", []):
            
            title = job.get("title", "")
            location = job.get("location", {}).get("name", "")
            
            # Sony categorizes studios by department. Let's grab all department names for this job.
            departments = [dept.get("name", "") for dept in job.get("departments", [])]
            
            # Check if this specific job belongs to Bend Studio
            is_bend_studio = False
            
            if "Bend" in location:
                is_bend_studio = True
                
            for dept in departments:
                if "Bend Studio" in dept or "Bend" in dept:
                    is_bend_studio = True
                    
            if is_bend_studio:
                jobs.append({
                    "company": "Bend Studio",
                    "title": title.strip(),
                    "url": job.get("absolute_url", ""),
                    "location": location
                })
                
    except Exception as e:
        pass
        
    return jobs