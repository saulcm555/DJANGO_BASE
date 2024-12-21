from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import cloudinary
from django.utils.html import format_html


class ConfiguracionNegocioManager(models.Manager):
    def get_or_create(self, defaults = ..., **kwargs):
        if ConfiguracionNegocio.objects.exists():
            return ConfiguracionNegocio.objects.first(), False
        return ConfiguracionNegocio.objects.create(**kwargs), True
    

class ConfiguracionNegocio(models.Model):
    class Meta:
        verbose_name = "Configuración del Negocio"
        verbose_name_plural = "Configuraciones del Negocio"

    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    logo = CloudinaryField("Logo", blank=True, null=True)
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    pagina_web = models.URLField(blank=True, null=True, verbose_name="Página Web")
    red_social_facebook = models.URLField(
        blank=True, null=True, verbose_name="Red Social Facebook"
    )
    red_social_x = models.URLField(blank=True, null=True, verbose_name="Red Social X")
    red_social_instagram = models.URLField(
        blank=True, null=True, verbose_name="Red Social Instagram"
    )
    
    nombre_banco = models.CharField(max_length=50, verbose_name="Nombre del Banco")
    tipo_cuenta = models.CharField(max_length=20, verbose_name="Tipo de Cuenta")
    numero_cuenta = models.CharField(max_length=20, verbose_name="Número de Cuenta")

    objects = ConfiguracionNegocioManager()

    def clean(self):
        if ConfiguracionNegocio.objects.exists() and not self.pk:
            raise ValidationError("Solo se puede crear una configuración de negocio.")

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionNegocio.objects.exists():
            raise ValidationError("Solo se puede crear una configuración de negocio.")
        return super(ConfiguracionNegocio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    
    def get_img(self):
        if self.logo:
            url = cloudinary.utils.cloudinary_url(
                self.logo.public_id, format="jpg", width=100, height=100, crop="fill"
            )[0]
            return f'<img src="{url}" alt="Demo Image" style="border-radius: 5px;" />'
        return "<span>No image available</span>"

    @property
    def foto_view(self):
        html = self.get_img()
        return format_html(html)

