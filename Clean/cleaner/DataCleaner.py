import pandas as pd
import numpy as np
from ..analyzer import DataAnalyzer


class DataCleaner:
    """
    Clase responsable únicamente de las estrategias de limpieza de datos.
    Se enfoca en transformar y limpiar los datos según diferentes estrategias.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Inicializa el limpiador con un DataFrame.
        
        Args:
            data (pd.DataFrame): Los datos a limpiar
        """
        self.original_data = data.copy()
        self.data = data.copy()
        self.original_shape = data.shape
        
    def clean_remove_rows(self):
        """
        Elimina filas con valores nulos.
        
        Returns:
            pd.DataFrame: Datos con filas nulas eliminadas
        """
        self.data = self.data.dropna()
        return self.data
        
    def clean_remove_columns(self, threshold=0.5):
        """
        Elimina columnas que tengan más del threshold% de valores nulos.
        
        Args:
            threshold (float): Umbral para eliminar columnas (% de nulos)
            
        Returns:
            pd.DataFrame: Datos con columnas problemáticas eliminadas
        """
        analyzer = DataAnalyzer(self.data)
        columns_to_drop = analyzer.get_columns_by_null_percentage(threshold)
        self.data = self.data.drop(columns=columns_to_drop)
        return self.data
        
    def clean_fill_forward(self):
        """
        Rellena valores nulos con el valor anterior (forward fill).
        
        Returns:
            pd.DataFrame: Datos con valores rellenados hacia adelante
        """
        # Rellenar valores nulos con el valor anterior
        self.data = self.data.fillna(method='ffill')
        # Si aún quedan nulos al inicio, usar backward fill
        self.data = self.data.fillna(method='bfill')
        return self.data
        
    def clean_fill_mean(self):
        """
        Rellena valores nulos con la media para columnas numéricas
        y con el valor más frecuente para columnas no numéricas.
        
        Returns:
            pd.DataFrame: Datos con valores rellenados con media/moda
        """
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
                
        return self.data
        
    def clean_fill_zero(self):
        """
        Rellena valores nulos con ceros.
        
        Returns:
            pd.DataFrame: Datos con valores nulos reemplazados por ceros
        """
        self.data = self.data.fillna(0)
        return self.data
    
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
        strategy_methods = {
            'remove_rows': self.clean_remove_rows,
            'remove_columns': lambda: self.clean_remove_columns(threshold),
            'fill_forward': self.clean_fill_forward,
            'fill_mean': self.clean_fill_mean,
            'fill_zero': self.clean_fill_zero
        }
        
        if strategy in strategy_methods:
            return strategy_methods[strategy]()
        else:
            raise ValueError(f"Estrategia '{strategy}' no reconocida. "
                           f"Estrategias disponibles: {list(strategy_methods.keys())}")
    
    def get_cleaned_data(self):
        """
        Retorna los datos limpios actuales.
        
        Returns:
            pd.DataFrame: Datos después de la limpieza
        """
        return self.data
    
    def get_original_data(self):
        """
        Retorna los datos originales sin modificar.
        
        Returns:
            pd.DataFrame: Datos originales
        """
        return self.original_data
    
    def reset_data(self):
        """
        Resetea los datos a su estado original.
        
        Returns:
            pd.DataFrame: Datos restaurados al estado original
        """
        self.data = self.original_data.copy()
        return self.data
