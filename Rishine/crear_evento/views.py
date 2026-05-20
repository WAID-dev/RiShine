from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required(login_url='/?show_login=1&next=/crear_evento/')
def index(request):
    if not hasattr(request.user, 'promotor'):
        return redirect('/?show_promotor=1&next=/crear_evento/')
    return render(request, 'crear_evento/formulario_crear_evento.html')






