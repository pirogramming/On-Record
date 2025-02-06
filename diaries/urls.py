from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diaries'

urlpatterns = [
    #01 온기록 시작하기 누르면 나오는 화면 : 동물 식물 중 선택하기
    path('pet_or_plant', pet_or_plant, name='pet_or_plant'), 

    #02 01에서 동물을 누르는 액션
    path('create_friend/', create_friend, name='create_friend'),

    #03 01에서 식물을 누르는 액션    
    path('create_plant/', create_plant, name='create_plant'),

    #04 캘린더 라우팅
    path('calendar/', calendar, name='calendar'),

    #05 다이어리 생성 페이지
    path('create_diaries', create_diaries, name='create_diaries'),
    
    #06 다이어리 상세 페이지 
    path('detail_diaries/<int:pk>', detail_diaries, name='detail_diaries'),

    #07 마이 페이지
    path('mypage/<int:pk>', mypage, name='mypage'),

    #08 다이어리 삭제 페이지
    path('delete_diaries/<int:pk>', delete_diaries, name='delete_diaries'),

    #09 다이어리 수정 ( views 미구현 )
    path('update_diaries/<int:pk>', update_diaries, name='update_diaries'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
