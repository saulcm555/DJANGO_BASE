from usuarios.models import PerfilUsuario


class ValidadorUsuario:

    @classmethod
    def validar_correo_verificado(cls,user):
        if user:
            perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=user)
            print(perfil_usuario)
            if not perfil_usuario.correo_electronico_verificado:
                return False
        return True

    @classmethod
    def validar_perfil_completo(cls,user):
        if user:
            perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=user)
            if not perfil_usuario.datos_completos:
                return False
        return True
    
    @classmethod
    def validar_correo_verificado_y_datos_completos(cls,user):
        return cls.validar_correo_verificado(user) and cls.validar_perfil_completo(user)