from app.models import *
from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django_select2.forms import ModelSelect2Widget
from dal import autocomplete

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = '__all__'

class CurriculoForm(forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = ['pessoa']

    def __init__(self, *args, **kwargs):
        super(CurriculoForm, self).__init__(*args, **kwargs)
        self.fields['pessoa'].queryset = Pessoa.objects.all()

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

class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FormacaoForm, self).__init__(*args, **kwargs)
        self.fields['instituicao'].queryset = Instituicao.objects.all()
        

FormacaoFormSet = custom_formset_factory(
    Curriculo,
    Formacao,
    form=FormacaoForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
    widgets={
        'data_de_inicio': forms.DateInput(attrs={'type': 'date'}),
        'data_de_conclusao': forms.DateInput(attrs={'type': 'date'}),
    },
    formset=CustomBaseInlineFormSet
)

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = '__all__'

ExperienciaFormSet = custom_formset_factory(
    Curriculo,
    Experiencia,
    form=ExperienciaForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
    widgets={
        'data_de_inicio': forms.DateInput(attrs={'type': 'date'}),
        'data_de_saida': forms.DateInput(attrs={'type': 'date'}),
        'descricao': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
    },
    formset=CustomBaseInlineFormSet
)

class HabilidadeForm(forms.ModelForm):
    class Meta:
        model = Habilidade
        fields = '__all__'

HabilidadeFormSet = custom_formset_factory(
    Curriculo,
    Habilidade,
    form=HabilidadeForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)