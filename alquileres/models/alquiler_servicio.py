from django.db import models
from servicios.models import Servicio
from .alquiler import Alquiler


class AlquilerServicio(models.Model):
    ESTADO_SERVICIO_RESERVA_CHOICES = [
        ("pendiente", "Pendiente"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    reserva = models.ForeignKey(
        Alquiler, on_delete=models.CASCADE, related_name="servicios_reserva"
    )
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE, related_name="reservas_servicio"
    )
    estado_servicio_reserva = models.CharField(
        max_length=50, choices=ESTADO_SERVICIO_RESERVA_CHOICES, default="pendiente"
    )

    fecha_entrega = models.DateTimeField()

    def __str__(self):
        return f"Servicio: {self.servicio.nombre} - Estado: {self.estado_servicio_reserva} - Reserva: {self.reserva.id}"
