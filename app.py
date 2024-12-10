from flask import Flask, render_template
import sqlite3
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use environment variables in the app
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database.db')  # Fallback to default if not found
SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')


app = Flask(__name__)

# Function to get a random GIF URL from the database
def get_random_cat_gif():
    # Connect to the database
    conn = sqlite3.connect(os.getenv('DATABASE_URL', 'database.db'))
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

# Route for the home page
@app.route('/')
def index():
    random_gif = get_random_cat_gif()
    if random_gif:
        return render_template('index.html', gif_url=random_gif)
    else:
        return "No GIFs available!", 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
