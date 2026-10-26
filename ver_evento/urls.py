from django.urls import path
from . import views

app_name = 'ver_evento'

urlpatterns = [
    path('', views.ver_evento, name='ver_evento')
]