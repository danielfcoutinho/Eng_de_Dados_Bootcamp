# Realizado no Bootcamp de Eng de Dados por Daniel Coutinho

# Fundamentos de Engenharia de Dados

# Script de introdução a orientação a objetos
# Criação de classes, propriedades e métodos

import datetime  # Para tratar a data de nascimento e idade da pessoa
import math


class Pessoa:
    # inicialização da classe com __init__
    def __init__(self, name: str, surname: str, date_of_birth: datetime.date):
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth

    @property  # decorator para transformar o método em propriedade
    def age(self) -> int:  # Criação de método esperando receber inteiro como retorno
        # Uso de math.floor para arredondar a idade para número inteiro
        # Diferença do dia atual com a data de nascimento para calcular idade
        return math.floor((datetime.date.today() - self.date_of_birth).days / 365.2425)

    # Sobrescrever um método para retornar uma string customizada quando print(Pessoa)
    def __str__(self) -> str:
        return f"{self.name} {self.surname} tem {self.age} anos"

# Teste da classe


daniel = Pessoa(name='Daniel', surname='Coutinho',
                date_of_birth=datetime.date(1995, 10, 27))
larissa = Pessoa(name='Larissa', surname='Príncipe',
                 date_of_birth=datetime.date(1996, 5, 3))

print(daniel)
print(daniel.name)
print(daniel.surname)
print(daniel.age)
print('\t')
print(larissa)
print(larissa.name)
print(larissa.surname)
print(larissa.age)
