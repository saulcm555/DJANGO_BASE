from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



from .forms import (
    CrearCuentaFormulario,
    IniciarSesionFormulario,
    ValidarCorreoFormulario,
    CompletarPerfilFormulario,
)

from .models import PerfilUsuario
from .decoradores import admin_required
from utilidades import ValidadorUsuario


@admin_required
def usuarios(request):
    perfiles = PerfilUsuario.objects.all()
    return render(request, "usuarios/usuarios.html", {"perfiles": perfiles})


def crear_cuenta(request):
    if request.user.is_authenticated:
        return redirect("usuarios:perfil")
    if request.method == "POST":
        form = CrearCuentaFormulario(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("usuarios:validar_correo")

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

            if not ValidadorUsuario.validar_correo_verificado(usuario):
                return redirect("usuarios:validar_correo")

            return redirect("core:home")
    else:
        form = IniciarSesionFormulario()
    return render(request, "usuarios/iniciar_sesion.html", {"form": form})


@login_required
def cerrar_sesion(request):
    # if request.method == "POST":
    if request.method == "GET":  # Cambiar cuando este listo
        logout(request)
        return redirect("usuarios:iniciar_sesion")


@login_required
def validar_correo(request):
    usuario = request.user
    if ValidadorUsuario.validar_correo_verificado(usuario):
        return redirect("usuarios:perfil")
    if request.method == "POST":

        form = ValidarCorreoFormulario(data=request.POST)
        form.user = usuario
        if form.is_valid():
            form.save()
            return redirect("usuarios:perfil")
    else:
        form = ValidarCorreoFormulario()

    return render(request, "usuarios/validar_correo.html", {"form": form})


@login_required
def perfil(request):
    usuario = request.user
    perfil = PerfilUsuario.objects.get(usuario=usuario)
    if request.method == "POST":
        formulario = CompletarPerfilFormulario(request.POST, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Perfil actualizado correctamente")
            
    else:
        formulario = CompletarPerfilFormulario(instance=perfil)
    
    return render(request, "usuarios/perfil.html", {"usuario": perfil, "form": formulario})


@login_required
def completar_perfil(request):
    usuario = request.user
    if ValidadorUsuario.validar_perfil_completo(usuario):
        return redirect("usuarios:perfil")
    if not ValidadorUsuario.validar_correo_verificado(usuario):
        return redirect("usuarios:validar_correo")
    perfil = PerfilUsuario.objects.get(usuario=usuario)
    if request.method == "POST":
        form = CompletarPerfilFormulario(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("usuarios:perfil")
    else:
        form = CompletarPerfilFormulario(instance=perfil)
    return render(request, "usuarios/completar_perfil.html", {"form": form})


