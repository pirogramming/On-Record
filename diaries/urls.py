from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diaries'

urlpatterns = [
    #01 온기록 시작하기 누르면 나오는 화면 : 동물 식물 중 선택하기
    path('pet_or_plant/', pet_or_plant, name='pet_or_plant'), 

    #02 01에서 동물을 누르는 액션
    path('create_pet/', create_pet, name='create_pet'),

    #03 01에서 식물을 누르는 액션    
    path('create_plant/', create_plant, name='create_plant'),

    #04 캘린더 라우팅
    path('view_calendar/', view_calendar, name='view_calendar'),
    
    # 년 월을 받아서 calender를 업데이트하는 url 라우팅
    path('view_calendar/<int:year>/<int:month>/', view_calendar, name='calendar_view'),

    #05 다이어리 생성 페이지
    path('create_diaries/', create_diaries, name='create_diaries'),

    # 다이어리 공개 비공개 전환
    path("toggle_disclosure/<int:diary_id>/", toggle_disclosure, name="toggle_disclosure"),
    
    #06 다이어리 상세 페이지 
    path('detail_diaries/<int:pk>/', detail_diaries, name='detail_diaries'),

    #07 마이 페이지
    path('mypage/<int:pk>/', mypage, name='mypage'),

    #08 다이어리 삭제 페이지
    path('delete_diaries/<int:pk>/', delete_diaries, name='delete_diaries'),

    #09 다이어리 수정 ( views 미구현 )
    path('update_diaries/<int:pk>/', update_diaries, name='update_diaries'),

    #10 
    path('check_diaries_GET/' , check_diaries_GET , name="check_diaries_GET"),

    #11
    path('render_diaries/' , render_diaries , name="render_diaries"),

    #12 달력에서 날짜 클릭 시 friend-list 페이지로 이동
    path('friend_list/', friend_list, name='friend_list'),

    #14 마이페이지 -> 반려동물 수정 시 반려동물 수정 페이지로 이동
    path('update_pet/<int:pk>/', update_pet, name='update_pet'),

    #15 마이페이지 -> 식물 수정 시 식물 수정 페이지로 이동
    path('update_plant/<int:pk>/', update_plant, name='update_plant'),

    #16 마이페이지 -> 반려동물 삭제 시 반려동물 삭제 페이지로 이동
    path('delete_pet/<int:pk>/', delete_pet, name='delete_pet'),

    #17 마이페이지 -> 식물 삭제 시 식물 삭제 페이지로 이동
    path('delete_plant/<int:pk>/', delete_plant, name='delete_plant'),

    # path('detail_diaries_by_friend_date/<int:friend_id>/<int:selected_date>' , detail_diaries_by_friend_date , name = 'detail_diaries_by_friend_date')

    # 반려친구에게 쓴 일기 목록
    path('mydiary_list/<int:friend_id>/', mydiary_list, name='mydiary_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)