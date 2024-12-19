from django import forms
from ..models import Eventualidad


class EventualidadFormulario(forms.ModelForm):
    alquiler = forms.CharField(widget=forms.HiddenInput(), required=False)
    descripcion_eventualidad = forms.CharField(
        label="Descripción de la eventualidad",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        required=True,
    )

    nivel_impacto_eventualidad = forms.ChoiceField(
        label="Nivel de impacto de la eventualidad",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=Eventualidad.NIVEL_IMPACTO_CHOICES,
        required=True,
    )

    categoria_eventualidad = forms.ChoiceField(
        label="Categoría de la eventualidad",
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=Eventualidad.CATEGORIA_EVENTUALIDAD_CHOICES,
        required=True,
    )
    monto_penalidad_eventualidad = forms.DecimalField(
        label="Monto de la penalidad",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=True,
    )
    fecha_ocurrencia_eventualidad = forms.DateField(
        label="Fecha de ocurrencia de la eventualidad",
        widget=forms.DateInput(attrs={"class": "form-control"}),
        required=True,
    )

    class Meta:
        model = Eventualidad
        fields = [
            "alquiler",
            "descripcion_eventualidad",
            "nivel_impacto_eventualidad",
            "categoria_eventualidad",
            "monto_penalidad_eventualidad",
            "fecha_ocurrencia_eventualidad",
        ]
