from app.models import *
from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

# Forms

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: João'}),
            'sobrenome': forms.TextInput(attrs={'placeholder': 'Ex: Silva'}),
            'data_de_nascimento': forms.DateInput(attrs={'placeholder': 'Ex: 01/01/2000'}),
            'sexo': forms.Select(attrs={'placeholder': 'Selecione seu gênero'}),
            'cpf': forms.TextInput(attrs={'placeholder': 'Ex: 123.456.789-00'}),
            'rg': forms.TextInput(attrs={'placeholder': 'Ex: 12.345.678'}),
            'e_pcd': forms.CheckboxInput(attrs={'placeholder': 'Você é uma pessoa com deficiência?'}),
            'possui_cnh': forms.CheckboxInput(attrs={'placeholder': 'Você possui CNH?'}),
            'categoria': forms.Select(attrs={'placeholder': 'Selecione a categoria da CNH'}),
            'e_primeiro_emprego': forms.CheckboxInput(attrs={'placeholder': 'É seu primeiro emprego?'}),
            'imagem': forms.ClearableFileInput(attrs={'placeholder': 'Envie uma imagem'}),
        }

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        exclude = ['pessoa']
        widgets = {
            'telefone': forms.TextInput(attrs={'placeholder': 'Ex: (11) 98765-4321', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ex: joaosilva@example.com'}),
        }

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        exclude = ['pessoa']
        widgets = {
            'rua': forms.TextInput(attrs={'placeholder': 'Ex: Rua das Flores'}),
            'numero': forms.NumberInput(attrs={'placeholder': 'Ex: 123'}),
            'complemento': forms.TextInput(attrs={'placeholder': 'Ex: Apto 101', 'required': False}),
            'bairro': forms.TextInput(attrs={'placeholder': 'Ex: Centro'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Ex: São Paulo'}),
            'estado': forms.Select(attrs={'placeholder': 'Ex: SP'}),
            'cep': forms.TextInput(attrs={'placeholder': 'Ex: 12345-678', 'pattern': '[0-9]{5}-[0-9]{3}', 'title': 'Formato: 12345-678'}),
        }

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = '__all__'

class AreaInteresseForm(forms.ModelForm):
    class Meta:
        model = AreaInteresse
        fields = '__all__'

class SubAreaInteresseForm(forms.ModelForm):
    class Meta:
        model = SubareaInteresse
        fields = '__all__'

class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = '__all__'
        exclude = ['usuario', 'pessoa']
        widgets = {
            'resumo': forms.Textarea(attrs={'placeholder': 'Ex: Sou um desenvolvedor web com 5 anos de experiência em Python, Django, HTML, CSS e JavaScript', 'rows': 3}),
            'subareas_de_interesse': forms.SelectMultiple(attrs={'placeholder': 'Selecione suas áreas de interesse'}),
            'informacoes_adicionais': forms.Textarea(attrs={'placeholder': 'Ex: Disponibilidade para viagens e mudanças de cidade', 'rows': 3}),
        }

class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = '__all__'

class FormacaoAcademicaForm(forms.ModelForm):
    class Meta:
        model = FormacaoAcademica
        fields = '__all__'
        widgets = {
            'instituicao': forms.Select(attrs={'placeholder': 'Selecione a instituição'}),
            'grau': forms.TextInput(attrs={'placeholder': 'Ex: Bacharelado'}),
            'curso': forms.TextInput(attrs={'placeholder': 'Ex: Ciência da Computação'}),
            'data_de_inicio': forms.DateInput(attrs={'placeholder': 'Ex: 01/01/2015', 'type': 'text', 'class': 'date-field'}),
            'data_de_conclusao': forms.DateInput(attrs={'placeholder': 'Ex: 01/01/2019', 'type': 'text', 'class': 'date-field'}),
        }

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

class ExperienciaProfissionalForm(forms.ModelForm):
    class Meta:
        model = ExperienciaProfissional
        fields = '__all__'
        widgets = {
            'empresa': forms.Select(attrs={'placeholder': 'Selecione a empresa'}),
            'cargo': forms.TextInput(attrs={'placeholder': 'Ex: Desenvolvedor Web'}),
            'data_de_inicio': forms.TextInput(attrs={'placeholder': 'Ex: 01/01/2015', 'type': 'text', 'class': 'date-field'}),
            'data_de_saida': forms.TextInput(attrs={'placeholder': 'Ex: 01/01/2019', 'type': 'text', 'class': 'date-field'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Ex: Desenvolvimento de aplicações web com Django', 'rows': 3}),
        }

class HabilidadeForm(forms.ModelForm):
    class Meta:
        model = Habilidade
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Proativo'}),
        }

# Formsets

class CustomBaseInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomBaseInlineFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

def custom_formset_factory(parent_model, model, form, formset=BaseInlineFormSet, **kwargs):
    FormSet = inlineformset_factory(parent_model, model, form=form, formset=formset, **kwargs)

    class CustomFormSet(FormSet):
        def add_fields(self, form, index):
            super().add_fields(form, index)
            form.fields['DELETE'].widget = forms.HiddenInput()

    return CustomFormSet

IdiomaFormSet = custom_formset_factory(Pessoa, Idioma, form=IdiomaForm, extra=1)
FormacaoAcademicaFormSet = custom_formset_factory(Curriculo, FormacaoAcademica, form=FormacaoAcademicaForm, extra=1)
ExperienciaProfissionalFormSet = custom_formset_factory(Curriculo, ExperienciaProfissional, form=ExperienciaProfissionalForm, extra=1)
HabilidadeFormSet = custom_formset_factory(Curriculo, Habilidade, form=HabilidadeForm, extra=1)