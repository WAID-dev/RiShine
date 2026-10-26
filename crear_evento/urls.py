from django.urls import path
from . import views

app_name = 'crear_evento'

urlpatterns = [
    path('', views.crear_evento, name='crear_evento'),
]