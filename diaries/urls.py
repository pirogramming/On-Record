from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diaries'

urlpatterns = [
    path('friend_create/', friend_create, name='friend_create'),
    # 기본 calender를 받아오는 url 라우팅
    path('calendar/', calendar_view, name='calendar_view'),
    # 날짜와 월을 받았을 때 calender를 업데이트하는 url 라우팅
    path('calendar/<int:year>/<int:month>', calendar_view, name='calendar_view'),
    # 일기 생성 페이지
    path('diaries_create', diaries_form, name='diaries_form'),
    # 다이어리 상세 내용을 가져오는 url 라우팅
    path('diary/<int:year>/<int:month>/<int:day>', diary_view, name='diary_view'),
    # 다이어리 상세 내용 불러옴
    path('diaries_detail/<int:pk>', diaries_detail, name='diaries_detail'),
    path('mypage/<int:pk>', mypage_view, name='mypage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
