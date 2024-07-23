import os
from app.forms import *
from app.models import *
from collections import defaultdict
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, ListStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, Frame, ListFlowable, ListItem, FrameBreak
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT




# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('curriculo:home')

    if request.method == 'GET':
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'pages/login.html', context)
    elif request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if not request.POST.get('username') or not request.POST.get('password'):
            messages.error(request, 'Preencha todos os campos.')
            return redirect('curriculo:login')
        
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except User.DoesNotExist:
            messages.error(request, 'Usuário não existe.')
            return redirect('curriculo:login')
        
        if form.is_valid():
            user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

            if user is not None:
                login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('curriculo:home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('curriculo:login')
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout realizado com sucesso.')

    return redirect('curriculo:login')

def register(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'pages/register.html', context)
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)

        if not request.POST.get('username') or not request.POST.get('password1') or not request.POST.get('password2'):
            messages.error(request, 'Preencha todos os campos.')
            return redirect('curriculo:register')
        
        try:
            user = User.objects.get(username=request.POST.get('username'))
            messages.error(request, 'Esse usuário já existe.')
            return redirect('curriculo:register')
        except User.DoesNotExist:
            pass

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('curriculo:login')
        else:
            messages.error(request, 'Erro ao criar usuário.')
            return redirect('curriculo:register')

def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'pages/home.html', context)

@login_required(login_url=reverse_lazy('curriculo:login'))
def pessoas(request):
    pessoas = Pessoa.objects.all()
    context = {
        'pessoas': pessoas
    }

    return render(request, 'pages/pessoas.html', context)

@login_required(login_url=reverse_lazy('curriculo:login'))
def curriculos(request):
    curriculos = Curriculo.objects.all()
    pessoa_sexo_choices = Pessoa.SEXO_CHOICES
    pessoa_categoria_choices = Pessoa.CATEGORIA_CHOICES
    areas_de_interesse = AreaInteresse.objects.all()
    subareas_de_interesse = SubareaInteresse.objects.all()
    context = {
        'curriculos': curriculos,
        'pessoa_sexo_choices': pessoa_sexo_choices,
        'pessoa_categoria_choices': pessoa_categoria_choices,
        'areas_de_interesse': areas_de_interesse,
        'subareas_de_interesse': subareas_de_interesse
    }

    return render(request, 'pages/curriculos.html', context)

@login_required(login_url=reverse_lazy('curriculo:login'))
def criar_curriculo(request):
    if request.method == 'GET':
        pessoa_form = PessoaForm()
        contato_form = ContatoForm()
        endereco_form = EnderecoForm()
        idioma_formset = IdiomaFormSet()
        curriculo_form = CurriculoForm()
        formacao_formset = FormacaoAcademicaFormSet()
        experiencia_formset = ExperienciaProfissionalFormSet()
        habilidade_formset = HabilidadeFormSet()

        context = {
            'pessoa_form': pessoa_form,
            'contato_form': contato_form,
            'endereco_form': endereco_form,
            'idioma_formset': idioma_formset,
            'curriculo_form': curriculo_form,
            'formacao_formset': formacao_formset,
            'experiencia_formset': experiencia_formset,
            'habilidade_formset': habilidade_formset
        }

        return render(request, 'pages/criar_curriculo.html', context)
    elif request.method == 'POST':
        pessoa_form = PessoaForm(request.POST, request.FILES)
        contato_form = ContatoForm(request.POST)
        endereco_form = EnderecoForm(request.POST)
        idioma_formset = IdiomaFormSet(request.POST)
        curriculo_form = CurriculoForm(request.POST)
        formacao_formset = FormacaoAcademicaFormSet(request.POST)
        experiencia_formset = ExperienciaProfissionalFormSet(request.POST)
        habilidade_formset = HabilidadeFormSet(request.POST)

        if pessoa_form.is_valid() and contato_form.is_valid() and endereco_form.is_valid() and idioma_formset.is_valid() and curriculo_form.is_valid() and formacao_formset.is_valid() and experiencia_formset.is_valid() and habilidade_formset.is_valid():
            with transaction.atomic():
                pessoa = pessoa_form.save()
                contato = contato_form.save(commit=False)
                contato.pessoa = pessoa
                contato.save()
                endereco = endereco_form.save(commit=False)
                endereco.pessoa = pessoa
                endereco.save()
                idioma_formset.instance = pessoa
                idioma_formset.save()
                curriculo = curriculo_form.save(commit=False)
                curriculo.usuario = request.user
                curriculo.pessoa = pessoa
                curriculo.save()
                curriculo_form.save_m2m()  # Salvar os ManyToMany fields
                formacao_formset.instance = curriculo
                formacao_formset.save()
                experiencia_formset.instance = curriculo
                experiencia_formset.save()
                habilidade_formset.instance = curriculo
                habilidade_formset.save()

            messages.success(request, 'Currículo criado com sucesso!')

            return redirect('curriculos')
        else:
            messages.error(request, 'Erro ao criar currículo!')

            context = {
                'pessoa_form': pessoa_form,
                'contato_form': contato_form,
                'endereco_form': endereco_form,
                'idioma_formset': idioma_formset,
                'curriculo_form': curriculo_form,
                'formacao_formset': formacao_formset,
                'experiencia_formset': experiencia_formset,
                'habilidade_formset': habilidade_formset
            }

            return render(request, 'pages/criar_curriculo.html', context)
        

