import requests
from bs4 import BeautifulSoup


def get_jobs():

    url = "https://wbgamesmontreal.com/careers/"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    jobs = []

    # Every job links to /jobs/...
    for link in soup.select('a[href*="/jobs/"]'):

        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        if href.startswith("/"):
            href = "https://wbgamesmontreal.com" + href

        jobs.append({
            "company": "WB Games Montréal",
            "title": title,
            "url": href,
            "location": "Montréal, QC"
        })

    return jobs