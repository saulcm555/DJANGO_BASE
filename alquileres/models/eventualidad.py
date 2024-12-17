from django.db import models


from .alquiler import Alquiler


class Eventualidad(models.Model):
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
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE, related_name="eventualidades")
    descripcion_eventualidad = models.TextField()
    nivel_impacto_eventualidad = models.CharField(
        max_length=50, choices=NIVEL_IMPACTO_CHOICES, default="BAJO"
    )
    categoria_eventualidad = models.CharField(
        max_length=50,
        choices=CATEGORIA_EVENTUALIDAD_CHOICES,
        default="OTROS",
    )

    monto_penalidad_eventualidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ocurrencia_eventualidad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Eventualidad ocurrida en el evento {self.alquiler.id} en {self.fecha_ocurrencia_eventualidad}"
