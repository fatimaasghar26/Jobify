import json
import sqlite3
import urllib.request

api_url = "https://remoteok.com/api"

internship_keywords = ["intern", "internship"]
entry_level_keywords = ["junior", "entry level", "entry-level", "graduate", "trainee", "no experience needed"]

request = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
response = urllib.request.urlopen(request, timeout=15)
jobs = json.loads(response.read())[1:]  # first item is just site info, skip it

print(f"Fetched {len(jobs)} listings from RemoteOK.")

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

inserted = 0

for job in jobs:
    position = job.get("position", "")
    tags = job.get("tags", [])
    text = (position + " " + " ".join(tags)).lower()

    category = None
    if any(word in text for word in internship_keywords):
        category = "Internship"
    elif any(word in text for word in entry_level_keywords):
        category = "Entry-level"

    if category is None:
        continue

    location = (job.get("location") or "").strip().rstrip(",").strip()
    if not location:
        location = "Remote"

    salary_min = job.get("salary_min", 0)
    salary_max = job.get("salary_max", 0)
    if salary_min and salary_max:
        salary = f"${salary_min:,} - ${salary_max:,}"
    elif salary_min or salary_max:
        salary = f"${salary_min or salary_max:,}"
    else:
        salary = "Not disclosed"

    cursor.execute("""
        INSERT INTO jobs (title, company, location, category, deadline, link, salary, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (position, job.get("company", ""), location, category, "N/A",
          job.get("url") or job.get("apply_url", ""), salary, "RemoteOK"))
    inserted += 1

conn.commit()
conn.close()

print(f"RemoteOK scraping done! Inserted {inserted} entry-level/internship jobs out of {len(jobs)} total listings.")
