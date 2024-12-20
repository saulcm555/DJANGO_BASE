from django.db import models

from .alquiler import Alquiler

class Eventualidad(models.Model):
    class Meta:
        verbose_name = "Eventualidad"
        verbose_name_plural = "Eventualidades"
    NIVEL_IMPACTO_CHOICES = [
        ("BAJO", "Bajo"),
        ("MEDIO", "Medio"),
        ("ALTO", "Alto"),
    ]

    CATEGORIA_EVENTUALIDAD_CHOICES = [
        ("ECONOMICA", "Económica"),
        ("TECNICA", "Técnica"),
        ("HUMANA", "Humana"),
        ("AMBIENTAL", "Ambiental"),
        ("OTROS", "Otros"),
    ]
    alquiler = models.ForeignKey(
        Alquiler, 
        on_delete=models.CASCADE, 
        related_name="eventualidades",
        verbose_name="Alquiler"
    )
    descripcion_eventualidad = models.TextField(verbose_name="Descripción de la eventualidad")
    nivel_impacto_eventualidad = models.CharField(
        max_length=50, 
        choices=NIVEL_IMPACTO_CHOICES, 
        default="BAJO",
        verbose_name="Nivel de impacto de la eventualidad"
    )
    categoria_eventualidad = models.CharField(
        max_length=50,
        choices=CATEGORIA_EVENTUALIDAD_CHOICES,
        default="OTROS",
        verbose_name="Categoría de la eventualidad"
    )
    monto_penalidad_eventualidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Monto de penalidad de la eventualidad"
    )
    fecha_ocurrencia_eventualidad = models.DateTimeField(verbose_name="Fecha de ocurrencia de la eventualidad")

    def __str__(self):
        return f"Eventualidad ocurrida en el evento {self.alquiler.id} en {self.fecha_ocurrencia_eventualidad}"
