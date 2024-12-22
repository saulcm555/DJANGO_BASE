from django.shortcuts import render
from eventos.models import TipoEvento
# Create your views here.

def index_view(request):
    tipo_eventos = TipoEvento.objects.all()[:5]
    return render(request, 'core/home.html', {'tipo_eventos': tipo_eventos})