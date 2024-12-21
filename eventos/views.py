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

    return render(request, "eventos/eventos.html", {"eventos": eventos})


def evento_detalle(request, id):
    evento = Evento.objects.filter(id=id).first()
    if not evento:
        return HttpResponseNotFound("Evento no encontrado")

    return render(request, "eventos/detalle_evento.html", {"evento": evento})



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


def fotos_evento(request, id):
    evento = Evento.objects.filter(id=id).first()
    print(evento)
    if not evento:
        return HttpResponseNotFound("Evento no encontrado")
    fotos = evento.fotos.all()

    return render(
        request,
        "eventos/fotos_evento.html",
        {
            "evento": evento,
            "fotos": fotos,
        },
    )
