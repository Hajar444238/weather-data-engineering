import json
import pandas as pd
from main import RAW_DIR

pd.set_option("display.max_columns", None)

chemin_rabat = RAW_DIR / "rabat_meteo.json"
with open(chemin_rabat, "r", encoding="utf-8") as f:
    rabat_data = json.load(f) # load() = lit le fichier json et le transforme en dictionnaire Python
    rabat_df = pd.DataFrame(rabat_data["hourly"]) # DataFrame() = crée un DataFrame à partir d'un dictionnaire
    print(rabat_df.head()) # head() = affiche les 5 premières lignes du DataFrame
    print(rabat_df.info()) # info() = affiche des informations sur le DataFrame (nombre de lignes, colonnes, types de données, mémoire utilisée)
rabat_df["time"] = pd.to_datetime(rabat_df["time"]) # to_datetime() = convertit une colonne en datetime
print(rabat_df.info())
print(rabat_df["time"].dt.hour)
print(rabat_df["time"].dt.day)

# Ajoute deux colonnes "heure" et "date" au DataFrame
print("Ajout des colonnes 'date' et 'heure' au DataFrame :")
rabat_df["date"] = rabat_df["time"].dt.date
rabat_df["heure"] = rabat_df["time"].dt.hour
print(rabat_df.head())


rabat_df["ville"] = "Rabat"
print(rabat_df.head()) 