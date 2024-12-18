from django import forms
from usuarios.models import PerfilUsuario

INPUT_STYLE = " "

class CompletarPerfilFormulario(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = [
            'identificacion_cliente',
            'nacionalidad',
            'telefono',
            'nombres',
            'apellidos',
            'correo_electronico',
            'genero',
            'fecha_nacimiento',
        ]
        widgets = {
            'identificacion_cliente': forms.TextInput(attrs={'class': INPUT_STYLE, 'required': 'required'}),
            'nacionalidad': forms.TextInput(attrs={'class': INPUT_STYLE, 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'class': INPUT_STYLE, 'required': 'required'}),
            'nombres': forms.TextInput(attrs={'class': INPUT_STYLE, 'required': 'required'}),
            'apellidos': forms.TextInput(attrs={'class': INPUT_STYLE, 'required': 'required'}),
            'genero': forms.Select(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], attrs={'class': INPUT_STYLE, 'required': 'required'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE, 'required': 'required'}),
        }

    def clean_identificacion_cliente(self):
        identificacion_cliente = self.cleaned_data.get('identificacion_cliente')
        if PerfilUsuario.objects.filter(identificacion_cliente=identificacion_cliente).exists():
            raise forms.ValidationError("Este número de identificación ya está en uso.")
        return identificacion_cliente
