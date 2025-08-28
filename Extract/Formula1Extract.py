import pandas as pd

class Formula1Extract:
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.data = None

    def queries(self):
        data = pd.read_csv(self.data)
        return data
        self.data = pd.read_csv(self.csv)
        return self.data

    def response(self, data):
        return data.head()
    def response(self):
        if self.data is None:
            raise ValueError("Los datos no han sido cargados. Llama al método queries() primero.")
        return self.data.head()