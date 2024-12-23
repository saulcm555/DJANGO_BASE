from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    Alquiler,
    Eventualidad,
    FotoAlquiler,
    Promocion,
    CalificacionAlquiler,
    AlquilerServicio,
)


class AlquilerResource(resources.ModelResource):
    class Meta:
        model = Alquiler


class EventualidadResource(resources.ModelResource):
    class Meta:
        model = Eventualidad


class FotoAlquilerResource(resources.ModelResource):
    class Meta:
        model = FotoAlquiler


class CalificacionAlquilerResource(resources.ModelResource):
    class Meta:
        model = CalificacionAlquiler


class PromocionResource(resources.ModelResource):
    class Meta:
        model = Promocion


class AlquilerServicioResource(resources.ModelResource):
    class Meta:
        model = AlquilerServicio


# Inline definitions
class AlquilerServicioInline(admin.TabularInline):
    model = AlquilerServicio
    extra = 1
    readonly_fields = (
        "servicio",
        "cantidad",
        "estado_servicio_reserva",
        "fecha_entrega",
    )


class FotoAlquilerInline(admin.TabularInline):
    model = FotoAlquiler
    extra = 1
    readonly_fields = ("foto_view",)


class EventualidadInline(admin.TabularInline):
    model = Eventualidad
    extra = 1


class CalificacionAlquilerInline(admin.TabularInline):
    model = CalificacionAlquiler
    extra = 1


# Admin classes
class AlquilerAdmin(ImportExportModelAdmin):
    resource_class = AlquilerResource
    list_display = (
        "id",
        "cliente",
        "evento",
        "fecha_alquiler",
        "hora_inicio_alquiler",
        "hora_fin_planificada_alquiler",
        "costo_alquiler",
        "estado_de_alquiler",
    )
    search_fields = (
        "cliente__username",
        "evento__nombre",
        "fecha_alquiler",
        "hora_inicio_alquiler",
        "hora_fin_planificada_alquiler",
        "estado_de_alquiler",
    )
    list_filter = (
        "estado_de_alquiler",
        "fecha_alquiler",
        "fecha_creacion",
    )
    inlines = [
        FotoAlquilerInline,
        EventualidadInline,
        CalificacionAlquilerInline,
        AlquilerServicioInline,
    ]


class EventualidadAdmin(ImportExportModelAdmin):
    resource_class = EventualidadResource
    list_display = (
        "id",
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


class FotoAlquilerAdmin(ImportExportModelAdmin):
    resource_class = FotoAlquilerResource
    list_display = (
        "id",
        "foto_view",
        "alquiler",
        "descripcion",
        "fecha_publicacion",
        "numero_likes",
    )
    search_fields = (
        "alquiler__cliente__username",
        "alquiler__evento__nombre",
    )
    list_filter = ("fecha_publicacion", "numero_likes", "alquiler")
    readonly_fields = ("foto_view",)


class CalificacionAlquilerAdmin(ImportExportModelAdmin):
    resource_class = CalificacionAlquilerResource
    list_display = (
        "id",
        "alquiler",
        "usuario",
        "calificacion",
        "comentario",
        "fecha_calificacion",
    )
    search_fields = (
        "alquiler__cliente__username",
        "usuario__username",
    )
    list_filter = (
        "fecha_calificacion",
        "calificacion",
    )


class PromocionAdmin(ImportExportModelAdmin):
    resource_class = PromocionResource
    list_display = (
        "id",
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


class AlquilerServicioAdmin(ImportExportModelAdmin):
    resource_class = AlquilerServicioResource
    list_display = (
        "id",
        "alquiler",
        "servicio",
        "cantidad",
        "estado_servicio_reserva",
        "fecha_entrega",
    )
    search_fields = (
        "alquiler__cliente__username",
        "servicio__nombre",
        "estado_servicio_reserva",
    )
    list_filter = (
        "fecha_entrega",
        "estado_servicio_reserva",
    )


admin.site.register(Alquiler, AlquilerAdmin)
admin.site.register(Eventualidad, EventualidadAdmin)
admin.site.register(FotoAlquiler, FotoAlquilerAdmin)
admin.site.register(CalificacionAlquiler, CalificacionAlquilerAdmin)
admin.site.register(Promocion, PromocionAdmin)
admin.site.register(AlquilerServicio, AlquilerServicioAdmin)
