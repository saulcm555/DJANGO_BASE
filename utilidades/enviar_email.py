from django.core.mail import send_mail
from django.conf import settings
import random

from usuarios.models import PerfilUsuario
from alquileres.models import Alquiler


class EmailEnviador:

    @staticmethod
    def enviar_email(subject, message, recipient_list):

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    @staticmethod
    def enviar_codigo_validar_email(perfil: PerfilUsuario):
        subject = "Código de verificación"
        message = (
            f"Hola {perfil.usuario.username},\n\n"
            f"Gracias por registrarte. Tu código de verificación es: {perfil.codigo_verificacion}\n\n"
            "Por favor, utiliza este código para verificar tu cuenta."
        )
        recipient_list = [perfil.correo_electronico]

        EmailEnviador.enviar_email(subject, message, recipient_list)


def enviar_codigo_confirmacion(alquiler:Alquiler):

    alquiler.generar_codigo_confirmacion()
    codigo_confirmacion = alquiler.codigo_confirmacion
    alquiler.save()

    asunto = "Confirmación de Alquiler"
    mensaje = f"""
    Estimado/a {alquiler.cliente},
    
    Gracias por realizar su reserva para el evento "{alquiler.evento}".
    Por favor, use el siguiente código para confirmar su reserva:
    
    Código de confirmación: {codigo_confirmacion}
    
    Saludos,
    Equipo de Gestión de Alquileres
    """
    destinatarios = [alquiler.cliente.email] 

    EmailEnviador.send_email(asunto, mensaje, destinatarios)
