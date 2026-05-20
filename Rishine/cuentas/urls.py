from django.urls import path

from . import views

app_name = 'cuentas'

urlpatterns = [
    path('registro/', views.crear_cuenta, name='registro'),
    path('login/', views.inicio_sesion, name='login'),
    path('promotor/', views.crear_cuenta_promotor, name='promotor'),
]
