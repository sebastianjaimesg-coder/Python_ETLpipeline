# src/clean.py
from pathlib import Path
import pandas as pd
from datetime import datetime
from dateutil import parser

# ========= CONFIG =========
BASE_DIR = Path(__file__).resolve().parents[1]
INTERIM_DIR = BASE_DIR / "data" / "interim"
CLEAN_DIR = BASE_DIR / "data" / "clean"
REPORTS_DIR = BASE_DIR / "reports"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
# ==========================

def standardize_dates(df, col):
    """Convierte cualquier formato de fecha a YYYY-MM-DD si es posible"""
    def parse_date(x):
        if pd.isna(x):
            return None
        try:
            return parser.parse(str(x), dayfirst=True).date()
        except:
            return None
    if col in df.columns:
        df[col] = df[col].apply(parse_date)
    return df

def recalc_age(df, birth_col, age_col):
    """Recalcula edad usando fecha_nacimiento"""
    today = datetime.today().date()
    if birth_col in df.columns:
        df["edad_calc"] = df[birth_col].apply(
            lambda d: today.year - d.year - ((today.month, today.day) < (d.month, d.day))
            if pd.notna(d) else None
        )
        if age_col in df.columns:
            df[age_col] = df.apply(
                lambda r: r["edad_calc"] if pd.notna(r["edad_calc"]) else r[age_col],
                axis=1
            )
        else:
            df[age_col] = df["edad_calc"]
        df.drop(columns=["edad_calc"], inplace=True)
    return df

def normalize_sex(df, col):
    """Normaliza valores de sexo"""
    mapping = {
        "male": "M", "m": "M", "masculino": "M",
        "female": "F", "f": "F", "femenino": "F"
    }
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower().map(mapping).fillna(df[col])
    return df

def remove_duplicates(df, subset_cols):
    """Elimina duplicados basados en columnas clave"""
    before = len(df)
    df = df.drop_duplicates(subset=subset_cols, keep="first")
    after = len(df)
    return df, before - after

def validate_integrity(citas_df, pacientes_df):
    """Devuelve citas con pacientes inexistentes"""
    if "id_paciente" in citas_df.columns and "id_paciente" in pacientes_df.columns:
        orphan_citas = citas_df[~citas_df["id_paciente"].isin(pacientes_df["id_paciente"])]
        return orphan_citas
    return pd.DataFrame()

def main():
    # --- Cargar datos intermedios ---
    pacientes = pd.read_csv(INTERIM_DIR / "pacientes_raw.csv")
    citas = pd.read_csv(INTERIM_DIR / "citas_medicas_raw.csv")

    # --- Limpieza de pacientes ---
    pacientes = standardize_dates(pacientes, "fecha_nacimiento")
    pacientes = recalc_age(pacientes, "fecha_nacimiento", "edad")
    pacientes = normalize_sex(pacientes, "sexo")
    pacientes, dup_pac = remove_duplicates(pacientes, ["id_paciente"])

    # --- Limpieza de citas ---
    citas = standardize_dates(citas, "fecha_cita")
    citas, dup_citas = remove_duplicates(citas, ["id_cita"])

    # --- Validación cruzada ---
    orphan_citas = validate_integrity(citas, pacientes)

    # --- Guardar datos limpios ---
    pacientes.to_csv(CLEAN_DIR / "pacientes_clean.csv", index=False)
    citas.to_csv(CLEAN_DIR / "citas_medicas_clean.csv", index=False)

    # --- Guardar reporte de limpieza ---
    report_path = REPORTS_DIR / "cleaning_summary.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Resumen de limpieza de datos\n\n")
        f.write(f"- Pacientes eliminados por duplicados: {dup_pac}\n")
        f.write(f"- Citas eliminadas por duplicados: {dup_citas}\n")
        f.write(f"- Citas huérfanas (sin paciente): {len(orphan_citas)}\n")

    if not orphan_citas.empty:
        orphan_citas.to_csv(REPORTS_DIR / "orphan_citas.csv", index=False)

    print("Limpieza completada. Archivos en 'data/clean/' y reporte en 'reports/cleaning_summary.md'.")

if __name__ == "__main__":
    main()
