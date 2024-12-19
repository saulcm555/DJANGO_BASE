from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q

from usuarios.decoradores import admin_required
from .models import Alquiler
from .forms import (
    AlquilerFormulario,
    AlquilerServicioFormulario,
    CalificacionAlquilerFormulario,
    FotoAlquilerFormulario,
    EventualidadFormulario
)


def alquileres(request):
    query = request.GET.get("query", "")
    alquileres = Alquiler.objects.filter(vigencia=True)
    if query:
        alquileres = alquileres.filter(
            Q(cliente__username__icontains=query)
            | Q(evento__nombre__icontains=query)
            | Q(observacion__icontains=query)
        )

    return render(request, "alquileres/alquileres.html", {"alquileres": alquileres})


@admin_required
def nuevo_alquiler(request):
    if request.method == "POST":
        formulario = AlquilerFormulario(request.POST)
        if formulario.is_valid():
            alquiler = formulario.save(commit=False)
            alquiler.agregado_por = request.user
            alquiler.save()
            return redirect("alquileres")
    else:
        formulario = AlquilerFormulario()
    return render(request, "alquileres/nuevo_alquiler.html", {"form": formulario})


def alquiler_detalle(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")

    if request.method == "GET":
        return render(
            request, "alquileres/detalle_alquiler.html", {"alquiler": alquiler}
        )

    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        formulario = AlquilerFormulario(request.POST, instance=alquiler)
        if formulario.is_valid():
            formulario.save()
            return redirect("alquileres:alquileres")

    if request.method == "DELETE":
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        alquiler.delete()

        return redirect("alquileres")

    return HttpResponseForbidden("Método no permitido")


def calificaciones_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    calificaciones = alquiler.calificacion_alquiler.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("usuarios:iniciar_sesion")
        formulario = CalificacionAlquilerFormulario(request.POST)
        if formulario.is_valid():
            calificacion = formulario.save(commit=False)
            calificacion.alquiler = alquiler
            calificacion.usuario = request.user
            calificacion.save()
            return redirect("alquileres:alquileres")
    else:
        formulario = CalificacionAlquilerFormulario()

    return render(
        request,
        "alquileres/calificacion_alquiler.html",
        {
            "alquiler": alquiler,
            "calificaciones": calificaciones,
            "form": formulario,
        },
    )


def fotos_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    fotos = alquiler.fotos_alquiler.all()
    if request.method == "POST" and request.user.is_superuser:
        formulario = FotoAlquilerFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            foto = formulario.save(commit=False)
            foto.alquiler = alquiler
            foto.save()
            return redirect("alquileres")

    else:
        formulario = FotoAlquilerFormulario() if request.user.is_superuser else None

    return render(
        request,
        "alquileres/fotos_alquiler.html",
        {
            "alquiler": alquiler,
            "fotos": fotos,
            "form": formulario,
        },
    )

def eventualidades_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    eventualidades = alquiler.eventualidades.all()
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        formulario = EventualidadFormulario(request.POST)
        if formulario.is_valid():
            eventualidad = formulario.save()
            alquiler.eventualidades.add(eventualidad)
            return redirect("alquileres:alquileres")
    else:
        formulario = EventualidadFormulario()

    return render(
        request,
        "alquileres/eventualidades_alquiler.html",
        {
            "alquiler": alquiler,
            "eventualidades": eventualidades,
            "form": formulario,
        },
    )


def servicios_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    servicios = alquiler.servicios.all()
    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        formulario = AlquilerServicioFormulario(request.POST)
        if formulario.is_valid():
            servicio = formulario.save()
            alquiler.servicios.add(servicio)
            return redirect("alquileres:alquileres")
    else:
        formulario = AlquilerServicioFormulario()

    return render(
        request,
        "alquileres/servicios_alquiler.html",
        {
            "alquiler": alquiler,
            "servicios": servicios,
            "form": formulario,
        },
    )