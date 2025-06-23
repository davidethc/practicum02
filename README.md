# 📊 Análisis de Sentimientos en Clases Universitarias

Un proyecto ETL completo que analiza emociones y sentimientos registrados en clases universitarias mediante códigos QR, proporcionando insights valiosos sobre la experiencia educativa.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Descripción del Proyecto

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) completo para analizar datos emocionales recopilados en entornos universitarios. Los estudiantes registran sus emociones durante las clases escaneando códigos QR, generando un dataset valioso para análisis de sentimientos y mejora de la experiencia educativa.

### ✨ Características Principales

- **Pipeline ETL Completo**: Extracción, transformación y carga de datos automatizada
- **Análisis de Sentimientos**: Procesamiento y categorización de emociones estudiantiles
- **Visualizaciones Interactivas**: Gráficos y dashboards para insights claros
- **Base de Datos Optimizada**: Estructura MySQL eficiente para consultas complejas
- **Reportes Automatizados**: Generación de informes por docente, materia y período

## 📁 Estructura del Proyecto

```
📦 sentiment-analysis-university/
├── 📁 Scripts/
│   ├── 📁 Extraccion/
│   │   └── 📄 Extraccion.ipynb
│   ├── 📁 Transformation/
│   │   └── 📄 Transformacion.ipynb
│   ├── 📁 Loading/
│   │   └── 📄 load.ipynb
│   └── 📁 VisualizacionDatos/
│       └── 📄 [notebooks de análisis]
├── 📁 Data/
│   └── 📄 alr_inscritos.csv
├── 📁 Database/
│   └── 📄 schema.sql
|── 📁 Documentacion/
├── 📄 requirements.txt
├── 📄 config.ini
└── 📄 README.md

```

## 🛠️ Tecnologías Utilizadas

| Categoría | Tecnologías |
|-----------|------------|
| **Lenguaje** | Python 3.10+ |
| **Base de Datos** | MySQL 8.0+ |
| **Análisis de Datos** | Pandas, NumPy, Matplotlib, Seaborn |
| **Notebooks** | Jupyter Lab/Notebook |
| **Visualización** | Plotly, Matplotlib |

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- ✅ **Python 3.10 o superior**
- ✅ **MySQL Server 8.0+**
- ✅ **Git** para clonar el repositorio
- ✅ **pip** (gestor de paquetes de Python)

### Herramientas Recomendadas
- 🔧 **VSCode** o **JupyterLab** como IDE
- 🗄️ **MySQL Workbench** para gestión de base de datos

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/sentiment-analysis-university.git
cd sentiment-analysis-university
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configuración de Base de Datos

Crea la base de datos en MySQL:
```sql
CREATE DATABASE FinalProyecto;
USE FinalProyecto;
```

Configura el archivo `config.ini`:
```ini
[mysql]
user = root
password = TU_CONTRASEÑA_AQUI
host = localhost
database = FinalProyecto
port = 3306
```


## 📊 Ejecución del Pipeline ETL

Ejecuta los notebooks en el siguiente orden:

### 1. 📥 Extracción de Datos
```bash
jupyter notebook Scripts/Extraccion/Extraccion.ipynb
```
- Carga inicial del archivo `alr_inscritos.csv`
- Validación de integridad de datos
- Generación de logs de extracción

### 2. 🔄 Transformación de Datos
```bash
jupyter notebook Scripts/Transformation/Transformacion.ipynb
```
- Limpieza y normalización de datos
- Conversión de tipos de datos
- Manejo de valores nulos y duplicados
- Estandarización de fechas y formatos

### 3. 📤 Carga de Datos
```bash
jupyter notebook Scripts/Loading/load.ipynb
```
- Carga optimizada a MySQL
- Creación de índices para consultas eficientes
- Validación de integridad referencial

### 4. 📈 Análisis y Visualización
```bash
jupyter notebook Scripts/VisualizacionDatos/
```
- Generación de insights y métricas clave
- Creación de visualizaciones interactivas

## 📊 Análisis Realizados

### 🔍 Métricas Principales

| Análisis | Descripción |
|----------|-------------|
| **Tendencias Temporales** | Evolución de emociones por año y mes |
| **Ranking de Materias** | Top 10 materias con más interacciones |
| **Performance Docente** | Top 5 docentes con mayor engagement |
| **Análisis Emocional** | Materias que generan emociones positivas/negativas |
| **Participación Estudiantil** | Estudiantes únicos por período |
| **Sesiones Destacadas** | QR codes con mayor actividad emocional |

### 📈 Visualizaciones Disponibles

- 📊 **Gráficos de Tendencias**: Evolución temporal de emociones
- 🥧 **Gráficos Circulares**: Distribución de sentimientos
- 📈 **Gráficos de Barras**: Rankings y comparaciones
- 🔥 **Mapas de Calor**: Correlaciones entre variables
- 📉 **Dashboards Interactivos**: Análisis multidimensional

## 👨‍💻 Autor

**Davide Manotoa**


*Proyecto desarrollado como entrega final del módulo de ETL y Análisis de Datos - 2025*
