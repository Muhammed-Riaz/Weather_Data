from flask import Flask, render_template, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

app = Flask(__name__)

def fetch_weather_data():
    """Website se data scrape karega aur CSV me save karega."""
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Browser ko background me run karega
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 🌍 Target Website
    url = "https://www.wunderground.com/dashboard/pws/KKYLOUIS329/table/2025-02-17/2025-02-17/daily"
    driver.get(url)
    time.sleep(5)  # Wait for page to load

    try:
        # 🔍 Extract data from table
        table_div = driver.find_element(By.CLASS_NAME, "history-tabs")
        weather_data = table_div.text.split("\n")  # Data list me convert karein
        
        # ✅ Save data to CSV
        csv_file = "weather_data.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Weather Data"])  # Header row
            for row in weather_data:
                writer.writerow([row])
        
        print("✅ Data saved successfully in CSV!")
    except Exception as e:
        print("❌ Error:", e)
    
    driver.quit()

@app.route('/')
def home():
    """Home page where user can download the CSV file."""
    return render_template("index.html")

@app.route('/download')
def download_file():
    """Allow user to download the weather data CSV file."""
    return send_file("weather_data.csv", as_attachment=True)

if __name__ == "__main__":
    fetch_weather_data()  # Scrape data & save to CSV
    app.run(debug=True)
