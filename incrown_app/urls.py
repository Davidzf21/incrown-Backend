from django.urls import include, path
from .views import UsuarioList

urlpatterns = [
    # USUARIOS
    path('Usuarios/', UsuarioList.as_view(), name='create-usuario'),
]