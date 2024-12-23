from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from .servicio import Servicio


class CalificacionServicio(models.Model):
    class Meta:
        verbose_name = "Calificación de Servicio"
        verbose_name_plural = "Calificaciones de Servicios"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "servicio"],
                name="unique_calificacion_servicio",
                violation_error_message="Ya has calificado este servicio.",
            )
        ]

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="calificacion_servicio",
        verbose_name="Servicio",
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="calificacion_servicio",
        verbose_name="Usuario",
    )
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación",
    )
    comentario = models.TextField(verbose_name="Comentario")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    def __str__(self):
        return f"{self.usuario} - {self.servicio} - {self.fecha}"
