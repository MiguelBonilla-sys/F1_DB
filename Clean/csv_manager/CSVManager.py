import pandas as pd
import os
from Config.Config import Config
from ..analyzer import DataAnalyzer
from ..cleaner import DataCleaner
from ..report import CleaningReport


class CSVManager:
    """
    Clase responsable del manejo de archivos CSV.
    Se enfoca únicamente en la lectura, escritura y gestión de archivos CSV.
    """
    
    @staticmethod
    def load_csv(csv_filename):
        """
        Carga un archivo CSV desde la ruta especificada.
        
        Args:
            csv_filename (str): Ruta del archivo CSV a cargar
            
        Returns:
            pd.DataFrame: DataFrame con los datos cargados o None si hay error
        """
        # Obtener la ruta del proyecto (ir 3 niveles arriba: csv_manager -> Clean -> F1_DB)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        csv_path = os.path.join(project_root, csv_filename)
        
        if not os.path.exists(csv_path):
            print(f"❌ Error: No se encontró el archivo {csv_path}")
            return None
        
        try:
            print(f"📂 Cargando datos desde {csv_filename}...")
            data = pd.read_csv(csv_path)
            print(f"✅ Datos cargados exitosamente: {data.shape}")
            return data
        except Exception as e:
            print(f"❌ Error al cargar el archivo: {e}")
            return None
    
    @staticmethod
    def save_csv(data, output_filename, show_preview=True):
        """
        Guarda un DataFrame como archivo CSV.
        
        Args:
            data (pd.DataFrame): Datos a guardar
            output_filename (str): Nombre del archivo de salida
            show_preview (bool): Si mostrar vista previa de los datos guardados
            
        Returns:
            str: Ruta completa del archivo guardado o None si hay error
        """
        try:
            # Usar Config.OUTPUT para determinar la carpeta de salida
            output_dir = os.path.dirname(Config.OUTPUT)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            output_path = os.path.join(project_root, output_dir, output_filename)
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Guardar CSV
            data.to_csv(output_path, index=False)
            
            print(f"💾 Archivo guardado como: {output_filename}")
            print(f"📁 Ruta completa: {output_path}")
            
            if show_preview:
                print(f"📊 Datos guardados: {data.shape}")
                print("👀 Primeras 5 filas guardadas:")
                print(data.head())
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error al guardar el archivo: {e}")
            return None
    
    @staticmethod
    def generate_clean_filename(original_filename):
        """
        Genera un nombre de archivo para la versión limpia.
        
        Args:
            original_filename (str): Nombre del archivo original
            
        Returns:
            str: Nombre del archivo limpio
        """
        csv_name = os.path.splitext(os.path.basename(original_filename))[0]
        return f"{csv_name}_clean.csv"
    
    @staticmethod
    def process_csv_file(csv_filename, strategy='remove_rows', threshold=0.5, show_detailed_report=True):
        """
        Procesa un archivo CSV completo: carga, limpia y guarda.
        
        Args:
            csv_filename (str): Ruta del archivo CSV a procesar
            strategy (str): Estrategia de limpieza a aplicar
            threshold (float): Umbral para eliminar columnas (% de nulos)
            show_detailed_report (bool): Si mostrar reporte detallado
            
        Returns:
            str: Ruta del archivo CSV limpio generado o None si hay error
        """
        print("🚀 Iniciando procesamiento de CSV...")
        
        # 1. Cargar datos originales
        original_data = CSVManager.load_csv(csv_filename)
        if original_data is None:
            return None
        
        # 2. Mostrar vista previa de datos originales
        print("\n📄 Vista previa de datos originales:")
        print(original_data.head())
        
        # 3. Analizar datos originales
        print("\n🔍 Analizando datos originales...")
        analyzer = DataAnalyzer(original_data)
        analyzer.print_null_analysis()
        
        # 4. Limpiar datos
        print(f"\n🧹 Limpiando datos con estrategia '{strategy}'...")
        cleaner = DataCleaner(original_data)
        cleaned_data = cleaner.clean_data(strategy=strategy, threshold=threshold)
        
        # 5. Generar reporte de limpieza
        if show_detailed_report:
            report = CleaningReport(original_data, cleaned_data)
            report.print_cleaning_summary()
            report.print_before_after_comparison()
        
        # 6. Guardar archivo limpio
        output_filename = CSVManager.generate_clean_filename(csv_filename)
        output_path = CSVManager.save_csv(cleaned_data, output_filename, show_preview=not show_detailed_report)
        
        if output_path:
            print("\n🎉 ¡Procesamiento completado exitosamente!")
            print(f"📁 Archivo limpio disponible en: {output_path}")
        
        return output_path
