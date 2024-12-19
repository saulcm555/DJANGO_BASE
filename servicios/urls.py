from django.urls import path
from . import views

urlpatterns = [
    path("", views.servicios, name="servicios"),
    path("nuevo/", views.nuevo_servicio, name="nuevo_servicio"),
    path("<int:id>/", views.servicio_detalle, name="servicio_detalle"),
    path("<int:id>/calificaciones/", views.calificaciones_servicio, name="calificacion_servicio"),
    path("<int:id>/fotos/", views.fotos_servicio, name="fotos_servicio"),
]