from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacao/', include('autenticacao.urls')),
    path('gerenciador_tabelas/', include('gerenciador_tabelas.urls')),
]