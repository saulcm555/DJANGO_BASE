from django.contrib import admin

# Register your models here.
from .models import Evento, TipoEvento

admin.site.register(Evento)
admin.site.register(TipoEvento)
