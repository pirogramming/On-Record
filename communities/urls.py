from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import filter_diaries

app_name = 'communities'

urlpatterns = [
    path('', render_communities_main , name='render_communities_main'),
    path('toggle_like/<int:pk>/' , toggle_like , name = 'toggle_like'),
    path('add_comment/<int:pk>/' , add_comment , name = 'add_comment'),
    path('delete_comment/<int:pk>/' ,delete_comment , name = 'delete_comment'),
    path('update_comment/<int:pk>/' , update_comment , name = 'update_comment'),
    path('filter_diaries/', filter_diaries, name='filter_diaries'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)