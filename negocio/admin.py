from django.contrib import admin

# Register your models here.
from .models import ConfiguracionNegocio


class ConfiguracionNegocioAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "correo",
        "telefono",
        "nombre_banco",
        "tipo_cuenta",
        "numero_cuenta",
    )
    

admin.site.register(ConfiguracionNegocio, ConfiguracionNegocioAdmin)
