from django.urls import path

from . import views

app_name = 'crear_evento'

urlpatterns = [
    path('', views.index, name='index'),


]
