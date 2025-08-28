import pandas as pd
from ..analyzer import DataAnalyzer


class CleaningReport:
    """
    Clase responsable de generar reportes y resúmenes del proceso de limpieza.
    Se enfoca únicamente en reportar y documentar los cambios realizados.
    """
    
    def __init__(self, original_data: pd.DataFrame, cleaned_data: pd.DataFrame):
        """
        Inicializa el generador de reportes.
        
        Args:
            original_data (pd.DataFrame): Datos originales
            cleaned_data (pd.DataFrame): Datos después de la limpieza
        """
        self.original_data = original_data
        self.cleaned_data = cleaned_data
        self.original_analyzer = DataAnalyzer(original_data)
        self.cleaned_analyzer = DataAnalyzer(cleaned_data)
        
    def get_cleaning_summary(self):
        """
        Obtiene un resumen completo del proceso de limpieza.
        
        Returns:
            dict: Resumen detallado del proceso de limpieza
        """
        original_shape = self.original_data.shape
        current_shape = self.cleaned_data.shape
        
        # Análisis de calidad antes y después
        original_quality = self.original_analyzer.get_data_quality_score()
        cleaned_quality = self.cleaned_analyzer.get_data_quality_score()
        
        summary = {
            'original_shape': original_shape,
            'current_shape': current_shape,
            'rows_removed': original_shape[0] - current_shape[0],
            'columns_removed': original_shape[1] - current_shape[1],
            'original_nulls': self.original_data.isnull().sum().sum(),
            'remaining_nulls': self.cleaned_data.isnull().sum().sum(),
            'nulls_removed': self.original_data.isnull().sum().sum() - self.cleaned_data.isnull().sum().sum(),
            'original_quality_score': original_quality,
            'data_quality_score': cleaned_quality,
            'quality_improvement': cleaned_quality - original_quality,
            'data_reduction_percentage': ((original_shape[0] - current_shape[0]) / original_shape[0]) * 100 if original_shape[0] > 0 else 0
        }
        
        return summary
    
    def print_cleaning_summary(self):
        """
        Imprime un resumen detallado del proceso de limpieza.
        """
        summary = self.get_cleaning_summary()
        
        print("\n=== RESUMEN DE LIMPIEZA ===")
        print(f"📊 Forma original: {summary['original_shape']}")
        print(f"📊 Forma actual: {summary['current_shape']}")
        print(f"🗑️  Filas eliminadas: {summary['rows_removed']}")
        print(f"🗑️  Columnas eliminadas: {summary['columns_removed']}")
        print(f"❌ Valores nulos originales: {summary['original_nulls']}")
        print(f"❌ Valores nulos restantes: {summary['remaining_nulls']}")
        print(f"✅ Valores nulos eliminados: {summary['nulls_removed']}")
        print(f"📈 Calidad original: {summary['original_quality_score']:.2f}%")
        print(f"📈 Calidad final: {summary['data_quality_score']:.2f}%")
        print(f"⬆️  Mejora en calidad: {summary['quality_improvement']:.2f}%")
        print(f"📉 Reducción de datos: {summary['data_reduction_percentage']:.2f}%")
    
    def print_before_after_comparison(self):
        """
        Imprime una comparación antes/después de la limpieza.
        """
        print("\n=== COMPARACIÓN ANTES/DESPUÉS ===")
        
        print("\n📄 DATOS ORIGINALES:")
        print(f"Forma: {self.original_data.shape}")
        print("Primeras 5 filas:")
        print(self.original_data.head())
        print("\nInformación de valores nulos:")
        print(self.original_data.isnull().sum())
        
        print("\n✨ DATOS LIMPIOS:")
        print(f"Forma: {self.cleaned_data.shape}")
        print("Primeras 5 filas:")
        print(self.cleaned_data.head())
        print("\nInformación de valores nulos:")
        print(self.cleaned_data.isnull().sum())
    
    def get_detailed_analysis(self):
        """
        Obtiene un análisis detallado de los cambios realizados.
        
        Returns:
            dict: Análisis detallado de los cambios
        """
        original_nulls = self.original_analyzer.analyze_null_values()
        cleaned_nulls = self.cleaned_analyzer.analyze_null_values()
        
        # Columnas que fueron eliminadas
        removed_columns = set(self.original_data.columns) - set(self.cleaned_data.columns)
        
        # Columnas que ya no tienen nulos
        fixed_columns = []
        for col in self.cleaned_data.columns:
            if col in original_nulls['columns_with_nulls'] and col not in cleaned_nulls['columns_with_nulls']:
                fixed_columns.append(col)
        
        return {
            'removed_columns': list(removed_columns),
            'fixed_columns': fixed_columns,
            'original_null_analysis': original_nulls,
            'cleaned_null_analysis': cleaned_nulls,
            'columns_still_with_nulls': list(cleaned_nulls['columns_with_nulls'].keys()) if cleaned_nulls['columns_with_nulls'] else []
        }
