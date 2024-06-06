from app.models import *
from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
class CurriculoAdmin(admin.ModelAdmin):
    class FormacaoInline(admin.TabularInline):
        model = Formacao
        extra = 0

    class ExperienciaInline(admin.StackedInline):
        model = Experiencia
        extra = 0

    class HabilidadeInline(admin.TabularInline):
        model = Habilidade
        extra = 0

    list_display = ['user', 'pessoa', 'get_formacoes', 'get_experiencias', 'get_habilidades', 'created_at', 'updated_at']
    list_display_links = ['pessoa', 'user']
    inlines = [FormacaoInline, ExperienciaInline, HabilidadeInline]

    def get_formacoes(self, obj):
        return mark_safe('<br>'.join([f.curso for f in obj.formacoes.all()]))
    
    def get_experiencias(self, obj):
        return mark_safe('<br>'.join([e.empresa for e in obj.experiencias.all()]))
    
    def get_habilidades(self, obj):
        return mark_safe('<br>'.join([h.nome for h in obj.habilidades.all()]))
    
    get_formacoes.short_description = 'Formações'
    get_experiencias.short_description = 'Experiências'
    get_habilidades.short_description = 'Habilidades'

admin.site.register(Pessoa)
admin.site.register(Instituicao)
# admin.site.register(Formacao)
# admin.site.register(Experiencia)
# admin.site.register(Habilidade)
admin.site.register(Curriculo, CurriculoAdmin)

# $(document).ready(function() {
#         $('#id_pessoa').select2();
#     });