# Importación de módulos necesarios para la API
# FastAPI: Framework para crear APIs rápidas y eficientes
# SQLModel: Para interactuar con bases de datos usando modelos
# Otros módulos: Para funciones adicionales como CORS y manejo de excepciones
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, create_engine, SQLModel, select, func
from collections import Counter
import re

# Configuración de la conexión a la base de datos
# Aquí se define la URL de conexión a MySQL usando el usuario, contraseña y nombre de la base de datos
url_connection = 'mysql+pymysql://root:Susanthc123@localhost:3306/FinalProyecto'
engine = create_engine(url_connection, echo=True)  # Crear conexión a la base de datos

# Crear instancia de FastAPI
# Esta instancia será usada para definir los endpoints
app = FastAPI()

# Configurar CORS
# Permite que la API sea accesible desde aplicaciones externas como React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Agregar ambos orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

# Definir el modelo de datos para la tabla TablasAnalisisJoin
# Este modelo representa la estructura de la tabla en la base de datos
class TablasAnalisisJoin(SQLModel, table=True):
    qr_code: int  # Código QR asociado a cada registro
    id: int = Field(primary_key=True)  # ID único de cada registro
    fecha: str  # Fecha del registro
    det: str  # Detalles adicionales
    nombre_docente: str  # Nombre del docente
    nombre_asignatura: str  # Nombre de la asignatura
    UIDE: str  # Comentarios asociados al registro

# Endpoint para obtener todos los datos de la tabla TablasAnalisisJoin
# Este endpoint devuelve todos los registros de la tabla
@app.get('/analisis/')
def get_analisis():
    with Session(engine) as session:
        statement = select(TablasAnalisisJoin)  # Consulta para seleccionar todos los registros
        results = session.exec(statement).all()  # Ejecutar la consulta
        if not results:
            raise HTTPException(status_code=404, detail="No data found in TablasAnalisisJoin")  # Manejo de errores
        return results  # Devolver los resultados

# Ejemplo de uso:
# curl -X GET "http://127.0.0.1:8000/analisis/"

# Endpoint para obtener datos por ID
# Devuelve información específica de un registro basado en su ID
@app.get('/analisis/{item_id}')
def get_analisis_by_id(item_id: int):
    with Session(engine) as session:
        statement = select(
            TablasAnalisisJoin.nombre_asignatura,
            TablasAnalisisJoin.nombre_docente,
            TablasAnalisisJoin.qr_code
        ).where(TablasAnalisisJoin.id == item_id)  # Filtrar por ID
        result = session.exec(statement).first()  # Obtener el primer resultado
        if not result:
            raise HTTPException(status_code=404, detail=f"No data found for id {item_id}")  # Manejo de errores
        
        # Convertir el resultado en un diccionario
        return {
            "nombre_asignatura": result[0],
            "nombre_docente": result[1],
            "qr_code": result[2]
        }

# Ejemplo de uso:
# curl -X GET "http://127.0.0.1:8000/analisis/1"

# Endpoint para obtener comentarios filtrados por código QR
# Devuelve los comentarios asociados a un código QR específico
@app.get('/uids-by-qr/')
def get_uids_by_qr(qr_code: int):
    with Session(engine) as session:
        # Filtrar por qr_code y ordenar los resultados
        statement = select(TablasAnalisisJoin.UIDE).where(TablasAnalisisJoin.qr_code == qr_code).order_by(TablasAnalisisJoin.id)
        results = session.exec(statement).all()
        if not results:
            raise HTTPException(status_code=404, detail=f"No UIDE values found for qr_code {qr_code}")
        
        # Agregar registros de depuración
        print(f"Raw UIDE values: {results}")
        
        # Filtrar valores nulos y devolver los comentarios como strings completos
        filtered_results = [result for result in results if result and result != 'null']
        return {"uids": filtered_results}

# Ejemplo de uso:
# curl -X GET "http://127.0.0.1:8000/uids-by-qr/?qr_code=387249"

# Endpoint para agrupar comentarios por materia, año y mes
# Devuelve los comentarios agrupados y ordenados por año
@app.get('/grouped-comments/')
def get_grouped_comments():
    with Session(engine) as session:
        try:
            # Consulta para agrupar por materia, año y mes
            statement = select(
                TablasAnalisisJoin.nombre_asignatura,
                func.year(TablasAnalisisJoin.fecha).label("year"),
                func.month(TablasAnalisisJoin.fecha).label("month"),
                TablasAnalisisJoin.UIDE
            ).order_by(
                func.year(TablasAnalisisJoin.fecha),
                TablasAnalisisJoin.nombre_asignatura,
                func.month(TablasAnalisisJoin.fecha)
            )
            results = session.exec(statement).all()
            if not results:
                raise HTTPException(status_code=404, detail="No grouped comments found")
            
            # Agrupar manualmente los resultados y filtrar valores 'null'
            grouped_data = {}
            for result in results:
                if result.UIDE and result.UIDE != 'null':
                    key = (result.nombre_asignatura, result.year, result.month)
                    if key not in grouped_data:
                        grouped_data[key] = []
                    grouped_data[key].append(result.UIDE)
            
            # Formatear los resultados
            formatted_data = [
                {
                    "materia": key[0],
                    "year": key[1],
                    "month": key[2],
                    "comments": comments
                }
                for key, comments in grouped_data.items()
            ]
            return {"grouped_comments": formatted_data}
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

# Ejemplo de uso:
# curl -X GET "http://127.0.0.1:8000/grouped-comments/"



