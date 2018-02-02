from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from codec import views as codec_views
from core import views as core_views

from . import settings

urlpatterns = [
    path('', core_views.index),
    path('admin/', admin.site.urls),
    path('signup/', core_views.signup),
    path('login/', auth_views.login, {'template_name': 'login.html'}),
    path('logout/', core_views.logout_view),
    path('encode/', codec_views.encode),
    path('decode/', codec_views.decode),
    path('my_algorithms/', codec_views.my_algorithms),
    path('algorithm_configuration/', codec_views.algorithm_configuration),
    path('algorithm_delete/<int:algo_id>', codec_views.algorithm_delete),
    path('encode/results/', codec_views.encode_results),
    path('decode/results/', codec_views.decode_results),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
