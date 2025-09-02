# Weather Data Collector (London Edition)

Detta projekt hämtar väderdata för **London,GB** från [Open-Meteo API](https://open-meteo.com/en/docs),
sparar resultatet i en lokal **SQLite-databas**, och loggar allt i `logs/app.log`.

## Features
- Hämtar aktuell temperatur + väderstatus (Open-Meteo, ingen API-nyckel behövs).
- Sparar i SQLite `weatherdata.db` (tabell `weather_data`).
- Loggar i tydligt format: `YYYY-MM-DD HH:MM:SS,ms - INFO - ...`.
- Inkluderar pytest-test för databasen.

## Project Structure
```
weather_project/
├─ main.py
├─ test_main.py
├─ requirements.txt
├─ .gitignore
├─ weatherdata.db
├─ logs/
│  └─ app.log
└─ images/
   ├─ db_example_vscode.png
   ├─ logs_example_vscode.png
   └─ test_example_vscode.png
```

## Setup
```bash
git clone <repo-url>
cd weather_project
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Usage
```bash
python main.py --city "London,GB" --timezone "Europe/London"
```

## Database Example
![Database](images/db_example_vscode.png)

## Logging Example
![Logs](images/logs_example_vscode.png)

## Testing Example
![Testing](images/test_example_vscode.png)

## Logging
Exempelrader från `logs/app.log`:
```
2025-08-31 10:10:02,617 - INFO - Database setup complete.
2025-08-31 10:10:03,623 - INFO - Successfully fetched weather data for London,GB.
2025-08-31 10:10:03,642 - INFO - Data inserted successfully.
```

## Source (API)
- Open-Meteo Weather & Geocoding API (ingen API-nyckel krävs)
