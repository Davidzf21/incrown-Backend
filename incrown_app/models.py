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
