from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from autenticacao.views import signup_view  # Importando a função signup_view

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='autenticacao/login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('autenticacao/', include('autenticacao.urls')),
    path('gerenciador_tabelas/', include('gerenciador_tabelas.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', signup_view, name='signup'),  # Usando a função signup_view
]
