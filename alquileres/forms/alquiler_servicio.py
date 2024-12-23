from django import forms
from ..models import AlquilerServicio
from servicios.models import Servicio


class AlquilerServicioFormulario(forms.ModelForm):
    cantidad = forms.IntegerField(
        label="Cantidad",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad",
                "min": 1,
                "max": 100,
            }
        ),
        required=False,  # Inicialmente no requerido
    )

    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Servicio",
            }
        ),
    )

    class Meta:
        model = AlquilerServicio
        fields = [
            "servicio",
            "cantidad",
        ]

    def clean(self):
        cleaned_data = super().clean()
        servicio = cleaned_data.get("servicio")
        cantidad = cleaned_data.get("cantidad")

        if servicio and not cantidad:
            self.add_error('cantidad', 'Este campo es requerido si hay un servicio seleccionado.')

        return cleaned_data
