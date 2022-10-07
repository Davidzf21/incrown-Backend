from rest_framework import serializers
from .models import Usuario

# Serializador de un usuario estandar
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario 
        fields = ['nombre', 'username', 'password', 'correo', 'valoracion', 'numEventosCreados', 'numValoraciones', 'numEventosParticipa']
        #fields = '__all__'