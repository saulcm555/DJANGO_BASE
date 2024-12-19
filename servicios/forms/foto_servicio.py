from django import forms
from ..models import FotoServicio

class FotoServicioFormulario(forms.ModelForm):
    servicio = forms.CharField(widget=forms.HiddenInput())
    foto = forms.ImageField(label='Foto')
    descripcion = forms.CharField(label='Descripción', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    
    
    class Meta:
        model = FotoServicio
        fields = ['servicio', 'foto', 'descripcion']


    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if not foto:
            raise forms.ValidationError("Debe cargar una foto.")
        return foto
