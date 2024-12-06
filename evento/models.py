from django.db import models

class Tipo_Evento(models.Model):
    nombre_evento = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_created=True)
    
    def __str__(self) -> str:
        return f"{self.nombre_evento}"

class Evento(models.Model):
    descripcion = models.CharField(max_length=500)
    valor_referencial = models.FloatField()
    numero_horas_permitidas = models.IntegerField()
    valor_extra_hora = models.FloatField()
    tipo_evento = models.ForeignKey(Tipo_Evento, on_delete=models.CASCADE)

