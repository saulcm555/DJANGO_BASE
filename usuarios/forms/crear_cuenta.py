from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from utilidades import EmailEnviador
from ..models import PerfilUsuario


class CrearCuentaFormulario(UserCreationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su usuario"}),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        error_messages={"unique": "El correo electrónico ya está en uso."},
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña"}),
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme su contraseña"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

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
