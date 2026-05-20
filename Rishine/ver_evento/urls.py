from django.urls import path

from . import views

app_name = 'ver_evento'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id_evento>/', views.detalle_evento, name='detalle'),
]
