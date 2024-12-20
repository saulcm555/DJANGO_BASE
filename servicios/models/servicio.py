from django.db import models
from django.contrib.auth.models import User


class Servicio(models.Model):

    agregado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="servicios"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    valor_unidad = models.FloatField()
    vigencia = models.BooleanField(default=True)
    descripcion_unidad = models.CharField(max_length=500)
    fecha_actualizacion_precio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} "
