import pandas as pd
import numpy as np
import os
from .analyzer import DataAnalyzer
from .cleaner import DataCleaner
from .report import CleaningReport
from .csv_manager import CSVManager


class DataClean:
    """
    Clase de limpieza de datos con compatibilidad legacy.
    
    NOTA: Para nuevos desarrollos, se recomienda usar las clases modulares:
    - DataAnalyzer: Para análisis de datos
    - DataCleaner: Para limpieza de datos  
    - CleaningReport: Para reportes
    - CSVManager: Para manejo de archivos CSV
    
    Esta clase actúa como un wrapper que usa internamente los módulos especializados.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa la clase DataClean con un DataFrame.
        
        Args:
            data (pd.DataFrame): Los datos a limpiar
        """
        print("💡 Consejo: Para nuevos proyectos considera usar las clases modulares especializadas.")
        
        self.data = data.copy()
        self.original_shape = data.shape
        
        # Usar las nuevas clases modulares internamente
        self._analyzer = DataAnalyzer(data)
        self._cleaner = DataCleaner(data)
        
    def analyze_null_values(self):
        """Método de compatibilidad - usa DataAnalyzer internamente"""
        return self._analyzer.analyze_null_values()
    
    def clean_data(self, strategy='remove_rows', threshold=0.5):
        """Método de compatibilidad - usa DataCleaner internamente"""
        self.data = self._cleaner.clean_data(strategy, threshold)
        return self.data
    
    def get_cleaning_summary(self):
        """Método de compatibilidad - usa CleaningReport internamente"""
        report = CleaningReport(self._cleaner.original_data, self.data)
        return report.get_cleaning_summary()
    
    def get_cleaned_data(self):
        """Método de compatibilidad"""
        return self.data
    
    def print_null_analysis(self):
        """Método de compatibilidad - usa DataAnalyzer internamente"""
        self._analyzer.print_null_analysis()
    
    def generate_clean_csv(self, csv_filename, strategy='remove_rows', threshold=0.5):
        """Método de compatibilidad - usa CSVManager internamente"""
        print("💡 Consejo: Usa CSVManager.process_csv_file() para mayor funcionalidad")
        return CSVManager.process_csv_file(csv_filename, strategy, threshold, show_detailed_report=False)
    
    @staticmethod
    def process_csv_file(csv_filename, strategy='remove_rows', threshold=0.5):
        """Método de compatibilidad - usa CSVManager internamente"""
        print("💡 Consejo: Usa CSVManager.process_csv_file() directamente")
        return CSVManager.process_csv_file(csv_filename, strategy, threshold, show_detailed_report=False)