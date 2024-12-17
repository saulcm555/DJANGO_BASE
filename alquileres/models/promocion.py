from django.db import models


class Promocion(models.Model):
    ESTADO_ALQUILER_CHOICES = [
        ("activo", "Activo"),
        ("caducado", "Caducado"),
        ("proximo", "Proximo"),
    ]
    descripcion_promocion = models.CharField(max_length=100)
    valor_referencial_promo = models.FloatField()
    tipo_promocion = models.CharField(max_length=100)
    porcentaje_promocion = models.IntegerField()
    fecha_vigencia = models.DateField()
    fecha_caducidad = models.DateField()
    estado_promocion = models.CharField(
        choices=ESTADO_ALQUILER_CHOICES, default="proximo"
    )
