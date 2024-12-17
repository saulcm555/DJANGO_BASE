from django.db import models
from cloudinary.models import CloudinaryField
from .alquiler import Alquiler


class FotoAlquiler(models.Model):
    alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE, related_name='fotos')
    foto = CloudinaryField('image')
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    numero_likes = models.IntegerField(default=0)
    
    
    def dar_like(self): 
        self.numero_likes += 1
        self.save()

    def __str__(self):
        return f'Foto de {self.alquiler}'