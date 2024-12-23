from django.shortcuts import render
from eventos.models import TipoEvento
from alquileres.models import Promocion
# Create your views here.

def index_view(request):

    promociones = Promocion.objects.all()[:5]

    tipo_eventos = TipoEvento.objects.all()[:5]

    return render(request, 'core/home.html', {'tipo_eventos': tipo_eventos, 'promociones': promociones})