from playwright.sync_api import sync_playwright


def get_jobs():

    url = "https://www.turtlerockstudios.com/careers/"

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

        buttons = page.get_by_text(
            "VIEW ROLE"
        ).all()

        for button in buttons:

            try:

                # Move up several levels to get the job card
                card = button.locator(
                    "xpath=../../.."
                )

                text = card.inner_text()

                lines = [
                    x.strip()
                    for x in text.split("\n")
                    if x.strip()
                ]

                if not lines:
                    continue


                # Find the first meaningful line
                title = None

                for line in lines:

                    if line.upper() == "VIEW ROLE":
                        continue

                    if line.upper() in [
                        "ART",
                        "PRODUCTION",
                        "UI/UX",
                        "DESIGN",
                        "PROGRAMMING"
                    ]:
                        continue

                    title = line
                    break


                if not title:
                    continue


                href = button.get_attribute("href")


                if href and href.startswith("/"):
                    href = (
                        "https://www.turtlerockstudios.com"
                        + href
                    )


                jobs.append({
                    "company": "Turtle Rock Studios",
                    "title": title,
                    "url": href,
                    "location": "Unknown"
                })


            except Exception:
                pass


        browser.close()


    return jobs