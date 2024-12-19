from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.usuarios, name="usuarios"),
    path("crear-cuenta/", views.crear_cuenta, name="crear_cuenta"),
    path("iniciar-sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("validar-correo/", views.validar_correo, name="validar_correo"),
    path("perfil/", views.perfil, name="perfil"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("actualizar-perfil/", views.actualizar_perfil, name="actualizar_perfil"),
    path("completar-perfil/", views.completar_perfil, name="completar_perfil"),
]
