from django import forms
from ..models import FotoEvento  

class FotoEventoFormulario(forms.ModelForm):
    foto = forms.ImageField(label='Foto', required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    descripcion = forms.CharField(label='Descripción', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    class Meta:
        model = FotoEvento
        fields = ['evento', 'foto', 'descripcion']


    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if not foto:
            raise forms.ValidationError("Debe cargar una foto.")
        return foto
