from django import forms
from ..models import Servicio


class ServicioFormulario(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "nombre",
            "descripcion",
            "valor_unidad",
            "vigencia",
            "descripcion_unidad",
        ]


    def clean_valor_unidad(self):
        valor_unidad = self.cleaned_data.get("valor_unidad")
        if valor_unidad <= 0:
            raise forms.ValidationError(
                "El valor de la unidad debe ser mayor que cero."
            )
        return valor_unidad

