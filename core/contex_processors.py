from django.conf import settings
from negocio.models import ConfiguracionNegocio

def configuracion_negocio_context(request):
    return {'configuracion_negocio': ConfiguracionNegocio.objects.first()}