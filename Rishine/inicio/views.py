from django.shortcuts import render

from crear_evento.models import Evento


def index(request):
    eventos = Evento.objects.select_related('categoria').order_by('-id_evento')[:20]
    return render(request, 'inicio/inicio.html', {'eventos': eventos})
