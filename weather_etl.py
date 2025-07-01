import requests
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITY = "Kathmandu"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Fetch data from API
response = requests.get(URL)
if response.status_code != 200:
    print("❌ Failed to fetch weather data")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    exit()

data = response.json()

# Extract useful fields
weather_data = {
    "city": data["name"],
    "temperature": data["main"]["temp"],
    "description": data["weather"][0]["description"],
    "humidity": data["main"]["humidity"],
    "wind_speed": data["wind"]["speed"],
    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Connect to SQLite
conn = sqlite3.connect("database/weather.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    temperature REAL,
    description TEXT,
    humidity INTEGER,
    wind_speed REAL,
    datetime TEXT
)
''')

# Insert the data
cursor.execute('''
INSERT INTO weather (city, temperature, description, humidity, wind_speed, datetime)
VALUES (:city, :temperature, :description, :humidity, :wind_speed, :datetime)
''', weather_data)

conn.commit()
conn.close()

print("✅ Weather data saved successfully.")
