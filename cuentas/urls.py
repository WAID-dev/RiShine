from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('login/', views.login_vista, name='login'),
    path('registro/', views.registro_vista, name='registro'),
    path('registro/promotor/', views.registro_promotor_vista, name='registro_promotor'),
]
