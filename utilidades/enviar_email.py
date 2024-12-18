from django.core.mail import send_mail
from django.conf import settings

from usuarios.models import PerfilUsuario


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
