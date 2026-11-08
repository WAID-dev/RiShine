from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import (Categoria, Evento, ESTATUS_BORRADOR, ESTATUS_PUBLICADO)


@login_required
def crear_evento(request):
    if not hasattr(request.user, 'promotor'):
        messages.error(request, 'Necesitas una cuenta de promotor para crear eventos.')
        return redirect('cuentas:registro_promotor')

    if request.method == 'POST':
        p = request.POST
        estatus = ESTATUS_PUBLICADO if p.get('accion') == 'publicado' else ESTATUS_BORRADOR
        modo = p.get('modo', 'presencial')
        fecha_inicio = p.get('fecha_inicio', '')

        if p.get('tipo_evento') == 'un_dia':
            fecha_fin = fecha_inicio
        else:
            fecha_fin = p.get('fecha_fin', '')

        direccion = p.get('direccion', '').strip()
        url_evento = p.get('url_evento', '').strip()

        error = None
        if not fecha_inicio or not fecha_fin:
            error = 'Indica las fechas del evento.'
        elif fecha_fin < fecha_inicio:
            error = 'La fecha de fin no puede ser anterior a la de inicio.'
        elif modo in ('presencial', 'hibrido') and not direccion:
            error = 'Escribe la dirección del evento.'
        elif modo in ('virtual', 'hibrido') and not url_evento:
            error = 'Escribe la URL del evento.'

        if error:
            messages.error(request, error)
        else:
            Evento.objects.create(
                estatus=estatus,
                imagen=request.FILES.get('imagen'),
                nombre_evento=p.get('titulo', '').strip(),
                categoria_id=p.get('categoria'),
                descripcion=p.get('descripcion', '').strip(),
                cupo=p.get('cupo') or 0,
                costo=p.get('costo') or 0,
                modo=modo,
                direccion=direccion,
                referencias=p.get('referencias', '').strip(),
                url_evento=url_evento,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                contacto=p.get('contacto', '').strip(),
                promotor=request.user.promotor,
            )
            if estatus == ESTATUS_PUBLICADO:
                messages.success(request, 'Tu evento fue publicado.')
            else:
                messages.success(request, 'Tu borrador quedó guardado.')
            return redirect('inicio:inicio')

    return render(request, 'crear_evento/crear_evento.html', {
        'categorias': Categoria.objects.all(),
    })