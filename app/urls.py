from app.views import *
from django.urls import path

app_name = 'curriculo'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('criar/', criar_curriculo, name='criar_curriculo'),
    path('curriculos/', curriculos, name='curriculos'),
    path('pessoas/', pessoas, name='pessoas'),
    path('filtrar_curriculos/', filtrar_curriculos, name='filtrar_curriculos'),
    path('curriculo/<int:pk>/', curriculo_pdf_view, name='curriculo_pdf'),
]