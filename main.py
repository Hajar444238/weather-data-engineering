
from src.extract import extraire_toutes_les_villes
from src.quality import verifier_qualite
from src.transform import transformer
from src.load import charger_parquet, charger_csv, charger_postgres
from src.logger import get_logger

# Initialisation du logger
logger = get_logger("WeatherPipeline")


def main():
    logger.info("Demarrage du pipeline Weather Data Engineering")

    # 1. Extraction
    logger.info("Debut de l'extraction des donnees meteorologiques")
    extraire_toutes_les_villes()
    logger.info("Extraction terminee")

    # 2. Transformation
    logger.info("Debut de la transformation")
    df = transformer()

    if df.empty:
        logger.warning("Aucune donnee a traiter. Arret du pipeline.")
        return

    # 3. Verification de la qualite
    logger.info("Verification de la qualite des donnees")
    erreurs = verifier_qualite(df)

    if erreurs:
        logger.error("Qualite insuffisante : %s", erreurs)
        return
    else:
        logger.info("Qualite des donnees suffisante")

    logger.info("Nombre de lignes a traiter : %d", len(df))

    # 4. Chargement
    logger.info("Debut du chargement des donnees")

    charger_parquet(df)
    charger_csv(df)
    charger_postgres(df)

    logger.info("Chargement termine avec succes")
    logger.info("Pipeline termine avec succes")


if __name__ == "__main__":
    main()
