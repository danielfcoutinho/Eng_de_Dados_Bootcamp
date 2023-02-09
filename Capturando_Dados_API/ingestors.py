import datetime
from abc import ABC, abstractmethod
from typing import List

from apis import DaySummaryApi

# Criar uma classe para fazer a ingestão dos dados utilizando as classes criadas anteriormente para realizar as ações
class DataIngestor(ABC):

    def __init__(self, writer, coins: List[str], default_start_date: datetime.date) -> None:
        self.default_start_date = default_start_date
        self.coins = coins
        self.writer = writer
        self._checkpoint = self._load_checkpoint()

    @property
    def _checkpoint_filename(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, "w") as f:
            f.write(f"{self._checkpoint}")

    def _load_checkpoint(self) -> datetime.date:
        try:
            with open(self._checkpoint_filename, "r") as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return self.default_start_date

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()

    # Criação de método para ingestão
    # Como existem diferentes formas de ingestão, esse método será sobrescrito posteriormente
    @abstractmethod
    def ingest(self) -> None:
        pass

# Criando extensões das classes

# Classe para fazer ingestão do day summary utilizando as classes DaySummary e Writer criadas previamente

class DaySummaryIngestor(DataIngestor):

    def ingest(self) -> None:
        date = self._load_checkpoint()
        if date < datetime.date.today():
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.get_data(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(date + datetime.timedelta(days=1))

'''
# Teste de ingest 
ingestor = DaySummaryIngestor(writer=DataWriter, coins=[
                              "BTC", "ETH", "LTC"], default_start_date=datetime.date(2021, 6, 1))

ingestor.ingest()'''