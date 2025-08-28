# 🏎️ Formula1DB - Sistema Modular de Análisis de Datos de Fórmula 1

## 📋 Descripción del Proyecto

Este proyecto implementa un **sistema modular completo** de extracción, limpieza y análisis de datos de Fórmula 1, enfocándose específicamente en los resultados de calificación desde el año 2000 hasta 2024. 

**🎯 Características Principales:**
- **Arquitectura Modular**: Sistema diseñado con responsabilidades bien definidas y módulos especializados
- **Doble Interfaz**: API legacy para compatibilidad y nueva arquitectura modular para desarrollo avanzado
- **Limpieza Inteligente**: Múltiples estrategias de limpieza con análisis automático de calidad
- **Procesamiento Automatizado**: Pipeline completo desde carga hasta archivo limpio exportado

---

## 🏗️ Estructura del Proyecto

```
F1_DB/
│
├── main.py                              # Punto de entrada principal
├── README.md                            # Documentación del proyecto
├── requirements.txt                     # Dependencias del proyecto
├── LICENSE                              # Licencia del proyecto
│
├── Config/                              # Configuración del proyecto
│   ├── __init__.py
│   └── Config.py                        # Rutas y configuraciones
│
├── Extract/                             # Módulo de extracción (legacy)
│   ├── __init__.py
│   └── Formula1Extract.py               # Clase principal de extracción
│
├── Clean/                               # Sistema modular de limpieza
│   ├── __init__.py
│   ├── DataClean.py                     # Clase unificada (compatibilidad)
│   ├── ReadmeClean.md                   # Documentación del módulo Clean
│   │
│   ├── analyzer/                        # 🔍 Análisis y diagnóstico
│   │   ├── __init__.py
│   │   └── DataAnalyzer.py
│   │
│   ├── cleaner/                         # 🧹 Limpieza de datos
│   │   ├── __init__.py
│   │   └── DataCleaner.py
│   │
│   ├── report/                          # 📊 Reportes y resúmenes
│   │   ├── __init__.py
│   │   └── CleaningReport.py
│   │
│   └── csv_manager/                     # 📁 Manejo de archivos CSV
│       ├── __init__.py
│       └── CSVManager.py
│
└── Sources/                             # Archivos de datos
    ├── qualifying_results.csv           # Dataset original de F1
    └── qualifying_results_clean.csv     # Dataset procesado
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Configuración del Entorno Virtual

Es **altamente recomendable** crear un entorno virtual para este proyecto. Los entornos virtuales permiten:

- **Aislamiento de dependencias:** Evita conflictos entre diferentes proyectos
- **Gestión de versiones:** Controla las versiones específicas de las librerías
- **Reproducibilidad:** Garantiza que el proyecto funcione en diferentes sistemas
- **Limpieza del sistema:** Mantiene el Python global sin modificaciones

### Instalación

1. Crea y activa un entorno virtual:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en Linux/Mac
source .venv/bin/activate
```

2. Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

3. Para desactivar el entorno virtual cuando termines:

```bash
deactivate
```

---

## 💻 Uso del Sistema

### Ejecución Básica

```bash
python main.py
```

**¿Qué hace la ejecución básica?**
El `main.py` ejecuta dos flujos de trabajo:

1. **Método Legacy** (compatibilidad): Usa la clase `Formula1Extract` para procesamiento básico
2. **Arquitectura Modular** (recomendado): Usa `CSVManager` para procesamiento completo con reportes detallados

### Ejemplo de Uso - Método Legacy

```python
from Extract.Formula1Extract import Formula1Extract

# Crear extractor y cargar datos
extractor = Formula1Extract("Sources/qualifying_results.csv")

# Cargar datos originales
extractor.queries()

# Limpiar datos automáticamente (eliminar filas con nulos)
extractor.clean_data(strategy='fill_mean', verbose=True)

# Obtener datos limpios y mostrar información
clean_data = extractor.response()
print(f"Datos procesados: {clean_data.shape}")
print(f"Valores nulos restantes: {clean_data.isnull().sum().sum()}")
```

### Ejemplo de Uso - Arquitectura Modular (Recomendado)

