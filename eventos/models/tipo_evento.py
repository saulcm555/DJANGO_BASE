from django.db import models
from cloudinary.models import CloudinaryField


class TipoEvento(models.Model):
    nombre_evento = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_created=True)
    imagen = CloudinaryField('imagen', blank=True, null=True)
    
    
    def __str__(self) -> str:
        return f"{self.nombre_evento}"

