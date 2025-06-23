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

# Conectar a la base de datos
conexion = mysql.connector.connect(**mysql_config)

query = """
SELECT
  fecha,
  nombre_asignatura,
  qr_code
FROM TablasAnalisisJoin
WHERE fecha BETWEEN '2020-01-01' AND '2025-12-31'
  AND nombre_asignatura IS NOT NULL
  AND qr_code IS NOT NULL
ORDER BY fecha;
"""

df = pd.read_sql(query, conexion)
conexion.close()

# Procesar fechas y años
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
df = df.dropna(subset=['fecha'])  # elimina fechas inválidas
df['anio'] = df['fecha'].dt.year

# Quitar duplicados por año y qr_code
df_unicos = df.drop_duplicates(subset=['anio', 'qr_code'])

# Conteo clases distintas por asignatura
conteo_total = df_unicos.groupby('nombre_asignatura').size().reset_index(name='clases_distintas_total')

# Top 10
conteo_total = conteo_total.sort_values(by='clases_distintas_total', ascending=False).head(10)

# Gráfico
plt.figure(figsize=(12, 8))
plt.barh(conteo_total['nombre_asignatura'], conteo_total['clases_distintas_total'], color='teal')
plt.xlabel("Cantidad total de clases distintas (QR únicos)")
plt.ylabel("Asignatura")
plt.title("Cantidad total de clases distintas por asignatura (2020-2025)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
