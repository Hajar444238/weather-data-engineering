import json
import requests
from src.config import API_URL, RAW_DIR, VILLES, FORECAST_DAYS

def extraire_ville(nom, lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m",
        "forecast_days": FORECAST_DAYS,
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=10,
        )
    except requests.exceptions.RequestException:
        return None

    if response.status_code == 200:
        return response.json()

    return None


def extraire_toutes_les_villes():
    for nom, (lat, lon) in VILLES.items():
        data = extraire_ville(nom, lat, lon)

        if data is None:
            continue

        chemin = RAW_DIR / f"{nom}_meteo.json"

        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump( 
                data,
                fichier,
                indent=4,
                ensure_ascii=False,
            )


if __name__ == "__main__":
    extraire_toutes_les_villes()