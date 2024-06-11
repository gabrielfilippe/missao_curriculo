from app.forms import *
from app.models import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    user = request.user
    context = {'user': user}
    return render(request, 'pages/home.html', context)

@login_required(login_url=reverse_lazy('admin:login'))
def pessoas(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pessoa cadastrada com sucesso!')
            return redirect('pessoas')
        else:
            messages.error(request, 'Erro ao cadastrar pessoa!')
    else:
        form = PessoaForm()

    pessoas = Pessoa.objects.all()
    context = {
        'form': form,
        'pessoas': pessoas
    }
    return render(request, 'pages/pessoas.html', context)

@login_required(login_url=reverse_lazy('admin:login'))
def curriculos(request):
    curriculos = Curriculo.objects.all()
    context = {
        'curriculos': curriculos
    }

    return render(request, 'pages/curriculos.html', context)

@login_required(login_url=reverse_lazy('admin:login'))
def criar_curriculo(request):
    if request.method == 'GET':
        curriculo_form = CurriculoForm()
        formacao_formset = FormacaoFormSet()
        experiencia_formset = ExperienciaFormSet()
        habilidade_formset = HabilidadeFormSet()

        context = {
            'curriculo_form': curriculo_form,
            'formacao_formset': formacao_formset,
            'experiencia_formset': experiencia_formset,
            'habilidade_formset': habilidade_formset
        }

        return render(request, 'pages/criar_curriculo.html', context)
    elif request.method == 'POST':
        curriculo_form = CurriculoForm(request.POST)
        formacao_formset = FormacaoFormSet(request.POST)
        experiencia_formset = ExperienciaFormSet(request.POST)
        habilidade_formset = HabilidadeFormSet(request.POST)

        if curriculo_form.is_valid() and formacao_formset.is_valid() and experiencia_formset.is_valid() and habilidade_formset.is_valid():
            curriculo = curriculo_form.save(commit=False)
            curriculo.user = request.user
            curriculo.save()
            formacao_formset.instance = curriculo
            formacao_formset.save()
            experiencia_formset.instance = curriculo
            experiencia_formset.save()
            habilidade_formset.instance = curriculo
            habilidade_formset.save()
            messages.success(request, 'Currículo criado com sucesso!')
            return redirect('criar_curriculo')
        else:
            messages.error(request, 'Erro ao criar currículo!')
            context = {
                'curriculo_form': curriculo_form,
                'formacao_formset': formacao_formset,
                'experiencia_formset': experiencia_formset,
                'habilidade_formset': habilidade_formset
            }

            return render(request, 'pages/criar_curriculo.html', context)

    return render(request, 'pages/criar_curriculo.html')

@login_required(login_url=reverse_lazy('admin:login'))
def editar_curriculo(request, id):
    curriculo = get_object_or_404(Curriculo, id=id)

    if request.method == 'GET':
        curriculo_form = CurriculoForm(instance=curriculo)
        formacao_formset = FormacaoFormSet(instance=curriculo)
        experiencia_formset = ExperienciaFormSet(instance=curriculo)
        habilidade_formset = HabilidadeFormSet(instance=curriculo)

        context = {
            'curriculo_form': curriculo_form,
            'formacao_formset': formacao_formset,
            'experiencia_formset': experiencia_formset,
            'habilidade_formset': habilidade_formset
        }

        return render(request, 'pages/editar_curriculo.html', context)
    elif request.method == 'POST':
        curriculo_form = CurriculoForm(request.POST, instance=curriculo)
        formacao_formset = FormacaoFormSet(request.POST, instance=curriculo)
        experiencia_formset = ExperienciaFormSet(request.POST, instance=curriculo)
        habilidade_formset = HabilidadeFormSet(request.POST, instance=curriculo)

        if curriculo_form.is_valid() and formacao_formset.is_valid() and experiencia_formset.is_valid() and habilidade_formset.is_valid():
            curriculo = curriculo_form.save(commit=False)
            curriculo.user = request.user
            curriculo.save()
            formacao_formset.instance = curriculo
            formacao_formset.save()
            experiencia_formset.instance = curriculo
            experiencia_formset.save()
            habilidade_formset.instance = curriculo
            habilidade_formset.save()
            messages.success(request, 'Currículo editado com sucesso!')
            return redirect('curriculos')
        else:
            messages.error(request, 'Erro ao editar currículo!')
            context = {
                'curriculo_form': curriculo_form,
                'formacao_formset': formacao_formset,
                'experiencia_formset': experiencia_formset,
                'habilidade_formset': habilidade_formset
            }

            return render(request, 'pages/editar_curriculo.html', context)

    return render(request, 'pages/editar_curriculo.html')

@login_required(login_url=reverse_lazy('admin:login'))
def excluir_curriculo(request, id):
    curriculo = get_object_or_404(Curriculo, id=id)
    curriculo.delete()
    messages.success(request, 'Currículo excluído com sucesso!')
    return redirect('curriculos')


#sistema de filtragem
@login_required(login_url=reverse_lazy('admin:login'))
def filtrar_curriculo(request):
    form = CurriculoFilterForm(request.GET or None)
    curriculos = Curriculo.objects.none()

    if form.is_valid():
        curriculos = Curriculo.objects.all()
        nome = form.cleaned_data.get('nome')
        sobrenome = form.cleaned_data.get('sobrenome')
        sexo = form.cleaned_data.get('sexo')

        if nome:
            curriculos = curriculos.filter(pessoa__nome__icontains=nome)
        if sobrenome:
            curriculos = curriculos.filter(pessoa__sobrenome__icontains=sobrenome)
        if sexo:
            curriculos = curriculos.filter(pessoa__sexo=sexo)

    # Obter as pessoas que têm currículos
    pessoas_com_curriculo = Pessoa.objects.filter(curriculo__in=curriculos)

    context = {
        'form': form,
        'pessoas_com_curriculo': pessoas_com_curriculo
    }

    return render(request, 'pages/filtrar_curriculo.html', context)