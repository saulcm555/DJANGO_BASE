from django.db import models
from servicios.models import Servicio
from .alquiler import Alquiler


class AlquilerServicio(models.Model):
    class Meta:
        verbose_name = "Servicios de alquiler"
        verbose_name_plural = "Servicios de alquieres"
    ESTADO_SERVICIO_RESERVA_CHOICES = [
        ("pendiente", "Pendiente"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    reserva = models.ForeignKey(
        Alquiler,
        on_delete=models.CASCADE,
        related_name="servicios_reserva",
        verbose_name="Reserva",
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="reservas_servicio",
        verbose_name="Servicio",
    )
    estado_servicio_reserva = models.CharField(
        max_length=50,
        choices=ESTADO_SERVICIO_RESERVA_CHOICES,
        default="pendiente",
        verbose_name="Estado del Servicio de Alquiler",
    )

    fecha_entrega = models.DateTimeField(verbose_name="Fecha de Entrega")

    def __str__(self):
        return f"Servicio: {self.servicio.nombre} - Estado: {self.estado_servicio_reserva} - Reserva: {self.reserva.id}"

