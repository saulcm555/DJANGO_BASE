from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.eventos, name="eventos"),
    path("categorias", views.tipos_eventos, name="categorias"),
    path("categorias/<int:id>", views.tipo_evento, name="categoria-evento"),
    path("<int:id>/", views.evento_detalle, name="evento_detalle"),
]
