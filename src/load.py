import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.config import PROCESSED_DIR

def charger_parquet(df):
    chemin = PROCESSED_DIR / "meteo.parquet"
    df.to_parquet(chemin, index=False)

def charger_postgres(df):
    load_dotenv()

    url = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    engine = create_engine(url) 

    try:
        df.to_sql(
            "meteo",
            engine,
            if_exists="replace",
            index=False,
        )
    finally:
        engine.dispose()


def charger_csv(df):
    chemin = PROCESSED_DIR / "meteo.csv"
    df.to_csv(chemin, index=False)