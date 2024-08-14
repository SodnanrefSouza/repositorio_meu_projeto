from django.urls import path
from .views import login_view, signup_view  # Certifique-se de que a view signup_view está definida em views.py

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),  # Adicione esta linha se não existir
]

