from playwright.sync_api import sync_playwright

def get_jobs():
    url = "https://jobs.zenimax.com/jobs"
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(8000)

            seen = set()

            job_links = page.evaluate(
                """
                () => {
                    let results = [];
                    // Only target links that point to actual ZeniMax job requisitions
                    let links = document.querySelectorAll('a[href*="/requisitions/view/"]');
                    
                    for (let a of links) {
                        let href = a.href;
                        let title = a.innerText.trim();
                        
                        if (!title || title.toLowerCase() === 'apply' || title.toLowerCase() === 'view') {
                            let container = a.closest('tr, div.job-card, div.row, li, div');
                            if (container) {
                                let heading = container.querySelector('h3, h4, h5, a.job-title, .title');
                                if (heading) {
                                    title = heading.innerText.trim();
                                } else {
                                    let firstLine = container.innerText.split('\\n')[0].trim();
                                    if (firstLine && firstLine.toLowerCase() !== 'apply') {
                                        title = firstLine;
                                    }
                                }
                            }
                        }
                        
                        let location = "Unknown";
                        let container = a.closest('tr, div.job-card, div.row, li, div');
                        if (container) {
                            let textContent = container.innerText;
                            let lines = textContent.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
                            for (let line of lines) {
                                if (line.includes(',') && line !== title) {
                                    location = line;
                                    break;
                                }
                            }
                        }

                        if (title && href) {
                            results.push({
                                title: title.split('\\n')[0].trim(),
                                url: href,
                                location: location
                            });
                        }
                    }
                    return results;
                }
                """
            )

            for item in job_links:
                title = item.get("title", "").strip()
                href = item.get("url", "").strip()
                location = item.get("location", "Unknown").strip()

                if not title or not href:
                    continue

                if title.lower() in ["apply", "apply now", "view", "learn more"] or len(title) < 4:
                    continue

                if href not in seen:
                    seen.add(href)
                    jobs.append({
                        "company": "ZeniMax",
                        "title": title,
                        "url": href,
                        "location": location
                    })

        except Exception:
            pass
        finally:
            browser.close()

    return jobs