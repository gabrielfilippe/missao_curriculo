from django.contrib.auth.models import User
from django.db import models

# Create your models here.
SEXO = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
    ('N', 'Não Informar')
]

ESTADOS = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins')
]

class Pessoa(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    sobrenome = models.CharField(max_length=255, verbose_name='Sobrenome')
    data_de_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=255, choices=SEXO, default='N', verbose_name='Sexo')
    rg = models.CharField(max_length=255, verbose_name='RG')
    cpf = models.CharField(max_length=255, verbose_name='CPF')
    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')
    telefone = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telefone')
    endereco = models.CharField(max_length=255, null=True, blank=True, verbose_name='Endereço')
    numero = models.CharField(max_length=255, null=True, blank=True, verbose_name='Número')
    complemento = models.CharField(max_length=255, null=True, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=255, null=True, blank=True, verbose_name='Cidade')
    estado = models.CharField(max_length=255, null=True, blank=True, choices=ESTADOS, verbose_name='Estado')
    cep = models.CharField(max_length=255, null=True, blank=True, verbose_name='CEP')
    imagem = models.ImageField(upload_to='pessoas', null=True, blank=True, verbose_name='Imagem')

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.nome
    
class Instituicao(models.Model):
    nome = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome')

    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

    def __str__(self):
        return self.nome
    
class Formacao(models.Model):
    curso = models.CharField(max_length=255, null=True, blank=True, verbose_name='Curso')
    instituicao = models.ForeignKey(Instituicao, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Instituição')
    data_de_inicio = models.DateField(null=True, blank=True, verbose_name='Data de Início')
    data_de_conclusao = models.DateField(null=True, blank=True, verbose_name='Data de Conclusão')
    curriculo = models.ForeignKey('Curriculo', on_delete=models.CASCADE, related_name='formacoes', verbose_name='Currículo')

    class Meta:
        verbose_name = 'Formação'
        verbose_name_plural = 'Formações'

    def __str__(self):
        return self.curso
    
class Experiencia(models.Model):
    cargo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Cargo')
    empresa = models.CharField(max_length=255, null=True, blank=True, verbose_name='Empresa')
    data_de_inicio = models.DateField(null=True, blank=True, verbose_name='Data de Início')
    data_de_saida = models.DateField(null=True, blank=True, verbose_name='Data de Saída')
    descricao = models.TextField(null=True, blank=True, verbose_name='Descrição')
    curriculo = models.ForeignKey('Curriculo', on_delete=models.CASCADE, related_name='experiencias', verbose_name='Currículo')

    class Meta:
        verbose_name = 'Experiência'
        verbose_name_plural = 'Experiências'

    def __str__(self):
        return self.cargo
    
class Habilidade(models.Model):
    nome = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nome')
    curriculo = models.ForeignKey('Curriculo', on_delete=models.CASCADE, related_name='habilidades', verbose_name='Currículo')

    class Meta:
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return self.nome
    
class Curriculo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    pessoa = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Pessoa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Currículo'
        verbose_name_plural = 'Currículos'

    def __str__(self):
        return self.pessoa.nome