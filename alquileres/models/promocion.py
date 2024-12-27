from django.db import models
from cloudinary.models import CloudinaryField


class Promocion(models.Model):
    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"

    ESTADO_ALQUILER_CHOICES = [
        ("activo", "Activo"),
        ("caducado", "Caducado"),
    ]

    nombre_promocion = models.CharField(
        max_length=100, verbose_name="Nombre de la Promoción"
    )
    imagen = CloudinaryField("Imagen de la promocion", null=True, blank=True)
    descripcion_promocion = models.CharField(
        max_length=100, verbose_name="Descripción de la Promoción"
    )
    valor_referencial_promo = models.FloatField(
        verbose_name="Valor Referencial de la Promoción"
    )
    tipo_promocion = models.CharField(max_length=100, verbose_name="Tipo de Promoción")
    porcentaje_promocion = models.IntegerField(verbose_name="Porcentaje de Promoción")
    fecha_vigencia = models.DateField(verbose_name="Fecha de Vigencia")
    fecha_caducidad = models.DateField(verbose_name="Fecha de Caducidad")
    estado_promocion = models.CharField(
        max_length=100,
        choices=ESTADO_ALQUILER_CHOICES,
        default="proximo",
        verbose_name="Estado de la Promoción",
    )

    def __str__(self):
        return self.nombre_promocion
