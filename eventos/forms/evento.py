from django import forms
from ..models import Evento  

class EventoFormulario(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False
    )
    class Meta:
        model = Evento
        fields = [
            "nombre",
            "descripcion",
            "valor_referencial",
            "numero_horas_permitidas",
            "valor_extra_hora",
            "tipo_evento",
        ]

    def clean_valor_referencial(self):
        valor_referencial = self.cleaned_data.get("valor_referencial")
        if valor_referencial < 0:
            raise forms.ValidationError(
                "El valor referencial no puede ser negativo."
            )
        return valor_referencial

    def clean_valor_extra_hora(self):
        valor_extra_hora = self.cleaned_data.get("valor_extra_hora")
        if valor_extra_hora < 0:
            raise forms.ValidationError(
                "El valor extra por hora no puede ser negativo."
            )
        return valor_extra_hora

    