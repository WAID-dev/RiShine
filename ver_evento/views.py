from django.shortcuts import render

def ver_evento(request):
    return render(request, 'ver_evento/ver_evento.html')
