from django.db import models
from eventos.models import Evento
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from servicios.models import Servicio
from .promocion import Promocion


# Create your models here.
class Alquiler(models.Model):
    class Meta:
        verbose_name = "Alquiler"
        verbose_name_plural = "Alquileres"

    ESTADO_ALQUILER_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmado", "Confirmado"),
        ("completado", "Completado"),
        ("cancelado", "Cancelado"),
    ]
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cliente")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    fecha_alquiler = models.DateField(verbose_name="Fecha de reserva")
    fecha_creacion = models.DateField(
        auto_now_add=True, verbose_name="Fecha de Creación"
    )
    hora_inicio_alquiler = models.TimeField(
        verbose_name="Hora de Inicio de reserva"
    )
    hora_fin_planificada_alquiler = models.TimeField(
        verbose_name="Hora Fin Planificada de reserva"
    )
    hora_fin_real_alquiler = models.TimeField(
        null=True, blank=True, verbose_name="Hora Fin Real de reserva"
    )
    calificacion_dueno = models.OneToOneField(
        "CalificacionAlquiler",
        on_delete=models.CASCADE,
        related_name="calificacion_dueno",
        null=True,
        blank=True,
        verbose_name="Calificación del Dueño",
    )
    calificacion_cliente = models.OneToOneField(
        "CalificacionAlquiler",
        on_delete=models.CASCADE,
        related_name="calificacion_cliente",
        null=True,
        blank=True,
        verbose_name="Calificación del Cliente",
    )
    observacion = models.CharField(
        max_length=500, blank=True, default="", verbose_name="Observación"
    )
    cantidad_anticipo = models.FloatField(
        default=0.0, verbose_name="Cantidad de Anticipo"
    )

    promociones = models.ManyToManyField(
        Promocion, blank=True, related_name="alquileres", verbose_name="Promociones"
    )

    estado_de_alquiler = models.CharField(
        max_length=20,
        choices=ESTADO_ALQUILER_CHOICES,
        default="pendiente",
        verbose_name="Estado de reserva",
    )

    codigo_confirmacion = models.CharField(
        max_length=10, blank=True, default="", verbose_name="Código de Confirmación"
    )


    correo_electronico_verificado = models.BooleanField(
        default=False, verbose_name="Correo Electrónico Verificado"
    )

    def generar_codigo_confirmacion(self):
        if self.codigo_confirmacion:
            return self.codigo_confirmacion
        self.codigo_confirmacion = get_random_string(length=6)
        self.save()

    
    @property
    def costo_alquiler(self):
        costo = self.evento.valor_referencial
        for servicio_reserva in self.servicios_reserva.all():
            costo += servicio_reserva.servicio.valor_unidad * servicio_reserva.cantidad
        for promocion in self.promociones.all():
            costo -= (costo * promocion.porcentaje_promocion) / 100
        return costo

    def clean(self):
        # Verifica que ambos campos no sean None
        if not self.hora_inicio_alquiler or not self.hora_fin_planificada_alquiler:
            raise ValidationError(
                "La hora de inicio y la hora de fin planificada son obligatorias"
            )

        if self.hora_inicio_alquiler >= self.hora_fin_planificada_alquiler:
            raise ValidationError(
                "La hora de inicio de la reserva debe ser menor a la hora de fin planificada de la reserva"
            )
