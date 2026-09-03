from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

JOBS_PER_PAGE = 9


def get_jobs(category, search, page):

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    query = """
        SELECT title, company, location, category,
               deadline, link, salary
        FROM jobs
        WHERE 1=1
    """
    params = []
    # Category filter
    if category != "All":
        query += " AND category = ?"
        params.append(category)

    # Search filter
    if search:
        query += " AND title LIKE ?"
        params.append("%" + search + "%")

    # Count total jobs
    count_query = """
        SELECT COUNT(*)
        FROM jobs
        WHERE 1=1
    """
    count_params = []
    if category != "All":
        count_query += " AND category = ?"
        count_params.append(category)
    if search:
        count_query += " AND title LIKE ?"
        count_params.append("%" + search + "%")
    cursor.execute(count_query, count_params)
    total_jobs = cursor.fetchone()[0]
    # Pagination
    offset = (page - 1) * JOBS_PER_PAGE
    query += " LIMIT ? OFFSET ?"
    params.extend([JOBS_PER_PAGE, offset])
    cursor.execute(query, params)
    jobs = cursor.fetchall()
    conn.close()
    return jobs, total_jobs


def days_left(deadline):
    try:
        deadline_date = datetime.strptime(deadline, "%b %d, %Y")
        return (deadline_date - datetime.today()).days
    except (ValueError, TypeError):
        return None


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def home():
    category = request.args.get("category", "All")
    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)
    jobs, total_jobs = get_jobs(category, search, page)
    jobs_with_days = []
    for job in jobs:
        remaining = days_left(job[4])
        jobs_with_days.append(job + (remaining,))
    total_pages = (total_jobs + JOBS_PER_PAGE - 1) // JOBS_PER_PAGE

    return render_template(
        "index.html",
        jobs=jobs_with_days,
        selected_category=category,
        search_query=search,
        page=page,
        total_pages=total_pages,
        total_jobs=total_jobs,
    )


if __name__ == "__main__":
    app.run(debug=True)
