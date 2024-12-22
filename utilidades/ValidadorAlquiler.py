class ValidadorAlquiler:
    @classmethod
    def validar_alquiler(cls, alquiler):
        if alquiler:
            if not alquiler.correo_electronico_verificado:
                return False
        return True
