from django import forms
from ..models import Alquiler
from utilidades.enviar_email import EmailEnviador


class AlquilerFormulario(forms.ModelForm):
    cliente = forms.CharField(widget=forms.HiddenInput(), required=False)
    evento = forms.CharField(max_length=100, required=True)
    fecha_alquiler = forms.DateField(
        label="Fecha de alquiler",
        widget=forms.DateInput(attrs={"class": "form-control"}),
        required=True,
    )

    horainicio_reserva = forms.TimeField(
        label="Hora de inicio de la reserva",
        widget=forms.TimeInput(attrs={"class": "form-control"}),
        required=True,
    )
    horafin_planificada_reserva = forms.TimeField(
        label="Hora de fin planificada de la reserva",
        widget=forms.TimeInput(attrs={"class": "form-control"}),
        required=True,
    )
    horafin_real_reserva = forms.TimeField(
        label="Hora de fin real de la reserva",
        widget=forms.TimeInput(attrs={"class": "form-control"}),
        required=True,
    )
    costo_alquiler = forms.DecimalField(
        label="Costo de alquiler",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
    )
    calificacion_dueno = forms.IntegerField(
        label="Calificación del dueño",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
    )

    calificacion_cliente = forms.IntegerField(
        label="Calificación del cliente",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
    )
    observacion = forms.CharField(
        label="Observación",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        required=False,
    )
    cantidad_anticipo = forms.DecimalField(
        label="Cantidad de anticipo",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
    )
    promociones = forms.CharField(
        label="Promociones",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        required=False,
    )
    estado_de_alquiler = forms.ChoiceField(
        label="Estado de alquiler",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=Alquiler.ESTADO_ALQUILER_CHOICES,
        required=True,
    )

    class Meta:
        model = Alquiler
        fields = [
            "cliente",
            "evento",
            "fecha_alquiler",
            "horainicio_reserva",
            "horafin_planificada_reserva",
            "horafin_real_reserva",
            "costo_alquiler",
            "calificacion_dueno",
            "calificacion_cliente",
            "observacion",
            "cantidad_anticipo",
            "promociones",
            "estado_de_alquiler",
        ]
