from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.db.models import Q

from .models import Evento
from .forms import (
    EventoFormulario,
    CalificacionEventoFormulario,
    FotoEventoFormulario,
)


def eventos(request):
    query = request.GET.get("query", "")
    eventos = Evento.objects.all()
    if query:
        eventos = eventos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    queryset = []
    for evento in eventos:
        primera_foto = evento.fotos.first()
        calificaciones = evento.calificacion_evento.all()
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
                "evento": evento,
                "imagen_url": imagen_url,
                "promedio_calificaciones": range(0, int(promedio_calificaciones)),
            }
        )

    return render(request, "eventos/eventos.html", {"eventos": queryset})


def evento_detalle(request, id):
    evento = Evento.objects.filter(id=id).first()
    if not evento:
        return HttpResponseNotFound("Evento no encontrado")
    fotos = evento.fotos.all()
    calificaciones = evento.calificacion_evento.all()
    promedio_calificaciones = 0
    if calificaciones:
        promedio_calificaciones = sum(
            [calificacion.calificacion for calificacion in calificaciones]
        ) / len(calificaciones)

    return render(
        request,
        "eventos/detalle_evento.html",
        {
            "evento": evento,
            "promedio_range": range(0, int(promedio_calificaciones)),
            "promedio_calificaciones": promedio_calificaciones,
            "fotos": fotos,
        },
    )


def calificaciones_evento(request, id):
    evento = Evento.objects.filter(id=id).first()
    if not evento:
        return HttpResponseNotFound("Evento no encontrado")

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("usuarios:iniciar_sesion")
        formulario = CalificacionEventoFormulario(request.POST)
        if formulario.is_valid():
            calificacion = formulario.save(commit=False)
            calificacion.evento = evento
            calificacion.usuario = request.user
            calificacion.save()
            return redirect("eventos:eventos")
    else:
        formulario = CalificacionEventoFormulario()

        calificaciones = evento.calificacion_evento.all()
        if not calificaciones:
            return HttpResponseNotFound("Este evento no tiene calificaciones")
    return render(
        request,
        "eventos/calificacion_evento.html",
        {
            "evento": evento,
            "calificaciones": calificaciones,
            "form": formulario,
        },
    )
