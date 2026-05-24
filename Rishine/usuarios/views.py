from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'usuarios/index.html')

@login_required(login_url='/?show_login=1&next=/usuarios/perfil/')
def perfil(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        correo = request.POST.get('correo', '').strip()

        if correo:
            try:
                validate_email(correo)
            except ValidationError:
                messages.error(request, 'El correo no tiene un formato valido.')
                return redirect('usuarios:perfil')

        request.user.first_name = nombre
        request.user.last_name = apellido
        request.user.email = correo
        request.user.save(update_fields=['first_name', 'last_name', 'email'])

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('usuarios:perfil')

    return render(request, 'usuarios/perfil.html')


@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Tu cuenta ha sido eliminada.')
        return redirect('/')
    return redirect('usuarios:perfil')