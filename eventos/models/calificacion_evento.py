from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User
from .evento import Evento


class CalificacionEvento(models.Model):
    evento = models.ForeignKey(
        Evento, on_delete=models.CASCADE, related_name="calificacion_evento"
    )
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="calificacion_evento"
    )
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.evento} - {self.fecha}"
