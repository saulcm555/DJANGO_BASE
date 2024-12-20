from django.contrib import admin

# Register your models here.
from .models import PerfilUsuario


class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "identificacion_cliente",
        "telefono",
        "nombres",
        "apellidos",
        "correo_electronico",
        "fecha_nacimiento",
    )

    search_fields = (
        "usuario__username",
        "identificacion_cliente",
        "nombres",
        "apellidos",
        "correo_electronico",
    )

    list_filter = (
        "genero",
        "fecha_registro",
        "correo_electronico_verificado",
        "datos_completos",
    )

    ordering = ("id", "usuario", "nombres", "apellidos")

admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
