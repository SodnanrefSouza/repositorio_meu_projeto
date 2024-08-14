from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('autenticacao:home')  # Redireciona para a página home após login
    else:
        form = AuthenticationForm()
    return render(request, 'autenticacao/login.html', {'form': form})

def signup_view(request):
    error_message = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                error_message = 'Esse nome de usuário já está em uso. Escolha outro.'
            else:
                user = form.save()
                login(request, user)
                return redirect('autenticacao:home')
        else:
            # Adiciona erros específicos do formulário
            if form.errors.get('username'):
                error_message = _(form.errors['username'][0])  # Pega o primeiro erro do campo username
            elif form.errors.get('password1'):
                error_message = _(form.errors['password1'][0])  # Pega o primeiro erro do campo password1
            elif form.errors.get('password2'):
                error_message = _(form.errors['password2'][0])  # Pega o primeiro erro do campo password2
    else:
        form = UserCreationForm()
    
    return render(request, 'autenticacao/signup.html', {'form': form, 'error_message': error_message})



@login_required
def home_view(request):
    return render(request, 'autenticacao/home.html')  # Renderiza a página home

