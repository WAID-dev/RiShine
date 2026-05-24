from django.shortcuts import render

from crear_evento.models import Evento


def index(request):
    eventos_para_ti = Evento.objects.filter(estatus='publicado').order_by('-id_evento')[:10]
    eventos_gratis = Evento.objects.filter(estatus='publicado', costo=0).order_by('-id_evento')[:10]
    eventos_200 = Evento.objects.filter(estatus='publicado', costo__gt=0, costo__lte=200).order_by('-id_evento')[:10]
    eventos_500 = Evento.objects.filter(estatus='publicado', costo__gt=0, costo__lte=500).order_by('-id_evento')[:10]

    return render(request, 'inicio/inicio.html', {
        'eventos_para_ti': eventos_para_ti,
        'eventos_gratis': eventos_gratis,
        'eventos_200': eventos_200,
        'eventos_500': eventos_500
    })
