@login_required(login_url=reverse_lazy('curriculo:login'))
def filtrar_curriculos(request):
    nome_completo = request.GET.get('nome_completo', '')
    email = request.GET.get('email', '')
    data_de_nascimento = request.GET.get('data_de_nascimento', '')
    sexo = request.GET.get('sexo', '')
    categoria_da_cnh = request.GET.get('categoria_da_cnh', '')
    area_de_interesse = request.GET.get('area_de_interesse', '')
    subarea_de_interesse = request.GET.get('subarea_de_interesse', '')
    data_criacao = request.GET.get('data_criacao', '')
    e_pcd = request.GET.get('e_pcd', '')
    possui_cnh = request.GET.get('possui_cnh', '')
    e_primeiro_emprego = request.GET.get('e_primeiro_emprego', '')

    curriculos = Curriculo.objects.all()

    if nome_completo:
        curriculos = curriculos.filter(
            Q(pessoa__nome__icontains=nome_completo) | 
            Q(pessoa__sobrenome__icontains=nome_completo)
        )

    if email:
        curriculos = curriculos.filter(pessoa__contato__email__icontains=email)

    if sexo:
        curriculos = curriculos.filter(pessoa__sexo=sexo)

    if data_de_nascimento:
        curriculos = curriculos.filter(pessoa__data_de_nascimento=data_de_nascimento)

    if categoria_da_cnh:
        curriculos = curriculos.filter(pessoa__categoria_da_cnh=categoria_da_cnh)

    if area_de_interesse:
        curriculos = curriculos.filter(subareas_de_interesse__area_de_interesse__id=area_de_interesse)

    if subarea_de_interesse:
        curriculos = curriculos.filter(subareas_de_interesse__id=subarea_de_interesse)

    if data_criacao:
        curriculos = curriculos.filter(criado_em__date=data_criacao)

    if e_pcd:
        curriculos = curriculos.filter(pessoa__e_pcd=True)

    if possui_cnh:
        curriculos = curriculos.filter(pessoa__possui_cnh=True)

    if e_primeiro_emprego:
        curriculos = curriculos.filter(pessoa__e_primeiro_emprego=True)

    curriculos = curriculos.distinct()

    data = {
        'curriculos': [
            {
                'id': curriculo.id,
                'pessoa_nome': curriculo.pessoa.nome,
                'pessoa_sobrenome': curriculo.pessoa.sobrenome,
                'formacoes': list(curriculo.formacaoacademica_set.values_list('curso', flat=True)),
                'experiencias': list(curriculo.experienciaprofissional_set.values_list('cargo', flat=True)),
                'habilidades': list(curriculo.habilidade_set.values_list('nome', flat=True)),
                'criado_em': localtime(curriculo.criado_em).strftime('%d/%m/%Y %H:%M') if curriculo.criado_em else None,
                'atualizado_em': localtime(curriculo.atualizado_em).strftime('%d/%m/%Y %H:%M') if curriculo.atualizado_em else None,
            }
            for curriculo in curriculos
        ]
    }

    return JsonResponse(data)


