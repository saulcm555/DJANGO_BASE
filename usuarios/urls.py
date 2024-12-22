from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("crear-cuenta/", views.crear_cuenta, name="crear_cuenta"),
    path("iniciar-sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("validar-correo/", views.validar_correo, name="validar_correo"),
    path("perfil/", views.perfil, name="perfil"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path('validar-correo-helper/', views.reenvio_correo_validacion, name='reenvio_correo_validacion'),
]
