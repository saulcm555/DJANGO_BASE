from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from utilidades import EmailEnviador
from ..models import PerfilUsuario

INPUT_STYLE = " "


class CrearCuentaFormulario(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": INPUT_STYLE, "placeholder": "Ingrese su correo electrónico"}
        ),
        error_messages={"unique": "El correo electrónico ya está en uso."},
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": INPUT_STYLE, "placeholder": "Ingrese su usuario"}
            ),
            "password1": forms.PasswordInput(
                attrs={"class": INPUT_STYLE, "placeholder": "Ingrese su contraseña"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": INPUT_STYLE, "placeholder": "Confirme su contraseña"}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isalnum():
            raise forms.ValidationError(
                "El usuario solo puede contener letras y números."
            )
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está en uso.")
        return email
    

    def save(self, commit=True):
        user = super().save(commit=commit)
        perfil = PerfilUsuario.objects.create(
            usuario=user, correo_electronico=self.cleaned_data["email"]
        )
        perfil.generar_codigo_verificacion()
        perfil.save()

        EmailEnviador.enviar_codigo_validar_email(perfil)
        return user
