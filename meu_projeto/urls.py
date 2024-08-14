# urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from autenticacao.views import signup_view, home_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirecionar a URL raiz para a página home se o usuário já estiver logado
    path('', RedirectView.as_view(url='autenticacao/home/', permanent=False), name='root'),

    # Rotas de autenticação
    path('autenticacao/', include(([
        path('', auth_views.LoginView.as_view(template_name='autenticacao/login.html', redirect_authenticated_user=True), name='login'),
        path('signup/', signup_view, name='signup'),
        path('home/', home_view, name='home'),
        path('logout/', auth_views.LogoutView.as_view(next_page='autenticacao:login'), name='logout'),
    ], 'autenticacao'), namespace='autenticacao')),

    # Rotas do gerenciador de tabelas
    path('gerenciador_tabelas/', include('gerenciador_tabelas.urls')),
]
