from django.db import models
from .tipo_evento import TipoEvento

class Evento(models.Model):
    nombre = models.CharField(max_length=100, default='Nombre del evento')
    descripcion = models.CharField(max_length=500, default='Descripción del evento')
    valor_referencial = models.FloatField(default=0.0)
    numero_horas_permitidas = models.IntegerField(default=0)
    valor_extra_hora = models.FloatField(default=0.0)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.nombre}"
