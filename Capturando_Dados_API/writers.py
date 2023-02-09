import datetime
import json
import os
from typing import List


# Criando classe para tratar possível erro na ingestão do dado em DataWriter
class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion"
        super().__init__(self.message)

# Criando classe com objetivo de escrever em um arquivo os dados recebidos do endpoint


class DataWriter:

    # Inicialização recebendo apenas o nome do arquivo, a moeda e a api para salvar dados em diferentes arquivos e pastas
    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now().strftime('/%Y/%m/%d')}.json"

    # método para escrever uma linha no arquivo
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        # Abre o arquivo no modo append para adicionar novos dados e não sobrescrever
        with open(self.filename, "a") as f:
            f.write(row)

    # método para receber os dados e organiza em lista ou dicionário
    def write(self, data: [List, dict]):
        if isinstance(data, dict):  # IsInstance() determina se a variável é uma instância de uma classe e verificar se data é uma instância de dict e é um dicionário
            self._write_row(json.dumps(data) + "\n")

        # Caso seja uma lista de dicionários, a ideia é acessar cada elemento da lista e escrever os dicionários
        elif isinstance(data, List):
            for element in data:  # utiliza a função de forma recursiva para escrever os dicionários dentro da lista
                self.write(element)

        else:
            raise DataTypeNotSupportedForIngestionException(data)

'''
# Testes DataWriter
data = DaySummaryApi("BTC").get_data(date=datetime.date(2021, 6, 21))
writer = DataWriter('day_summary.json')
writer.write(data)

data = TradesApi("BTC").get_data()
writer = DataWriter('trades.json')
writer.write(data)
'''