from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.db.models import Q

from .models import Evento, TipoEvento
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


def tipos_eventos(request):
    tipos_eventos = TipoEvento.objects.all()
    return render(
        request, "eventos/tipos_eventos.html", {"tipos_eventos": tipos_eventos}
    )


def tipo_evento(request, id):
    tipo_evento = TipoEvento.objects.filter(id=id).first()
    if not tipo_evento:
        return HttpResponseNotFound("Tipo de evento no encontrado")
    eventos = tipo_evento.eventos.all()[:5]

    return render(
        request,
        "eventos/tipo_evento.html",
        {"tipo_evento": tipo_evento, "eventos": eventos},
    )


def evento_detalle(request, id):
    evento = Evento.objects.filter(id=id).first()
    if not evento:
        messages.warning(request, "Evento no encontrado")
        return redirect("eventos:eventos")
    
    calificaciones = evento.calificacion_evento.all()
    promedio_calificaciones = 0
    if calificaciones:
        promedio_calificaciones = sum(
            [calificacion.calificacion for calificacion in calificaciones]
        ) / len(calificaciones)

    # Manejar el formulario de calificaciones
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("usuarios:iniciar_sesion")
        formulario = CalificacionEventoFormulario(request.POST)
        if formulario.is_valid():
            calificacion = formulario.save(commit=False)
            calificacion.evento = evento
            calificacion.usuario = request.user
            calificacion.save()
            return redirect("eventos:evento_detalle", id=id)
    else:
        formulario = CalificacionEventoFormulario(
            initial={
                'evento': evento.id,
                'usuario': request.user.id if request.user.is_authenticated else None,
            }
        )

    fotos = evento.fotos.all()

    return render(
        request,
        "eventos/detalle_evento.html",
        {
            "evento": evento,
            "promedio_range": range(0, int(promedio_calificaciones)),
            "promedio_calificaciones": round(promedio_calificaciones,1  ),
            "fotos": fotos,
            "calificaciones": calificaciones,
            "form": formulario,
        },
    )