#View que gera o PDF, tudo relacionado ao PDF, é aqui.
@login_required(login_url=reverse_lazy('admin:login'))
def curriculo_pdf_view(request, pk):
    curriculo = get_object_or_404(Curriculo, pk=pk)
    

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="curriculo_{curriculo.pessoa.nome}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    width, height = A4

    pessoa = curriculo.pessoa
    contato = pessoa.contato
    endereco = pessoa.endereco

    # Coordenadas de posição inicial
    x_offset = 2 * cm
    y_offset = height - 2 * cm

   # Adicionar a foto no lado superior esquerdo
    if pessoa.imagem:
        image_path = os.path.join(settings.MEDIA_ROOT, pessoa.imagem.name)
        image_reader = ImageReader(image_path)
        image_width, image_height = image_reader.getSize()
        aspect_ratio = image_width / image_height
        img_width = 4 * cm
        img_height = img_width / aspect_ratio
        
        if img_height > 4 * cm:
            img_height = 4 * cm
            img_width = img_height * aspect_ratio
        
        p.drawImage(image_reader, x_offset, y_offset - img_height, width=img_width, height=img_height)
        x_offset += img_width + 1 * cm  # Ajustar o offset para o texto ao lado da imagem

    # Ajustar o tamanho e estilo do nome
    p.setFont("Helvetica-Bold", 17)

    # Ajustar posição do nome
    p.drawString(x_offset, y_offset - 0.6 * cm, f"{pessoa.nome} {pessoa.sobrenome}")

    #espaço entre o nome e as info

    y_offset -= 0 * cm

    # Ajustar o tamanho e estilo das informações
    p.setFont("Helvetica", 11)

    # Informações ao lado da foto
    p.drawString(x_offset, y_offset - 1.5 * cm, f"Data de Nascimento: {pessoa.data_de_nascimento.strftime('%d/%m/%Y')}")
    p.drawString(x_offset, y_offset - 2 * cm, f"Sexo: {pessoa.sexo}")
    p.drawString(x_offset, y_offset - 2.5 * cm, f"CPF: {pessoa.cpf} | RG: {pessoa.rg}")

    # Espaço após as informações ao lado da foto
    y_offset -= 2.5 * cm

    # Endereço
    p.drawString(x_offset, y_offset - 0.5 * cm, f"Endereço: {endereco.rua}, {endereco.numero} - {endereco.bairro}, {endereco.cidade} - {endereco.estado} - {endereco.cep}")
    # Espaço após o endereço
    y_offset -= 0.5 * cm

    # Contato
    p.drawString(x_offset, y_offset - 0.5 * cm, f"Telefone: {contato.telefone}")
    p.drawString(x_offset, y_offset - 1 * cm, f"Email: {contato.email}")
    # Espaço após o contato
    y_offset -= 2.0 * cm

    # Adicionar conteúdo adicional (resumo, formação acadêmica, experiência profissional, habilidades, idiomas, áreas e subáreas de interesse)
    styles = getSampleStyleSheet()
    elements = []


    styles = getSampleStyleSheet()
    elements = []

    # Adicionando resumo
    styles = getSampleStyleSheet()
    if curriculo.resumo:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y_offset, "RESUMO")
        #Distancia entre o topico e a linha separadora
        y_offset -= 0.2 * cm
        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)
        y_offset -= 0.3 * cm

        # Adiciona o resumo como um parágrafo com quebra de linha automática
        resumo_paragraph = Paragraph(curriculo.resumo, styles['Normal'])
        resumo_width, resumo_height = resumo_paragraph.wrap(width - 4 * cm, height - y_offset)
        resumo_paragraph.drawOn(p, 2 * cm, y_offset - resumo_height)
        y_offset -= resumo_height + 0.8 * cm  # Atualiza a posição y_offset com base na altura do resumo


  # Formação Acadêmica
    if curriculo.formacaoacademica_set.exists():
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y_offset, "FORMAÇÃO ACADÊMICA")
        # espaço entre o tópico e a linha separadora
        y_offset -= 0.2 * cm
        # Linha separadora
        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)
        y_offset -= 0.8 * cm

        # Adicionar o texto das formações acadêmicas em forma de tópicos
        p.setFont("Helvetica", 11)
        for formacao in curriculo.formacaoacademica_set.all():
            data_de_conclusao = formacao.data_de_conclusao.strftime('%m/%Y') if formacao.data_de_conclusao else 'Em andamento'
            formacao_text = f"\u2022 {formacao.curso} - {formacao.instituicao.nome} - {data_de_conclusao}"
            p.drawString(2.0 * cm, y_offset, formacao_text)
            y_offset -= 0.5 * cm

        # Ajustar o y_offset após adicionar as formações acadêmicas
        y_offset -= 0.5 * cm

    # Experiência Profissional
    if curriculo.experienciaprofissional_set.exists():
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y_offset, "EXPERIÊNCIA PROFISSIONAL")
        # espaço entre o tópico e a linha separadora
        y_offset -= 0.2 * cm
        # Linha separadora
        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)
        y_offset -= 0.8 * cm

        p.setFont("Helvetica", 11)
        for experiencia in curriculo.experienciaprofissional_set.all():
            data_de_saida = experiencia.data_de_saida.strftime('%m/%Y') if experiencia.data_de_saida else 'Presente'
            exp_text = f"{experiencia.cargo} - {experiencia.empresa.nome} - {experiencia.data_de_inicio.strftime('%m/%Y')} - {data_de_saida}"
            p.drawString(2 * cm, y_offset, exp_text)
            if experiencia.descricao:
                y_offset -= 0.5 * cm
                p.drawString(2 * cm, y_offset, experiencia.descricao)
            y_offset -= 1 * cm

        y_offset -= 0.3 * cm

     # Habilidades
    if curriculo.habilidade_set.exists():
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y_offset, "HABILIDADES")
        # espaço entre o tópico e a linha separadora
        y_offset -= 0.2 * cm

        # Linha separadora
        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)
        y_offset -= 0.8 * cm

        # Adicionar o texto das habilidades em forma de tópicos
        p.setFont("Helvetica", 11)
        for habilidade in curriculo.habilidade_set.all():
            habilidade_text = f"\u2022 {habilidade.nome}"
            p.drawString(2.0 * cm, y_offset, habilidade_text)
            y_offset -= 0.5 * cm

        # Ajustar o y_offset após adicionar as habilidades
        y_offset -= 0.5 * cm

    # y_offset -= 1.5 * cm

    # Idiomas
    if pessoa.idioma_set.exists():
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y_offset, "IDIOMAS")
        y_offset -= 0.2 * cm
        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)
        y_offset -= 0.8 * cm
        p.setFont("Helvetica", 11)
        for idioma in pessoa.idioma_set.all():
            idioma_text = f"\u2022 {idioma.nome} - {idioma.nivel}"
            p.drawString(2 * cm, y_offset, idioma_text)
            y_offset -= 0.5 * cm

    y_offset -= 0.5 * cm

    # Áreas e Subáreas de Interesse
    if curriculo.subareas_de_interesse.exists():
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y_offset, "ÁREAS E SUBÁREAS DE INTERESSE")
        y_offset -= 0.2 * cm
        p.line(2 * cm, y_offset, width - 2 * cm, y_offset)
        y_offset -= 0.8 * cm
        p.setFont("Helvetica", 11)
        for subarea in curriculo.subareas_de_interesse.all():
            subarea_text = f"\u2022 {subarea.nome} ({subarea.area_de_interesse.nome})"
            p.drawString(2 * cm, y_offset, subarea_text)
            y_offset -= 0.5 * cm

    p.showPage()
    p.save()

    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()
    return response