from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User

from .alquiler import Alquiler


class CalificacionAlquiler(models.Model):
    class Meta:
        verbose_name = "Calificación de Alquiler"
        verbose_name_plural = "Calificaciones de Alquiler"
        
    alquiler = models.ForeignKey(
        Alquiler, on_delete=models.CASCADE, related_name="calificacion_alquiler", verbose_name="Alquiler"
    )
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="calificacion_alquiler", verbose_name="Usuario"
    )
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Calificación"
    )
    comentario = models.TextField(verbose_name="Comentario")
    fecha_calificacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    def __str__(self):
        return f"{self.usuario} - {self.alquiler} - {self.fecha_calificacion}"

