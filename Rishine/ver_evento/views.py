from django.shortcuts import get_object_or_404, render

from crear_evento.models import Evento


def index(request):
    return render(request, 'ver_evento/visualizar_evento.html')


def detalle_evento(request, id_evento):
    evento = get_object_or_404(Evento.objects.select_related('categoria', 'promotor__usuario'), id_evento=id_evento)
    return render(request, 'ver_evento/visualizar_evento.html', {'evento': evento})
