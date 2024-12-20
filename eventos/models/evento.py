from django.db import models
from .tipo_evento import TipoEvento

class Evento(models.Model):
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
    nombre = models.CharField(max_length=100, default='Nombre del evento', verbose_name='Nombre')
    descripcion = models.CharField(max_length=500, default='Descripción del evento', verbose_name='Descripción')
    valor_referencial = models.FloatField(default=0.0, verbose_name='Valor Referencial')
    numero_horas_permitidas = models.IntegerField(default=0, verbose_name='Número de Horas Permitidas')
    valor_extra_hora = models.FloatField(default=0.0, verbose_name='Valor Extra por Hora')
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, verbose_name='Tipo de Evento')
    
    def __str__(self) -> str:
        return f"{self.nombre}"
