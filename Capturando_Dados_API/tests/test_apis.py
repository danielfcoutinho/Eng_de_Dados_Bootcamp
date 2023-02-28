import datetime
import pytest
from apis import DaySummaryApi, TradesApi

# Teste unitário do método get_endpoint dentro de DaySummaryApi(MercadoBitcoinApi)

class TestDaySummaryApi:
    @pytest.mark.parametrize(  # Aplicação do módulo do pytest para parametrizar os testes para evitar repetição de código
        # definição dos parâmetros coin, date e expected
        "coin, date, expected",
        [
            ("BTC", datetime.date(2021, 6, 21),
            "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21"),
            ("ETH", datetime.date(2021, 6, 21),
            "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/21"),
            ("ETH", datetime.date(2019, 1, 2),
            "https://www.mercadobitcoin.net/api/ETH/day-summary/2019/1/2")
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin=coin)  # Aplicação da api DaySummaryApi
        actual = api._get_endpoint(date=date)  # Aplicação get_endpoint
        assert actual == expected  # Comparação do capturado e esperado para verificação

class TestTradesApi:
    @pytest.mark.parametrize(  # Aplicação do módulo do pytest para parametrizar os testes para evitar repetição de código
        # definição dos parâmetros coin, date e expected
        "coin, date_from, date_to, expected",
        [
            ("TEST", datetime.datetime(2019,1,1), datetime.datetime(2019,1,2), 
            "https://www.mercadobitcoin.net/api/TEST/trades/1546311600/1546398000"),

            ("TEST", datetime.datetime(2012, 8, 20), datetime.datetime(2015, 4, 3), 
            "https://www.mercadobitcoin.net/api/TEST/trades/1345431600/1428030000"),

            ("TEST", None, None, 
            "https://www.mercadobitcoin.net/api/TEST/trades"),

            ("TEST", None, datetime.datetime(2012, 8, 20), 
            "https://www.mercadobitcoin.net/api/TEST/trades"),

            ("TEST", datetime.datetime(2012, 8, 20), None, 
            "https://www.mercadobitcoin.net/api/TEST/trades/1345431600"),
        ]
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        api = TradesApi(coin=coin)  # Aplicação da api DaySummaryApi
        actual = api._get_endpoint(date_from=date_from, date_to=date_to)  # Aplicação get_endpoint
        assert actual == expected  # Comparação do capturado e esperado para verificação

    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError): #Teste caso erro ocorra
            TradesApi(coin="TEST")._get_endpoint(
                date_from=datetime.datetime(2021, 6, 15), 
                date_to=datetime.datetime(2021, 6, 12))


    @pytest.mark.parametrize(
        "date, expected",
        [
            (datetime.datetime(2019, 1, 1), 1546311600),
            (datetime.datetime(2019, 1, 2), 1546398000),
            (datetime.datetime(2015, 4, 3), 1428030000),
            (datetime.datetime(2012, 8, 20), 1345431600),
            (datetime.datetime(2021, 6, 15), 1623726000)
        ]
    )
    def test_get_unix_epoch(self, date, expected):
        api = TradesApi(coin="TEST")
        actual = api._get_unix_epoch(date)
        assert actual == expected