wfrom negocio.models import ConfiguracionNegocio

from django.db.models import Avg

from eventos.models import Evento


def configuracion_negocio_context(request):
    return {"configuracion_negocio": ConfiguracionNegocio.objects.first()}


def eventos_mas_gustados_context(request):
    eventos_mas_gustados = Evento.objects.annotate(
        promedio_calificacion=Avg("calificacion_evento__calificacion")
    ).order_by("-promedio_calificacion")[:5]
    
    return {"eventos_mas_gustados": eventos_mas_gustados}
