from django.shortcuts import render, redirect, get_object_or_404
from .forms import FriendForm, DiaryForm
from .models import Personality, Diary
# 캘린더 관련
from datetime import date
import calendar

# 테스트용 코드
from django.http import HttpResponse

#반려동물과 반려식물 중에 선택 처리하는 view
def pet_or_plant(request):
    return render(request, 'diaries/pet_or_plant.html')
# html에 캘린더를 보내주는 view
def calendar_view(request, year = None, month = None):
    today = date.today()

    # URL에서 연도와 월을 받아오지 않았을 때, 오늘 날짜로 설정
    year_range = list(range(2020, 2031))
    month_range = list(range(1, 13))
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    # 해당 월의 1일과 마지막 날짜 가져오기
    first_day, num_days = calendar.monthrange(year, month)
    first_date = date(year, month, 1)
    last_date = date(year, month, num_days)
    # 해당 월의 일자를 리스트 형태로 클라이언트에게 전달
    days = list(range(1, num_days + 1))

    # 해당 월의 모든 일기 조회(first_date와 last_date 사이의 정보를 가지고 오도록 구현)
    diaries = Diary.objects.filter(date__range = (first_date, last_date))

    # 날짜별 일기 매핑
    diary_map = {diary.date.day: diary for diary in diaries}

    context = {
        "year_range": year_range,
        "month_range": month_range,
        "year": year,
        "month": month,
        "today": today,
        "first_day": first_day,
        "days": days,
        "diary_map": diary_map,
    }
    return render(request, "diaries/calendar.html", context)

# 캘린더에서 날짜 클릭 시 해당 날짜에 해당하는 일기로 이동하도록 하는 로직
# 오늘 날짜 클릭 => friend_create.html로 이동
# 다른 날짜 클릭 => diaries_detail.html로 이동
def diary_view(request, year, month, day):
    selected_date = date(year, month, day)
    diary = Diary.objects.filter(date__date = selected_date).first() # date__date를 이용해 날짜만 비교하도록 함

    if selected_date == date.today():
        if diary: # 오늘 날짜에 일기가 있을 경우
            return redirect("diaries:diaries_detail", pk = diary.pk)
        else: # 오늘 날짜에 일기가 없을 경우
            return redirect("diaries:diary_view")  # 오늘 날짜로 리디렉션 # 오늘 날짜 -> 일기 작성 페이지
    elif diary:
        return redirect("diaries:diaries_detail", pk = diary.pk) # 해당 날짜 일기 O -> 상세 페이지
    else:
        return HttpResponse('test: 해당 날짜 일기 없음') # 해당 날짜에 일기가 없다는 것을 지정

def main(request):
    return render(request, 'users/main.html')

def friend_create(request):
    if request.method == 'POST':
        # request가 POST일 때, 이미지와 텍스트를 저장
        print("🔹 원본 POST 데이터:", request.POST)

        # POST 데이터 복사해서 수정 가능하게 변환
        post_data = request.POST.copy()

        # "1,3,4" → ["1", "3", "4"] 변환
        selected_personalities = post_data.get("personal", "").split(",")
        selected_personalities = [int(pid) for pid in selected_personalities if pid.isdigit()]
        print("🔹 변환된 personal ID 리스트:", selected_personalities)

        # 수정된 데이터 QueryDict에 반영
        post_data.setlist("personal", selected_personalities) # Django 폼이 올바르게 인식하도록 수정

        # 수정된 post_data를 사용해 폼 생성
        form = FriendForm(post_data, request.FILES)
        if form.is_valid():
            friend = form.save(commit=False)
            friend.user = request.user # 현재 로그인한 사용자를 user 필드에 저장
            friend.save()
            
            # ManyToManyField 자동 저장
            form.save_m2m()

            return redirect('diaries:calendar_view')
        else:
            print("Personality 테이블 내용: ", Personality.objects.all()) # 테이블 내용 출력
            print("폼 에러:", form.errors)  # ✅ 폼 오류 확인
            print("POST 데이터:", request.POST)  # ✅ POST 데이터 확인
            print(form.errors) # 어떤 오류가 발생했는지 출력
            context = {
              'form': form,
            }
            return render(request, 'diaries/calendar.html', context) 
    else:
        # GET 요청일 때 작성 form을 출력
        form = FriendForm()

        context = {
          'form': form,
        }

        return render(request, 'diaries/friend_create.html', context)
    
# 일기 상세 페이지
def diaries_detail(request, pk):
    diaries = get_object_or_404(Diary, id=pk)

    if diaries.user == request.user:
        content = {
            'diaries': diaries,
        }
        return render(request, 'diaries/diaries_detail.html', content)
    else:
        # 사용자가 다를 경우 에러 메시지 출력
        return HttpResponse('사용자가 다릅니다.')
    
# 일기 생성/업데이트
def diaries_form(request, pk):
    if request.method == 'POST':
        diaries = get_object_or_404(Diary, id=pk)
        form = DiaryForm(request.POST, request.FILES, instance=diaries)
        if form.is_valid():
            diaries = form.save(commit=False)
            diaries.user = request.user
            diaries.save()
            return redirect('users:main')
        else:
            print("Diary 테이블 내용: ", Diary.objects.all())
    else:
        form = DiaryForm()
        content = {
            'form': form,
        }
        return render(request, 'diaries/diaries_form.html', content)

# 일기 삭제
def diaries_delete(request, pk):
    diaries = get_object_or_404(Diary, id=pk)

    if diaries:
        if diaries.user == request.user:
            diaries.delete()
            return redirect('users:main')
        else:
            return HttpResponse('사용자가 다릅니다.')
    else:
        return HttpResponse('해당 일기가 없습니다.')