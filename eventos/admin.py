from django.contrib import admin

# Register your models here.
from .models import Evento, TipoEvento, FotoEvento, CalificacionEvento


class FotoEventoInline(admin.TabularInline):
    model = FotoEvento
    extra = 0


class CalificacionEventoInline(admin.TabularInline):
    model = CalificacionEvento
    extra = 0


class EventoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "valor_referencial",
        "numero_horas_permitidas",
        "valor_extra_hora",
        "tipo_evento",
    )
    search_fields = ("nombre", "tipo_evento__nombre_evento")
    list_filter = ("tipo_evento", "numero_horas_permitidas", "valor_extra_hora")


class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ("nombre_evento", "descripcion", "fecha_creacion")
    search_fields = ("nombre_evento",)
    list_filter = ("nombre_evento", "fecha_creacion")


class FotoEventoAdmin(admin.ModelAdmin):
    list_display = (
        "evento",
        "foto",
        "descripcion",
        "fecha_publicacion",
        "numero_likes",
    )
    search_fields = ("evento__nombre",)
    list_filter = ("evento",)


class CalificacionEventoAdmin(admin.ModelAdmin):
    list_display = ("evento", "usuario", "calificacion")
    search_fields = ("evento__nombre", "usuario__username")
    list_filter = (
        "calificacion",
        "evento",
    )


admin.site.register(
    Evento, EventoAdmin, inlines=[FotoEventoInline, CalificacionEventoInline]
)
admin.site.register(TipoEvento, TipoEventoAdmin)
admin.site.register(FotoEvento, FotoEventoAdmin)
admin.site.register(CalificacionEvento, CalificacionEventoAdmin)
