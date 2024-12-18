from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


INPUT_STYLE = " "
CHECKBOX_STYLE = ""


class IniciarSesionFormulario(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": INPUT_STYLE,
                "placeholder": "Ingrese su usuario",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": INPUT_STYLE,
                "placeholder": "Ingrese su contrasena",
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "El usuario no existe", code="username_not_found"
            )
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError(
                    "La contrasena es incorrecta", code="invalid_password"
                )
        return password
