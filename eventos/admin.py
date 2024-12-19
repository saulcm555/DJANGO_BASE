from django.contrib import admin

# Register your models here.
from .models import Evento, TipoEvento, FotoEvento, CalificacionEvento

admin.site.register(Evento)
admin.site.register(TipoEvento)
admin.site.register(FotoEvento)
admin.site.register(CalificacionEvento)
