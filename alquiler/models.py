from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from evento.models import Evento
from registro.models import Cliente
from servicio.models import Imagen

# Create your models here.
class Alquiler(models.Model):
    ESTADO_ALQUILER_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_alquiler = models.DateField()
    horainicio_reserva = models.DateTimeField()
    horafin_planificada_reserva	= models.DateTimeField()
    horafin_real_reserva = models.DateTimeField()
    costo_alquiler = models.FloatField()
    calificacion_negocio = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )	
    observacion	= models.CharField(max_length=500)	
    cantidad_anticipo = models.FloatField()
    Estado_de_alquiler = Estado_de_alquiler = models.CharField(
        max_length=20,
        choices=ESTADO_ALQUILER_CHOICES,
        default='pendiente'
    )
    
    imagen =  models.ManyToManyField(Imagen, related_name="servicios")


class Promocion(models.Model):
    ESTADO_ALQUILER_CHOICES = [
        ('activo', 'Activo'),
        ('caducado', 'Caducado'),
        ('proximo', 'Proximo'),
    ]
    descripcion_promocion	= models.CharField(max_length=100)
    valor_referencial_promo	= models.FloatField()
    tipo_promocion	= models.CharField(max_length=100)
    porcentaje_promocion = models.IntegerField()	
    fecha_vigencia	= models.DateField()	
    fecha_caducidad	= models.DateField()	
    estado_promocion = models.CharField(
        choices=ESTADO_ALQUILER_CHOICES,
        default='proximo'
    )