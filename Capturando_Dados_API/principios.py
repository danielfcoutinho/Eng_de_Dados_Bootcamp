# Realizado no Bootcamp de Eng de Dados por Daniel Coutinho

# Fundamentos de Engenharia de Dados

# Script de introdução a orientação a objetos para trabalhar princípios e heranças de classe
# Princípio de aberto e fechado
# Princípio da responsabilidade única

# Parte 1 - Criando classes diferentes para responsabilidades únicas no código

import datetime
import math
from typing import List

# Criando a classe pessoa


class person:
    def __init__(
        self,
        name: str,
        surname: str,
        date_of_birth: datetime.date,
    ) -> None:
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth

    @property
    def age(self) -> int:
        return math.floor((datetime.date.today() - self.date_of_birth).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.name} {self.surname} tem {self.age} anos"

# Criando a classe curriculo


class Curriculum:
    def __init__(self, person: person, experiences: List[str]):
        self.experiences = experiences
        self.person = person

    @property  # Decorator transformando em propriedade
    def quantity_experiences(self) -> int:
        # Captura a quantidade de experiências no currículo
        return len(self.experiences)

    @property  # Decorator transformando em propriedade
    def current_company(self) -> str:
        # Captura a última experiência do currículo
        return self.experiences[-1]

    # Adiciona uma experiência ao currículo
    def add_experience(self, experience: str) -> None:
        self.experiences.append(experience)

    def __str__(self):  # Sobrescrever um método para retornar uma string customizada quando print(Curriculum)
        return f"{self.person.name} {self.person.surname} tem {self.person.age} anos e já " \
               f"trabalhou em {self.quantity_experiences} empresas e atualmente trabalha " \
               f"na empresa {self.current_company}"


# Instanciando a variável daniel da classe person
daniel = person(name='Daniel', surname='Coutinho',
                date_of_birth=datetime.date(1995, 10, 27))

curriculum_daniel = Curriculum(
    person=daniel,  # recebendo uma variável de classe person no argumento person da classe Curriculum
    experiences=['A', 'B', 'C', 'D']
)

print(curriculum_daniel)
curriculum_daniel.add_experience('E')
print(curriculum_daniel)

# Parte 2 - Trabalhando com herança entre classes


class Living:
    def __init__(self, name: str, date_of_birth: datetime.date) -> None:
        self.name = name
        self.date_of_birth = date_of_birth

    @property
    def age(self) -> int:
        return math.floor((datetime.date.today() - self.date_of_birth).days / 365.2425)

    def sound(self, sound: str):
        print(f"{self.name} fez som: {sound}")


class PersonHeritage(Living):
    def __str__(self) -> str:
        return f"{self.name} tem {self.age} anos"

    def talk(self, word):
        return self.sound(word)


class Dog(Living):
    # Inicializa a classe Dog porém utilizando os parâmetros da classe Living e adicionando breed
    def __init__(self, name: str, date_of_birth: datetime.date, breed: str):
        super().__init__(name, date_of_birth)
        self.breed = breed

    def __str__(self) -> str:
        return f"{self.name} é da raça {self.breed} e tem {self.age} anos"

    def barks(self):
        return self.sound("Au! Au!")


larissa = PersonHeritage(
    name='Larissa', date_of_birth=datetime.date(1996, 5, 3))
print(larissa)

cachorro = Dog(name='Arrasca', date_of_birth=datetime.date(
    2019, 4, 15), breed='Vira Lata')
print(cachorro)

cachorro.barks()
larissa.talk("Oi")
cachorro.barks()
