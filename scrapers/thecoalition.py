from playwright.sync_api import sync_playwright

def get_jobs():
    url = "https://www.thecoalitionstudio.com/careers/"
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(5000)

            seen = set()

            job_data = page.evaluate(
                """
                () => {
                    let results = [];
                    let elements = document.querySelectorAll('h3, h4, h5, li, p, strong');
                    
                    for (let el of elements) {
                        let text = el.innerText.trim();
                        
                        if (!text || text.length < 3 || text.length > 80) continue;
                        
                        let lowerText = text.toLowerCase();
                        
                        // Comprehensive ignore list for site boilerplate and announcements
                        let ignoreList = [
                            "come work with us", "follow along", "follow us", "linkedin", 
                            "full-time positions", "contract roles", "internship opportunities", 
                            "about our studio", "acknowledging traditional territory", "privacy", 
                            "cookies", "terms of use", "xbox game studios", "open positions", 
                            "check back soon", "slide", "mug", "culture", "benefits"
                        ];
                        
                        if (ignoreList.some(ign => lowerText.includes(ign))) {
                            continue;
                        }
                        
                        let href = "";
                        let a = el.tagName === 'A' ? el : el.querySelector('a');
                        if (!a) {
                            let container = el.closest('div, section, article, li');
                            if (container) {
                                a = container.querySelector('a');
                            }
                        }
                        
                        if (a) {
                            href = a.href;
                        } else {
                            href = window.location.href;
                        }
                        
                        results.push({
                            title: text.split('\\n')[0].trim(),
                            url: href
                        });
                    }
                    return results;
                }
                """
            )

            for item in job_data:
                title = item.get("title", "").strip()
                href = item.get("url", "").strip()

                if title and href:
                    title = title.lstrip("•-—* ").strip()
                    lower_title = title.lower()
                    
                    skip_words = ["learn more", "content", "overview", "step", "supplier", "contact", "follow along"]
                    if any(w in lower_title for w in skip_words) or len(title) < 4:
                        continue

                    if title not in seen:
                        seen.add(title)
                        jobs.append({
                            "company": "The Coalition",
                            "title": title,
                            "url": href,
                            "location": "Vancouver, BC"
                        })

        except Exception:
            pass
        finally:
            browser.close()

    return jobs