```python
from Clean.csv_manager import CSVManager
from Config.Config import Config

# Procesamiento completo: carga → analiza → limpia → guarda
clean_csv_path = CSVManager.process_csv_file(
    csv_filename=Config.INPUT, 
    strategy='remove_rows',
    show_detailed_report=True
)

print(f"Archivo limpio generado en: {clean_csv_path}")
```

### Ejemplo de Uso - Control Granular

```python
from Clean.analyzer import DataAnalyzer
from Clean.cleaner import DataCleaner
from Clean.report import CleaningReport
from Clean.csv_manager import CSVManager

# 1. Cargar datos
data = CSVManager.load_csv("Sources/qualifying_results.csv")

# 2. Analizar calidad de datos
analyzer = DataAnalyzer(data)
analyzer.print_null_analysis()
quality_score = analyzer.get_data_quality_score()

# 3. Limpiar datos con estrategia específica
cleaner = DataCleaner(data)
cleaned_data = cleaner.clean_data(strategy='remove_rows')

# 4. Generar reporte detallado
report = CleaningReport(data, cleaned_data)
report.print_cleaning_summary()
report.print_before_after_comparison()

# 5. Guardar resultado
output_path = CSVManager.save_csv(cleaned_data, "my_clean_data.csv")
```

---

## 🧹 Sistema Modular de Limpieza de Datos

El proyecto utiliza una **arquitectura modular avanzada** con responsabilidades separadas por módulos especializados. Para una documentación detallada del módulo Clean, consulta: **[Clean/ReadmeClean.md](Clean/ReadmeClean.md)**

### 🎯 Módulos Especializados

- **`analyzer/`** - 🔍 **DataAnalyzer**: Análisis y diagnóstico de calidad de datos
- **`cleaner/`** - 🧹 **DataCleaner**: Estrategias de limpieza configurables
- **`report/`** - 📊 **CleaningReport**: Reportes detallados y comparaciones
- **`csv_manager/`** - 📁 **CSVManager**: Manejo completo de archivos CSV
- **`DataClean.py`** - 🔄 **Compatibilidad Legacy**: API original mantenida

### 🔧 Estrategias de Limpieza Disponibles

- **`remove_rows`** - Elimina filas con valores nulos (recomendado)
- **`remove_columns`** - Elimina columnas con muchos nulos (configurable por umbral)
- **`fill_mean`** - Rellena con promedio (numéricas) / moda (categóricas)
- **`fill_zero`** - Rellena valores nulos con ceros
- **`fill_forward`** - Rellena con valor anterior (forward/backward fill)

### ✨ Funcionalidades del Sistema

- ✅ **Análisis automático de calidad** con puntuación de integridad
- ✅ **Detección inteligente de valores nulos** por columna y tipo
- ✅ **Múltiples estrategias de limpieza** configurables según necesidades
- ✅ **Reportes detallados** con comparaciones antes/después
- ✅ **Pipeline automatizado** de procesamiento completo
- ✅ **Exportación automática** de archivos limpios
- ✅ **Compatibilidad legacy** para proyectos existentes

---

## 📊 Dataset de Fórmula 1

### Información del Dataset Utilizado

- **Archivo principal:** `qualifying_results.csv`
- **Período de cobertura:** 2000-2024 (25 años)
- **Registros totales:** 8,918 filas
- **Campos disponibles:** 17 columnas incluyendo:
  - `Season`, `Round`, `CircuitID` - Información del evento
  - `DriverID`, `Code`, `PermanentNumber` - Identificación del piloto
  - `GivenName`, `FamilyName`, `DateOfBirth`, `Nationality` - Datos personales
  - `ConstructorID`, `ConstructorName`, `ConstructorNationality` - Información del equipo
  - `Q1`, `Q2`, `Q3` - Tiempos de las sesiones de calificación

### Calidad de los Datos

- **Valores nulos detectados:** 244 en columna `Code` (2.74% del total)
- **Después de limpieza:** 0 valores nulos restantes
- **Puntuación de calidad original:** 99.84%
- **Puntuación de calidad final:** 100%
- **Registros procesados:** 8,674 filas (tras eliminar filas con nulos)

