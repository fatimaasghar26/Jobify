from playwright.sync_api import sync_playwright
import sqlite3

BASE_URL = "https://www.mustakbil.com"
SEARCH_URLS = [
    (BASE_URL + "/jobs/search?countryid=162&keywords=internship", "Internship"),
    (BASE_URL + "/jobs/search?countryid=162&keywords=entry%20level", "Entry-level"),
    (BASE_URL + "/jobs/pakistan/online", "Entry-level"),
]

# Connect to database
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for url, category in SEARCH_URLS:
        print("\nOpening:", url)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector(".jl-card", timeout=15000)
        except Exception:
            print("No jobs found. Skipping...")
            continue
        cards = page.query_selector_all(".jl-card")
        print("Jobs found:", len(cards))
        for card in cards:
            try:
                # Job title
                title_element = card.query_selector(".jc-title__link")
                if not title_element:
                    continue
                title = title_element.inner_text().strip()
                link = title_element.get_attribute("href")
                if link and link.startswith("/"):
                    link = BASE_URL + link
                # Company
                company_element = card.query_selector(".jc-byline__company")
                company = (
                    company_element.inner_text().strip()
                    if company_element
                    else "Unknown"
                )
                # Location
                location_element = card.query_selector(".jc-byline__place")
                location = (
                    location_element.inner_text().strip()
                    if location_element
                    else "Pakistan"
                )
                # Salary
                salary_element = card.query_selector(".jc-pay")
                salary = (
                    salary_element.inner_text().replace("\n", " ").strip()
                    if salary_element
                    else "Not disclosed"
                )
                # Check for duplicate
                cursor.execute("SELECT id FROM jobs WHERE link = ?", (link,))
                exists = cursor.fetchone()
                if exists:
                    print("Already exists:", title)
                    continue
                # Save job
                cursor.execute(
                    """
                    INSERT INTO jobs
                    (
                        title,
                        company,
                        location,
                        category,
                        deadline,
                        link,
                        salary,
                        source
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        title,
                        company,
                        location,
                        category,
                        "N/A",
                        link,
                        salary,
                        "Mustakbil",
                    ),
                )
                print("Added:", title)
            except Exception as error:

                print("Skipped job:", error)
    browser.close()
# Save changes
conn.commit()
conn.close()
print("\nScraping complete!")
