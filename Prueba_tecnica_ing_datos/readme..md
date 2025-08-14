# Prueba Técnica – Ingeniero de Datos

Este proyecto corresponde a la solución de una prueba técnica para un rol de **Ingeniero de Datos**.  
El objetivo fue analizar, limpiar y validar un dataset hospitalario contenido en un archivo `JSON`.

## Estructura del proyecto

prueba_tecnica_ing_datos/
│
├─ data/
│ ├─ raw/ # Datos originales (JSON)
│ ├─ interim/ # Datos intermedios (CSV generados por explore.py)
│ └─ clean/ # Datos limpios finales
│
├─ reports/ # Reportes de exploración y limpieza
│
├─ src/ # Scripts de Python
│ ├─ explore.py # Exploración inicial del dataset
│ ├─ clean.py # Limpieza y validación
│ └─ export_excel.py # Exportar dataset limpio a Excel
│
├─ requirements.txt # Dependencias del proyecto
└─ README.md # Este archivo


## ⚙️ Requerimientos

- Python 3.10 o superior
- Librerías:
  - pandas
  - numpy
  - python-dateutil
  - openpyxl
  - pyarrow

Instalación:
pip install -r requirements.txt

**Ejecución paso a paso**
Colocar el JSON original
Guardar el archivo dataset_hospital.json en la carpeta data/raw/.

Exploración de datos
python src/explore.py

Salidas:
-CSV intermedios (pacientes_raw.csv, citas_medicas_raw.csv) en data/interim/
-Reporte exploration_report.md en reports/

Limpieza y validación
python src/clean.py

Salidas:
-CSV limpios en data/clean/
-cleaning_summary.md y orphan_citas.csv en reports/

Exportar a Excel
python src/export_excel.py

Salida:
-Archivo hospital_dataset_clean.xlsx en data/

**Descripción de la limpieza aplicada**
Estandarización de fechas: todos los campos de fecha convertidos a formato YYYY-MM-DD.
Recalculado de edad: usando fecha_nacimiento.
Normalización de género (sexo): convertido a "M" o "F".
Eliminación de duplicados:
	Pacientes duplicados por id_paciente.
	Citas duplicadas por id_cita.
Validación de integridad:
	Detección de citas médicas con id_paciente inexistente.
	Registro de dichas citas en orphan_citas.csv.

**Entregables**
reports/exploration_report.md → Análisis inicial.
reports/cleaning_summary.md → Resumen de limpieza.
data/clean/ → Archivos CSV limpios.
data/hospital_dataset_clean.xlsx → Dataset limpio final.