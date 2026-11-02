from django.shortcuts import render
from .models import Evento, Categoria

def crear_evento(request):

    if request.method == 'POST':
        # accion = request.POST.get('accion')
        imagen_evento = request.FILES.get('imagen', None)
        nombre_evento = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        cupo = request.POST.get('cupo')
        costo = request.POST.get('costo')
        modo = request.POST.get('modo')
        direccion = request.POST.get('direccion')
        referencias = request.POST.get('referencias')
        url_evento = request.POST.get('url_evento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        contacto = request.POST.get('contacto')

        evento = Evento.objects.create(
            imagen=imagen_evento,
            nombre_evento=nombre_evento,
            categoria_id=categoria,
            descripcion=descripcion,
            cupo=cupo,
            costo=costo,
            modo=modo,
            direccion=direccion,
            referencias=referencias,
            url_evento=url_evento,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            contacto=contacto,
            promotor=request.user.promotor
        )
        evento.save()

        # Muestra las categorias disponibles
    categorias = Categoria.objects.all()

    return render(request, 'crear_evento/crear_evento.html', {
        'categorias': categorias})
