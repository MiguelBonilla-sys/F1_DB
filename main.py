from Extract.Formula1Extract import Formula1Extract
from Config.Config import Config
from Clean.csv_manager import CSVManager

# Procesamiento con método legacy (compatibilidad hacia atrás)
print("🔄 PROCESAMIENTO CON MÉTODO LEGACY")
print("="*60)
extractor = Formula1Extract(Config.INPUT)

# Cargar y limpiar datos automáticamente
extractor.queries()
extractor.clean_data(strategy='fill_mean')

# Mostrar datos 
print(extractor.response())

# Procesamiento con nueva arquitectura modular
print("\n" + "="*60)
print("🔄 INICIANDO PROCESAMIENTO CON ARQUITECTURA MODULAR")
print("="*60)

clean_csv_path = CSVManager.process_csv_file(
    csv_filename=Config.INPUT, 
    strategy='remove_rows',
    show_detailed_report=True
)

if clean_csv_path:
    print("\n" + "="*60)
    print("🎉 ¡Archivo CSV limpio generado exitosamente!")
    print(f"📁 Ubicación: {clean_csv_path}")
    print("✅ El archivo ha sido almacenado y está listo para su uso.")
    print("="*60)
else:
    print("\n❌ Error: No se pudo generar el archivo CSV limpio.")