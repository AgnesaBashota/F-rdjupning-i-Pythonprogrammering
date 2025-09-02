# pytest -q
import sqlite3
from main import setup_database, insert_weather

def test_insert(tmp_path):
    db = tmp_path / "weather.db"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE weather_data (id INTEGER PRIMARY KEY, timestamp TEXT, status TEXT, temperature REAL)")
    conn.commit(); conn.close()
    row = {"timestamp":"2025-08-31T10:10:02","status":"overcast clouds","temperature":18.5}
    conn = sqlite3.connect(str(db))
    conn.execute("INSERT INTO weather_data (timestamp,status,temperature) VALUES (?,?,?)",
                 (row["timestamp"], row["status"], row["temperature"]))
    conn.commit(); conn.close()
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM weather_data")
    n = cur.fetchone()[0]
    conn.close()
    assert n == 1
