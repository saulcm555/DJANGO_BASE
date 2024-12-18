from django import forms
from usuarios.models import PerfilUsuario

INPUT_STYLE = " " 

class ActualizarPerfilFormulario(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = [
            'nacionalidad',
            'telefono',
            'nombres',
            'apellidos',
            'genero',
            'fecha_nacimiento',
        ]
        widgets = {
            'nacionalidad': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'telefono': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'nombres': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'apellidos': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'genero': forms.Select(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], attrs={'class': INPUT_STYLE}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
        }

    def clean_identificacion_cliente(self):
        # Preventing the modification of identificacion_cliente
        identificacion_cliente = self.cleaned_data.get('identificacion_cliente')
        if identificacion_cliente != self.instance.identificacion_cliente:
            raise forms.ValidationError("No puedes cambiar tu número de identificación.")
        return identificacion_cliente

    def clean_correo_electronico(self):
        # Preventing the modification of correo_electronico
        correo_electronico = self.cleaned_data.get('correo_electronico')
        if correo_electronico != self.instance.correo_electronico:
            raise forms.ValidationError("No puedes cambiar tu correo electrónico.")
        return correo_electronico
