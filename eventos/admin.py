from django.contrib import admin

# Register your models here.
from .models import Evento, TipoEvento, FotoEvento, CalificacionEvento


class FotoEventoInline(admin.TabularInline):
    model = FotoEvento
    extra = 0
    readonly_fields = ("foto_view",)


class CalificacionEventoInline(admin.TabularInline):
    model = CalificacionEvento
    extra = 0


class EventoAdmin(admin.ModelAdmin):
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


class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_evento", "descripcion", "fecha_creacion")
    search_fields = ("nombre_evento",)
    list_filter = ("nombre_evento", "fecha_creacion")
    list_per_page = 10


class FotoEventoAdmin(admin.ModelAdmin):
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


class CalificacionEventoAdmin(admin.ModelAdmin):
    list_display = ("id", "evento", "usuario", "calificacion")
    search_fields = ("evento__nombre", "usuario__username")
    list_filter = (
        "calificacion",
        "evento",
    )
    list_per_page = 10


admin.site.register(
    Evento, EventoAdmin, inlines=[FotoEventoInline, CalificacionEventoInline]
)
admin.site.register(TipoEvento, TipoEventoAdmin)
admin.site.register(FotoEvento, FotoEventoAdmin)
admin.site.register(CalificacionEvento, CalificacionEventoAdmin)
