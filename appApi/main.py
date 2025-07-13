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
from sqlalchemy.types import Integer

# Configuración de la conexión a la base de datos
# Aquí se define la URL de conexión a MySQL usando el usuario, contraseña y nombre de la base de datos
url_connection = 'mysql+pymysql://root:Susanthc123@localhost:3306/FinalProyecto'
engine = create_engine(url_connection, echo=True)  # Crear conexión a la base de datos

# Crear instancia de FastAPI
# Esta instancia será usada para definir los endpoints
app = FastAPI()

# Configurar CORS
# Permite que la API sea accesible desde aplicaciones externas como React y Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],  # Agregado nuevo origen
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
    feliz: str  # Emoción feliz
    interesado: str  # Emoción interesado
    motivado: str  # Emoción motivado
    entusiasmado: str  # Emoción entusiasmado
    preocupado: str  # Emoción preocupado
    temeroso: str  # Emoción temeroso
    triste: str  # Emoción triste
    cansado: str  # Emoción cansado

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

@app.get('/top-docentes-por-anio/')
def get_top_docentes_por_anio(year: int = None, limit: int = 10):
    with Session(engine) as session:
        try:
            # Consulta base para obtener el conteo de clases únicas por docente y año
            query = (
                select(
                    func.year(TablasAnalisisJoin.fecha).label("anio"),
                    TablasAnalisisJoin.nombre_docente,
                    func.count(TablasAnalisisJoin.qr_code.distinct()).label("clases_unicas")
                )
                .where(TablasAnalisisJoin.nombre_docente.isnot(None))
                .group_by(
                    func.year(TablasAnalisisJoin.fecha),
                    TablasAnalisisJoin.nombre_docente
                )
                .order_by(
                    func.year(TablasAnalisisJoin.fecha),
                    func.count(TablasAnalisisJoin.qr_code.distinct()).desc()
                )
            )

            if year:
                query = query.where(func.year(TablasAnalisisJoin.fecha) == year)

            results = session.exec(query).all()
            
            if not results:
                raise HTTPException(
                    status_code=404, 
                    detail="No se encontraron datos de docentes"
                )

            # Organizar resultados por año
            data_by_year = {}
            for result in results:
                year = result[0]
                if year not in data_by_year:
                    data_by_year[year] = []
                if len(data_by_year[year]) < limit:
                    data_by_year[year].append({
                        "docente": result[1],
                        "clases_unicas": result[2]
                    })

            return {
                "message": f"Top {limit} docentes por año",
                "data": data_by_year
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get('/top-asignaturas-por-anio/')
def get_top_asignaturas_por_anio(year: int = None, limit: int = 10):
    with Session(engine) as session:
        try:
            # Consulta modificada para contar todas las apariciones de cada asignatura
            query = (
                select(
                    func.year(TablasAnalisisJoin.fecha).label("anio"),
                    TablasAnalisisJoin.nombre_asignatura,
                    func.count(TablasAnalisisJoin.qr_code).label("total_clases"),  # Contar todas las apariciones
                    func.count(func.distinct(TablasAnalisisJoin.qr_code)).label("clases_unicas")  # Mantener también el conteo de clases únicas
                )
                .where(
                    TablasAnalisisJoin.nombre_asignatura.isnot(None),
                    TablasAnalisisJoin.qr_code.isnot(None)
                )
                .group_by(
                    func.year(TablasAnalisisJoin.fecha),
                    TablasAnalisisJoin.nombre_asignatura
                )
                .order_by(
                    func.year(TablasAnalisisJoin.fecha).asc(),
                    func.count(TablasAnalisisJoin.qr_code).desc()  # Ordenar por total de clases
                )
            )

            if year:
                query = query.where(func.year(TablasAnalisisJoin.fecha) == year)

            results = session.exec(query).all()
            
            if not results:
                raise HTTPException(
                    status_code=404, 
                    detail="No se encontraron datos de asignaturas"
                )

            # Organizar resultados por año
            data_by_year = {}
            for result in results:
                year = result[0]
                if year not in data_by_year:
                    data_by_year[year] = []
                if len(data_by_year[year]) < limit:
                    data_by_year[year].append({
                        "asignatura": result[1],
                        "total_clases": result[2],  # Total de veces que aparece la asignatura
                        "clases_unicas": result[3]   # Mantener también el conteo de clases únicas
                    })

            return {
                "message": f"Top {limit} asignaturas por año",
                "data": data_by_year
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get('/emociones-por-anio/')
def get_emociones_por_anio():
    try:
        with Session(engine) as session:
            query = (
                select(
                    func.year(TablasAnalisisJoin.fecha).label("anio"),
                    func.sum(func.cast(TablasAnalisisJoin.feliz, Integer)).label("feliz"),
                    func.sum(func.cast(TablasAnalisisJoin.interesado, Integer)).label("interesado"),
                    func.sum(func.cast(TablasAnalisisJoin.motivado, Integer)).label("motivado"),
                    func.sum(func.cast(TablasAnalisisJoin.entusiasmado, Integer)).label("entusiasmado"),
                    func.sum(func.cast(TablasAnalisisJoin.preocupado, Integer)).label("preocupado"),
                    func.sum(func.cast(TablasAnalisisJoin.temeroso, Integer)).label("temeroso"),
                    func.sum(func.cast(TablasAnalisisJoin.triste, Integer)).label("triste"),
                    func.sum(func.cast(TablasAnalisisJoin.cansado, Integer)).label("cansado")
                )
                .group_by(func.year(TablasAnalisisJoin.fecha))
                .order_by(func.year(TablasAnalisisJoin.fecha).asc())
            )

            print("Ejecutando consulta SQL...")
            results = session.exec(query).all()
            print("Resultados obtenidos:", results)

            if not results:
                raise HTTPException(status_code=404, detail="No se encontraron datos de emociones por año")

            emociones_anio = []
            for result in results:
                emociones_anio.append({
                    "anio": result[0] if result[0] is not None else 0,
                    "feliz": result[1] if result[1] is not None else 0,
                    "interesado": result[2] if result[2] is not None else 0,
                    "motivado": result[3] if result[3] is not None else 0,
                    "entusiasmado": result[4] if result[4] is not None else 0,
                    "preocupado": result[5] if result[5] is not None else 0,
                    "temeroso": result[6] if result[6] is not None else 0,
                    "triste": result[7] if result[7] is not None else 0,
                    "cansado": result[8] if result[8] is not None else 0,
                    "positivas": (result[1] if result[1] is not None else 0) + 
                                  (result[2] if result[2] is not None else 0) + 
                                  (result[3] if result[3] is not None else 0) + 
                                  (result[4] if result[4] is not None else 0),
                    "negativas": (result[5] if result[5] is not None else 0) + 
                                  (result[6] if result[6] is not None else 0) + 
                                  (result[7] if result[7] is not None else 0) + 
                                  (result[8] if result[8] is not None else 0)
                })

            return {"emociones_por_anio": emociones_anio}
    except Exception as e:
        print("Error en el endpoint /emociones-por-anio/:", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")
