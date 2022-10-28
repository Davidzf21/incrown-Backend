from django.urls import include, path
from .views import UsuarioCreate, UsuarioUpdate, UsuarioList, UsuariosList, UsuarioDelete, Login
from .views import EventoCreate, EventosList, EventoList, EventoListAll, EventoListUsuario, EventoUpdate, EventoDelete
from .views import anadirParticipante, eliminarParticipante, esParticipante
from .views import createMensaje, listMensajes, listMensajeEventos

urlpatterns = [
    # USUARIOS
    path('CreateUsuario/', UsuarioCreate.as_view(), name='create-usuario'),
    path('UpdateUsuario/<str:username>/', UsuarioUpdate.as_view(), name='update-usuario'),
    path('Usuarios/', UsuariosList.as_view(), name='list-usuarios'),
    path('Usuario/<str:username>/', UsuarioList.as_view(), name='list-usuario'),
    path('DeleteUsuario/<str:username>/', UsuarioDelete.as_view(), name='delete-usuario'),
    path('Login/<str:username>/<str:contrasena>', Login.as_view(), name='login-usuario'),

    # EVENTOS
    path('CreateEvento/', EventoCreate.as_view(), name='create-evento'),
    path('Eventos/', EventosList.as_view(), name='list-eventos'),
    path('Evento/<str:nombre>/', EventoList.as_view()),
    path('Eventos/<str:username>/', EventoListUsuario.as_view()),
    path('EventosAll/', EventoListAll.as_view()),
    path('UpdateEvento/<str:nombre>/', EventoUpdate.as_view(), name='update-evento'),
    path('DeleteEvento/<str:nombre>/', EventoDelete.as_view(), name='delete-evento'),

    # PARTICIPANTES
    path('anadirParticipante/<str:nomEvento>/<str:nomUsuario>/', anadirParticipante.as_view()),
    path('esParticipante/<str:nomEvento>/<str:nomUsuario>/', esParticipante.as_view()),
    path('deleteParticipante/<str:nomEvento>/<str:nomUsuario>/', eliminarParticipante.as_view()),

    # MENSAJES
    path('CreateMensaje/', createMensaje.as_view()),
    path('Mensajes/', listMensajes.as_view()),
    path('Mensajes/<str:nomEvento>/', listMensajeEventos.as_view()),

]