from django.urls import path
from .views import *

app_name = 'diaries'

urlpatterns = [
    path('', test, name='test'), # 수정 필요
]