"""
Módulo Clean - Sistema modular de limpieza de datos

Estructura modular:
- analyzer/: Análisis de calidad y diagnóstico de datos
- cleaner/: Estrategias de limpieza de datos  
- report/: Generación de reportes y resúmenes
- csv_manager/: Manejo de archivos CSV
- DataClean.py: Clase unificada con compatibilidad

Uso recomendado:
    from Clean.csv_manager import CSVManager
    CSVManager.process_csv_file("archivo.csv")
"""

# Importaciones principales para facilidad de uso
from .analyzer import DataAnalyzer
from .cleaner import DataCleaner
from .report import CleaningReport
from .csv_manager import CSVManager
from .DataClean import DataClean  # Clase unificada con compatibilidad

__all__ = [
    'DataAnalyzer',
    'DataCleaner', 
    'CleaningReport',
    'CSVManager',
    'DataClean'
]