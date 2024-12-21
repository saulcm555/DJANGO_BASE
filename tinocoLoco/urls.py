from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('servicios/', include('servicios.urls')),
    path('eventos/', include('eventos.urls')),
    path('alquileres/', include('alquileres.urls')),
]
