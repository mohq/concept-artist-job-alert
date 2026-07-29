from playwright.sync_api import sync_playwright


def get_jobs():

    url = "https://jobs.zenimax.com/jobs"

    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        links = page.locator("a").all()

        for link in links:

            try:
                title = link.inner_text().strip()
                href = link.get_attribute("href")

                if title and href:

                    jobs.append({
                        "company": "ZeniMax",
                        "title": title,
                        "url": (
                            "https://jobs.zenimax.com"
                            + href
                            if href.startswith("/")
                            else href
                        ),
                        "location": "Unknown"
                    })

            except:
                pass

        browser.close()

    return jobs