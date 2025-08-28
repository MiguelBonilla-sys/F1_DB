import pandas as pd
import numpy as np


class DataClean:
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa la clase DataClean con un DataFrame.
        
        Args:
            data (pd.DataFrame): Los datos a limpiar
        """
        self.data = data.copy()  # Crear una copia para no modificar los datos originales
        self.original_shape = data.shape
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
    
    def clean_data(self, strategy='remove_rows', threshold=0.5):
        """
        Limpia los datos según la estrategia especificada.
        
        Args:
            strategy (str): Estrategia de limpieza:
                - 'remove_rows': Eliminar filas con valores nulos
                - 'remove_columns': Eliminar columnas con muchos nulos
                - 'fill_forward': Rellenar con el valor anterior
                - 'fill_mean': Rellenar con la media (solo columnas numéricas)
                - 'fill_zero': Rellenar con ceros
            threshold (float): Umbral para eliminar columnas (% de nulos)
        
        Returns:
            pd.DataFrame: Datos limpios
        """
        if strategy == 'remove_rows':
            # Eliminar filas con cualquier valor nulo
            self.data = self.data.dropna()
            
        elif strategy == 'remove_columns':
            # Eliminar columnas que tengan más del threshold% de valores nulos
            null_percentages = (self.data.isnull().sum() / len(self.data))
            columns_to_drop = null_percentages[null_percentages > threshold].index
            self.data = self.data.drop(columns=columns_to_drop)
            
        elif strategy == 'fill_forward':
            # Rellenar valores nulos con el valor anterior
            self.data = self.data.fillna(method='ffill')
            # Si aún quedan nulos al inicio, usar backward fill
            self.data = self.data.fillna(method='bfill')
            
        elif strategy == 'fill_mean':
            # Rellenar valores nulos con la media para columnas numéricas
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                self.data[col] = self.data[col].fillna(self.data[col].mean())
            # Para columnas no numéricas, usar el valor más frecuente
            non_numeric_columns = self.data.select_dtypes(exclude=[np.number]).columns
            for col in non_numeric_columns:
                most_frequent = self.data[col].mode()
                if len(most_frequent) > 0:
                    self.data[col] = self.data[col].fillna(most_frequent[0])
                    
        elif strategy == 'fill_zero':
            # Rellenar valores nulos con ceros
            self.data = self.data.fillna(0)
            
        return self.data
    
    def get_cleaning_summary(self):
        """
        Obtiene un resumen del proceso de limpieza.
        
        Returns:
            dict: Resumen del proceso de limpieza
        """
        current_shape = self.data.shape
        
        summary = {
            'original_shape': self.original_shape,
            'current_shape': current_shape,
            'rows_removed': self.original_shape[0] - current_shape[0],
            'columns_removed': self.original_shape[1] - current_shape[1],
            'remaining_nulls': self.data.isnull().sum().sum(),
            'data_quality_score': ((self.data.notna().sum().sum()) / (current_shape[0] * current_shape[1])) * 100
        }
        
        return summary
    
    def get_cleaned_data(self):
        """
        Retorna los datos limpios.
        
        Returns:
            pd.DataFrame: Datos después de la limpieza
        """
        return self.data
    
    def print_null_analysis(self):
        """
        Imprime un análisis detallado de los valores nulos.
        """
        info = self.analyze_null_values()
        
        print("=== ANÁLISIS DE VALORES NULOS ===")
        print(f"Total de filas: {info['total_rows']}")
        print(f"Total de columnas: {info['total_columns']}")
        print(f"Total de valores nulos: {info['total_null_values']}")
        print("\nColumnas con valores nulos:")
        
        if info['columns_with_nulls']:
            for col, count in info['columns_with_nulls'].items():
                percentage = info['null_percentages'][col]
                print(f"  - {col}: {count} nulos ({percentage:.2f}%)")
        else:
            print("  ¡No se encontraron valores nulos!")
            
        print(f"\nColumnas disponibles: {', '.join(info['columns_names'])}")