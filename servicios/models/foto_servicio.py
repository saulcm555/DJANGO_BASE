from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary
from django.utils.html import format_html
from .servicio import Servicio


class FotoServicio(models.Model):
    class Meta:
        verbose_name = "Foto de Servicio"
        verbose_name_plural = "Fotos de Servicios"

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="fotos",
        verbose_name="Servicio",
    )
    foto = CloudinaryField("Foto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_publicacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Publicación"
    )
    numero_likes = models.IntegerField(default=0, verbose_name="Número de Likes")

    def dar_like(self):
        self.numero_likes += 1
        self.save()

    def __str__(self):
        return f"Foto de {self.servicio}"

    def get_img(self):
        if self.foto:
            url = cloudinary.utils.cloudinary_url(
                self.foto.public_id, format="jpg", width=100, height=100, crop="fill"
            )[0]
            return f'<img src="{url}" alt="Demo Image" style="border-radius: 5px;" />'
        return "<span>No image available</span>"

    @property
    def foto_view(self):
        html = self.get_img()
        return format_html(html)
