import pandas as pd

from src.config import VILLES, FORECAST_DAYS


def verifier_qualite(df):
    erreurs = []

    # 1. Valeurs manquantes
    nb_manquantes = df.isna().sum().sum()
    if nb_manquantes > 0:
        erreurs.append(f"{nb_manquantes} valeur(s) manquante(s)")

    # 2. Doublons
    nb_doublons = df.duplicated().sum()
    if nb_doublons > 0:
        erreurs.append(f"{nb_doublons} ligne(s) dupliquée(s)")

    # 3. Température hors limites
    nb_temp = (~df["temperature"].between(-10, 50)).sum()
    if nb_temp > 0:
        erreurs.append(f"{nb_temp} température(s) invalide(s)")

    # 4. Humidité hors limites
    nb_hum = (~df["humidite"].between(0, 100)).sum()
    if nb_hum > 0:
        erreurs.append(f"{nb_hum} humidité(s) invalide(s)")

    # 5. Nombre de lignes attendu
    attendu = len(VILLES) * FORECAST_DAYS * 24
    if len(df) != attendu:
        erreurs.append(f"{len(df)} ligne(s) au lieu de {attendu}")

    # 6. Dates valides
    if not pd.api.types.is_datetime64_any_dtype(df["time"]):
        erreurs.append("la colonne time n'est pas de type datetime")

    return erreurs