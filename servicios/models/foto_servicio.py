from django.db import models
from cloudinary.models import CloudinaryField
from .servicio import Servicio

class FotoServicio(models.Model):
    alquiler = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='fotos')
    foto = CloudinaryField('image')
    descripcion = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    numero_likes = models.IntegerField(default=0)
    
    
    def dar_like(self): 
        self.numero_likes += 1
        self.save()

    def __str__(self):
        return f'Foto de {self.alquiler}'