from django import forms
from ..models import Alquiler

class AlquilerFormulario(forms.ModelForm):
    fecha_alquiler = forms.DateField(
        label="Fecha de alquiler",
        widget=forms.DateInput(attrs={
            "class": "form-control", 
            "type": "date"
        }),
        required=True,
    )

    hora_inicio_alquiler = forms.TimeField(
        label="Hora de inicio de la reserva",
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
        required=True,
    )
    hora_fin_planificada_alquiler = forms.TimeField(
        label="Hora de fin planificada de la reserva",
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
        required=True,
    )

    cantidad_anticipo = forms.DecimalField(
        label="Cantidad de anticipo",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Alquiler
        fields = [
            "fecha_alquiler",
            "hora_inicio_alquiler",
            "hora_fin_planificada_alquiler",
            "cantidad_anticipo",
            "promociones",
        ]

    def clean(self):
        cleaned_data = super().clean()
        
        hora_inicio_alquiler = cleaned_data.get("hora_inicio_alquiler")
        hora_fin_planificada_alquiler = cleaned_data.get("hora_fin_planificada_alquiler")
        
        # Validación de hora de inicio y hora de fin
        if hora_inicio_alquiler and hora_fin_planificada_alquiler:
            if hora_inicio_alquiler >= hora_fin_planificada_alquiler:
                raise forms.ValidationError(
                    "La hora de inicio de la reserva debe ser menor a la hora de fin planificada de la reserva"
                )

        # Validación adicional para verificar si ambas horas existen
        if not hora_inicio_alquiler or not hora_fin_planificada_alquiler:
            raise forms.ValidationError(
                "La hora de inicio y la hora de fin planificada son obligatorias"
            )
        
        return cleaned_data
