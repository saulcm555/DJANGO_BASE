from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utilidades import EmailEnviador
from django.http import JsonResponse

from .forms import (
    CrearCuentaFormulario,
    IniciarSesionFormulario,
    ValidarCorreoFormulario,
    CompletarPerfilFormulario,
)

from .models import PerfilUsuario
from utilidades import ValidadorUsuario


def crear_cuenta(request):
    if request.user.is_authenticated:
        return redirect("usuarios:perfil")
    if request.method == "POST":
        form = CrearCuentaFormulario(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Cuenta creada correctamente")
            messages.info(request, "Por favor, verifica tu correo electrónico")
            return redirect("usuarios:perfil")

    else:
        form = CrearCuentaFormulario()
    return render(request, "usuarios/crear_cuenta.html", {"form": form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("usuarios:perfil")
    if request.method == "POST":

        form = IniciarSesionFormulario(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)

            return redirect("core:home")
    else:
        form = IniciarSesionFormulario()
    return render(request, "usuarios/iniciar_sesion.html", {"form": form})


@login_required
def cerrar_sesion(request):
    if request.method == "GET":
        logout(request)
        return redirect("usuarios:iniciar_sesion")


@login_required
def validar_correo(request):
    try:
        usuario = request.user
        if ValidadorUsuario.validar_correo_verificado(usuario):
            return redirect("usuarios:perfil")
        
        if request.method == "POST":
            form = ValidarCorreoFormulario(data=request.POST)
            form.user = usuario
            if form.is_valid():
                form.save()
                return JsonResponse({"success": True, "message": "Correo verificado correctamente."})
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        else:
            return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)
    except Exception as e:
        # Imprime el error en los logs para depurar
        print(f"Error en validar_correo: {str(e)}")
        return JsonResponse({"success": False, "message": "Error interno del servidor."}, status=500)


@login_required
def perfil(request):
    usuario = request.user
    perfil = PerfilUsuario.objects.get_or_create(usuario=usuario)[0]

    formulario_validar_correo = ValidarCorreoFormulario()

    if request.method == "POST":
        formulario = CompletarPerfilFormulario(request.POST, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Perfil actualizado correctamente")
    else:
        formulario = CompletarPerfilFormulario(instance=perfil)

    return render(
        request,
        "usuarios/perfil.html",
        {
            "usuario": perfil,
            "form": formulario,
            "form_validar_correo": formulario_validar_correo,
        },
    )


@login_required
def reenvio_correo_validacion(request):

    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)

    perfil_usuario.generar_codigo_verificacion()
    perfil_usuario.save()

    EmailEnviador.enviar_codigo_validar_email(perfil_usuario)

    return JsonResponse(
        {"success": True, "message": "Correo de validación enviado nuevamente."}
    )




@login_required
def validar_correo(request):
    usuario = request.user
    if ValidadorUsuario.validar_correo_verificado(usuario):
        messages.info(request, "Correo ya verificado")
        return redirect("usuarios:perfil")

    if request.method == "POST":
        print(request.POST)
        form = ValidarCorreoFormulario(data=request.POST)
        form.user = usuario
        if form.is_valid():
            form.save()
            messages.success(request, "Correo verificado correctamente")
            return redirect("usuarios:perfil")
        messages.error(request, "Código de verificación incorrecto")
    else:
        form = ValidarCorreoFormulario()

    return render(request, "usuarios/validar_correo.html", {"form": form})
