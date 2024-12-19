from django import forms
from ..models import CalificacionServicio

class CalificacionServicioFormulario(forms.ModelForm):
    servicio = forms.CharField(widget=forms.HiddenInput())
    calificacion = forms.IntegerField(label='Calificación', min_value=1, max_value=5)
    comentario = forms.CharField(label='Comentario', widget=forms.Textarea(attrs={'rows': 3}))
    class Meta:
        model = CalificacionServicio
        fields = ['servicio', 'calificacion', 'comentario']


    def clean_comentario(self):
        comentario = self.cleaned_data.get('comentario')
        if len(comentario) < 10:
            raise forms.ValidationError("El comentario debe tener al menos 10 caracteres.")
        return comentario
