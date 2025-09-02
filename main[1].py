#!/usr/bin/env python3
"""
Weather Data Collector (London Edition)
- Hämtar väderdata för London,GB via Open-Meteo
- Sparar i SQLite (weather_data)
- Loggar till logs/app.log
"""
import argparse, os, sqlite3, logging, sys
import requests

def get_logger() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("weather")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s,%(msecs)03d - %(levelname)s - %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")
        fh = logging.FileHandler(os.path.join("logs", "app.log"), encoding="utf-8")
        sh = logging.StreamHandler()
        fh.setFormatter(fmt)
        sh.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger

logger = get_logger()
DB_FILE = "weatherdata.db"

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            temperature REAL NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()
    logger.info("Database setup complete.")

def geocode_city(city: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1}, timeout=30)
    r.raise_for_status()
    res = r.json()["results"][0]
    return res["latitude"], res["longitude"]

WMO_MAP = {0:"clear sky",1:"mainly clear",2:"partly cloudy",3:"overcast clouds",61:"rain: slight",63:"rain: moderate",65:"rain: heavy"}

def fetch_weather(lat, lon, timezone):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude":lat,"longitude":lon,"hourly":["temperature_2m","weathercode"],
              "timezone":timezone,"forecast_days":1}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()["hourly"]
    ts, temp, code = data["time"][-1], data["temperature_2m"][-1], data["weathercode"][-1]
    return {"timestamp":ts,"status":WMO_MAP.get(code,"unknown"),"temperature":temp}

def insert_weather(row):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO weather_data (timestamp,status,temperature) VALUES (?,?,?)",
                (row["timestamp"], row["status"], row["temperature"]))
    conn.commit()
    conn.close()
    logger.info("Data inserted successfully.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--city", default="London,GB")
    ap.add_argument("--timezone", default="Europe/London")
    args = ap.parse_args()
    try:
        setup_database()
        lat, lon = geocode_city(args.city)
        logger.info(f"Successfully fetched weather data for {args.city}.")
        row = fetch_weather(lat, lon, args.timezone)
        insert_weather(row)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__=="__main__":
    main()
