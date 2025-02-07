from django.shortcuts import render, redirect, get_object_or_404
from .forms import PetForm, PlantForm, DiaryForm
from .models import User, Personality, Diary, Pet, Plant

# 캘린더 관련
from datetime import date
import calendar
from replies.views import create_response
# 테스트용 코드
from django.http import HttpResponse


from datetime import datetime, time
from django.utils import timezone


#01 반려동물과 반려식물 중에 선택 처리하는 view
def pet_or_plant(request):
    return render(request, 'diaries/pet_or_plant.html')

#02 반려동물 생성하는 view
def create_pet(request):
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
        form = PetForm(post_data, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user # 현재 로그인한 사용자를 user 필드에 저장
            pet.save()
            
            # ManyToManyField 자동 저장
            form.save_m2m()

            return redirect('diaries:view_calendar')
        else:
            print("Personality 테이블 내용: ", Personality.objects.all()) # 테이블 내용 출력
            print("폼 에러:", form.errors)  # ✅ 폼 오류 확인
            print("POST 데이터:", request.POST)  # ✅ POST 데이터 확인
            print(form.errors) # 어떤 오류가 발생했는지 출력
            context = {
              'form': form,
            }
            return render(request, 'diaries/view_calendar.html', context) 
    else:
        # GET 요청일 때 작성 form을 출력
        form = PetForm()

        context = {
          'form': form,
        }

        return render(request, 'diaries/create_pet.html', context)

#03 반려식물 생성하는 view
def create_plant(request):
    if request.method == 'POST':
        # request가 POST일 때, 이미지와 텍스트를 저장
        print("🔹 원본 POST 데이터:", request.POST)

        # POST 데이터 복사해서 수정 가능하게 변환
        post_data = request.POST.copy()

        # 수정된 post_data를 사용해 폼 생성
        form = PlantForm(post_data, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user # 현재 로그인한 사용자를 user 필드에 저장
            plant.save()
            
            # ManyToManyField 자동 저장
            form.save_m2m()

            return redirect('diaries:calendar')
        else:
            print("폼 에러:", form.errors)  # ✅ 폼 오류 확인
            print("POST 데이터:", request.POST)  # ✅ POST 데이터 확인
            print(form.errors) # 어떤 오류가 발생했는지 출력
            context = {
              'form': form,
            }
            return render(request, 'diaries/calendar.html', context) 
    else:
        # GET 요청일 때 작성 form을 출력
        form = PlantForm()

        context = {
          'form': form,
        }

        return render(request, 'diaries/create_plant.html', context)

#04 큰 캘린더 보여주는 페이지 -> urls에 이름 두개인거 왜그런지?
def view_calendar(request, year = None, month = None):
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

#05 
from datetime import date
from django.shortcuts import render
from .models import Pet, Diary
# 05 -1 : 캘린더에서 날짜를 선택했을 경우
def check_diaries_GET(request):
    request_day = int(request.GET.get('day'))
    request_month = int(request.GET.get('month'))
    request_year = int(request.GET.get('year'))
    selected_date = date(request_year, request_month, request_day)

    # 현재 사용자에게 연결된 모든 친구 목록 가져오기
    pets = Pet.objects.filter(user=request.user)

    # 각 친구에 대해 다이어리 작성 여부 체크
    pets_with_status = []
    for pet in pets:
        has_diary = check_already_written(selected_date, request.user, pet)
    
        pets_with_status.append({
            'pet': pet,
            'has_diary': has_diary,
        })

    return render(request, 'diaries/daily_list.html', {
        'selected_date': selected_date,
        'pets_with_status': pets_with_status,
    })

from django.core.exceptions import ObjectDoesNotExist  # 예외 처리용
#05-2 중복 검사
def check_already_written(date , user , pet):
    return Diary.objects.filter(
            date=date,
            user=user,
            pet = pet,
        ).exists()

from datetime import date
from django.shortcuts import render
from .forms import DiaryForm
from datetime import date
from django.shortcuts import render
from .forms import DiaryForm
#다이어리 쓰는 화면 렌더링
def write_diaries(request):
    form = DiaryForm()

    # GET 파라미터에서 날짜 정보 가져오기
    day = int(request.GET.get('day'))
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))

    # 날짜 객체 생성
    selected_date = date(year, month, day)

    content = {
        'form': form,
        'selected_date': selected_date
    }
    return render(request, 'diaries/write_diaries.html', content)

# 다이어리 db에 생성하는 함수 즉, 완료버튼 누르면 실행되는 함수
def create_diaries(request): #다이어리를 db에 생성하는 함수post 요청으로 day,month,year를 넘겨줘야함, 현재는 생성 시간은 지금 시간으로로
    if request.method == 'POST':
        
        post_data = request.POST.copy()
        post_data['date'] = datetime(
            year=int(request.GET.get('year')),
            month=int(request.GET.get('month')),
            day=int(request.GET.get('day'))
        ).date()

        form = DiaryForm(post_data, request.FILES)

        if form.is_valid():
            diaries = form.save(commit=False)
            diaries.user = request.user  # 현재 사용자를 연결
            
            diaries.save()  # 새로운 Diary 저장

            # 저장된 Diary의 pk로 Reply 생성
            create_response(diaries.pk)

            return redirect('diaries:detail_diaries', pk=diaries.pk)

        else: 
            print(form.errors)
            return redirect('diaries:view_calendar')









#06 다이어리 상세페이지
def detail_diaries(request, pk):
    diaries = get_object_or_404(Diary, id=pk)

    if diaries.user == request.user:
        content = {
            'diaries': diaries,
            'reply' : diaries.reply
        }
        return render(request, 'diaries/diaries_detail.html', content)
    else:
        # 사용자가 다를 경우 에러 메시지 출력
        return HttpResponse('사용자가 다릅니다.')

def detail_diaries_by_pet_date(request , pet_id , selected_date):
    user = request.user
    date_str = str(selected_date)
    date = datetime.strptime(date_str , "%Y%m%d").date()
    pet = Pet.objects.get(id = pet_id)
    
    diaries = Diary.objects.get(
        user = user,
        pet = pet,
        date = date
    )
    content = {
            'diaries': diaries,
            'reply' : diaries.reply
        }
    return render(request, 'diaries/diaries_detail.html', content)

#07 마이페이지    
def mypage(request, pk):
    user = User.objects.get(id=pk)
    diaries = Diary.objects.filter(user=user)
    context = {
        'user': user,
        'diaries': diaries,
    }
    return render(request, 'diaries/mypage.html', context)

#08 다이어리 삭제
def delete_diaries(request, pk):
    diaries = get_object_or_404(Diary, id=pk)

    if diaries:
        if diaries.user == request.user:
            diaries.delete()
            return redirect('users:main')
        else:
            return HttpResponse('사용자가 다릅니다.')
    else:
        return HttpResponse('해당 일기가 없습니다.')

#09 다이어리 수정(미구현현)
def update_diaries(request, pk):
    pass

def main(request):
    return render(request, 'users/main.html')

#마이페이지    
def mypage_view(request, pk):
    user = User.objects.get(id=pk)
    diaries = Diary.objects.filter(user=user)
    pets = Pet.objects.filter(user=user)
    plants = Plant.objects.filter(user=user)

    combined_list = list(pets) + list(plants)

    context = {
        'user': user,
        'diaries': diaries,
        'pets': pets,
        'plants': plants,
        'combined_list': combined_list,
    }
    return render(request, 'diaries/mypage.html', context)