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

    queryset = []
    for evento in servicios:
        primera_foto = evento.fotos.first()
        calificaciones = evento.calificacion_servicio.all()
        promedio_calificaciones = 0
        if calificaciones:
            promedio_calificaciones = sum(
                [calificacion.calificacion for calificacion in calificaciones]
            ) / len(calificaciones)

        if primera_foto:
            imagen_url = primera_foto.foto.url
        else:
            imagen_url = None
        queryset.append(
            {
                "servicio": evento,
                "imagen_url": imagen_url,
                "promedio_calificaciones": range(0, int(promedio_calificaciones)),
            }
        )

    return render(request, "servicios/servicios.html", {"servicios": queryset})


def servicio_detalle(request, id):
    servicio = Servicio.objects.filter(id=id).first()
    if not servicio:
        return HttpResponseBadRequest("Servicio no encontrado")

    fotos = servicio.fotos.all()
    promedio_calificaciones = 0
    calificaciones = servicio.calificacion_servicio.all()
    if calificaciones:
        promedio_calificaciones = sum(
            [calificacion.calificacion for calificacion in calificaciones]
        ) / len(calificaciones)

    return render(
        request,
        "servicios/detalle_servicio.html",
        {
            "servicio": servicio,
            "fotos": fotos,
            "promedio_range": range(0, promedio_calificaciones),
            "promedio_calificaciones": promedio_calificaciones,
        },
    )


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
