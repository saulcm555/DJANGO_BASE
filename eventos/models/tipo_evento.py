from django.db import models

class TipoEvento(models.Model):
    nombre_evento = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_created=True)
    imagen = models.ImageField(upload_to='eventos', null=True, blank=True)
    
    
    def __str__(self) -> str:
        return f"{self.nombre_evento}"

