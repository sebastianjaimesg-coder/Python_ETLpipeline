# src/explore.py
from pathlib import Path
import json
import pandas as pd
from datetime import datetime

# ========= CONFIG =========
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_JSON_PATH = BASE_DIR / "data" / "raw" / "dataset_hospital.json"
OUTPUT_INTERIM = BASE_DIR / "data" / "interim"
REPORTS_DIR = BASE_DIR / "reports"
OUTPUT_INTERIM.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
# ==========================

# Candidate keys for detecting tables
PATIENT_KEYS = ["pacientes", "patients"]
APPOINT_KEYS = ["citas_medicas", "citas", "appointments"]

def _to_df(obj) -> pd.DataFrame:
    if isinstance(obj, list):
        return pd.DataFrame(obj)
    if isinstance(obj, dict):
        # If it is nested, try to normalize it.
        return pd.json_normalize(obj)
    return pd.DataFrame()

def load_tables():
    with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    pacientes_df = pd.DataFrame()
    citas_df = pd.DataFrame()

    if isinstance(data, dict):
        # Search by known keywords
        for k in PATIENT_KEYS:
            if k in data:
                pacientes_df = _to_df(data[k])
                break
        for k in APPOINT_KEYS:
            if k in data:
                citas_df = _to_df(data[k])
                break

        # If you didn't find any, take the first two lists that look like tables.
        if pacientes_df.empty or citas_df.empty:
            for v in data.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    if pacientes_df.empty:
                        pacientes_df = pd.DataFrame(v)
                    elif citas_df.empty:
                        citas_df = pd.DataFrame(v)
    elif isinstance(data, list):
        # The archive is a single list (we treat it as patients).
        pacientes_df = pd.DataFrame(data)
    else:
        raise ValueError("Unrecognized JSON structure.")

    return pacientes_df, citas_df

def profile(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"rows": 0, "columns": [], "dtypes": {}, "null_counts": {}, "duplicates_all": 0}

    info = {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isna().sum().to_dict(),
        "duplicates_all": int(df.duplicated().sum()),
    }
    # Duplicates by common keys if they exist
    for key in ["id", "id_paciente", "idPaciente", "id_cita", "idCita"]:
        if key in df.columns:
            info[f"duplicates_by_{key}"] = int(df.duplicated(subset=[key]).sum())
            info[f"unique_{key}"] = int(df[key].nunique(dropna=True))
    # Duplicates due to frequent combination
    if {"nombre", "fecha_nacimiento"}.issubset(df.columns):
        info["duplicates_by_nombre_fecha"] = int(df.duplicated(subset=["nombre", "fecha_nacimiento"]).sum())
    return info

def write_report(pacientes_df, citas_df, p_info, c_info):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = REPORTS_DIR / "exploration_report.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# Data Exploration Report\n\n")
        f.write(f"_Generated: {ts}_\n\n")

        if not pacientes_df.empty:
            f.write("## Tabla: pacientes\n")
            f.write(f"- Filas: {p_info['rows']}\n")
            f.write(f"- Columnas: {', '.join(p_info['columns'])}\n")
            f.write(f"- Tipos: {p_info['dtypes']}\n")
            f.write(f"- Nulos por columna: {p_info['null_counts']}\n")
            for k, v in p_info.items():
                if k.startswith("duplicates") or k.startswith("unique_"):
                    f.write(f"- {k}: {v}\n")
            f.write("\n")
        else:
            f.write("## No patient table detected.\n\n")

        if not citas_df.empty:
            f.write("## Tabla: citas_medicas\n")
            f.write(f"- Filas: {c_info['rows']}\n")
            f.write(f"- Columnas: {', '.join(c_info['columns'])}\n")
            f.write(f"- Tipos: {c_info['dtypes']}\n")
            f.write(f"- Nulos por columna: {c_info['null_counts']}\n")
            for k, v in c_info.items():
                if k.startswith("duplicates") or k.startswith("unique_"):
                    f.write(f"- {k}: {v}\n")
            f.write("\n")
        else:
            f.write("## No medical appointment table detected.\n\n")

        f.write("> Next step: define cleaning rules (dates, gender, age, duplicates, integrity between tables).\n")

def main():
    print(f"Cargando JSON desde: {RAW_JSON_PATH}")
    pacientes_df, citas_df = load_tables()

    # Save intermediate copies
    if not pacientes_df.empty:
        pacientes_df.to_csv(OUTPUT_INTERIM / "pacientes_raw.csv", index=False)
    if not citas_df.empty:
        citas_df.to_csv(OUTPUT_INTERIM / "citas_medicas_raw.csv", index=False)

    # Basic profile
    p_info = profile(pacientes_df)
    c_info = profile(citas_df)

    # Report
    write_report(pacientes_df, citas_df, p_info, c_info)
    print("Exploration complete. Review. 'reports/exploration_report.md' y 'data/interim/'.")

if __name__ == "__main__":
    main()

