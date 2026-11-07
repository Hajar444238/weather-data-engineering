import json
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

from main import RAW_DIR, PROCESSED_DIR

pd.set_option("display.max_columns", None)

# 1. Lecture des JSON (un tableau par ville)
villes = ["rabat", "casablanca", "tanger"]
liste_df = []

for ville in villes:
    chemin = RAW_DIR / f"{ville}_meteo.json"
    with open(chemin, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date
    df["heure"] = df["time"].dt.hour
    df["ville"] = ville
    df["latitude"] = data["latitude"]
    df["longitude"] = data["longitude"]
    liste_df.append(df)

# 2. Assemblage et renommage
df_final = pd.concat(liste_df, ignore_index=True)
df_final = df_final.rename(columns={
    "temperature_2m": "temperature",
    "relative_humidity_2m": "humidite",
})

# 3. Colonnes dérivées
df_final["chaud"] = df_final["temperature"] > 25


def periode(h):
    if h < 6:
        return "nuit"
    elif h < 12:
        return "matin"
    elif h < 18:
        return "apres-midi"
    else:
        return "soir"


df_final["periode"] = df_final["heure"].apply(periode)

# 4. Ajout de la région
df_villes = pd.DataFrame({
    "ville": ["rabat", "casablanca", "tanger"],
    "region": ["Rabat-Salé-Kénitra", "Casablanca-Settat", "Tanger-Tétouan-Al Hoceïma"],
})
df_final = df_final.merge(df_villes, on="ville", how="left")
print("Lignes :", len(df_final))

# 5. Sauvegarde dans processed/
df_final["date"] = pd.to_datetime(df_final["date"])
df_final.to_parquet(PROCESSED_DIR / "meteo.parquet", index=False)
df_final.to_csv(PROCESSED_DIR / "meteo.csv", index=False)

# 6. Envoi dans PostgreSQL
load_dotenv()
url = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(url)

df_final.to_sql("meteo", engine, if_exists="replace", index=False)
print("Table meteo chargée :", len(df_final), "lignes")