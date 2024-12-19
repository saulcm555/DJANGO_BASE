from django import forms
from ..models import AlquilerServicio


class AlquilerServicioFormulario(forms.ModelForm):
    reerva = forms.CharField(widget=forms.HiddenInput(), required=False)
    servicio = forms.CharField(widget=forms.HiddenInput(), required=False)
    estado_servicio_reserva = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    fecha_entrega = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Fecha de entrega",
                "type": "date",
            }
        ),
        required=False,
    )

    class Meta:
        model = AlquilerServicio
        fields = [
            "reserva",
            "servicio",
            "estado_servicio_reserva",
            "fecha_entrega",
        ]
