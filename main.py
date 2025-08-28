from Extract.Formula1Extract import Formula1Extract
from Config.Config import Config

extractor = Formula1Extract(Config.INPUT)

extractor.queries()

print(extractor.response())