from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('cerrar-sesion/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('guardados/', views.guardados, name='guardados'),
]
