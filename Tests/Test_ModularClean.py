"""
Ejemplo de uso de los módulos individuales
Demuestra cómo usar cada módulo por separado
"""

import pandas as pd
import shutil
import os
import sys

# Agregar el directorio padre al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Clean.analyzer import DataAnalyzer
from Clean.cleaner import DataCleaner  
from Clean.report import CleaningReport
from Clean.csv_manager import CSVManager

def test_modular_clean():
    """Ejemplo paso a paso usando cada módulo por separado"""
    
    print("🔬 === EJEMPLO DE USO MODULAR ===")
    
    # 1. Cargar datos usando CSVManager
    print("\n📂 1. CARGANDO DATOS...")
    data = CSVManager.load_csv("Sources/qualifying_results.csv")
    if data is None:
        print("❌ No se pudieron cargar los datos")
        return
    
    # 2. Analizar datos usando DataAnalyzer
    print("\n🔍 2. ANALIZANDO DATOS...")
    analyzer = DataAnalyzer(data)
    analyzer.print_null_analysis()
    
    quality_score = analyzer.get_data_quality_score()
    print(f"Puntuación de calidad inicial: {quality_score:.2f}%")
    
    problematic_columns = analyzer.get_columns_by_null_percentage(0.02)
    print(f"Columnas problemáticas (>2% nulos): {problematic_columns}")
    
    # 3. Limpiar datos usando DataCleaner
    print("\n🧹 3. LIMPIANDO DATOS...")
    cleaner = DataCleaner(data)
    clean_data = cleaner.clean_data(strategy='remove_rows')
    
    print(f"Forma original: {data.shape}")
    print(f"Forma después de limpieza: {clean_data.shape}")
    
    # 4. Generar reporte usando CleaningReport
    print("\n📊 4. GENERANDO REPORTE...")
    report = CleaningReport(data, clean_data)
    report.print_cleaning_summary()
    
    # 5. Guardar usando CSVManager
    print("\n💾 5. GUARDANDO RESULTADO...")
    # Usar ruta relativa desde el proyecto para evitar que se concatene con Config.OUTPUT
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_output_path = os.path.join(project_root, "Tests", "Test_Source", "ejemplo_modular_clean.csv")
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(test_output_path), exist_ok=True)
    
    # Guardar directamente usando pandas
    clean_data.to_csv(test_output_path, index=False)
    print(f"💾 Archivo guardado como: Tests/Test_Source/ejemplo_modular_clean.csv")
    print(f"📁 Ruta completa: {test_output_path}")
    print(f"📊 Datos guardados: {clean_data.shape}")
    print("👀 Primeras 5 filas guardadas:")
    print(clean_data.head())
    
    output_path = test_output_path
    
    if output_path:
        print(f"✅ Archivo guardado en: {output_path}")
    else:
        print("❌ Error al guardar archivo")

def test_uso_directo():
    """Ejemplo usando CSVManager para procesamiento directo"""
    
    print("\n🚀 === EJEMPLO DE USO DIRECTO ===")
    
    output_path = CSVManager.process_csv_file(
        csv_filename="Sources/qualifying_results.csv",
        strategy='fill_mean',
        show_detailed_report=False
    )
    
    # Mover el archivo generado a Tests/Test_Source si se creó exitosamente
    if output_path:
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_output_path = os.path.join(project_root, "Tests", "Test_Source", "uso_directo_clean.csv")
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(test_output_path), exist_ok=True)
        
        # Mover archivo
        shutil.move(output_path, test_output_path)
        output_path = test_output_path
        print(f"📁 Archivo movido a: {test_output_path}")
    
    if output_path:
        print(f"✅ Procesamiento completo exitoso: {output_path}")
    else:
        print("❌ Error en procesamiento")

if __name__ == "__main__":
    # Ejecutar ejemplos
    test_modular_clean()
    print("\n" + "="*80)
    test_uso_directo()
