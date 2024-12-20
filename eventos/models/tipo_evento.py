from django.db import models
from cloudinary.models import CloudinaryField


class TipoEvento(models.Model):
    class Meta:
        verbose_name = "Tipo de Evento"
        verbose_name_plural = "Tipos de Eventos"
    nombre_evento = models.CharField(max_length=100, verbose_name="Nombre del Evento")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name="Fecha de Creación")
    imagen = CloudinaryField('Foto', blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.nombre_evento}"
