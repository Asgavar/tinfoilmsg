from django.contrib import admin
from django.urls import path
from django.urls import include

from django.contrib.auth import views as auth_views
from codec import views as codec_views
from core import views as core_views

urlpatterns = [
    path('', codec_views.index),
    path('admin/', admin.site.urls),
    path('signup/', core_views.signup),
    path('login/', auth_views.login, {'template_name': 'login.html'}),
    path('encode/', codec_views.encode),
    path('decode/', codec_views.decode),
]
