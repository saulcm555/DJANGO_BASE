from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import ConfiguracionNegocio


class ConfiguracionNegocioResource(resources.ModelResource):
    class Meta:
        model = ConfiguracionNegocio


class ConfiguracionNegocioAdmin(ImportExportModelAdmin):
    resource_class = ConfiguracionNegocioResource
    list_display = (
        "nombre",
        "correo",
        "telefono",
        "nombre_banco",
        "tipo_cuenta",
        "numero_cuenta",
    )


admin.site.register(ConfiguracionNegocio, ConfiguracionNegocioAdmin)
