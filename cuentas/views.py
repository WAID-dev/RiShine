from django.shortcuts import render


def login_vista(request):
    return render(request, 'cuentas/inicio_sesion.html')


def registro_vista(request):
    return render(request, 'cuentas/crear_cuenta.html')


def registro_promotor_vista(request):
    return render(request, 'cuentas/crear_cuenta_promotor.html')
