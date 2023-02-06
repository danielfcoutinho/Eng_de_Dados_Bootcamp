# Projeto para coletar os dados de um site de imóveis e criar um banco de dados .csv

# Realizado no Bootcamp de Eng de Dados por Daniel Coutinho

# Ingestão de Dados

# %%
# imports

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# %%
# Leitura da url para capturar os dados do site Viva Real
# URL com variável i que vai mudar e capturar os dados de todas as páginas

url = 'https://www.vivareal.com.br/venda/rj/rio-de-janeiro/zona-oeste/jacarepagua/?pagina={}'
i = 1
ret = requests.get(url.format(i))
soup = bs(ret.text)

# %%
# Com soup.find_all encontramos a classe que indica o nome de cada imóvel na página
houses = soup.find_all(
    'a', {'class': 'property-card__content-link js-card-title'})
len(houses)  # testando a quantidade de imóveis encontrados em uma página do site

# Capturando o total de imóveis
qtd_imoveis = soup.find(
    'strong', {'class': 'results-summary__count js-total-records'})
# Removendo o ponto no número total de imóveis e transformando em float
qtd_imoveis = float(qtd_imoveis.text.replace('.', ''))

# %%

# Criação do dataframe para receber os valores

df = pd.DataFrame(
    columns=[
        'descricao',
        'endereco',
        'area',
        'quartos',
        'wc',
        'vagas',
        'valor',
        'condominio',
        'wlink'
    ]
)

i = 0


# %%
# Enquanto a quantidade de imóveis for maior que 36, executa (até a última página da busca)
while qtd_imoveis > df.shape[0]:
    print(f"Valor i: {i} \t\t qtd_imoveis: {df.shape[0]}")
    i = i+1
    ret = requests.get(url.format(i))
    soup = bs(ret.text, features="lxml")
    houses = soup.find_all(
        'a', {'class': 'property-card__content-link js-card-title'})

    for house in houses:  # Criação de loop para passar por todos os imóveis das páginas

        # Para cada um dos itens pode dar erro por falta de valores na página como os imóveis que não tem valor de condomínio no card
        # A forma de resolver isso será utilizando try e except para indicar o que fazer quando o valor não é encontrado

        # Capturando os dados dos imóveis
        try:
            # Capturando a descrição no site
            descricao = house.find(
                'span', {'class': 'property-card__title js-cardLink js-card-title'}).text
            descricao = descricao.strip()  # Removendo os espaços
        except:
            descricao = None

        # Realizar o mesmo procedimento para os outros dados desejados
        try:
            endereco = house.find(
                'span', {'class': 'property-card__address'}).text.strip()
        except:
            endereco = None
        try:
            area = house.find(
                'span', {'class': 'js-property-card-detail-area'}).text.strip()
        except:
            area = None
        try:
            # Pegando apenas o span do texto para capturar apenas o número
            quartos = house.find(
                'li', {'class': 'js-property-detail-rooms'}).span.text.strip()
        except:
            quartos = None
        try:
            wc = house.find(
                'li', {'class': 'js-property-detail-bathroom'}).span.text.strip()
        except:
            wc = None
        try:
            vagas = house.find(
                'li', {'class': 'js-property-detail-garages'}).span.text.strip()
        except:
            vagas = None
        try:
            valor = house.find(
                'div', {'class': 'property-card__price'}).p.text.strip()
        except:
            valor = None
        try:
            condominio = house.find(
                'strong', {'class': 'js-condo-price'}).text.strip()
        except:
            condominio = None
        try:
            wlink = 'https://www.vivareal.com.br' + house['href']
        except:
            wlink = None

        df.loc[df.shape[0]] = [
            descricao,
            endereco,
            area,
            quartos,
            wc,
            vagas,
            valor,
            condominio,
            wlink
        ]

# %%

df  # Verificação do dataframe

# %%

# Gerando arquivo csv com o banco de dados
df.to_csv('imoveis_jacarepagua.csv', sep=';', index=False)

# %%
