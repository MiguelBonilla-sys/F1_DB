import requests
import pandas as pd
import numpy as np
from Clean.DataClean import DataClean


class Formula1Extract:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.data = None
        self.cleaned_data = None
        self.data_cleaner = None

    def queries(self):
        """Carga los datos desde el archivo CSV."""
        self.data = pd.read_csv(self.csv)
        return self.data

    def clean_data(self, strategy='remove_rows', threshold=0.5, verbose=False):
        """
        Limpia los datos utilizando la clase DataClean.
        
        Args:
            strategy (str): Estrategia de limpieza
            threshold (float): Umbral para eliminar columnas
            verbose (bool): Si mostrar información detallada del proceso
        
        Returns:
            pd.DataFrame: Datos limpios
        """
        if self.data is None:
            raise ValueError("Los datos no han sido cargados. Llama al método queries() primero.")
        
        # Crear instancia de DataClean
        self.data_cleaner = DataClean(self.data)
        
        if verbose:
            # Analizar valores nulos
            print("Analizando calidad de los datos...")
            self.data_cleaner.print_null_analysis()
            print(f"\nLimpiando datos con estrategia: {strategy}")
        
        # Limpiar datos
        self.cleaned_data = self.data_cleaner.clean_data(strategy=strategy, threshold=threshold)
        
        if verbose:
            # Mostrar resumen de limpieza
            summary = self.data_cleaner.get_cleaning_summary()
            print("\n=== RESUMEN DE LIMPIEZA ===")
            print(f"Forma original: {summary['original_shape']}")
            print(f"Forma actual: {summary['current_shape']}")
            print(f"Filas eliminadas: {summary['rows_removed']}")
            print(f"Columnas eliminadas: {summary['columns_removed']}")
            print(f"Valores nulos restantes: {summary['remaining_nulls']}")
            print(f"Puntuación de calidad: {summary['data_quality_score']:.2f}%")
        
        return self.cleaned_data

    def get_original_data(self):
        """Retorna los datos originales sin limpiar."""
        if self.data is None:
            raise ValueError("Los datos no han sido cargados. Llama al método queries() primero.")
        return self.data

    def get_cleaned_data(self):
        """Retorna los datos limpios."""
        if self.cleaned_data is None:
            raise ValueError("Los datos no han sido limpiados. Llama al método clean_data() primero.")
        return self.cleaned_data

    def response(self, use_cleaned=True):
        """
        Retorna una muestra de los datos.
        Por defecto retorna datos limpios si están disponibles.
        
        Args:
            use_cleaned (bool): Si usar datos limpios (True) o originales (False)
        
        Returns:
            pd.DataFrame
        """
        if use_cleaned and self.cleaned_data is not None:
            return self.cleaned_data
        elif self.data is not None:
            return self.data
        else:
            raise ValueError("Los datos no han sido cargados. Llama al método queries() primero.")

    def compare_data(self):
        """Compara los datos originales con los datos limpios."""
        if self.data is None:
            raise ValueError("Los datos no han sido cargados.")
        if self.cleaned_data is None:
            raise ValueError("Los datos no han sido limpiados.")
        
        print("=== COMPARACIÓN DE DATOS ===")
        print(f"Datos originales: {self.data.shape}")
        print(f"Datos limpios: {self.cleaned_data.shape}")
        print(f"Valores nulos originales: {self.data.isnull().sum().sum()}")
        print(f"Valores nulos después de limpieza: {self.cleaned_data.isnull().sum().sum()}")
