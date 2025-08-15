# Reporte de Exploración de Datos

_Generado: 2025-08-13 18:57_

## Tabla: pacientes
- Filas: 5010
- Columnas: id_paciente, nombre, fecha_nacimiento, edad, sexo, email, telefono, ciudad
- Tipos: {'id_paciente': 'int64', 'nombre': 'object', 'fecha_nacimiento': 'object', 'edad': 'float64', 'sexo': 'object', 'email': 'object', 'telefono': 'object', 'ciudad': 'object'}
- Nulos por columna: {'id_paciente': 0, 'nombre': 0, 'fecha_nacimiento': 0, 'edad': 1647, 'sexo': 1023, 'email': 2506, 'telefono': 1668, 'ciudad': 827}
- duplicates_all: 10
- duplicates_by_id_paciente: 10
- unique_id_paciente: 5000
- duplicates_by_nombre_fecha: 25

## Tabla: citas_medicas
- Filas: 9961
- Columnas: id_cita, id_paciente, fecha_cita, especialidad, medico, costo, estado_cita
- Tipos: {'id_cita': 'object', 'id_paciente': 'int64', 'fecha_cita': 'object', 'especialidad': 'object', 'medico': 'object', 'costo': 'float64', 'estado_cita': 'object'}
- Nulos por columna: {'id_cita': 0, 'id_paciente': 0, 'fecha_cita': 3278, 'especialidad': 1673, 'medico': 2033, 'costo': 1724, 'estado_cita': 2542}
- duplicates_all: 0
- duplicates_by_id_paciente: 4807
- unique_id_paciente: 5154
- duplicates_by_id_cita: 0
- unique_id_cita: 9961

> Siguiente paso: definir reglas de limpieza (fechas, sexo, edad, duplicados, integridad entre tablas).
