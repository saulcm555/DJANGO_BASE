from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q


from usuarios.decoradores import admin_required
from .models import Servicio, FotoServicio
from .forms import (
    ServicioFormulario,
    CalificacionServicioFormulario,
)


def servicios(request):
    query = request.GET.get("query", "")
    servicios = Servicio.objects.filter(vigencia=True)
    if query:
        servicios = servicios.filter(
            Q(nombre__icontains=query)
            | Q(descripcion_servicio__icontains=query)
            | Q(descripcion_unidad__icontains=query)
        )

    return render(request, "servicios/servicios.html", {"servicios": servicios})


def servicio_detalle(request, id):
    servicio = Servicio.objects.filter(id=id).first()
    if not servicio:
        return HttpResponseBadRequest("Servicio no encontrado")

    if request.method == "GET":
        fotos = servicio.fotos.all()
        return render(
            request, "servicios/detalle_servicio.html", {"servicio": servicio, "fotos": fotos}
        )

    return HttpResponseForbidden("Método no permitido")


def calificaciones_servicio(request, id):
    servicio = Servicio.objects.filter(id=id).first()
    if not servicio:
        return HttpResponseBadRequest("Servicio no encontrado")
    calificaciones = servicio.calificacion_servicio.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("usuarios:iniciar_sesion")
        formulario = CalificacionServicioFormulario(request.POST)
        if formulario.is_valid():
            calificacion = formulario.save(commit=False)
            calificacion.servicio = servicio
            calificacion.usuario = request.user
            calificacion.save()
            return redirect("servicios:servicios")
    else:
        formulario = CalificacionServicioFormulario()

    return render(
        request,
        "servicios/calificacion_servicio.html",
        {
            "servicio": servicio,
            "calificaciones": calificaciones,
            "form": formulario,
        },
    )


