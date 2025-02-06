from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diaries'

urlpatterns = [
    #01 온기록 시작하기 누르면 나오는 화면 : 동물 식물 중 선택하기
    path('pet_or_plant', pet_or_plant, name='pet_or_plant'), 

    #02 01에서 동물을 누르는 액션
    path('friend_create/', friend_create, name='friend_create'),

    #03 01에서 식물을 누르는 액션    
    path('plant_create/', plant_create, name='plant_create'),

    #04 캘린더 라우팅
    path('calendar/', calendar_view, name='calendar_view'),

    #05 다이어리 작성 페이지
    path('diary/<int:year>/<int:month>/<int:day>/', diary_view, name='diary_view'),

    #06 다이어리 상세 페이지 
    path('diaries_detail/<int:pk>', diaries_detail, name='diaries_detail'),


    # path('calendar/<int:year>/<int:month>', calendar_view, name='calendar_view'),
    # # 날짜와 월을 받았을 때 calender를 업데이트하는 url 라우팅


    path('diaries_create', diaries_form, name='diaries_form'),
    # 일기 생성 페이지

    # 일기 수정 페이지
    path('diaries_update/<int:pk>', diaries_update, name='diaries_update'),

    # 일기 삭제 페이지
    path('diaries_delete/<int:pk>', diaries_delete, name='diaries_delete'),
    # 다이어리 상세 내용을 가져오는 url 라우팅

    
    # 다이어리 상세 내용 불러옴
    path('mypage/<int:pk>', mypage_view, name='mypage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
