from django.db import models
from eventos.models import Evento
from django.contrib.auth.models import User
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
    fecha_alquiler = models.DateField(verbose_name="Fecha de Alquiler")
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Creación")
    hora_inicio_alquiler = models.DateTimeField(verbose_name="Hora de Inicio de Alquiler")
    hora_fin_planificada_alquiler = models.DateTimeField(verbose_name="Hora Fin Planificada de Alquiler")
    hora_fin_real_alquiler = models.DateTimeField(null=True, blank=True, verbose_name="Hora Fin Real de Alquiler")
    costo_alquiler = models.FloatField(default=0.0, verbose_name="Costo de Alquiler")
    calificacion_dueno = models.OneToOneField(
        "CalificacionAlquiler",
        on_delete=models.CASCADE,
        related_name="calificacion_dueno",
        null=True,
        blank=True,
        verbose_name="Calificación del Dueño"
    )
    calificacion_cliente = models.OneToOneField(
        "CalificacionAlquiler",
        on_delete=models.CASCADE,
        related_name="calificacion_cliente",
        null=True,
        blank=True,
        verbose_name="Calificación del Cliente"
    )
    observacion = models.CharField(max_length=500, blank=True, default="", verbose_name="Observación")
    cantidad_anticipo = models.FloatField(default=0.0, verbose_name="Cantidad de Anticipo")

    promociones = models.ManyToManyField(
        Promocion, blank=True, related_name="alquileres", verbose_name="Promociones"
    )

    estado_de_alquiler = models.CharField(
        max_length=20, choices=ESTADO_ALQUILER_CHOICES, default="pendiente", verbose_name="Estado de Alquiler"
    )

    codigo_confirmacion = models.CharField(max_length=10, blank=True, default="", verbose_name="Código de Confirmación")
    
    def generar_codigo_confirmacion(self):
        if self.codigo_confirmacion:
            return self.codigo_confirmacion
        self.codigo_confirmacion = get_random_string(length=6)
        self.save()


    def __str__(self):
        return f"Alquiler para {self.evento.nombre} el {self.fecha_alquiler}"