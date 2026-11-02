from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def crear_evento(request):
    return render(request, 'crear_evento/crear_evento.html')
