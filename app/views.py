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
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

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

@login_required(login_url=reverse_lazy('admin:login'))
def curriculo_pdf_view(request, pk):
    curriculo = get_object_or_404(Curriculo, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="curriculo_{curriculo.pessoa.nome}.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    p = curriculo.pessoa

    # Add image if exists
    if p.imagem:
        image_path = os.path.join(settings.MEDIA_ROOT, p.imagem.name)
        img = Image(image_path)
        img.drawHeight = 100
        img.drawWidth = 100
        elements.append(img)
        elements.append(Spacer(1, 12))

    # Heading
    heading = Paragraph(f"<b>{p.nome} {p.sobrenome}</b>", styles['Title'])
    elements.append(heading)

    contact_info = Paragraph(f"Data de nascimento: {p.data_de_nascimento.strftime('%d/%m/%Y')}, {p.sexo}", styles['Normal'])
    elements.append(contact_info)
    contact_info = Paragraph(f"Endereço: {p.endereco.endereco}, {p.endereco.numero} - {p.endereco.bairro}, {p.endereco.cidade} - {p.endereco.estado}", styles['Normal'])
    elements.append(contact_info)
    contact_info = Paragraph(f"Telefone: {p.contato.telefone} Email: {p.contato.email}", styles['Normal'])
    elements.append(contact_info)
    elements.append(Spacer(1, 12))

    # Resumo
    if curriculo.resumo:
        elements.append(Paragraph("Resumo", styles['Heading2']))
        elements.append(Paragraph(curriculo.resumo, styles['Normal']))
        elements.append(Spacer(1, 12))

    # Formação Acadêmica
    elements.append(Paragraph("Formação Acadêmica", styles['Heading2']))
    for formacao in curriculo.formacaoacademica_set.all():
        data_de_conclusao = formacao.data_de_conclusao.strftime('%m/%Y') if formacao.data_de_conclusao else 'Em andamento'
        formacao_text = f"{formacao.curso} - {formacao.instituicao.nome} - {data_de_conclusao}"
        elements.append(Paragraph(formacao_text, styles['Normal']))
        elements.append(Spacer(1, 6))

    # Experiência Profissional
    elements.append(Paragraph("Experiência Profissional", styles['Heading2']))
    for experiencia in curriculo.experienciaprofissional_set.all():
        data_de_saida = experiencia.data_de_saida.strftime('%m/%Y') if experiencia.data_de_saida else 'Presente'
        exp_text = f"{experiencia.cargo} - {experiencia.empresa.nome} - {experiencia.data_de_inicio.strftime('%m/%Y')} - {data_de_saida}"
        elements.append(Paragraph(exp_text, styles['Normal']))
        if experiencia.descricao:
            elements.append(Paragraph(experiencia.descricao, styles['Normal']))
        elements.append(Spacer(1, 6))

    # Habilidades
    if curriculo.habilidade_set.exists():
        elements.append(Paragraph("Habilidades", styles['Heading2']))
        for habilidade in curriculo.habilidade_set.all():
            elements.append(Paragraph(habilidade.nome, styles['Normal']))
            elements.append(Spacer(1, 6))

    # Idiomas
    if curriculo.pessoa.idioma_set.exists():
        elements.append(Paragraph("Idiomas", styles['Heading2']))
        for idioma in curriculo.pessoa.idioma_set.all():
            idioma_text = f"{idioma.nome} - {idioma.nivel}"
            elements.append(Paragraph(idioma_text, styles['Normal']))
            elements.append(Spacer(1, 6))

    # Áreas e Subáreas de Interesse
    if curriculo.subareas_de_interesse.exists():
        elements.append(Paragraph("Áreas de Interesse", styles['Heading2']))
        
        # Usar defaultdict para agrupar subáreas por áreas de interesse
        area_subareas = defaultdict(list)
        
        for subarea in curriculo.subareas_de_interesse.all():
            area_subareas[subarea.area_de_interesse.nome].append(subarea.nome)
        
        # Adicionar ao PDF
        for area, subareas in area_subareas.items():
            elements.append(Paragraph(f"Área: {area}", styles['Normal']))
            for subarea in subareas:
                elements.append(Paragraph(f"Subárea: {subarea}", styles['Normal']))
            elements.append(Spacer(1, 6))

    # Informações Adicionais
    if curriculo.informacoes_adicionais:
        elements.append(Paragraph("Informações Adicionais", styles['Heading2']))
        elements.append(Paragraph(curriculo.informacoes_adicionais, styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response