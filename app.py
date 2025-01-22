from flask import Flask, render_template
import sqlite3
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Retrieve environment variables
DATABASE_URL = os.getenv('DATABASE_URL', 'database.db')  # Default to 'database.db' if not set
SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
PORT = int(os.getenv('PORT', 5000))

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Function to get a random GIF URL from the database
def get_random_cat_gif():
    # Resolve the correct path to the SQLite database
    db_path = DATABASE_URL
    if db_path.startswith("sqlite:///"):
        db_path = db_path.replace("sqlite:///", "")  # Remove the prefix for sqlite3 compatibility

    # Connect to the database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch all GIF URLs from the database
        cursor.execute("SELECT url FROM gifs")
        all_gifs = cursor.fetchall()
        conn.close()

        # If there are no GIFs, return None
        if not all_gifs:
            return None

        # Pick a random GIF URL
        return random.choice(all_gifs)[0]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

# Route for the home page
@app.route('/')
def index():
    random_gif = get_random_cat_gif()
    if random_gif:
        return render_template('index.html', gif_url=random_gif)
    else:
        return "No GIFs available or database error!", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)

