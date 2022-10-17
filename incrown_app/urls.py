from django.urls import include, path
from .views import UsuarioCreate, UsuarioUpdate, UsuarioList, UsuariosList, UsuarioDelete

urlpatterns = [
    # USUARIOS
    path('CreateUsuario/', UsuarioCreate.as_view(), name='create-usuario'),
    path('UpdateUsuario/<str:username>/', UsuarioUpdate.as_view(), name='update-usuario'),
    path('Usuarios/', UsuariosList.as_view(), name='list-usuarios'),
    path('Usuario/<str:username>/', UsuarioList.as_view(), name='list-usuario'),
    path('DeleteUsuario/<str:username>/', UsuarioDelete.as_view(), name='delete-usuario'),
]