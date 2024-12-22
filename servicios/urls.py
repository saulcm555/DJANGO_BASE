from django.urls import path
from . import views

app_name = "servicios"

urlpatterns = [
    path("", views.servicios, name="servicios"),
    path("<int:id>/", views.servicio_detalle, name="servicio_detalle"),
    

]
