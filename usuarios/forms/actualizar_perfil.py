from django import forms
from usuarios.models import PerfilUsuario


class ActualizarPerfilFormulario(forms.ModelForm):
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
            "nacionalidad",
            "telefono",
            "nombres",
            "apellidos",
            "genero",
            "fecha_nacimiento",
        ]

    def clean_identificacion_cliente(self):
        identificacion_cliente = self.cleaned_data.get("identificacion_cliente")
        if identificacion_cliente != self.instance.identificacion_cliente:
            raise forms.ValidationError(
                "No puedes cambiar tu número de identificación."
            )
        return identificacion_cliente

    def clean_correo_electronico(self):
        correo_electronico = self.cleaned_data.get("correo_electronico")
        if correo_electronico != self.instance.correo_electronico:
            raise forms.ValidationError("No puedes cambiar tu correo electrónico.")
        return correo_electronico
