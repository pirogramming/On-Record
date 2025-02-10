from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'communities'

urlpatterns = [
    path('', render_communities_main , name='render_communities_main'),
    path('toggle_like/<int:pk>/' , toggle_like , name = 'toggle_like'),
    path('add_comment/<int:pk>/' , add_comment , name = 'add_comment'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)