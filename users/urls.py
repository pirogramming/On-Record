from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', main, name='main'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('test/', test, name='test'),
]