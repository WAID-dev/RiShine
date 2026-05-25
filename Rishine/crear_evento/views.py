from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria, Evento, Horario
from datetime import datetime

@login_required(login_url='/?show_login=1&next=/crear_evento/')
def index(request):
    """
    Permite a los usuarios con rol de promotor
    registrar nuevos eventos dentro de la plataforma
    """

    # Verifica que el usuario autenticado tenga permisos de promotor
    if not hasattr(request.user, 'promotor'):
        return redirect('/?show_promotor=1&next=/crear_evento/')

    if request.method == 'POST':
        # Obtiene la acción seleccionada (borrador o publicado).
        accion = request.POST.get('accion')

        # Obtiene y limpia los datos enviados desde el formulario
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

        # Verifica que todos los campos obligatorios contengan información
        if not all([titulo, descripcion, direccion, cupo, costo, fecha_inicio, fecha_fin, categoria_id]):
            messages.error(request, 'Todos los campos obligatorios deben estar llenos.')
            categorias = Categoria.objects.all()
            horarios = Horario.objects.all()
            return render(request, 'crear_evento/formulario_crear_evento.html', {
                'categorias': categorias,
                'horarios': horarios,
            })

        # Convierte las fechas recibidas desde el formulario
        # al formato Date utilizado por Django
        fecha_inicio = datetime.strptime(request.POST.get('fecha_inicio'), '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(request.POST.get('fecha_fin'), '%Y-%m-%d').date()

        # Verifica que la fecha final no sea menor
        # a la fecha inicial
        if fecha_fin < fecha_inicio:
            messages.error(request, 'La fecha de fin no puede ser menor a la fecha de inicio.')
            categorias = Categoria.objects.all()
            horarios = Horario.objects.all()
            return render(request, 'crear_evento/formulario_crear_evento.html', {
                'categorias': categorias,
                'horarios': horarios,
            })

        # Crea el nuevo evento utilizando la información
        # proporcionada por el promotor
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

        #Obtiene los horarios seleccionados en el formulario
        horarios_seleccionados = request.POST.getlist('horarios')
        if horarios_seleccionados:
            evento.horario.set(horarios_seleccionados)

        return redirect('inicio:index')

    # Obtiene la información necesaria
    # para renderizar el formulario
    categorias = Categoria.objects.all()
    horarios = Horario.objects.all()
    return render(request, 'crear_evento/formulario_crear_evento.html', {
        'categorias': categorias,
        'horarios': horarios,
    })