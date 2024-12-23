from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q, Avg
from .models import Evento, TipoEvento
from .forms import CalificacionEventoFormulario


def eventos(request):
    query = request.GET.get("query", "")
    eventos = Evento.objects.prefetch_related("fotos", "calificacion_evento")
    
    if query:
        eventos = eventos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    
    eventos_data = [
        {
            "evento": evento,
            "imagen_url": evento.fotos.first().foto.url if evento.fotos.exists() else None,
            "promedio_calificaciones": range(
                0, int(evento.calificacion_evento.aggregate(Avg("calificacion"))["calificacion__avg"] or 0)
            ),
        }
        for evento in eventos
    ]
    
    return render(request, "eventos/eventos.html", {"eventos": eventos_data})


def tipos_eventos(request):
    tipos_eventos = TipoEvento.objects.all()
    return render(request, "eventos/tipos_eventos.html", {"tipos_eventos": tipos_eventos})


def tipo_evento(request, id):
    tipo_evento = get_object_or_404(TipoEvento, id=id)
    eventos = Evento.objects.filter(tipo_evento=tipo_evento).prefetch_related("fotos", "calificacion_evento")
    
    eventos_data = [
        {
            "evento": evento,
            "imagen_url": evento.fotos.first().foto.url if evento.fotos.exists() else None,
            "promedio_calificaciones": range(
                0, int(evento.calificacion_evento.aggregate(Avg("calificacion"))["calificacion__avg"] or 0)
            ),
        }
        for evento in eventos
    ]

    return render(
        request,
        "eventos/tipo_evento.html",
        {"tipo_evento": tipo_evento, "eventos": eventos_data},
    )


def evento_detalle(request, id):
    evento = get_object_or_404(Evento.objects.prefetch_related("fotos", "calificacion_evento"), id=id)
    
    promedio_calificaciones = evento.calificacion_evento.aggregate(Avg("calificacion"))["calificacion__avg"] or 0

    # Handle form submission
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("usuarios:iniciar_sesion")
        
        formulario = CalificacionEventoFormulario(request.POST)
        if formulario.is_valid():
            calificacion = formulario.save(commit=False)
            calificacion.evento = evento
            calificacion.usuario = request.user
            calificacion.save()
            messages.success(request, "Calificación registrada con éxito.")
            return redirect("eventos:evento_detalle", id=id)
    else:
        formulario = CalificacionEventoFormulario(
            initial={
                "evento": evento.id,
                "usuario": request.user.id if request.user.is_authenticated else None,
            }
        )

    return render(
        request,
        "eventos/detalle_evento.html",
        {
            "evento": evento,
            "promedio_range": range(0, int(promedio_calificaciones)),
            "promedio_calificaciones": round(promedio_calificaciones, 1),
            "fotos": evento.fotos.all(),
            "calificaciones": evento.calificacion_evento.all(),
            "form": formulario,
        },
    )
