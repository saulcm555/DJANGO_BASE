from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from usuarios.models import Cliente

from .alquiler import Alquiler


class CalificacionAlquiler(models.Model):
    alquiler = models.ForeignKey(
        Alquiler, on_delete=models.CASCADE, related_name="calificacion_alquiler"
    )
    usuario = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="calificacion_alquiler"
    )
    calificacion = models.IntegerField(MinValueValidator(0), MaxValueValidator(5))
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.alquiler} - {self.fecha}"
