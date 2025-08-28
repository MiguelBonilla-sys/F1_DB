import sys
import os
from ..DataClean import DataClean
import pandas as pd
from Config.Config import Config

def generate_clean_csv(csv_filename):
    """
    Genera un archivo CSV limpio basado en los datos extraídos y procesados usando DataClean.
    
    Args:
        csv_filename (str): Ruta del archivo CSV a procesar (ej: "Sources\\qualifying_results.csv")
    """
    # Obtener la ruta del proyecto (ir dos niveles arriba desde Clean/Export/)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(project_root, csv_filename)
    print(f"Cargando datos desde {csv_filename}...")
    
    if not os.path.exists(csv_path):
        print(f"Error: No se encontró el archivo {csv_path}")
        return None
    
    # Leer datos originales
    original_data = pd.read_csv(csv_path)
    print(f"Datos originales cargados: {original_data.shape}")
    print("Primeras 5 filas de datos originales:")
    print(original_data.head())
    print("\nInformación de valores nulos en datos originales:")
    print(original_data.isnull().sum())
    
    # Crear instancia de DataClean
    print("\nInicializando limpieza de datos...")
    data_cleaner = DataClean(original_data)
    
    # Analizar valores nulos
    data_cleaner.print_null_analysis()

    # Limpiar datos con estrategia 'remove_rows'
    print("\nLimpiando datos con estrategia 'remove_rows'...")
    clean_data = data_cleaner.clean_data(strategy='remove_rows')
    
    # Mostrar resumen de limpieza
    summary = data_cleaner.get_cleaning_summary()
    print("\n=== RESUMEN DE LIMPIEZA ===")
    print(f"Forma original: {summary['original_shape']}")
    print(f"Forma actual: {summary['current_shape']}")
    print(f"Filas eliminadas: {summary['rows_removed']}")
    print(f"Columnas eliminadas: {summary['columns_removed']}")
    print(f"Valores nulos restantes: {summary['remaining_nulls']}")
    print(f"Puntuación de calidad: {summary['data_quality_score']:.2f}%")
    
    # Crear nombre del archivo con formato: name_oldCSV_clean.csv
    csv_name = os.path.splitext(os.path.basename(csv_filename))[0]  # qualifying_results
    output_filename = f"{csv_name}_clean.csv"
    
    # Usar Config.OUTPUT para determinar la carpeta de salida
    output_dir = os.path.dirname(Config.OUTPUT)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(project_root, output_dir, output_filename)
    clean_data.to_csv(output_path, index=False)
    
    print(f"\n✓ Archivo limpio guardado como: {output_filename}")
    print(f"   Ruta completa: {output_path}")
    print(f"Datos limpios: {clean_data.shape}")
    print("Primeras 5 filas de datos limpios:")
    print(clean_data.head())
    print("\nInformación de valores nulos en datos limpios:")
    print(clean_data.isnull().sum())
    
    return clean_data
