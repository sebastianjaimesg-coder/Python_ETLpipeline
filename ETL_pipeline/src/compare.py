from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "data" / "interim"   # datos iniciales del explore.py
CLEAN = BASE_DIR / "data" / "clean"   # datos después de clean.py

def summary(df, name):
    return {
        "tabla": name,
        "filas": len(df),
        "nulos_totales": df.isna().sum().sum(),
        "duplicados": df.duplicated().sum()
    }

def main():
    pacientes_raw = pd.read_csv(RAW / "pacientes_raw.csv")
    citas_raw = pd.read_csv(RAW / "citas_medicas_raw.csv")

    pacientes_clean = pd.read_csv(CLEAN / "pacientes_clean.csv")
    citas_clean = pd.read_csv(CLEAN / "citas_medicas_clean.csv")

    resumen = [
        summary(pacientes_raw, "pacientes_raw"),
        summary(pacientes_clean, "pacientes_clean"),
        summary(citas_raw, "citas_raw"),
        summary(citas_clean, "citas_clean")
    ]

    print(pd.DataFrame(resumen))

if __name__ == "__main__":
    main()
