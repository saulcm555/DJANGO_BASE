from django.urls import path
from . import views

app_name = "alquileres"

urlpatterns = [
    path("", views.alquileres, name="alquileres"),
    path("nuevo/<int:item_id>", views.nuevo_alquiler, name="nuevo_alquiler"),
    path("<int:id>/", views.alquiler_detalle, name="alquiler_detalle"),
    path(
        "<int:id>/calificaciones/",
        views.calificaciones_alquiler,
        name="calificacion_alquiler",
    ),
    path(
        "<int:id>/eventualidades/",
        views.eventualidades_alquiler,
        name="eventualidades_alquiler",
    ),
    path("<int:id>/servicios/", views.servicios_alquiler, name="servicios_alquiler"),
    path("confirmar/<int:id>", views.confirmar_alquiler, name="confirmar_alquiler"),
    path("enviar-correo/<int:id>", views.enviar_correo_alquiler, name="enviar_correo_alquiler"),
]
