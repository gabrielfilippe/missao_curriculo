from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('pessoas/', pessoas, name='pessoas'),
    path('criar_curriculo/', criar_curriculo, name='criar_curriculo'),
    path('editar_curriculo/<int:id>/', editar_curriculo, name='editar_curriculo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)