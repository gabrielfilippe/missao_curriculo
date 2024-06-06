import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import random
from app.models import *
from app.models import SEXO, ESTADOS
from faker import Faker
from unidecode import unidecode
from validate_docbr import CPF

def criar_pessoas(n):
    fake = Faker('pt_BR')

    Faker.seed(50)

    for _ in range(n):
        nome = fake.first_name()
        sobrenome = fake.last_name()
        data_de_nascimento = fake.date_of_birth()
        sexo = random.choice([sexo[0] for sexo in SEXO])
        rg = '{}.{}.{}-{}'.format(random.randrange(10, 99), random.randrange(100, 999), random.randrange(100, 999), random.choice([0, random.randrange(1, 9)]))
        cpf = CPF().generate(True)
        email = '{}@{}'.format(unidecode((nome + sobrenome).lower()), 'example.com').replace(' ', '')
        telefone = '({}) {}-{}'.format(random.randrange(10, 99), random.randrange(10000, 99999), random.randrange(1000, 9999))
        endereco = fake.street_name()
        numero = str(random.randrange(1, 999))
        bairro = fake.bairro()
        cidade = fake.city()
        estado = random.choice([estado[0] for estado in ESTADOS])
        cep = '{}-{}'.format(random.randrange(10000, 99999), random.randrange(100, 999))

        pessoa = Pessoa.objects.create(
            nome=nome,
            sobrenome=sobrenome,
            data_de_nascimento=data_de_nascimento,
            sexo=sexo,
            rg=rg,
            cpf=cpf,
            email=email,
            telefone=telefone,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep
        )

        pessoa.save()

criar_pessoas(100)

print('Pessoas criadas com sucesso!')