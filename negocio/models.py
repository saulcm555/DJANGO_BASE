from django.db import models
from django.core.exceptions import ValidationError

class ConfiguracionNegocio(models.Model):
    class Meta:
        verbose_name = "Configuración del Negocio"
        verbose_name_plural = "Configuraciones del Negocio"
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    pagina_web = models.URLField(blank=True, null=True, verbose_name="Página Web")
    red_social_facebook = models.URLField(blank=True, null=True, verbose_name="Red Social Facebook")
    red_social_x = models.URLField(blank=True, null=True, verbose_name="Red Social X")
    nombre_banco = models.CharField(max_length=50, verbose_name="Nombre del Banco")
    tipo_cuenta = models.CharField(max_length=20, verbose_name="Tipo de Cuenta")
    numero_cuenta = models.CharField(max_length=20, verbose_name="Número de Cuenta")

    def clean(self):
        if ConfiguracionNegocio.objects.exists() and not self.pk:
            raise ValidationError('Solo se puede crear una configuración de negocio.')

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionNegocio.objects.exists():
            raise ValidationError('Solo se puede crear una configuración de negocio.')
        return super(ConfiguracionNegocio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre