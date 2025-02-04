from django.urls import path
from .views import *

app_name = 'diaries'

urlpatterns = [
    path('', test, name='test'), # 수정 필요
    path('friend_create/', friend_create, name='friend_create'), 
]