import sqlite3
from pathlib import Path
import pandas as pd

# Routes
BASE_DIR = Path(__file__).resolve().parents[1]  # we moved up a level
CLEAN_FILE = BASE_DIR / "data" / "hospital_dataset_clean.xlsx"
DW_FILE = BASE_DIR / "data_warehouse.db"

# Read Excel sheets
pacientes_df = pd.read_excel(CLEAN_FILE, sheet_name="pacientes")
citas_df = pd.read_excel(CLEAN_FILE, sheet_name="citas_medicas")

# Connection to SQLite
conn = sqlite3.connect(DW_FILE)

# Load tables
pacientes_df.to_sql("dim_pacientes", conn, if_exists="replace", index=False)
citas_df.to_sql("fact_citas", conn, if_exists="replace", index=False)

conn.close()

print("Datos migrados a data_warehouse.db correctamente.")
