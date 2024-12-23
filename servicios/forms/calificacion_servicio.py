from django import forms
from ..models import CalificacionServicio


class CalificacionServicioFormulario(forms.ModelForm):
    calificacion = forms.IntegerField(label="Calificación", min_value=1, max_value=5)
    comentario = forms.CharField(
        label="Comentario", widget=forms.Textarea(attrs={"rows": 3})
    )

    class Meta:
        model = CalificacionServicio
        fields = ["calificacion", "comentario"]

    def clean_calificacion(self):
        calificacion = self.cleaned_data.get("calificacion")
        if calificacion < 1 or calificacion > 5:
            raise forms.ValidationError(
                "La calificación debe ser un número entre 1 y 5."
            )
        return calificacion