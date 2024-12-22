from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.http import JsonResponse

from utilidades import ValidadorUsuario
from utilidades.ValidadorAlquiler import ValidadorAlquiler
from utilidades.enviar_email import EmailEnviador, enviar_codigo_confirmacion
from eventos.models import Evento
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


def nuevo_alquiler(request, item_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para alquilar un espacio")
        return redirect("usuarios:iniciar_sesion")
    if not ValidadorUsuario.validar_correo_verificado_y_datos_completos(request.user):
        messages.warning(
            request,
            "Debes verificar tu correo y completar tus datos antes de poder alquilar un espacio",
        )
        return redirect("usuarios:perfil")

    evento = Evento.objects.filter(id=item_id).first()
    if not evento:
        messages.warning(request, "Evento no encontrado")
        return redirect("eventos:eventos")

    if request.method == "POST":
        formulario = AlquilerFormulario(request.POST)
        if formulario.is_valid():
            alquiler = formulario.save(commit=False)
            alquiler.cliente = request.user
            alquiler.evento = evento

            alquiler.costo_alquiler = evento.valor_referencial
            
            alquiler.save()
            enviar_codigo_confirmacion(alquiler)
            return redirect("alquileres:alquiler_detalle", id=alquiler.id)
        messages.warning(request, "Error al crear el alquiler")
    else:
        formulario = AlquilerFormulario()

    return render(request, "alquileres/nuevo_alquiler.html", {"form": formulario})


def alquiler_detalle(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")

    if request.method == "GET":
        fotos = alquiler.fotos.all()
        formulario = ConfirmarAlquilerFormulario(alquiler=alquiler)  # Usa 'instance' aquí
        return render(
            request,
            "alquileres/detalle_alquiler.html",
            {"alquiler": alquiler, "fotos": fotos, "formulario": formulario},
        )


def calificaciones_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")

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
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")
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
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")
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


def enviar_correo_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")
    enviar_correo_alquiler = enviar_codigo_confirmacion(alquiler)
    return JsonResponse({"success": True, "message": "Correo enviado correctamente."})



def confirmar_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()

    if not alquiler:
        return JsonResponse({"success": False, "message": "Alquiler no encontrado."})

    if request.method == "POST":
        formulario = ConfirmarAlquilerFormulario(request.POST, alquiler=alquiler)

        if formulario.is_valid():
            formulario.save()
            return JsonResponse({"success": True, "message": "Alquiler confirmado correctamente."})
        else:
            return JsonResponse({"success": False, "errors": formulario.errors})

    else:
        formulario = ConfirmarAlquilerFormulario(alquiler=alquiler)

    return render(request, 'confirmar_alquiler.html', {'formulario': formulario, 'alquiler': alquiler})
