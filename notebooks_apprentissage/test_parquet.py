import pandas as pd
from main import PROCESSED_DIR

pd.set_option("display.max_columns", None)

df = pd.read_parquet(PROCESSED_DIR / "meteo.parquet")
print(df.head())
df.info()