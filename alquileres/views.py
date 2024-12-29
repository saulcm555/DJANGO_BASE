from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
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
            imagen_url = alquiler.evento.fotos.first().foto.url
        queryset.append(
            {
                "alquiler": alquiler,
                "imagen_url": imagen_url,
            }
        )

    return render(request, "alquileres/alquileres.html", {"alquileres": queryset})


def nuevo_alquiler(request, item_id):
    """Vista principal para crear un nuevo alquiler"""
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para alquilar un espacio")
        return redirect("usuarios:iniciar_sesion")

    if not ValidadorUsuario.validar_correo_verificado_y_datos_completos(request.user):
        messages.warning(
            request,
            "Debes verificar tu correo y completar tus datos antes de poder alquilar un espacio",
        )
        return redirect("usuarios:perfil")

    # Obtener evento
    evento = get_object_or_404(Evento, id=item_id)
    session_key = f"servicios_seleccionados_{item_id}"

    if request.method == "POST":
        # Determinar si es una petición AJAX para servicios
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            if request.POST.get("agregar_servicio"):
                return agregar_servicio(request, session_key)
            elif request.POST.get("eliminar_servicio"):
                return eliminar_servicio(request, session_key)

        print(request)
        return procesar_alquiler(request, evento, session_key)

    # GET request - mostrar formulario
    context = {
        "form": AlquilerFormulario(),
        "formServicios": AlquilerServicioFormulario(),
        "servicios_seleccionados": request.session.get(session_key, []),
    }
    return render(request, "alquileres/nuevo_alquiler.html", context)


def procesar_alquiler(request, evento, session_key):
    """Procesar la creación del alquiler con sus servicios"""
    formulario = AlquilerFormulario(request.POST)
    print(request.POST)
    if not formulario.is_valid():
        messages.error(request, "Por favor corrija los errores en el formulario")
        return render(
            request,
            "alquileres/nuevo_alquiler.html",
            {
                "form": formulario,
                "formServicios": AlquilerServicioFormulario(),
                "servicios_seleccionados": request.session.get(session_key, []),
            },
        )

    try:
        with transaction.atomic():
            # Crear alquiler
            alquiler = formulario.save(commit=False)
            alquiler.cliente = request.user
            alquiler.evento = evento
            alquiler.save()
            for promocion in request.POST.getlist("promociones"):
                alquiler.promociones.add(promocion)

            # Agregar servicios seleccionados
            servicios_seleccionados = request.session.get(session_key, [])
            for servicio_data in servicios_seleccionados:
                servicio = get_object_or_404(Servicio, id=servicio_data["id"])
                AlquilerServicio.objects.create(
                    alquiler=alquiler,
                    servicio=servicio,
                    cantidad=servicio_data["cantidad"],
                )

            # Limpiar sesión y enviar correo
            request.session.pop(session_key, None)
            EmailEnviador.enviar_codigo_confirmacion(alquiler)

            messages.success(request, "Alquiler creado exitosamente")
            return redirect("alquileres:alquiler_detalle", id=alquiler.id)

    except Exception as e:
        messages.error(request, f"Error al crear el alquiler: {str(e)}")
        return redirect("alquileres:nuevo_alquiler", item_id=evento.id)


def agregar_servicio(request, session_key):
    """Procesar la adición de servicios vía AJAX"""
    form = AlquilerServicioFormulario(request.POST)
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": form.errors})

    servicio = form.cleaned_data["servicio"]
    cantidad = form.cleaned_data["cantidad"]

    # Obtener o inicializar lista de servicios
    servicios = request.session.get(session_key, [])

    # Verificar si el servicio ya existe
    if any(s["id"] == servicio.id for s in servicios):
        return JsonResponse(
            {
                "success": False,
                "errors": {"servicio": ["Este servicio ya ha sido agregado"]},
            }
        )

    # Agregar nuevo servicio
    servicios.append(
        {"id": servicio.id, "nombre": servicio.nombre, "cantidad": cantidad}
    )

    request.session[session_key] = servicios
    request.session.modified = True

    return JsonResponse({"success": True, "servicios": servicios})


def eliminar_servicio(request, session_key):
    """Procesar la eliminación de un servicio vía AJAX"""
    servicio_id = request.POST.get("servicio_id")

    if not servicio_id:
        return JsonResponse(
            {
                "success": False,
                "errors": {"servicio": ["ID de servicio no proporcionado"]},
            }
        )

    servicios = request.session.get(session_key, [])
    servicios = [s for s in servicios if s["id"] != int(servicio_id)]

    request.session[session_key] = servicios
    request.session.modified = True

    return JsonResponse({"success": True, "servicios": servicios})


def alquiler_detalle(request, id):
    alquiler = Alquiler.objects.filter(id=id).first()
    if not alquiler:
        messages.warning(request, "Alquiler no encontrado")
        return redirect("alquileres:alquileres")

    if request.method == "GET":
        fotos = alquiler.fotos.all()
        if not fotos:
            fotos = alquiler.evento.fotos.all()
        formulario = ConfirmarAlquilerFormulario(alquiler=alquiler)
        servicios_seleccionados = alquiler.servicios_reserva.select_related(
            "servicio"
        ).all()  # Optimized query
        foto_servicios = [
            (
                servicio.servicio.fotos.first().foto.url
                if servicio.servicio.fotos.exists()
                else None
            )
            for servicio in servicios_seleccionados
        ]
        evento = alquiler.evento
        servicios_with_fotos = zip(servicios_seleccionados, foto_servicios)
        promociones = alquiler.promociones.all()
        return render(
            request,
            "alquileres/detalle_alquiler.html",
            {
                "alquiler": alquiler,
                "fotos": fotos,
                "formulario": formulario,
                "servicios_with_fotos": servicios_with_fotos,  
                "promociones": promociones,
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
