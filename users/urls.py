from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', main, name='main'),
    path('signup/', signup, name='signup'),
    path('user_login/', user_login, name='user_login'),
    path('logout/', logout, name='logout'),
    path('accounts/kakao/login/callback/', kakao_callback, name='kakao_callback'),
    path('render_profile/<int:pk>', render_profile, name='render_profile'),
    path('update_profile/', update_profile, name='update_profile'),
]