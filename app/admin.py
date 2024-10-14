from app.models import *
from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
class PessoaAdmin(admin.ModelAdmin):
    class IdiomaInline(admin.TabularInline):
        model = Pessoa.idiomas.through
        extra = 0
        verbose_name = 'idioma'
        verbose_name_plural = 'idiomas'

    class ContatoInline(admin.TabularInline):
        model = Contato
        verbose_name = 'Informações de Contato'

    class EnderecoInline(admin.StackedInline):
        model = Endereco
        verbose_name = 'Informações Residenciais'

    inlines = [ContatoInline, EnderecoInline, IdiomaInline]
    exclude = ['idiomas']
    fieldsets = [('INFORMAÇÕES PESSOAIS', {'fields': ['nome', 'sobrenome', 'data_de_nascimento', 'sexo', 'cpf', 'rg', 'e_pcd', 'possui_cnh', 'categoria_da_cnh', 'e_primeiro_emprego', 'imagem']})]
    list_display = ['nome', 'sobrenome', 'data_de_nascimento', 'sexo', 'cpf', 'rg', 'e_pcd', 'possui_cnh', 'categoria_da_cnh', 'e_primeiro_emprego', 'imagem']

    # def get_idiomas(self, obj):
    #     return mark_safe('<br>'.join([idioma.nome for idioma in obj.idioma_set.all()]) if obj.idioma_set.all() else '-')
    
    # get_idiomas.short_description = 'Idiomas'

class AreaInteresseAdmin(admin.ModelAdmin):
    class SubareaInteresseInline(admin.TabularInline):
        model = SubareaInteresse
        extra = 0

    inlines = [SubareaInteresseInline]
    list_display = ['nome', 'get_subareas']

    def get_subareas(self, obj):
        return mark_safe('<br>'.join([subarea.nome for subarea in obj.subareainteresse_set.all()]) if obj.subareainteresse_set.all() else '-')
    
    get_subareas.short_description = 'Subáreas de Interesse'

class CurriculoAdmin(admin.ModelAdmin):
    class FormacaoAcademicaInline(admin.StackedInline):
        model = FormacaoAcademica
        extra = 0

    class ExperienciaProfissionalInline(admin.StackedInline):
        model = ExperienciaProfissional
        extra = 0

    class HabilidadeInline(admin.TabularInline):
        model = Habilidade
        extra = 0
        
    inlines = [FormacaoAcademicaInline, ExperienciaProfissionalInline, HabilidadeInline]
    list_display = ['usuario', 'pessoa', 'resumo', 'get_subareas_de_interesse', 'get_formacoes_academicas', 'get_experiencias_profissionais', 'get_habilidades', 'informacoes_adicionais', 'criado_em', 'atualizado_em']
    filter_horizontal = ['subareas_de_interesse']

    def get_subareas_de_interesse(self, obj):
        return mark_safe('<br>'.join([subarea.nome for subarea in obj.subareas_de_interesse.all()]) if obj.subareas_de_interesse.all() else '-')
    
    get_subareas_de_interesse.short_description = 'Subáreas de Interesse'

    def get_formacoes_academicas(self, obj):
        return mark_safe('<br>'.join([formacao.instituicao.nome for formacao in obj.formacaoacademica_set.all()]) if obj.formacaoacademica_set.all() else '-')
    
    get_formacoes_academicas.short_description = 'Formações Acadêmicas'

    def get_experiencias_profissionais(self, obj):
        return mark_safe('<br>'.join([experiencia.empresa.nome for experiencia in obj.experienciaprofissional_set.all()]) if obj.experienciaprofissional_set.all() else '-')
    
    get_experiencias_profissionais.short_description = 'Experiências Profissionais'

    def get_habilidades(self, obj):
        return mark_safe('<br>'.join([habilidade.nome for habilidade in obj.habilidade_set.all()]) if obj.habilidade_set.all() else '-')
    
    get_habilidades.short_description = 'Habilidades'

admin.site.register(Idioma)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Contato)
admin.site.register(Endereco)
admin.site.register(AreaInteresse, AreaInteresseAdmin)
admin.site.register(SubareaInteresse)
admin.site.register(Curriculo, CurriculoAdmin)    
admin.site.register(Instituicao)
admin.site.register(FormacaoAcademica)
admin.site.register(Empresa)
admin.site.register(ExperienciaProfissional)
admin.site.register(Habilidade)