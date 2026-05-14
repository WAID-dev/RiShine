from django.shortcuts import render


def index(request):
    return render(request, 'crear_evento/formulario_crear_evento.html')






