from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .evento import Evento


class CalificacionEvento(models.Model):
    class Meta:
        verbose_name = "Calificación de Evento"
        verbose_name_plural = "Calificaciones de Eventos"

    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="calificacion_evento",
        verbose_name="Evento",
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="calificacion_evento",
        verbose_name="Usuario",
    )
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Calificación",
    )
    comentario = models.TextField(verbose_name="Comentario")
    fecha_publicacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Publicación"
    )



    def __str__(self):
        return f"{self.usuario} - {self.evento} - {self.fecha_publicacion}"
