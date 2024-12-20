from django.contrib import admin

# Register your models here.
from .models import CalificacionServicio, Servicio, FotoServicio


class FotosServiciosInline(admin.TabularInline):
    model = FotoServicio
    extra = 1
    readonly_fields = ("foto_view",)


class CalificacionesServiciosInline(admin.TabularInline):
    model = CalificacionServicio
    extra = 1
    


class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "descripcion",
        "valor_unidad",
        "agregado_por",
        "vigencia",
    )
    search_fields = ("id", "nombre", "descripcion", "valor_unidad", "agregado_por")
    list_filter = (
        "vigencia",
        "fecha_actualizacion_precio",
    )
    list_per_page = 10  



class CalificacionServicioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "calificacion",
        "comentario",
        "fecha",
        "servicio",
    )
    search_fields = ("id", "calificacion", "fecha", "servicio", "usuario")
    list_per_page = 10  


class FotoServicioAdmin(admin.ModelAdmin):
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
        "servicio",
    )
    readonly_fields = ("foto_view",)
    
    list_filter = ("fecha_publicacion",)
    list_per_page = 10  


admin.site.register(
    Servicio,
    ServicioAdmin,
    inlines=[FotosServiciosInline, CalificacionesServiciosInline],
)
admin.site.register(CalificacionServicio, CalificacionServicioAdmin)
admin.site.register(FotoServicio, FotoServicioAdmin)
