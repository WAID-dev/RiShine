from django.urls import path

from . import views

app_name = 'explorar'

urlpatterns = [
    path('', views.index, name='index'),
]
