# Jobify

Jobify is a simple job board website for students and entry-level job seekers in Pakistan.
It collects job listings from different sources and displays them in one place. Users can search jobs, filter them by category, and apply through the original job posting.

## Features

* Search for jobs
* Filter jobs by category
* Entry-level and internship jobs
* Salary information when available
* Job location
* Apply button linking to the original job
* Dark mode
* Jobs collected from Mustakbil and Remote OK
* SQLite database for storing jobs
* Duplicate job checking

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript
* Playwright

## Project Structure

```text
Jobify/
│
├── app.py
├── jobs.db
├── scraper_mustakbil.py
├── scraper_remoteok.py
├── delete_jobs.py
│
├── templates/
│   ├── index.html
│   └── about.html
│
└── static/
    └── style.css
```

## How to Run

### 1. Install dependencies

```bash
pip install flask playwright
```

Then install the Playwright browser:

```bash
playwright install
```

### 2. Run the scrapers

Run the Mustakbil scraper:

```bash
python scraper_mustakbil.py
```

Run the Remote OK scraper:

```bash
python scraper_remoteok.py
```

### 3. Start the Flask application

```bash
python app.py
```

Open the website in your browser at:

```text
http://127.0.0.1:5000
```

## Database

Jobify uses SQLite to store job listings in `jobs.db`.

The database stores information such as:

* Job title
* Company
* Location
* Category
* Deadline
* Application link
* Salary
* Source

The scrapers check existing job links to help prevent duplicate listings when they are run again.

## Delete All Jobs

If you want to remove all existing jobs and scrape fresh listings, run:

```bash
python delete_jobs.py
```

This deletes the jobs but keeps the database table.

## Job Sources

Currently, jobs are collected from:

* Mustakbil
* Remote OK

## Future Improvements

* Add more job sources
* Add actual job deadlines
* Add more categories
* Add sorting options
* Improve job filtering
* Add user accounts and saved jobs

## License

This project is for educational purposes.
