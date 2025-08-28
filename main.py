from Extract.Formula1Extract import Formula1Extract
from Config.Config import Config
from Clean.Export.generate_clean_csv import generate_clean_csv

extractor = Formula1Extract(Config.INPUT)

# Cargar y limpiar datos automáticamente
extractor.queries()
extractor.clean_data(strategy='fill_mean')

# Mostrar datos 
print(extractor.response())

csv = generate_clean_csv(Config.INPUT)