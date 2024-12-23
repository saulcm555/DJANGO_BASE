from django.contrib import admin

from django.contrib.admin import SimpleListFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import PerfilUsuario


class DatosCompletosFilter(SimpleListFilter):
    title = "Datos Completos"
    parameter_name = "datos_completos"

    def lookups(self, request, model_admin):
        return [
            ("completos", "Completos"),
            ("incompletos", "Incompletos"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "completos":
            return queryset.filter(
                nombres__isnull=False,
                apellidos__isnull=False,
                nacionalidad__isnull=False,
                telefono__isnull=False,
                fecha_nacimiento__isnull=False,
                correo_electronico__isnull=False,
                correo_electronico_verificado=True,
            )
        if self.value() == "incompletos":
            return queryset.exclude(
                nombres__isnull=False,
                apellidos__isnull=False,
                nacionalidad__isnull=False,
                telefono__isnull=False,
                fecha_nacimiento__isnull=False,
                correo_electronico__isnull=False,
                correo_electronico_verificado=True,
            )


class PerfilUsuarioResource(resources.ModelResource):
    class Meta:
        model = PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(ImportExportModelAdmin):
    resource_class = PerfilUsuarioResource
    list_display = (
        "id",
        "usuario",
        "identificacion_cliente",
        "telefono",
        "nombres",
        "apellidos",
        "correo_electronico",
        "fecha_nacimiento",
        "datos_completos_admin",
    )

    search_fields = (
        "usuario__username",
        "identificacion_cliente",
        "nombres",
        "apellidos",
        "correo_electronico",
        "telefono",
    )

    list_filter = (
        "genero",
        "fecha_registro",
        "correo_electronico_verificado",
        DatosCompletosFilter,
    )

    def datos_completos_admin(self, obj):
        return obj.datos_completos

    datos_completos_admin.boolean = True
    datos_completos_admin.short_description = "Datos Completos"
