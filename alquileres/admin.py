from django.contrib import admin

# Register your models here.
from .models import (
    Alquiler,
    Eventualidad,
    FotoAlquiler,
    Promocion,
    CalificacionAlquiler,
)


class FotoAlquilerInline(admin.TabularInline):
    model = FotoAlquiler
    extra = 1


class EventualidadInline(admin.TabularInline):
    model = Eventualidad
    extra = 1


# class CalificacionAlquilerInline(admin.TabularInline):
#     model = CalificacionAlquiler
#     extra = 1


class AlquilerAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "evento",
        "fecha_alquiler",
        "hora_inicio_alquiler",
        "hora_fin_planificada_alquiler",
        "costo_alquiler",
        "Estado_de_alquiler",
    )

    search_fields = (
        "cliente__username",
        "evento__nombre",
        "fecha_alquiler",
        "hora_inicio_alquiler",
        "hora_fin_planificada_alquiler",
        "costo_alquiler",
        "Estado_de_alquiler",
    )

    list_filter = (
        "Estado_de_alquiler",
        "fecha_alquiler",
        "fecha_creacion",
    )


class EventualidadAdmin(admin.ModelAdmin):
    list_display = (
        "alquiler",
        "descripcion_eventualidad",
        "categoria_eventualidad",
        "nivel_impacto_eventualidad",
        "fecha_ocurrencia_eventualidad",
    )

    search_fields = (
        "alquiler__cliente__username",
        "alquiler__evento__nombre",
        "descripcion_eventualidad",
        "nivel_impacto_eventualidad",
    )

    list_filter = (
        "fecha_ocurrencia_eventualidad",
        "nivel_impacto_eventualidad",
        "categoria_eventualidad",
    )


class FotoAlquilerAdmin(admin.ModelAdmin):
    list_display = (
        "alquiler",
        "foto",
        "descripcion",
        "fecha_publicacion",
        "numero_likes",
    )

    search_fields = (
        "alquiler__cliente__username",
        "alquiler__evento__nombre",
        "foto",
    )

    list_filter = ("fecha_publicacion", "numero_likes", "alquiler")


class CalificacionAlquilerAdmin(admin.ModelAdmin):
    list_display = (
        "alquiler",
        "usuario",
        "calificacion",
        "comentario",
        "fecha_calificacion",
    )
    list_display_links = (
        "usuario",
        "alquiler",
    )
    search_fields = (
        "alquiler__usuario__username",
        "usuario__username",
    )
    list_filter = (
        "fecha_calificacion",
        "calificacion",
    )


class PromocionAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_promocion",
        "descripcion_promocion",
        "fecha_vigencia",
        "fecha_caducidad",
        "porcentaje_promocion",
        "estado_promocion",
    )

    search_fields = (
        "nombre_promocion",
        "descripcion_promocion",
        "fecha_vigencia",
        "fecha_caducidad",
        "porcentaje_promocion",
    )

    list_filter = (
        "fecha_vigencia",
        "fecha_caducidad",
        "estado_promocion",
    )


admin.site.register(
    Alquiler, AlquilerAdmin, inlines=[FotoAlquilerInline, EventualidadInline]
)
admin.site.register(Eventualidad, EventualidadAdmin)
admin.site.register(FotoAlquiler, FotoAlquilerAdmin)
admin.site.register(CalificacionAlquiler, CalificacionAlquilerAdmin)
admin.site.register(Promocion, PromocionAdmin)
