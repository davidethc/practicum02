import configparser
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Leer configuración desde archivo ini
config = configparser.ConfigParser()
config.read('config/config.ini')  # Ajusta ruta si es diferente

mysql_config = {
    'user': config.get('mysql', 'user'),
    'password': config.get('mysql', 'password'),
    'host': config.get('mysql', 'host'),
    'database': config.get('mysql', 'database'),
    'port': config.getint('mysql', 'port')
}

conexion = mysql.connector.connect(**mysql_config)


# cnsulta SQL para obtener datos de materias dictadas
query = """
SELECT
  fecha,
  nombre_asignatura,
  nombre_docente,
  qr_code
FROM TablasAnalisisJoin
WHERE YEAR(fecha) BETWEEN 2020 AND 2025
  AND nombre_asignatura IS NOT NULL
ORDER BY fecha;
"""

# Recargar el DataFrame
df = pd.read_sql(query, conexion)
conexion.close()

# Procesar fechas
df['fecha'] = pd.to_datetime(df['fecha'])
df['anio'] = df['fecha'].dt.year

# Contar clases dictadas únicas (por qr_code) por asignatura y año
conteo = df.groupby(['anio', 'nombre_asignatura'])['qr_code'].nunique().reset_index(name='clases_dictadas')

# Visualizar por cada año
anios = sorted(conteo['anio'].unique())

for anio in anios:
    datos_anio = conteo[conteo['anio'] == anio].sort_values(by='clases_dictadas', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(datos_anio['nombre_asignatura'], datos_anio['clases_dictadas'], color='skyblue')
    plt.title(f"📚 Materias más dictadas en {anio}")
    plt.xlabel("Clases dictadas (QR únicos)")
    plt.ylabel("Asignatura")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
