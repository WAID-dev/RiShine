from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from crear_evento.models import Evento
from usuarios.models import Guardado, Favorito


def index(request):
    return render(request, 'ver_evento/visualizar_evento.html')


def detalle_evento(request, id_evento):
    evento = get_object_or_404(
        Evento.objects.select_related('categoria', 'promotor__usuario').prefetch_related('horario'),
        id_evento=id_evento
    )
    horarios = evento.horario.all()


    if request.method == "POST" and request.POST.get('accion') == 'guardar':
        if not request.user.is_authenticated:
            return redirect(f'/?show_login=1&next=/ver_evento/{id_evento}/')

        _, creado = Guardado.objects.get_or_create(usuario=request.user, evento=evento)

        if creado:
            messages.success(request, f'Evento guardado correctamente')
        else:
            messages.error(request, f'Este evento ya esta guardado')
        return redirect('ver_evento:detalle', id_evento=id_evento)

    if request.method == "POST" and request.POST.get('accion') == 'favorito':
        if not request.user.is_authenticated:
            return redirect(f'/?show_login=1&next=/ver_evento/{id_evento}/')

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






















