from django.shortcuts import render

# Create your views here.
def inicio(request):
    eventos_para_ti = []
    eventos_gratis = []
    eventos_200 = []
    eventos_500 = []
    return render(request, 'inicio/inicio.html', {
        'eventos_para_ti': eventos_para_ti,
        'eventos_gratis': eventos_gratis,
        'eventos_200': eventos_200,
        'eventos_500': eventos_500
    })