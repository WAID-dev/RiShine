from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from crear_evento.models import Evento
from usuarios.models import Guardado, Favorito


def index(request):
    """
    Renderiza la vista principal del módulo
    de visualización de eventos
    """
    return render(request, 'ver_evento/visualizar_evento.html')


def detalle_evento(request, id_evento):
    """
    Muestra la información detallada de un evento
    y permite guardarlo o agregarlo a favoritos
    """

    # Obtiene el evento solicitado junto con
    # sus relaciones para optimizar consultas
    evento = get_object_or_404(
        Evento.objects.select_related('categoria', 'promotor__usuario').prefetch_related('horario'),
        id_evento=id_evento
    )
    # Obtiene los horarios asociados al evento
    horarios = evento.horario.all()

    # Procesa la acción de guardar evento
    if request.method == "POST" and request.POST.get('accion') == 'guardar':
        # Verifica que el usuario haya iniciado sesión.
        if not request.user.is_authenticated:
            return redirect(f'/?show_login=1&next=/ver_evento/{id_evento}/')

        # Crea el registro únicamente si no existe
        _, creado = Guardado.objects.get_or_create(usuario=request.user, evento=evento)

        if creado:
            messages.success(request, f'Evento guardado correctamente')
        else:
            messages.error(request, f'Este evento ya esta guardado')
        return redirect('ver_evento:detalle', id_evento=id_evento)

    # Procesa la acción de agregar a favoritos
    if request.method == "POST" and request.POST.get('accion') == 'favorito':
        # Verifica que el usuario haya iniciado sesión
        if not request.user.is_authenticated:
            return redirect(f'/?show_login=1&next=/ver_evento/{id_evento}/')

        # Crea el registro únicamente si no existe
        _, creado = Favorito.objects.get_or_create(usuario=request.user, evento=evento)

        if creado:
            messages.success(request, 'Evento añadido a favoritos')
        else:
            messages.error(request, 'Este evento ya esta en favoritos')
        return redirect('ver_evento:detalle', id_evento=id_evento)

    return render(
        request,
        'ver_evento/visualizar_evento.html',{
            'evento': evento,
            'horarios': horarios
         })






















