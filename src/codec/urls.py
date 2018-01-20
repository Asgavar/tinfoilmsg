from django.urls import path

from . import views

app_name = 'codec'

urlpatterns = [
    path('', views.index, name='index'),
    path('encode/', views.encode, name='encode'),
    path('decode/', views.decode, name='decode'),
]
