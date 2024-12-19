from django import forms
from ..models import CalificacionAlquiler 

class CalificacionAlquilerFormulario(forms.ModelForm):
    alquiler = forms.CharField(widget=forms.HiddenInput())
    usuario = forms.CharField(widget=forms.HiddenInput())
    calificacion = forms.IntegerField(label='Calificación', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    comentario = forms.CharField(label='Comentario', widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    
    class Meta:
        model = CalificacionAlquiler
        fields = ['alquiler', 'usuario', 'calificacion', 'comentario']


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
