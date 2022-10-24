from rest_framework import serializers
from .models import Usuario, Evento

# Serializador de un usuario estandar
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario 
        fields = ['nombre', 'username', 'password', 'correo', 'valoracion', 'numEventosCreados', 'numValoraciones', 'numEventosParticipa']
        #fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    organizador = UsuarioSerializer
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'hora', 'esPublico', 'aforo', 'categoria', 'organizador']

class EventoSerializerAll(serializers.ModelSerializer):
    participantes = UsuarioSerializer(read_only=True, many=True)
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'hora', 'esPublico', 'aforo', 'categoria', 'organizador', 'participantes']