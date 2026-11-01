from django.shortcuts import get_object_or_404, render
from crear_evento.models import Evento

def ver_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    return render(request, 'ver_evento/ver_evento.html', {
        'evento': evento
    })
