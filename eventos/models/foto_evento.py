from django.db import models
from cloudinary.models import CloudinaryField
from .evento import Evento

class FotoEvento(models.Model):
    class Meta:
        verbose_name = 'Foto del Evento'
        verbose_name_plural = 'Fotos de los Eventos'
        ordering = ['fecha_publicacion']
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='fotos', verbose_name='Evento')
    foto = CloudinaryField("Foto", blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Publicación')
    numero_likes = models.IntegerField(default=0, verbose_name='Número de Likes')
    
    def dar_like(self): 
        self.numero_likes += 1
        self.save()

    def __str__(self):
        return f'Foto de {self.evento}'
