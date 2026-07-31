from playwright.sync_api import sync_playwright


def get_jobs():

    url = "https://www.arena.net/en/careers"

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

        # Get all links after JavaScript loads
        links = page.locator("a").all()

        for link in links:

            try:

                title = link.inner_text().strip()
                href = link.get_attribute("href")

                if not title or not href:
                    continue


                # ArenaNet job pages contain /careers/
                if "/careers/" in href:

                    if href.startswith("/"):
                        href = "https://www.arena.net" + href

                    jobs.append({
                        "company": "ArenaNet",
                        "title": title,
                        "url": href,
                        "location": "Bellevue, WA"
                    })

            except:
                pass


        browser.close()


    return jobs