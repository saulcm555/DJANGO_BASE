from django.contrib import admin

# Register your models here.
from .models import Alquiler, Eventualidad, FotoAlquiler,Promocion, CalificacionAlquiler

admin.site.register(Alquiler)
admin.site.register(Eventualidad)
admin.site.register(FotoAlquiler)
admin.site.register(Promocion)
admin.site.register(CalificacionAlquiler)
