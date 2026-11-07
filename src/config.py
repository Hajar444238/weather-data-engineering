from  pathlib import Path

FORECAST_DAYS = 3
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"              
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://api.open-meteo.com/v1/forecast"


VILLES = {
    "rabat": (34.0132, -6.8326),
    "casablanca": (33.5731, -7.5898),
    "tanger": (35.7595, -5.8340),
}

