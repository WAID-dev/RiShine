from django.shortcuts import render


def index(request):
    return render(request, 'ver_evento/index.html')
