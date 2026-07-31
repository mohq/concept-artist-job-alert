from playwright.sync_api import sync_playwright


def get_jobs():

    url = "https://careers.sledgehammergames.com/search-results?keywords=artist"

    jobs = []
    seen = set()


    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()


        def extract_jobs(data):

            if not isinstance(data, dict):
                return

            for job in data.get("jobs", []):

                title = job.get("title")

                if not title:
                    continue

                job_id = (
                    job.get("jobSeqNo")
                    or job.get("jobId")
                    or title
                )

                if job_id in seen:
                    continue

                seen.add(job_id)

                jobs.append(
                    {
                        "title": title,
                        "location": job.get("location", ""),
                        "url": job.get("applyUrl", "")
                    }
                )


        def log_response(response):

            if "/widgets" not in response.url:
                return

            try:
                data = response.json()

                if "latestJobs" in data:
                    extract_jobs(data["latestJobs"])

                if "leastAppliedJobs" in data:
                    extract_jobs(data["leastAppliedJobs"])

            except:
                pass


        page.on(
            "response",
            log_response
        )


        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        page.wait_for_timeout(8000)

        browser.close()


    return jobs