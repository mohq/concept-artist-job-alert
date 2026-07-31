import argparse
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import KEYWORDS

from scrapers.hasbro import get_jobs as get_hasbro_jobs
from scrapers.peoplecanfly import get_jobs as get_peoplecanfly_jobs
from scrapers.zenimax import get_jobs as get_zenimax_jobs
from scrapers.wbgames import get_jobs as get_wbgames_jobs
from scrapers.arenanet import get_jobs as get_arenanet_jobs
from scrapers.turtlerock import get_jobs as get_turtlerock_jobs
from scrapers.sledgehammer import get_jobs as get_sledgehammer_jobs
from scrapers.crystaldynamics import get_jobs as get_crystaldynamics_jobs
from scrapers.bendstudio import get_jobs as get_bendstudio_jobs
from scrapers.playstation import get_jobs as get_playstation_jobs
from scrapers.twok import get_jobs as get_twok_jobs
from scrapers.thecoalition import get_jobs as get_coalition_jobs
from scrapers.kraftonmontreal import get_jobs as get_kraftonmontreal_jobs

SCRAPERS = [
    ("Hasbro", get_hasbro_jobs),
    ("People Can Fly", get_peoplecanfly_jobs),
    ("ZeniMax", get_zenimax_jobs),
    ("WB Games Montréal", get_wbgames_jobs),
    ("ArenaNet", get_arenanet_jobs),
    ("Turtle Rock Studios", get_turtlerock_jobs),
    ("Sledgehammer Games", get_sledgehammer_jobs),
    ("Crystal Dynamics", get_crystaldynamics_jobs),
    ("Bend Studio", get_bendstudio_jobs),
    ("PlayStation", get_playstation_jobs),
    ("2K Games", get_twok_jobs),
    ("The Coalition", get_coalition_jobs),
    ("Krafton Montreal", get_kraftonmontreal_jobs),
]

def send_email_alert(matches):
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    receiver_email = os.environ.get("EMAIL_TO")

    if not sender_email or not sender_password or not receiver_email:
        print("Email credentials not found. Skipping email alert.")
        return

    subject = f"Job Alert: {len(matches)} New Concept Art / Lighting Roles Found"
    
    body = "Here are the matching job openings found today:\n\n"
    for job in matches:
        body += f"Company : {job['company']}\n"
        body += f"Title   : {job['title']}\n"
        body += f"Location: {job['location']}\n"
        body += f"URL     : {job['url']}\n"
        body += "-" * 40 + "\n"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

parser = argparse.ArgumentParser(
    description="Concept Artist Job Monitor"
)

parser.add_argument(
    "--debug",
    action="store_true",
    help="Show detailed output"
)

args = parser.parse_args()

print("Downloading jobs...\n")

jobs = []

for company_name, scraper in SCRAPERS:
    try:
        company_jobs = scraper()
        print(f"✓ {company_name}: {len(company_jobs)} jobs")
        jobs.extend(company_jobs)

        if args.debug:
            for job in company_jobs:
                print(f"    • {job['title']}")
    except Exception as e:
        print(f"✗ {company_name}")
        print(f"    {e}")

print(f"\nTotal jobs downloaded: {len(jobs)}\n")

matches = []

for job in jobs:
    title = job["title"].lower()
    if any(keyword.lower() in title for keyword in KEYWORDS):
        matches.append(job)

print("=" * 60)
print(f"Found {len(matches)} matching Concept Artist jobs.\n")

for job in matches:
    print(f"Company : {job['company']}")
    print(f"Title   : {job['title']}")
    print(f"Location: {job['location']}")
    print(f"URL     : {job['url']}")
    print("=" * 60)

# Automatically trigger email alert if environment variables are present
send_email_alert(matches)