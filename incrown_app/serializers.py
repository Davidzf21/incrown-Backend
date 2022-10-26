from rest_framework import serializers
from .models import Usuario, Evento, Mensaje

# Serializador de un usuario estandar
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario 
        fields = ['nombre', 'username', 'password', 'correo', 'valoracion', 'numEventosCreados', 'numValoraciones', 'numEventosParticipa']
        #fields = '__all__'

class UsuarioSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Usuario 
        fields = ['nombre', 'username', 'password', 'correo', 'valoracion', 'numEventosCreados', 'numValoraciones', 'numEventosParticipa', 'amigos']
        #fields = '__all__'

# Serializador de un evento estandar
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

# Serializador de un mensaje estandar
class MensajeSerializer(serializers.ModelSerializer):
    autor = UsuarioSerializerFull
    evento = EventoSerializer
    class Meta:
        model = Mensaje
        fields = ['id', 'autor', 'evento', 'texto']
        #fields = '__all__'
    depth = 2