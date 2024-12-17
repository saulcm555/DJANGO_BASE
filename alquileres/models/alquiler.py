from django.db import models
from eventos.models import Evento
from usuarios.models import Cliente

from servicios.models import Servicio
from .calificacion_alquiler import CalificacionAlquiler
from .promocion import Promocion


# Create your models here.
class Alquiler(models.Model):
    ESTADO_ALQUILER_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmado", "Confirmado"),
        ("completado", "Completado"),
        ("cancelado", "Cancelado"),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_alquiler = models.DateField(auto_now_add=True)
    horainicio_reserva = models.DateTimeField(auto_now_add=True)
    horafin_planificada_reserva = models.DateTimeField()
    horafin_real_reserva = models.DateTimeField(null=True, blank=True)
    costo_alquiler = models.FloatField(default=0.0)
    calificacion_dueno = models.OneToOneField(
        CalificacionAlquiler,
        on_delete=models.CASCADE,
        related_name="calificacion_dueno",
        null=True,
        blank=True,
    )
    calificacion_cliente = models.OneToOneField(
        CalificacionAlquiler,
        on_delete=models.CASCADE,
        related_name="calificacion_cliente",
        null=True,
        blank=True,
    )
    observacion = models.CharField(max_length=500, blank=True, default="")
    cantidad_anticipo = models.FloatField(default=0.0)

    promociones = models.ManyToManyField(
        Promocion, blank=True, related_name="alquileres"
    )
    
    servicios = models.ManyToManyField(
        Servicio, blank=True, related_name="alquileres"
    )

    Estado_de_alquiler = models.CharField(
        max_length=20, choices=ESTADO_ALQUILER_CHOICES, default="pendiente"
    )
