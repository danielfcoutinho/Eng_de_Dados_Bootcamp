# Realizado no Bootcamp de Eng de Dados por Daniel Coutinho

# Capturando dados com uma API

# Captura de dados utilizando API do Mercado Bitcoin: https://www.mercadobitcoin.com.br/api-doc/

import datetime
import time

from schedule import repeat, every, run_pending
from ingestors import DaySummaryIngestor
from writers import DataWriter


if __name__ == "__main__":
    day_summary_ingestor = DaySummaryIngestor(
        writer=DataWriter,
        coins=["BTC", "ETH", "LTC", "BCH"],
        default_start_date=datetime.date(2021, 6, 1)
    )


    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()


    while True:
        run_pending()
        time.sleep(0.5)


