from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q

from usuarios.decoradores import admin_required
from .models import Alquiler
from .forms import (
    AlquilerFormulario,
    AlquilerServicioFormulario,
    CalificacionAlquilerFormulario,
    ConfirmarAlquilerFormulario,
)


def alquileres(request):
    query = request.GET.get("query", "")
    if not request.user.is_superuser:
        alquileres = Alquiler.objects.filter(cliente=request.user)
    else:
        alquileres = Alquiler.objects.filter()
    if query:
        alquileres = alquileres.filter(
            Q(cliente__username__icontains=query)
            | Q(evento__nombre__icontains=query)
            | Q(observacion__icontains=query)
        )

    queryset = []
    for alquiler in alquileres:
        primera_foto = alquiler.fotos.first()


        if primera_foto:
            imagen_url = primera_foto.foto.url
        else:
            imagen_url = None
        queryset.append(
            {
                "alquiler": alquiler,
                "imagen_url": imagen_url,
            }
        )

    return render(request, "alquileres/alquileres.html", {"alquileres": queryset})


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
        fotos = alquiler.fotos.all()

        return render(
            request,
            "alquileres/detalle_alquiler.html",
            {"alquiler": alquiler, "fotos": fotos},
        )

    return HttpResponseForbidden("Método no permitido")


def calificaciones_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    calificaciones = alquiler.calificacion_alquiler.all()
    if request.method == "POST":
        if not alquiler.cliente == request.user or not request.user.is_superuser:
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


def eventualidades_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    eventualidades = alquiler.eventualidades.all()

    return render(
        request,
        "alquileres/eventualidades_alquiler.html",
        {
            "alquiler": alquiler,
            "eventualidades": eventualidades,
        },
    )


def servicios_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    servicios = alquiler.servicios.all()
    if request.method == "POST":
        if not request.user.is_superuser or not alquiler.cliente == request.user:
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


def confirmar_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        return HttpResponseBadRequest("Alquiler no encontrado")
    if request.method == "POST":
        formulario = ConfirmarAlquilerFormulario(request.POST, alquiler=alquiler)
        if formulario.is_valid():
            formulario.save()
            return redirect("alquileres:alquileres")
    else:
        formulario = ConfirmarAlquilerFormulario(alquiler=alquiler)

    return render(
        request,
        "alquileres/confirmar_alquiler.html",
        {
            "alquiler": alquiler,
            "form": formulario,
        },
    )
