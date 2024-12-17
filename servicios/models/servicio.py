from django.db import models


class Servicio(models.Model):
    ESTADO_SERVICIO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmado", "Confirmado"),
        ("completado", "Completado"),
        ("cancelado", "Cancelado"),
    ]
    descripcion_servicio = models.CharField(max_length=500)
    valor_unidad = models.FloatField()
    estado_servicio = models.CharField(
        max_length=50, choices=ESTADO_SERVICIO_CHOICES, default="pendiente"
    )
    fecha_entrega = models.DateTimeField()
    descripcion_unidad = models.CharField(max_length=500)
    fecha_actualizacion_precio = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f"{self.descripcion_servicio} - {self.estado_servicio}"
