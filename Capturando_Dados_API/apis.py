import datetime
from abc import ABC, abstractmethod

import logging
import ratelimit
import requests
from backoff import on_exception, expo

# Criando logging para monitorar captura de dados da api
# __name__ indica que o logger faz o tracking do pacote/módulo pela hierarquia, no caso o main é o arquivo ingestao.py
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MercadoBitcoinApi(ABC):  # Classe para receber dados da api do Mercado Bitcoin

    def __init__(self, coin: str) -> None:
        self.coin = coin
        # base_endpoint recebe a base da url do endpoint que é imutável
        self.base_endpoint = "https://www.mercadobitcoin.net/api"

    # Método para buscar o endpoint
    @abstractmethod
    # Underline na frente do método indica que é um método interno da classe e não disponível para classes externas
    # **kwargs deixa em aberto o que será necessário para a requisição do endpoint nas classes seguintes
    def _get_endpoint(self, **kwargs) -> str:
        pass  # Esse método será sobrescrito obrigatoriamente nas classes futuras criadas que vão herdar MercadoBitcoinApi

    # Método para buscar os dados
    @on_exception(expo, ratelimit.exception.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
    def get_data(self, **kwargs) -> dict:
        # Variável endpoint recebendo "{self.base_endpoint}/{self.coin}/day-summary/2013/6/20/"
        endpoint = self._get_endpoint(**kwargs)
        # Informando o endpoint que está sendo capturado
        logger.info(f"Getting data from endpoint: {endpoint}")
        # recebe o endpoint na variável response
        response = requests.get(endpoint)
        response.raise_for_status()  # raise_for_status informa HTTPError caso ocorra
        return response.json()


# A partir desse ponto o objetivo é criar extensões da classe para buscar endpoint e dados necessários
class DaySummaryApi(MercadoBitcoinApi):  # Busca endpoint da data dos dados
    type = "day-summary"  # Implementar day-summary para buscar os dados de um dia específico

    def _get_endpoint(self, date: datetime.date) -> str:
        return f"{self.base_endpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"

# Teste classe DaySummaryApi
# print(DaySummaryApi("BTC").get_data(date = datetime.date(2021,6,3)))


class TradesApi(MercadoBitcoinApi):
    type = "trades"  # Implementar trades para buscar as transações em um período de tempo

    # date_from precisa estar em formato unix de acordo com a documentação da api
    def _get_unix_epoch(self, date: datetime.datetime) -> int:
        return int(date.timestamp())

    # Por padrão as datas de início e de fim não existem como valor inicial
    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.datetime = None) -> str:

        if date_from and not date_to:  # Se recebermos uma data início mas não recebermos uma data de fim do intervalo
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}'

        elif date_from and date_to:  # Se recebermos uma data de início e data de fim
            if date_from > date_to:  # Caso a data de início seja maior que a data de fim, raise RuntimeError
                raise RuntimeError("date_from cannot be greater than date_to")
            unix_date_from = self._get_unix_epoch(
                date_from)  # convertendo date_from
            unix_date_to = self._get_unix_epoch(date_to)  # convertendo date_to
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}/{unix_date_from}/{unix_date_to}'

        else:
            endpoint = f'{self.base_endpoint}/{self.coin}/{self.type}'

        return endpoint
