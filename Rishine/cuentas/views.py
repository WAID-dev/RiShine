from django.shortcuts import render


def crear_cuenta(request):
    return render(request, 'cuentas/crear_cuenta.html')


def inicio_sesion(request):
    return render(request, 'cuentas/inicio_sesion.html')
