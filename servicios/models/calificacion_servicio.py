from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User
from .servicio import Servicio


class CalificacionServicio(models.Model):
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, related_name="calificacion_servicio"
    )
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="calificacion_servicio"
    )
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.servicio} - {self.fecha}"
