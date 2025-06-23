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

# Consulta
query = """
SELECT
  fecha,
  nombre_asignatura,
  nombre_docente
FROM TablasAnalisisJoin
WHERE YEAR(fecha) BETWEEN 2020 AND 2025
  AND nombre_asignatura IS NOT NULL
ORDER BY fecha;
"""

# Cargar a DataFrame
df = pd.read_sql(query, conexion)
conexion.close()

# Procesar fechas
df['fecha'] = pd.to_datetime(df['fecha'])
df['anio'] = df['fecha'].dt.year


# Contar cuántas veces se dictó cada asignatura por año
conteo = df.groupby(['anio', 'nombre_asignatura']).size().reset_index(name='cantidad')

# Visualizar por cada año
anios = sorted(conteo['anio'].unique())

for anio in anios:
    datos_anio = conteo[conteo['anio'] == anio].sort_values(by='cantidad', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(datos_anio['nombre_asignatura'], datos_anio['cantidad'], color='skyblue')
    plt.title(f"📚 Materias más calificadas en {anio}")
    plt.xlabel("Cantidad de veces dictadas")
    plt.ylabel("Asignatura")
    plt.gca().invert_yaxis()  # Mostrar la más alta arriba
    plt.tight_layout()
    plt.show()



