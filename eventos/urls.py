from django.urls import path
from . import views

urlpatterns = [
    path("", views.eventos, name="eventos"),
    path("<int:id>/", views.evento_detalle, name="evento_detalle"),
    path("<int:id>/calificaciones/", views.calificaciones_evento, name="calificacion_evento"),
    path("<int:id>/fotos/", views.fotos_evento, name="fotos_evento"),
]