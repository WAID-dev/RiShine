from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Favorito, Guardado


@login_required(login_url='/?show_login=1&next=/usuarios/perfil/')
def perfil(request):
    """
    Permite al usuario autenticado visualizar y actualizar
    la información básica de su perfil.
    """
    if request.method == 'POST':
        # Obtiene y limpia los datos enviados desde el formulario
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip()

        if correo:
            try:
                validate_email(correo)
            except ValidationError:
                messages.error(request, 'El correo no tiene un formato valido.')
                return redirect('usuarios:perfil')

        # Actualiza la información del usuario autenticado
        request.user.first_name = nombre
        request.user.last_name = apellido
        request.user.email = correo
        request.user.save(update_fields=['first_name', 'last_name', 'email'])

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('usuarios:perfil')

    return render(request, 'usuarios/perfil.html')


@login_required(login_url='/?show_login=1')
def eliminar_cuenta(request):
    """
    Permite eliminar la cuenta del usuario autenticado
    junto con la información relacionada
    """
    if request.method == 'POST':
        user = request.user

        # Cierra la sesión antes de eliminar la cuenta
        logout(request)

        # Si es promotor, borra primero
        # los eventos asociados para evitar errores
        # de integridad referencial
        if hasattr(user, 'promotor'):
            user.promotor.evento_promotor.all().delete()
            user.promotor.delete()

        #Elimina la cuenta del usuario
        user.delete()

        messages.success(request, 'Tu cuenta ha sido eliminada.')
        return redirect('/')
    return redirect('usuarios:perfil')

@login_required(login_url='/?show_login=1')
def favoritos(request):
    """
    Permite visualizar y eliminar eventos marcados
    como favoritos por el usuario
    """
    if request.method == 'POST':
        id_favorito = request.POST.get('id_favorito')

        # Elimina el registro seleccionado de favoritos
        Favorito.objects.filter(id_favorito=id_favorito).delete()

        return redirect('usuarios:favoritos')

    # Obtiene favoritos junto con información relacionada
    # del evento y promotor para optimizar consultas
    favoritos = Favorito.objects.select_related(
        'evento','evento__promotor'
    ).filter(usuario=request.user)
    return render(request, 'usuarios/ver_favoritos.html', {
        'favoritos': favoritos
    })


@login_required(login_url='/?show_login=1')
def guardados(request):
    """
    Permite visualizar y eliminar eventos guardados
    por el usuario.
    """
    if request.method == 'POST':
        id_guardado = request.POST.get('id_guardado')

        # Elimina el evento guardado seleccionado
        Guardado.objects.filter(id_guardado=id_guardado).delete()
        return redirect('usuarios:guardados')

    # Obtiene los eventos guardados junto con sus relaciones
    guardados = Guardado.objects.select_related(
        'evento','evento__promotor'
    ).filter(usuario=request.user)

    return render(request, 'usuarios/guardados.html', {
        'guardados': guardados
    })







