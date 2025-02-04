from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', main, name='main'),
    path('signup/', signup, name='signup'),
    path('user_login/', user_login, name='user_login'),
    path('logout/', logout, name='logout'),
    path('accounts/kakao/login/callback/', kakao_callback, name='kakao_callback'),
]