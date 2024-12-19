from django import forms
from usuarios.models import PerfilUsuario


class CompletarPerfilFormulario(forms.ModelForm):
    identificacion_cliente = forms.CharField(
        label="Identificación",
        widget=forms.TextInput(attrs={"required": "required"}),
    )
    nacionalidad = forms.CharField(
        label="Nacionalidad",
        widget=forms.TextInput(attrs={"required": "required"}),
    )
    telefono = forms.CharField(
        label="Teléfono",
        widget=forms.TextInput(attrs={"required": "required"}),
    )
    nombres = forms.CharField(
        label="Nombres",
        widget=forms.TextInput(attrs={"required": "required"}),
    )
    apellidos = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={"required": "required"}),
    )
    correo_electronico = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"required": "required"}),
    )
    genero = forms.ChoiceField(
        label="Género",
        choices=[("M", "Masculino"), ("F", "Femenino"), ("O", "Otro")],
        widget=forms.Select(attrs={"required": "required"}),
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date", "required": "required"}),
    )

    class Meta:
        model = PerfilUsuario
        fields = [
            "identificacion_cliente",
            "nacionalidad",
            "telefono",
            "nombres",
            "apellidos",
            "correo_electronico",
            "genero",
            "fecha_nacimiento",
        ]

    def clean_identificacion_cliente(self):
        identificacion_cliente = self.cleaned_data.get("identificacion_cliente")
        if PerfilUsuario.objects.filter(
            identificacion_cliente=identificacion_cliente
        ).exists():
            raise forms.ValidationError("Este número de identificación ya está en uso.")
        return identificacion_cliente
