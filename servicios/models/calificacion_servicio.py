from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from usuarios.models import Cliente

from .servicio import Servicio


class CalificacionServicio(models.Model):
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, related_name="calificacion_servicio"
    )
    usuario = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="calificacion_servicio"
    )
    calificacion = models.IntegerField(MinValueValidator(0), MaxValueValidator(5))
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.servicio} - {self.fecha}"
