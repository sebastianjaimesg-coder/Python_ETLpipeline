import sqlite3
from pathlib import Path
import pandas as pd

# Rutas
BASE_DIR = Path(__file__).resolve().parents[1]  # subimos un nivel
CLEAN_FILE = BASE_DIR / "data" / "hospital_dataset_clean.xlsx"
DW_FILE = BASE_DIR / "data_warehouse.db"

# Leer hojas
pacientes_df = pd.read_excel(CLEAN_FILE, sheet_name="pacientes")
citas_df = pd.read_excel(CLEAN_FILE, sheet_name="citas_medicas")

# Conexión a SQLite (o MySQL si quieres)
conn = sqlite3.connect(DW_FILE)

# Cargar tablas
pacientes_df.to_sql("dim_pacientes", conn, if_exists="replace", index=False)
citas_df.to_sql("fact_citas", conn, if_exists="replace", index=False)

conn.close()
print("Datos migrados a data_warehouse.db correctamente.")