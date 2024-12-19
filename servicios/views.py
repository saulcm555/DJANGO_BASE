from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q


from usuarios.decoradores import admin_required
from .models import Servicio
from .forms import (
    ServicioFormulario,
    CalificacionServicioFormulario,
    FotoServicioFormulario,
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


@admin_required
def nuevo_servicio(request):
    if request.method == "POST":
        formulario = ServicioFormulario(request.POST)
        if formulario.is_valid():
            servicio = formulario.save(commit=False)
            servicio.agregado_por = request.user
            servicio.save()
            return redirect("servicios")
    else:
        formulario = ServicioFormulario()
    return render(request, "servicios/nuevo_servicio.html", {"form": formulario})


def servicio_detalle(request, id):
    servicio = Servicio.objects.filter(id=id).first()
    if not servicio:
        return HttpResponseBadRequest("Servicio no encontrado")

    if request.method == "GET":
        return render(
            request, "servicios/detalle_servicio.html", {"servicio": servicio}
        )

    if request.method == "POST":
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        formulario = ServicioFormulario(request.POST, instance=servicio)
        if formulario.is_valid():
            formulario.save()
            return redirect("servicios:servicios")

    if request.method == "DELETE":
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        servicio.delete()

        return redirect("servicios")

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


def fotos_servicio(request, id):
    servicio = Servicio.objects.filter(id=id).first()
    if not servicio:
        return HttpResponseBadRequest("Servicio no encontrado")
    fotos = servicio.fotos_servicio.all()
    if request.method == "POST" and request.user.is_superuser:
        formulario = FotoServicioFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            foto = formulario.save(commit=False)
            foto.servicio = servicio
            foto.save()
            return redirect("servicios")

    else:
        formulario = FotoServicioFormulario() if request.user.is_superuser else None

    return render(
        request,
        "servicios/fotos_servicio.html",
        {
            "servicio": servicio,
            "fotos": fotos,
            "form": formulario,
        },
    )
