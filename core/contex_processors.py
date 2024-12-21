from django.conf import settings
from negocio.models import ConfiguracionNegocio

def configuracion_negocio_context(request):
    return {'configuracion': ConfiguracionNegocio.objects.first()}