---

## 🔧 Funcionalidades Principales

### Clase `Formula1Extract` (Legacy)

- **Carga de datos:** Importación desde archivos CSV especificados
- **Limpieza integrada:** Procesamiento automático usando `DataClean`
- **Análisis comparativo:** Métodos para comparar datos antes/después
- **Compatibilidad:** Mantiene API original para proyectos existentes

### Nueva Arquitectura Modular

- **`DataAnalyzer`:** Análisis de calidad y diagnóstico de datos
- **`DataCleaner`:** Estrategias múltiples de limpieza configurables
- **`CleaningReport`:** Reportes detallados con métricas de mejora
- **`CSVManager`:** Pipeline completo de procesamiento de archivos

---

## 📈 Resultados del Procesamiento

### Estadísticas del Dataset Procesado

- **Filas procesadas:** 8,674 registros de calificación (97.26% del total)
- **Cobertura temporal:** 25 años completos (2000-2024)
- **Integridad de datos:** 100% después de limpieza
- **Tiempo de procesamiento:** < 2 segundos
- **Mejora en calidad:** +0.16% (de 99.84% a 100%)
- **Archivo de salida:** `qualifying_results_clean.csv` (automático)

---

## 🔗 Fuente de Datos

Los datos utilizados en este proyecto provienen del dataset completo de Fórmula 1 disponible en Kaggle:

**[Formula One Data 2000-2024](https://www.kaggle.com/datasets/henriquerezermosqur/formula-one-data-2000-2024)**

### Archivos Adicionales Disponibles en el Dataset

- `F1_DATA.db` - Base de datos SQLite completa
- `FEATURES.db` - Base de datos de características
- `circuits.csv` - Información de circuitos
- `constructor_standings.csv` - Posiciones de constructores
- `constructors.csv` - Datos de constructores
- `driver_standings.csv` - Posiciones de pilotos
- `drivers.csv` - Información de pilotos
- `pitstops.csv` - Datos de paradas en boxes
- `results.csv` - Resultados de carreras
- `results_history.csv` - Historial de resultados
- `results_qualy.csv` - Resultados de calificación alternativo

---

## � Flujo de Trabajo del Sistema

### 1. Carga de Datos
- Lectura automática desde `Sources/qualifying_results.csv`
- Validación de estructura y formato del archivo
- Creación de copia de trabajo para preservar datos originales

### 2. Análisis de Calidad
- Detección automática de valores nulos por columna
- Cálculo de puntuación de calidad (0-100%)
- Identificación de patrones problemáticos en los datos

### 3. Limpieza Inteligente
- Aplicación de estrategia seleccionada (`remove_rows`, `fill_mean`, etc.)
- Preservación de integridad referencial
- Validación post-limpieza automática

### 4. Reporte y Exportación
- Generación de reporte detallado con métricas
- Comparación antes/después con estadísticas
- Exportación automática a `qualifying_results_clean.csv`

---

## 🛠️ Dependencias del Proyecto

```text
pandas==2.3.1          # Manipulación y análisis de datos
numpy==2.3.2           # Computación numérica
requests==2.32.5       # Cliente HTTP (para futuras expansiones)
python-dateutil==2.9.0 # Utilidades de fechas
pytz==2025.2           # Zona horaria
```

---

## �👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Abre un **issue** primero para discutir los cambios propuestos
2. Asegúrate de que tu código sigue las convenciones del proyecto
3. Incluye pruebas para nuevas funcionalidades
4. Actualiza la documentación según sea necesario

### Áreas de Mejora Sugeridas

- 🔄 Integración con APIs en tiempo real de F1
- 📊 Visualizaciones interactivas de datos
- 🤖 Modelos de machine learning para predicciones
- 🔍 Análisis estadísticos avanzados

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto y Soporte

Para preguntas, sugerencias o reportes de bugs, por favor:

- 🐛 Abre un [issue](../../issues) en GitHub
- 📖 Consulta la documentación en [Clean/ReadmeClean.md](Clean/ReadmeClean.md)
- 💡 Revisa los ejemplos de uso en este README

---

**🏎️ ¡Happy Racing Data Analysis!** 🏁