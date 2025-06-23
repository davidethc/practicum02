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

query = """
SELECT
  fecha,
  nombre_asignatura,
  qr_code
FROM TablasAnalisisJoin
WHERE YEAR(fecha) BETWEEN 2020 AND 2025
  AND nombre_asignatura IS NOT NULL
  AND qr_code IS NOT NULL
ORDER BY fecha;
"""

df = pd.read_sql(query, conexion)
conexion.close()

df['fecha'] = pd.to_datetime(df['fecha'])
df['anio'] = df['fecha'].dt.year

df_unicos = df.drop_duplicates(subset=['anio', 'qr_code'])

conteo = df_unicos.groupby(['anio', 'nombre_asignatura']).size().reset_index(name='clases_distintas')

# Elegir top 5 materias con más clases en total para no saturar el gráfico
top_materias = (conteo.groupby('nombre_asignatura')['clases_distintas']
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .index)

plt.figure(figsize=(12, 7))
for materia in top_materias:
    datos = conteo[conteo['nombre_asignatura'] == materia]
    plt.plot(datos['anio'], datos['clases_distintas'], marker='o', label=materia)

plt.title("Evolución de clases dictadas por materia (2020-2025)")
plt.xlabel("Año")
plt.ylabel("Cantidad de clases distintas (QR únicos)")
plt.legend(title="Asignatura")
plt.grid(True)
plt.tight_layout()
plt.show()
