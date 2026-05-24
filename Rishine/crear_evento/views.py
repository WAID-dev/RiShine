from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria, Evento, Horario
from datetime import datetime

@login_required(login_url='/?show_login=1&next=/crear_evento/')
def index(request):
    if not hasattr(request.user, 'promotor'):
        return redirect('/?show_promotor=1&next=/crear_evento/')

    if request.method == 'POST':
        accion = request.POST.get('accion')

        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        referencias = request.POST.get('referencias', '').strip()
        cupo = request.POST.get('cupo', 0)
        costo = request.POST.get('costo', 0)
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        categoria_id = request.POST.get('categoria')
        imagen = request.FILES.get('imagen')

        if not all([titulo, descripcion, direccion, cupo, costo, fecha_inicio, fecha_fin, categoria_id]):
            messages.error(request, 'Todos los campos obligatorios deben estar llenos.')
            categorias = Categoria.objects.all()
            horarios = Horario.objects.all()
            return render(request, 'crear_evento/formulario_crear_evento.html', {
                'categorias': categorias,
                'horarios': horarios,
            })


        fecha_inicio = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d').date()
        if fecha_fin < fecha_inicio:
            messages.error(request, 'La fecha de fin no puede ser menor a la fecha de inicio.')
            categorias = Categoria.objects.all()
            horarios = Horario.objects.all()
            return render(request, 'crear_evento/formulario_crear_evento.html', {
                'categorias': categorias,
                'horarios': horarios,
            })


        evento = Evento.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            direccion=direccion,
            referencias=referencias,
            cupo=cupo,
            costo=costo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            categoria_id=categoria_id,
            promotor=request.user.promotor,
            estatus=accion,
            imagen=imagen,
        )

        horarios_seleccionados = request.POST.getlist('horarios')
        if horarios_seleccionados:
            evento.horario.set(horarios_seleccionados)

        return redirect('inicio:index')

    categorias = Categoria.objects.all()
    horarios = Horario.objects.all()
    return render(request, 'crear_evento/formulario_crear_evento.html', {
        'categorias': categorias,
        'horarios': horarios,
    })