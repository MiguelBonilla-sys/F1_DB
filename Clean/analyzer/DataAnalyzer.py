import pandas as pd
import numpy as np


class DataAnalyzer:
    """
    Clase responsable del análisis de calidad y diagnóstico de datos.
    Se enfoca únicamente en analizar y reportar el estado de los datos.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa el analizador con un DataFrame.
        
        Args:
            data (pd.DataFrame): Los datos a analizar
        """
        self.data = data
        self.null_info = {}
        
    def analyze_null_values(self):
        """
        Analiza los valores nulos en el dataset.
        
        Returns:
            dict: Información detallada sobre valores nulos
        """
        # Contar valores nulos por columna
        null_counts = self.data.isnull().sum()
        
        # Porcentaje de valores nulos por columna
        null_percentages = (null_counts / len(self.data)) * 100
        
        # Crear resumen de información nula
        self.null_info = {
            'total_rows': len(self.data),
            'total_columns': len(self.data.columns),
            'columns_with_nulls': null_counts[null_counts > 0].to_dict(),
            'null_percentages': null_percentages[null_percentages > 0].to_dict(),
            'total_null_values': null_counts.sum(),
            'columns_names': list(self.data.columns)
        }
        
        return self.null_info
    
    def get_data_quality_score(self):
        """
        Calcula una puntuación de calidad de los datos.
        
        Returns:
            float: Puntuación de calidad (0-100%)
        """
        total_cells = self.data.shape[0] * self.data.shape[1]
        non_null_cells = self.data.notna().sum().sum()
        return (non_null_cells / total_cells) * 100 if total_cells > 0 else 0
    
    def get_columns_by_null_percentage(self, threshold=0.5):
        """
        Obtiene columnas que superan un umbral de valores nulos.
        
        Args:
            threshold (float): Umbral de porcentaje de nulos (0-1)
            
        Returns:
            list: Lista de columnas que superan el umbral
        """
        null_percentages = (self.data.isnull().sum() / len(self.data))
        return null_percentages[null_percentages > threshold].index.tolist()
    
    def print_null_analysis(self):
        """
        Imprime un análisis detallado de los valores nulos.
        """
        info = self.analyze_null_values()
        
        print("=== ANÁLISIS DE VALORES NULOS ===")
        print(f"Total de filas: {info['total_rows']}")
        print(f"Total de columnas: {info['total_columns']}")
        print(f"Total de valores nulos: {info['total_null_values']}")
        print(f"Puntuación de calidad: {self.get_data_quality_score():.2f}%")
        print("\nColumnas con valores nulos:")
        
        if info['columns_with_nulls']:
            for col, count in info['columns_with_nulls'].items():
                percentage = info['null_percentages'][col]
                print(f"  - {col}: {count} nulos ({percentage:.2f}%)")
        else:
            print("  ¡No se encontraron valores nulos!")
            
        print(f"\nColumnas disponibles: {', '.join(info['columns_names'])}")
    
    def get_basic_statistics(self):
        """
        Obtiene estadísticas básicas del dataset.
        
        Returns:
            dict: Estadísticas básicas
        """
        return {
            'shape': self.data.shape,
            'memory_usage': self.data.memory_usage(deep=True).sum(),
            'dtypes': self.data.dtypes.to_dict(),
            'null_count': self.data.isnull().sum().sum(),
            'duplicate_rows': self.data.duplicated().sum()
        }
