import sqlite3

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    category TEXT,
    deadline TEXT,
    link TEXT UNIQUE,
    salary TEXT,
    source TEXT
);
""")

conn.commit()
conn.close()

print("Database is ready.")
