# tests/test_data_quality.py
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
CLEAN_DIR = BASE_DIR / "data" / "clean"
REPORTS_DIR = BASE_DIR / "reports"

def load_data():
    pacientes = pd.read_csv(CLEAN_DIR / "pacientes_clean.csv")
    citas = pd.read_csv(CLEAN_DIR / "citas_medicas_clean.csv")
    return pacientes, citas

def test_no_duplicate_pacientes():
    pacientes, _ = load_data()
    assert pacientes["id_paciente"].is_unique, "Existen pacientes duplicados"

def test_no_duplicate_citas():
    _, citas = load_data()
    assert citas["id_cita"].is_unique, "Existen citas duplicadas"

def test_id_paciente_not_null():
    pacientes, _ = load_data()
    assert pacientes["id_paciente"].notna().all(), "Hay pacientes sin ID"

def test_citas_referential_integrity():
    pacientes, citas = load_data()
    ids_pacientes = set(pacientes["id_paciente"])
    citas_huerfanas = citas[~citas["id_paciente"].isin(ids_pacientes)]
    assert len(citas_huerfanas) == 190, (
        f"Cantidad de citas huérfanas distinta a lo esperado: {len(citas_huerfanas)}"
    )

def test_required_columns():
    pacientes, citas = load_data()
    pacientes_cols = {"id_paciente", "nombre", "fecha_nacimiento", "edad", "sexo"}
    citas_cols = {"id_cita", "id_paciente", "fecha_cita", "especialidad"}
    assert pacientes_cols.issubset(set(pacientes.columns)), "Faltan columnas en pacientes"
    assert citas_cols.issubset(set(citas.columns)), "Faltan columnas en citas"
