import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
url = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(url)

requete = "SELECT ville, temperature FROM meteo WHERE temperature > 27"

with engine.connect() as conn:
    resultat = conn.execute(text(requete))
    for ligne in resultat:
        print(ligne)