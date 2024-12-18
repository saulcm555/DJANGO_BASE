from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    identificacion_cliente = models.CharField(
        max_length=10, unique=True, blank=True, null=True
    )
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    codigo_verificacion = models.CharField(max_length=6, blank=True, null=True)
    correo_electronico_verificado = models.BooleanField(default=False)
    datos_completos = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username

    def generar_codigo_verificacion(self):
        self.codigo_verificacion = get_random_string(length=6)
