import json
import pandas as pd
from src.config import RAW_DIR, VILLES

REGIONS = {
    "rabat": "Rabat-Salé-Kénitra",
    "casablanca": "Casablanca-Settat",
    "tanger": "Tanger-Tétouan-Al Hoceïma",
}

def periode(h):
    if h < 6:
        return "nuit"
    elif h < 12:
        return "matin"
    elif h < 18:
        return "apres-midi"
    else:
        return "soir"


def transformer():
    liste_df = []

    for ville in VILLES:
        chemin = RAW_DIR / f"{ville}_meteo.json"

        if not chemin.exists():
            continue

        with open(chemin, "r", encoding="utf-8") as fichier:
            data = json.load(fichier) # Load the JSON data from the file

        df = pd.DataFrame(data["hourly"])

        df["time"] = pd.to_datetime(df["time"])
        df["date"] = df["time"].dt.date
        df["heure"] = df["time"].dt.hour
        df["ville"] = ville
        df["latitude"] = data["latitude"]
        df["longitude"] = data["longitude"]

        liste_df.append(df)

    if not liste_df:
        return pd.DataFrame()

    df_final = pd.concat(liste_df, ignore_index=True)

    df_final = df_final.rename(
        columns={
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidite",
        }
    )

    df_final["chaud"] = df_final["temperature"] > 25

    df_final["periode"] = df_final["heure"].apply(periode)

    df_regions = pd.DataFrame(
        list(REGIONS.items()),
        columns=["ville", "region"],
    )

    df_final = df_final.merge(
        df_regions,
        on="ville",
        how="left",
    )

    df_final["date"] = pd.to_datetime(df_final["date"])

    return df_final