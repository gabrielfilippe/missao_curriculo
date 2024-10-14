from django.contrib.auth.models import User
from django.db import models

class Idioma(models.Model):
    IDIOMA_CHOICES = [
        ('Inglês', 'Inglês'),
        ('Espanhol', 'Espanhol'),
        ('Francês', 'Francês'),
        ('Alemão', 'Alemão'),
        ('Italiano', 'Italiano'),
        ('Mandarim', 'Mandarim'),
        ('Japonês', 'Japonês'),
        ('Russo', 'Russo'),
        ('Coreano', 'Coreano'),
        ('Árabe', 'Árabe'),
        ('Hebraico', 'Hebraico'),
        ('Hindi', 'Hindi'),
        ('Outro', 'Outro'),
    ]

    NIVEL_CHOICES = [
        ('Básico', 'Básico'),
        ('Intermediário', 'Intermediário'),
        ('Avançado', 'Avançado'),
        ('Fluente', 'Fluente'),
    ]

    # pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name='Pessoa')
    nome = models.CharField(max_length=255, choices=IDIOMA_CHOICES, verbose_name='Idioma')
    nivel = models.CharField(max_length=255, choices=NIVEL_CHOICES, verbose_name='Nível')

    class Meta:
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'

    def __str__(self):
        return f'{self.nome} ({self.nivel})'

# Create your models here.
class Pessoa(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outro', 'Outro'),
    ]

    CATEGORIA_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    nome = models.CharField(max_length=255, verbose_name='Nome')
    sobrenome = models.CharField(max_length=255, verbose_name='Sobrenome')
    data_de_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=255, choices=SEXO_CHOICES, verbose_name='Sexo')
    cpf = models.CharField(max_length=255, verbose_name='CPF')
    rg = models.CharField(max_length=255, verbose_name='RG')
    e_pcd = models.BooleanField(default=False, verbose_name='É pessoa com deficiência?')
    possui_cnh = models.BooleanField(default=False, verbose_name='Possui CNH?')
    categoria_da_cnh = models.CharField(max_length=255, choices=CATEGORIA_CHOICES, null=True, blank=True, verbose_name='Categoria da CNH')
    e_primeiro_emprego = models.BooleanField(default=False, verbose_name='Primeiro Emprego?')
    idiomas = models.ManyToManyField(Idioma, verbose_name='Idiomas')
    imagem = models.ImageField(upload_to='imagens/', null=True, blank=True, verbose_name='Imagem')

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.nome + ' ' + self.sobrenome
    
class Contato(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, verbose_name='Pessoa')
    email = models.EmailField(max_length=255, verbose_name='E-mail')
    telefone = models.CharField(max_length=255, verbose_name='Telefone')

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return self.telefone + ' - ' + self.email
    
class Endereco(models.Model):
    ESTADOS_CHOICES = [
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

    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, verbose_name='Pessoa')
    rua = models.CharField(max_length=255, verbose_name='Rua')
    numero = models.PositiveIntegerField(verbose_name='Número')
    bairro = models.CharField(max_length=255, verbose_name='Bairro')
    complemento = models.CharField(max_length=255, verbose_name='Complemento')
    cidade = models.CharField(max_length=255, verbose_name='Cidade')
    estado = models.CharField(max_length=255, choices=ESTADOS_CHOICES, verbose_name='Estado')
    cep = models.CharField(max_length=255, verbose_name='CEP')

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):
        return self.rua + ', ' + str(self.numero) + ' - ' + self.bairro + ', ' + self.cidade + ' - ' + self.estado
    
class AreaInteresse(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')

    class Meta:
        verbose_name = 'Área de Interesse'
        verbose_name_plural = 'Áreas de Interesse'

    def __str__(self):
        return self.nome
    
class SubareaInteresse(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    area_de_interesse = models.ForeignKey(AreaInteresse, on_delete=models.CASCADE, verbose_name='Área de Interesse')

    class Meta:
        verbose_name = 'Subárea de Interesse'
        verbose_name_plural = 'Subáreas de Interesse'

    def __str__(self):
        return f'{self.nome} ({self.area_de_interesse.nome})'
    
class Curriculo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuário')
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, verbose_name='Pessoa')
    resumo = models.TextField(verbose_name='Resumo')
    # area_de_interesse = models.ForeignKey(AreaInteresse, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Área de Interesse')
    subareas_de_interesse = models.ManyToManyField(SubareaInteresse, verbose_name='Subáreas de Interesse')
    informacoes_adicionais = models.TextField(verbose_name='Informações Adicionais')
    status = models.BooleanField(default = True, verbose_name='Empregado ou não')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Currículo'
        verbose_name_plural = 'Currículos'

    def __str__(self):
        return self.pessoa.nome + ' ' + self.pessoa.sobrenome

class Instituicao(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    
    class Meta:
        verbose_name = 'Instituição'
        verbose_name_plural = 'Instituições'

    def __str__(self):
        return self.nome
    
class FormacaoAcademica(models.Model):
    curriculo = models.ForeignKey(Curriculo, on_delete=models.CASCADE, verbose_name='Currículo')
    instituicao = models.ForeignKey(Instituicao, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Instituição')
    grau = models.CharField(max_length=255, verbose_name='Grau')
    curso = models.CharField(max_length=255, verbose_name='Curso')
    data_de_inicio = models.DateField(verbose_name='Data de Início')
    data_de_conclusao = models.DateField(null=True, blank=True, verbose_name='Data de Conclusão')

    class Meta:
        verbose_name = 'Formação Acadêmica'
        verbose_name_plural = 'Formações Acadêmicas'

    def __str__(self):
        return self.curso + ' - ' + self.instituicao.nome
    
class Empresa(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nome
    
class ExperienciaProfissional(models.Model):
    curriculo = models.ForeignKey(Curriculo, on_delete=models.CASCADE, verbose_name='Currículo')
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Empresa')
    cargo = models.CharField(max_length=255, verbose_name='Cargo')
    data_de_inicio = models.DateField(verbose_name='Data de Início')
    data_de_saida = models.DateField(null=True, blank=True, verbose_name='Data de Saída')
    descricao = models.TextField(null=True, blank=True, verbose_name='Descrição')

    class Meta:
        verbose_name = 'Experiência Profissional'
        verbose_name_plural = 'Experiências Profissionais'

    def __str__(self):
        return self.cargo + ' - ' + self.empresa.nome
    
class Habilidade(models.Model):
    curriculo = models.ForeignKey(Curriculo, on_delete=models.CASCADE, verbose_name='Currículo')
    nome = models.CharField(max_length=255, verbose_name='Nome')

    class Meta:
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return self.nome