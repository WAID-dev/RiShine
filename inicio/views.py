from django.shortcuts import render
from crear_evento.models import Evento, ESTATUS_PUBLICADO

# Create your views here.
def inicio(request):
    publicados=(
        Evento.objects
        .filter(estatus=ESTATUS_PUBLICADO)
        .select_related('categoria')
        .order_by('fecha_inicio')
    )

    contexto = {
        'eventos_para_ti': publicados[:10],
        'eventos_500': publicados.filter(costo__lt=500)[:10],
        'eventos_200': publicados.filter(costo__lt=200)[:10],
    }
    return render(request, 'inicio/inicio.html', contexto)