from django.urls import include, path
from .views import UsuarioCreate, UsuarioUpdate, UsuarioList, UsuariosList, UsuarioDelete, Login, ValorarUsuario, RecuperarContrasena, UsuarioDeleteAll
from .views import EventoCreate, EventosList, EventoList, EventoListAll, EventoListUsuario, EventoUpdate, EventoDelete, eventosApuntados, eventosNoApuntados, EventoDeleteAll
from .views import anadirParticipante, eliminarParticipante, esParticipante
from .views import anadirAmigo, esAmigo, amigosUsuario, deleteAmigo
from .views import createMensaje, listMensajes, listMensajeEventos
from .views import DeleteAll

urlpatterns = [
    # USUARIOS
    path('CreateUsuario/', UsuarioCreate.as_view(), name='create-usuario'),
    path('UpdateUsuario/<str:username>/', UsuarioUpdate.as_view(), name='update-usuario'),
    path('Usuarios/', UsuariosList.as_view(), name='list-usuarios'),
    path('Usuario/<str:username>/', UsuarioList.as_view(), name='list-usuario'),
    path('DeleteUsuario/<str:username>/', UsuarioDelete.as_view(), name='delete-usuario'),
    path('DeleteAllUsuarios/', UsuarioDeleteAll.as_view(), name='delete-usuarios'),
    path('Login/<str:username>/<str:contrasena>', Login.as_view(), name='login-usuario'),
    path('valorarUsuario/<str:username>/', ValorarUsuario.as_view(), name='valorar-usuario'),
    path('enviarCorreo/<str:correo>/', RecuperarContrasena.as_view(), name='enviar-correo'),

    # EVENTOS
    path('CreateEvento/', EventoCreate.as_view(), name='create-evento'),
    path('Eventos/', EventosList.as_view(), name='list-eventos'),
    path('Evento/<str:nombre>/', EventoList.as_view()),
    path('Eventos/<str:username>/', EventoListUsuario.as_view()),
    path('EventosAll/', EventoListAll.as_view()),
    path('UpdateEvento/<str:nombre>/', EventoUpdate.as_view(), name='update-evento'),
    path('DeleteEvento/<str:nombre>/', EventoDelete.as_view(), name='delete-evento'),
    path('DeleteAllEventos/', EventoDeleteAll.as_view(), name='delete-usuarios'),


    # PARTICIPANTES
    path('anadirParticipante/<str:nomEvento>/<str:nomUsuario>/', anadirParticipante.as_view()),
    path('esParticipante/<str:nomEvento>/<str:nomUsuario>/', esParticipante.as_view()),
    path('deleteParticipante/<str:nomEvento>/<str:nomUsuario>/', eliminarParticipante.as_view()),
    path('eventosApuntados/<str:nomUsuario>/', eventosApuntados.as_view()),
    path('eventosNoApuntados/<str:nomUsuario>/', eventosNoApuntados.as_view()),

    # AMIGOS 
    path('anadirAmigo/<str:nomUsuario>/<str:nomAmigo>/', anadirAmigo.as_view()),
    path('esAmigo/<str:nomUsuario>/<str:nomAmigo>/', esAmigo.as_view()),
    path('amigosUsuario/<str:nomUsuario>/', amigosUsuario.as_view()),
    path('deleteAmigo/<str:nomUsuario>/<str:nomAmigo>/', deleteAmigo.as_view()),

    # MENSAJES
    path('CreateMensaje/', createMensaje.as_view()),
    path('Mensajes/', listMensajes.as_view()),
    path('Mensajes/<str:nomEvento>/', listMensajeEventos.as_view()),

    # ALL
    path('DeleteAll/', DeleteAll.as_view()),
]