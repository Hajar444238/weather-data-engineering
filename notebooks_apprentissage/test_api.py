import requests
import json
from main import RAW_DIR

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 34.0132,
    "longitude": -6.8326,
    "hourly": "temperature_2m,relative_humidity_2m",
    "forecast_days": 3,
}
villes = {
    "rabat": (34.0132, -6.8326),
    "casablanca": (33.5731, -7.5898),
    "tanger": (35.7595, -5.8340),
}

for ville, (lat, lon) in villes.items():
    params["latitude"] = lat
    params["longitude"] = lon
    print(f"Récupération des données pour {ville} (lat: {lat}, lon: {lon})")

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau pour {ville} :", e)
        continue 

    print("Status code :", response.status_code)

    if response.status_code == 200:
        chemin = RAW_DIR / f"{ville}_meteo.json"
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        print(f"Données de {ville} sauvegardées dans {chemin}")
    else:
        print(f"Erreur pour {ville} :", response.status_code)
        print("Rien n'a été sauvegardé.")