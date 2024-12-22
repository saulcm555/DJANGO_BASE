from django import forms
from ..models import CalificacionEvento 

class CalificacionEventoFormulario(forms.ModelForm):
    calificacion = forms.IntegerField(label='Calificación', required=True)
    comentario = forms.CharField(label='Comentario', required=True)
    
    class Meta:
        model = CalificacionEvento
        fields = ['calificacion', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        

    
    def clean_comentario(self):
        comentario = self.cleaned_data.get('comentario')
        if len(comentario) < 10:
            raise forms.ValidationError("El comentario debe tener al menos 10 caracteres.")
        return comentario

    def clean_calificacion(self):
        calificacion = self.cleaned_data.get('calificacion')
        if calificacion < 1 or calificacion > 5:
            raise forms.ValidationError("La calificación debe ser un número entre 1 y 5.")
        return calificacion
