from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    username = models.CharField(max_length=50,primary_key=True)
    password = models.CharField(max_length=200)
    correo = models.CharField(max_length=50,unique=True)
    valoracion = models.FloatField(default=0.0)
    numValoraciones = models.PositiveIntegerField(default=0)
    amigos = models.ManyToManyField('self')
    numEventosCreados = models.PositiveIntegerField(default=0)
    numEventosParticipa = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.username

class Evento(models.Model):
    nombre = models.CharField(max_length=50,primary_key=True)
    descripcion = models.CharField(max_length=200)
    fecha = models.CharField(max_length=50)   
    hora = models.CharField(max_length=50)
    esPublico = models.BooleanField(null=True)
    aforo = models.PositiveIntegerField(null=True)
    categoria = models.CharField(max_length=50)
    organizador = models.CharField(max_length=200)
    participantes = models.ManyToManyField(Usuario, related_name='usuario_apuntado_a')
    def __str__(self):
        return self.nombre