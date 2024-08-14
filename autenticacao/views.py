from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('criar_tabela')
    else:
        form = AuthenticationForm()
    return render(request, 'autenticacao/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário no banco de dados
            login(request, user)  # Faz login automaticamente após o signup
            return redirect('criar_tabela') # Redireciona para a página principal
    else:
        form = UserCreationForm()
    return render(request, 'autenticacao/signup.html', {'form': form})

