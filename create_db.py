import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect("database.db")

# Create users table
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print(" Database and users table created successfully!")