# src/export_excel.py
from pathlib import Path
import pandas as pd

# ========= CONFIG =========
BASE_DIR = Path(__file__).resolve().parents[1]
CLEAN_DIR = BASE_DIR / "data" / "clean"
OUTPUT_FILE = BASE_DIR / "data" / "hospital_dataset_clean.xlsx"
# ==========================

def main():
    # Cargar datos limpios
    pacientes_path = CLEAN_DIR / "pacientes_clean.csv"
    citas_path = CLEAN_DIR / "citas_medicas_clean.csv"

    if not pacientes_path.exists() or not citas_path.exists():
        print("❌ No se encuentran los archivos limpios. Ejecuta primero clean.py")
        return

    pacientes = pd.read_csv(pacientes_path)
    citas = pd.read_csv(citas_path)

    # Exportar a Excel con dos hojas
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        pacientes.to_excel(writer, sheet_name="pacientes", index=False)
        citas.to_excel(writer, sheet_name="citas_medicas", index=False)

    print(f"✅ Archivo Excel generado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
