from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.db.models import Q

from usuarios.decoradores import admin_required
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


@admin_required
def nuevo_evento(request):
    if request.method == "POST":
        formulario = EventoFormulario(request.POST)
        if formulario.is_valid():
            evento = formulario.save(commit=False)
            evento.save()
            return redirect("eventos")
    else:
        print("GET")
        formulario = EventoFormulario()
    return render(request, "eventos/nuevo_evento.html", {"form": formulario})


def evento_detalle(request, id):
    evento = Evento.objects.filter(id=id).first()
    if not evento:
        return HttpResponseNotFound("Evento no encontrado")

    if request.method == "GET":
        return render(request, "eventos/detalle_evento.html", {"evento": evento})

    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        formulario = EventoFormulario(request.POST, instance=evento)
        if formulario.is_valid():
            formulario.save()
            return redirect("eventos:eventos")

    if request.method == "DELETE":
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        evento.delete()
        return redirect("eventos")

    return HttpResponseForbidden("Método no permitido")


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
    if not evento:
        return HttpResponseNotFound("Evento no encontrado")
    fotos = evento.fotos.all()
    if request.method == "POST" and request.user.is_superuser:
        formulario = FotoEventoFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            foto = formulario.save(commit=False)
            foto.evento = evento
            foto.save()
            return redirect("eventos")

    else:
        formulario = FotoEventoFormulario() if request.user.is_superuser else None

    return render(
        request,
        "eventos/fotos_evento.html",
        {
            "evento": evento,
            "fotos": fotos,
            "form": formulario,
        },
    )
