from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import cloudinary
import cloudinary.models
from alquiler.models import Alquiler


# Create your models here.
class Imagen(models.Model):
    nombre_imagen = models.CharField(max_length=100)
    descripcion_imgen = models.CharField(max_length=500) 
    fecha_creacion = models.DateTimeField(auto_created=True)
    imagen = cloudinary.models.CloudinaryField('image')

    def __str__(self):
        return f"{self.nombre_imagen} {self.fecha_creacion}"
    

class Servicio(models.Model):
    ESTADO_SERVICIO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    descripcion_servicio = models.CharField(max_length=500)
    valor_unidad = models.FloatField()
    estado_servicio	= models.CharField(
        max_length=50, 
        choices=ESTADO_SERVICIO_CHOICES, 
        default='pendiente'
    )
    fecha_entrega = models.DateTimeField()
    descripcion_unidad	= models.CharField(max_length=500)
    fecha_actualizacion_precio = models.DateTimeField(auto_created=True)
    imagen =  models.ManyToManyField(Imagen, related_name="servicios")

    def __str__(self):
        return f"{self.descripcion_servicio} - {self.estado_servicio}"
    
class Alquiler_Servicio(models.Model):
    id_alquiler = models.ForeignKey(Alquiler, on_delete=models.CASCADE)
    idservicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    costo_total	= models.FloatField()	
    calificacion_cliente = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    ) 