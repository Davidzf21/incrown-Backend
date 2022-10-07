from rest_framework import viewsets, generics
from .models import Usuario
from .serializers import UsuarioSerializer

# Funciones del USUARIO
class UsuarioList(generics.ListAPIView):
   queryset = Usuario.objects.all()
   serializer_class = UsuarioSerializer

