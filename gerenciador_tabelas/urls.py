from django.urls import path
from .views import create_table, list_tables

urlpatterns = [
    path('criar-tabela/', create_table, name='criar_tabela'),
    path('listar-tabelas/', list_tables, name='listar_tabelas'),
]
