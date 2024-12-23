from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q


from usuarios.decoradores import admin_required
from .models import Servicio, FotoServicio, CalificacionServicio
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
            | Q(descripcion__icontains=query)
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
    print(type(servicio))
    if not servicio:
        messages.warning(request, "Servicio no encontrado")
        return redirect("servicios:servicios")
    calificaciones = servicio.calificacion_servicio.all()
    promedio_calificaciones = 0

    if calificaciones:
        promedio_calificaciones = sum(
            [calificacion.calificacion for calificacion in calificaciones]
        ) / len(calificaciones)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("usuarios:iniciar_sesion")
        formulario = CalificacionServicioFormulario(request.POST)
        if formulario.is_valid():

            if servicio.calificaciones_servicio.filter(usuario=request.user).exists():
                messages.warning(request, "Ya has calificado este servicio")
                return redirect("servicios:servicio_detalle", id=id)

            calificacion = formulario.save(commit=False)
            calificacion.servicio = servicio
            calificacion.usuario = request.user
            calificacion.save()
            messages.success(request, "Calificación registrada")
            return redirect("servicios:servicio_detalle", id=id)
        else:
            messages.error(request, "Error al registrar la calificación")
    else:
        formulario = CalificacionServicioFormulario(
            initial={
                "servicio": servicio,
                "usuario": request.user if request.user.is_authenticated else None,
            }
        )

    fotos = servicio.fotos.all()
    return render(
        request,
        "servicios/detalle_servicio.html",
        {
            "servicio": servicio,
            "fotos": fotos,
            "promedio_range": range(0, int(promedio_calificaciones)),
            "promedio_calificaciones": round(promedio_calificaciones, 1),
            "calificaciones": calificaciones,
            "form": formulario,
        },
    )
