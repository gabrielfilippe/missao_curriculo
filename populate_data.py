import os
import django
import random
from faker import Faker
from validate_docbr import CPF

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import Pessoa, Contato, Endereco, Idioma, AreaInteresse, SubareaInteresse, Curriculo, Instituicao, FormacaoAcademica, Empresa, ExperienciaProfissional, Habilidade

def create_area_interesse():
    areas = ["Tecnologia", "Saúde", "Educação", "Administração", "Engenharia"]
    for area in areas:
        AreaInteresse.objects.create(nome=area)
    print("Áreas de interesse criadas com sucesso!")

def create_subarea_interesse():
    subareas = {
        "Tecnologia": ["Desenvolvimento de Software", "Suporte Técnico", "Segurança da Informação"],
        "Saúde": ["Enfermagem", "Medicina", "Fisioterapia"],
        "Educação": ["Ensino Fundamental", "Ensino Médio", "Ensino Superior"],
        "Administração": ["Recursos Humanos", "Financeiro", "Logística"],
        "Engenharia": ["Civil", "Elétrica", "Mecânica"]
    }
    for area, subs in subareas.items():
        area_obj = AreaInteresse.objects.get(nome=area)
        for sub in subs:
            SubareaInteresse.objects.create(nome=sub, area_de_interesse=area_obj)
    print("Subáreas de interesse criadas com sucesso!")

def create_instituicoes():
    instituicoes = ["Universidade de São Paulo", "Universidade Federal do Rio de Janeiro", "Universidade Estadual de Campinas", "Universidade Federal de Minas Gerais", "Pontifícia Universidade Católica"]
    for nome in instituicoes:
        Instituicao.objects.create(nome=nome)
    print("Instituições criadas com sucesso!")

def create_empresas():
    empresas = ["Google", "Microsoft", "Apple", "Amazon", "Facebook"]
    for nome in empresas:
        Empresa.objects.create(nome=nome)
    print("Empresas criadas com sucesso!")

def create_pessoas(quantity):
    faker = Faker('pt_BR')

    SEXO_CHOICES = ['Masculino', 'Feminino', 'Outro']
    CATEGORIA_CHOICES = ['A', 'B', 'AB', 'C', 'D', 'E']
    ESTADOS_CHOICES = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    IDIOMA_CHOICES = ['Inglês', 'Espanhol', 'Francês', 'Alemão', 'Italiano', 'Mandarim', 'Japonês', 'Russo', 'Coreano', 'Árabe', 'Hebraico', 'Hindi', 'Outro']
    NIVEL_CHOICES = ['Básico', 'Intermediário', 'Avançado', 'Fluente']

    for _ in range(quantity):
        # Criar usuário
        user = User.objects.create_user(username=faker.user_name(), password='senha123')

        # Criar pessoa
        pessoa = Pessoa.objects.create(
            nome=faker.first_name(),
            sobrenome=faker.last_name(),
            data_de_nascimento=faker.date_of_birth(minimum_age=18, maximum_age=70),
            sexo=random.choice(SEXO_CHOICES),
            cpf=CPF().generate(True),
            rg="{}.{}.{}-{}".format(random.randrange(10, 99), random.randrange(100, 999), random.randrange(100, 999), random.choice([0, random.randrange(1, 9)])),
            e_pcd=faker.boolean(),
            possui_cnh=faker.boolean(),
            categoria_da_cnh=random.choice(CATEGORIA_CHOICES) if faker.boolean() else None,
            e_primeiro_emprego=faker.boolean(),
            imagem=None  # Ajuste conforme necessário para lidar com imagens
        )

        # Criar contato
        Contato.objects.create(
            pessoa=pessoa,
            email=faker.email(),
            telefone="({}) {}-{}".format(random.randrange(10, 99), random.randrange(10000, 99999), random.randrange(1000, 9999))
        )

        # Criar endereço
        Endereco.objects.create(
            pessoa=pessoa,
            rua=faker.street_name(),
            numero=faker.building_number(),
            bairro=faker.bairro(),
            complemento=faker.word(),  # Substituto para secondary_address
            cidade=faker.city(),
            estado=random.choice(ESTADOS_CHOICES),
            cep=faker.postcode()
        )

        # Criar idiomas
        num_idiomas = random.randint(1, 3)
        for _ in range(num_idiomas):
            Idioma.objects.create(
                pessoa=pessoa,
                nome=random.choice(IDIOMA_CHOICES),
                nivel=random.choice(NIVEL_CHOICES)
            )

        # Criar currículo
        curriculo = Curriculo.objects.create(
            usuario=user,
            pessoa=pessoa,
            resumo=faker.text(max_nb_chars=200),
            informacoes_adicionais=faker.text(max_nb_chars=100)
        )

        # Criar subáreas de interesse
        subareas = list(SubareaInteresse.objects.all())
        num_subareas = random.randint(1, min(3, len(subareas)))
        if num_subareas > 0:
            curriculo.subareas_de_interesse.set(random.sample(subareas, num_subareas))

        # Criar formação acadêmica
        instituicoes = list(Instituicao.objects.all())
        num_formacoes = random.randint(1, 3)
        for _ in range(num_formacoes):
            FormacaoAcademica.objects.create(
                curriculo=curriculo,
                instituicao=random.choice(instituicoes),
                grau=random.choice(['Bacharelado', 'Licenciatura', 'Tecnólogo', 'Mestrado', 'Doutorado']),
                curso=faker.job(),
                data_de_inicio=faker.date_between(start_date='-10y', end_date='-5y'),
                data_de_conclusao=faker.date_between(start_date='-5y', end_date='today')
            )

        # Criar experiência profissional
        empresas = list(Empresa.objects.all())
        num_experiencias = random.randint(1, 3)
        for _ in range(num_experiencias):
            ExperienciaProfissional.objects.create(
                curriculo=curriculo,
                empresa=random.choice(empresas),
                cargo=faker.job(),
                data_de_inicio=faker.date_between(start_date='-10y', end_date='-5y'),
                data_de_saida=faker.date_between(start_date='-5y', end_date='today'),
                descricao=faker.text(max_nb_chars=200)
            )

        # Criar habilidades
        habilidades = ['Python', 'Django', 'JavaScript', 'SQL', 'Git', 'Linux']
        num_habilidades = random.randint(2, 5)
        for _ in range(num_habilidades):
            Habilidade.objects.create(
                curriculo=curriculo,
                nome=random.choice(habilidades)
            )

    print('Dados criados com sucesso!')

# Primeiro criar as áreas de interesse, subáreas, instituições e empresas
create_area_interesse()
create_subarea_interesse()
create_instituicoes()
create_empresas()

# Em seguida, criar pessoas e currículos
create_pessoas(50)