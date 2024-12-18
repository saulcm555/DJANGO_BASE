from django.contrib import admin

# Register your models here.
from .models import CalificacionServicio, Servicio, FotoServicio

admin.site.register(CalificacionServicio)
admin.site.register(Servicio)
admin.site.register(FotoServicio)
