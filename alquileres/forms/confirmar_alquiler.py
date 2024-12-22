from django import forms
from alquileres.models import Alquiler

class ConfirmarAlquilerFormulario(forms.Form):
    codigo_confirmacion = forms.CharField(
        label="Código de confirmación",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese el código de confirmación"}),
    )

    def __init__(self, *args, **kwargs):
        # Extraemos el alquiler de los kwargs
        self.alquiler = kwargs.pop('alquiler', None)  # Se extrae el alquiler del kwargs
        super().__init__(*args, **kwargs)  # Llamamos al inicializador del formulario para mantener la funcionalidad predeterminada

    def clean(self):
        cleaned_data = super().clean()
        codigo_confirmacion = cleaned_data.get("codigo_confirmacion")

        if not self.alquiler:
            raise forms.ValidationError("No se encontró el alquiler asociado.")

        # Validación del código de confirmación
        if str(self.alquiler.codigo_confirmacion) != str(codigo_confirmacion):
            raise forms.ValidationError("El código de confirmación es incorrecto.")

        # Verificar si el alquiler ya está confirmado
        if self.alquiler.correo_electronico_verificado:
            raise forms.ValidationError("Este alquiler ya ha sido confirmado.")

        return cleaned_data
    
    def save(self):
        # Cambiar el estado del alquiler a 'confirmado'
        self.alquiler.correo_electronico_verificado = True
        self.alquiler.save()
        return self.alquiler
