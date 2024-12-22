from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class PerfilUsuario(models.Model):
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuario"
    )
    identificacion_cliente = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Identificación del Cliente",
    )
    nacionalidad = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Nacionalidad"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Registro"
    )
    telefono = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Teléfono"
    )
    nombres = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Nombres"
    )
    apellidos = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Apellidos"
    )
    correo_electronico = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Correo Electrónico"
    )
    genero = models.CharField(
        max_length=50,
        choices=[("M", "Masculino"), ("F", "Femenino"), ("O", "Otro")],
        blank=True,
        null=True,
        verbose_name="Género",
    )
    fecha_nacimiento = models.DateField(
        blank=True, null=True, verbose_name="Fecha de Nacimiento"
    )
    codigo_verificacion = models.CharField(
        max_length=6, blank=True, null=True, verbose_name="Código de Verificación"
    )
    correo_electronico_verificado = models.BooleanField(
        default=False, verbose_name="Correo Electrónico Verificado"
    )
    @property
    def datos_completos(self):
        campos_requeridos = [
            self.nombres,
            self.apellidos,
            self.nacionalidad,
            self.telefono,
            self.fecha_nacimiento,
            self.correo_electronico,
        ]
        return all(campos_requeridos) and self.correo_electronico_verificado
    def __str__(self):
        return self.usuario.username

    def generar_codigo_verificacion(self):
        self.codigo_verificacion = get_random_string(length=6)
