from alquileres.models import Alquiler

from django import forms
class ConfirmarAlquilerFormulario(forms.ModelForm):
    codigo_confirmacion = forms.CharField(
        label="Código de Confirmación",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ingrese el código enviado"}),
        required=True,)
    class Meta:
        model = Alquiler
        fields = ["codigo_confirmacion"]
        
    
    def clean_codigo_confirmacion(self):
            codigo = self.cleaned_data.get("codigo_confirmacion")
            if not self.alquiler:
                raise forms.ValidationError("No se encontró el alquiler asociado.")

            if str(self.alquiler.codigo_confirmacion) != str(codigo):
                raise forms.ValidationError("El código de confirmación es incorrecto.")
            return codigo

    def save(self):
        self.alquiler.confirmado = True
        self.alquiler.save()
        return self.alquiler