from django import forms
from usuarios.models import PerfilUsuario


class ValidarCorreoFormulario(forms.Form):
    codigo_verificacion = forms.CharField(
        label="Código de verificación",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese el código de verificación"}),
    )
    
    class Meta:
        fields = ("codigo_verificacion",)
    

    def clean(self):
        cleaned_data = super().clean()
        codigo_verificacion = cleaned_data.get("codigo_verificacion")

        user = self.user
        perfil = PerfilUsuario.objects.filter(usuario=user).first()

        if not perfil:
            raise forms.ValidationError("No se encontró un perfil asociado a este usuario.")

        if perfil.codigo_verificacion != codigo_verificacion:
            raise forms.ValidationError("El código de verificación es incorrecto.")

        if perfil.correo_electronico_verificado:
            raise forms.ValidationError("Este correo ya ha sido verificado.")

        return cleaned_data
    
    def save(self):
        perfil = PerfilUsuario.objects.get(usuario=self.user)
        perfil.correo_electronico_verificado = True
        perfil.save()
        return perfil
