from django.conf import settings
from negocio.models import ConfiguracionNegocio

def settings_context(request):
    return {'configuracion': ConfiguracionNegocio.objects.first()}