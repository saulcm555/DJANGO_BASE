from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.http import JsonResponse

from utilidades import ValidadorUsuario
from utilidades.ValidadorAlquiler import ValidadorAlquiler
from utilidades import EmailEnviador
from eventos.models import Evento
from servicios.models import Servicio

from .models import Alquiler, AlquilerServicio
from .forms import (
    AlquilerFormulario,
    AlquilerServicioFormulario,
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

    session_key = f"servicios_seleccionados_{item_id}"
    formServicios = AlquilerServicioFormulario()

    if request.method == "POST":
        print(request.headers)  # Debug headers
        print(request.POST)  # Debug POST data

        # Improved check for AJAX request and POST with add_service
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        is_add_service = "add_service" in request.POST

        print(f"Is AJAX: {is_ajax}, Is Add Service: {is_add_service}")

        if is_ajax and is_add_service:
            print("ES AJAX")
            formServicios = AlquilerServicioFormulario(request.POST)
            if formServicios.is_valid():
                servicio = formServicios.cleaned_data["servicio"]
                cantidad = formServicios.cleaned_data["cantidad"]

                if session_key not in request.session:
                    request.session[session_key] = []

                request.session[session_key].append(
                    {"id": servicio.id, "nombre": servicio.nombre, "cantidad": cantidad}
                )
                request.session.modified = True

                return JsonResponse(
                    {"success": True, "servicios": request.session[session_key]}
                )

            return JsonResponse({"success": False, "errors": formServicios.errors})

        print("NO ES AJAX")
        formulario = AlquilerFormulario(request.POST)
        if formulario.is_valid():
            alquiler = formulario.save(commit=False)
            alquiler.cliente = request.user
            alquiler.evento = evento
            alquiler.save()

            servicios_seleccionados = request.session.pop(session_key, [])
            for servicio_data in servicios_seleccionados:
                servicio = Servicio.objects.get(id=servicio_data["id"])
                AlquilerServicio.objects.create(
                    alquiler=alquiler,
                    servicio=servicio,
                    cantidad=servicio_data["cantidad"],
                )

            EmailEnviador.enviar_codigo_confirmacion(alquiler)
            return redirect("alquileres:alquiler_detalle", id=alquiler.id)

        messages.warning(request, "Error al crear el alquiler")

    else:
        formulario = AlquilerFormulario()

    servicios_seleccionados = request.session.get(session_key, [])

    return render(
        request,
        "alquileres/nuevo_alquiler.html",
        {
            "form": formulario,
            "formServicios": formServicios,
            "servicios_seleccionados": servicios_seleccionados,
        },
    )


def alquiler_detalle(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")

    if request.method == "GET":
        fotos = alquiler.fotos.all()
        formulario = ConfirmarAlquilerFormulario(alquiler=alquiler)
        servicios_seleccionados = alquiler.servicios_reserva.all()
        evento = alquiler.evento
        return render(
            request,
            "alquileres/detalle_alquiler.html",
            {
                "alquiler": alquiler,
                "fotos": fotos,
                "formulario": formulario,
                "servicios_seleccionados": servicios_seleccionados,
                "evento": evento,
            },
        )


def enviar_correo_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")
    EmailEnviador.enviar_codigo_confirmacion(alquiler)
    return JsonResponse({"success": True, "message": "Correo enviado correctamente."})


def confirmar_alquiler(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()

    if not alquiler:
        return JsonResponse({"success": False, "message": "Alquiler no encontrado."})

    if request.method == "POST":
        formulario = ConfirmarAlquilerFormulario(request.POST, alquiler=alquiler)

        if formulario.is_valid():
            formulario.save()
            return JsonResponse(
                {"success": True, "message": "Alquiler confirmado correctamente."}
            )
        else:
            return JsonResponse({"success": False, "errors": formulario.errors})

    else:
        formulario = ConfirmarAlquilerFormulario(alquiler=alquiler)

    return render(
        request,
        "confirmar_alquiler.html",
        {"formulario": formulario, "alquiler": alquiler},
    )
