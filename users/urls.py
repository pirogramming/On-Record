from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', main, name='main'),
    path('signup/', signup, name='signup'),
    path('verify_email/<uuid:token>/', verify_email, name='verify_email'),
    path('user_login/', user_login, name='user_login'),
    path('logout/', logout, name='logout'),
    path('accounts/kakao/login/callback/', kakao_callback, name='kakao_callback'),
    path('render_profile/', render_profile, name='render_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('delete_user/', delete_user, name='delete_user'),
]