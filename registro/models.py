from django.db import models

# Create your models here.
class Cliente(models.Model):
    identificacion_cliente = models.CharField(max_length=10)
    nacionalidad = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField(auto_created=True)
    telefono = models.CharField(max_length=10)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo_electronico = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)