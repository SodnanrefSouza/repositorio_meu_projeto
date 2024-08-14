from django.urls import path
from .views import create_table, list_tables, list_table_records

urlpatterns = [
    path('criar-tabela/', create_table, name='criar_tabela'),
    path('listar-tabelas/', list_tables, name='listar_tabelas'),
    path('listar-tabelas/<str:table_name>/', list_table_records, name='listar_registros'),
]
