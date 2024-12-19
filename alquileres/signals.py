from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Alquiler
from utilidades import EmailEnviador


@receiver(post_save, sender=Alquiler)
def enviar_correo_confirmacion(sender, instance, created, **kwargs):
    if created:  
        EmailEnviador.enviar_codigo_confirmacion(instance)
