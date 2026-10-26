from django.shortcuts import render

def crear_evento(request):
    return render(request, 'crear_evento/crear_evento.html')
