# from django import forms
# from ..models import Promocion


# class PromocionFormulario(forms.ModelForm):
#     descripcion_promocion = forms.CharField(
#         label="Descripcion de la promocion",
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#     )
#     valor_referencial_promo = forms.FloatField(
#         label="Valor referencial de la promocion",
#         widget=forms.NumberInput(attrs={"class": "form-control"}),
#     )
#     tipo_promocion = forms.CharField(
#         label="Tipo de promocion",
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#     )
#     porcentaje_promocion = forms.IntegerField(
#         label="Porcentaje de promocion",
#         widget=forms.NumberInput(attrs={"class": "form-control"}),
#     )
#     fecha_vigencia = forms.DateField(
#         label="Fecha de vigencia",
#         widget=forms.DateInput(attrs={"class": "form-control"}),
#     )
#     fecha_caducidad = forms.DateField(
#         label="Fecha de caducidad",
#         widget=forms.DateInput(attrs={"class": "form-control"}),
#     )
#     estado_promocion = forms.CharField(
#         label="Estado de la promocion",
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#     )

#     class Meta:
#         model = Promocion
#         fields = [
#             "descripcion_promocion",
#             "valor_referencial_promo",
#             "tipo_promocion",
#             "porcentaje_promocion",
#             "fecha_vigencia",
#             "fecha_caducidad",
#             "estado_promocion",
#         ]

#     def clean_fecha_vigencia(self):
#         fecha_vigencia = self.cleaned_data.get("fecha_vigencia")
#         fecha_caducidad = self.cleaned_data.get("fecha_caducidad")

#         if fecha_vigencia > fecha_caducidad:
#             raise forms.ValidationError(
#                 "La fecha de vigencia no puede ser posterior a la fecha de caducidad."
#             )

#         return fecha_vigencia
