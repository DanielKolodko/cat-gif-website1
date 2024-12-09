import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Drop the old table (if it exists) and create a new one
cursor.execute("DROP TABLE IF EXISTS gifs")
cursor.execute("""
    CREATE TABLE gifs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL
    )
""")

# Insert example GIF URLs
cursor.executemany("""
    INSERT INTO gifs (url) VALUES (?)
""", [
    ('https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif',),
    ('https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif',),
    ('https://media.giphy.com/media/3o7abkhOpu0NwenH3O/giphy.gif',),
    ('https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif',)
])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database initialized with sample GIF URLs!")
