from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Evento, TipoEvento, FotoEvento, CalificacionEvento


class EventoResource(resources.ModelResource):
    class Meta:
        model = Evento


class TipoEventoResource(resources.ModelResource):
    class Meta:
        model = TipoEvento


class FotoEventoResource(resources.ModelResource):
    class Meta:
        model = FotoEvento


class CalificacionEventoResource(resources.ModelResource):
    class Meta:
        model = CalificacionEvento


# Inline definitions
class FotoEventoInline(admin.TabularInline):
    model = FotoEvento
    extra = 0
    readonly_fields = ("foto_view",)


class CalificacionEventoInline(admin.TabularInline):
    model = CalificacionEvento
    extra = 0


# Admin classes
class EventoAdmin(ImportExportModelAdmin):
    resource_class = EventoResource
    list_display = (
        "id",
        "nombre",
        "valor_referencial",
        "numero_horas_permitidas",
        "valor_extra_hora",
        "tipo_evento",
    )
    search_fields = ("nombre", "tipo_evento__nombre_evento")
    list_filter = ("tipo_evento", "numero_horas_permitidas", "valor_extra_hora")
    list_per_page = 10
    inlines = [FotoEventoInline, CalificacionEventoInline]


class TipoEventoAdmin(ImportExportModelAdmin):
    resource_class = TipoEventoResource
    list_display = ("id", "nombre_evento", "descripcion", "fecha_creacion")
    search_fields = ("nombre_evento",)
    list_filter = ("nombre_evento", "fecha_creacion")
    list_per_page = 10


class FotoEventoAdmin(ImportExportModelAdmin):
    resource_class = FotoEventoResource
    list_display = (
        "id",
        "evento",
        "foto_view",
        "descripcion",
        "fecha_publicacion",
        "numero_likes",
    )
    search_fields = ("evento__nombre",)
    list_filter = ("evento",)
    list_per_page = 10


class CalificacionEventoAdmin(ImportExportModelAdmin):
    resource_class = CalificacionEventoResource
    list_display = (
        "id",
        "usuario",
        "evento",
        "calificacion",
        "comentario",
        "fecha_publicacion",
    )
    search_fields = ("evento__nombre", "usuario__username")
    list_filter = (
        "calificacion",
        "evento",
    )
    list_per_page = 10


# Register models with the admin
admin.site.register(Evento, EventoAdmin)
admin.site.register(TipoEvento, TipoEventoAdmin)
admin.site.register(FotoEvento, FotoEventoAdmin)
admin.site.register(CalificacionEvento, CalificacionEventoAdmin)
