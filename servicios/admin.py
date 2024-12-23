from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import CalificacionServicio, Servicio, FotoServicio


class ServicioResource(resources.ModelResource):
    class Meta:
        model = Servicio


class CalificacionServicioResource(resources.ModelResource):
    class Meta:
        model = CalificacionServicio


class FotoServicioResource(resources.ModelResource):
    class Meta:
        model = FotoServicio


class FotosServiciosInline(admin.TabularInline):
    model = FotoServicio
    extra = 1
    readonly_fields = ("foto_view",)


class CalificacionesServiciosInline(admin.TabularInline):
    model = CalificacionServicio
    extra = 1


class ServicioAdmin(ImportExportModelAdmin):
    resource_class = ServicioResource
    list_display = (
        "id",
        "nombre",
        "descripcion",
        "valor_unidad",
        "agregado_por",
        "vigencia",
    )
    search_fields = (
        "id",
        "nombre",
        "descripcion",
        "valor_unidad",
        "agregado_por__username",
    )
    list_filter = (
        "vigencia",
        "fecha_actualizacion_precio",
    )
    list_per_page = 10
    inlines = [FotosServiciosInline, CalificacionesServiciosInline]


class CalificacionServicioAdmin(ImportExportModelAdmin):
    resource_class = CalificacionServicioResource
    list_display = (
        "id",
        "usuario",
        "calificacion",
        "comentario",
        "fecha",
        "servicio",
    )
    search_fields = (
        "id",
        "calificacion",
        "fecha",
        "servicio__nombre",
        "usuario__username",
    )
    list_per_page = 10


class FotoServicioAdmin(ImportExportModelAdmin):
    resource_class = FotoServicioResource
    list_display = (
        "id",
        "servicio",
        "foto_view",
        "descripcion",
        "numero_likes",
        "fecha_publicacion",
    )
    search_fields = (
        "id",
        "servicio__nombre",
    )
    readonly_fields = ("foto_view",)
    list_filter = ("fecha_publicacion",)
    list_per_page = 10


admin.site.register(Servicio, ServicioAdmin)
admin.site.register(CalificacionServicio, CalificacionServicioAdmin)
admin.site.register(FotoServicio, FotoServicioAdmin)
