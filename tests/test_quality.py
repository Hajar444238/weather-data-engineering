import pandas as pd

from src.config import VILLES, FORECAST_DAYS
from src.quality import verifier_qualite

def creer_df_valide():
    """Fabrique un DataFrame que verifier_qualite doit accepter."""
    morceaux = []
    for ville in VILLES:
        df_ville = pd.DataFrame({
            "time": pd.date_range("2026-11-08", periods=FORECAST_DAYS * 24, freq="h"),
            "ville": ville,
            "temperature": 20.0,
            "humidite": 50.0,
        })
        morceaux.append(df_ville)
    return pd.concat(morceaux, ignore_index=True)

def test_donnees_valides():
    df = creer_df_valide()
    erreurs = verifier_qualite(df)
    assert erreurs == []

def test_temperature_invalide():
    df = creer_df_valide().copy()
    df.loc[0, "temperature"] = 999
    erreurs = verifier_qualite(df)
    assert len(erreurs) > 0


def test_humidite_invalide():
    df = creer_df_valide().copy()
    df.loc[0, "humidite"] = 150
    erreurs = verifier_qualite(df)
    assert len(erreurs) > 0

def test_valeur_manquante():
    df = creer_df_valide().copy()
    df.loc[0, "temperature"] = None
    erreurs = verifier_qualite(df)
    assert len(erreurs) > 0


def test_nombre_lignes_incorrect():
    df = creer_df_valide().iloc[:-5]
    erreurs = verifier_qualite(df)
    assert len(erreurs) > 0        