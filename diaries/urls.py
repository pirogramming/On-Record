from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diaries'

urlpatterns = [
    path('', test, name='test'), # 수정 필요
    path('friend_create/', friend_create, name='friend_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)