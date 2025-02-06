from django.shortcuts import render, redirect, get_object_or_404
from .forms import FriendForm, PlantForm, DiaryForm
from .models import User, Personality, Diary

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
def create_friend(request):
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

            return redirect('diaries:calendar')
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

        return render(request, 'diaries/plant_create.html', context)

#04 큰 캘린더 보여주는 페이지 -> urls에 이름 두개인거 왜그런지?
def calendar(request, year = None, month = None):
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

#05 다이어리 생성
def create_diaries(request):
    today = timezone.now().date().day
    if request.method == 'POST':
        # 새로운 Diary 객체 생성 및 폼 데이터 적용
        diaries = Diary()
        form = DiaryForm(request.POST, request.FILES, instance=diaries)
        date_str = request.POST.get('date')
        selected_date = datetime.strptime(date_str , '%Y-%m-%d')

        if form.is_valid():
            diaries = form.save(commit=False)
            diaries.user = request.user  # 현재 사용자를 연결
            diaries.date = datetime(
                year = selected_date.year,
                month = selected_date.month,
                day = selected_date.day,
                hour =12,
                minute = 0,
                second = 0 
            )
            diaries.save()  # 새로운 Diary 저장

            # 저장된 Diary의 pk로 Reply 생성
            create_response(diaries.pk)
            return redirect('diaries:detail_diaries', pk=diaries.pk)
        else:
            print("Diary 테이블 내용: ", Diary.objects.all())

    else:        
        request_day = int(request.GET.get('day'))
        request_month = int(request.GET.get('month'))
        request_year = int(request.GET.get('year'))

        if request_day != today:     
            request_time = time(12,0,0)
        else :
            request_time = timezone.now().time()
        try:
            
            diary = Diary.objects.get(
                date__day = request_day,
                date__month = request_month,
                date__year = request_year,
                date__time = request_time
                ) #오늘 작성된 일기를 가져옴
            return redirect("diaries:detail_diaries", pk=diary.pk)
        except Diary.DoesNotExist:
            form = DiaryForm()
            content = {
                'form': form,
            }

            return render(request, 'diaries/diary-write.html', content)

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



#????????
def diary_view(request, year, month, day):
    selected_date = date(year, month, day)
    today = date.today()

    # 미래 날짜 클릭 시 메시지 출력
    if selected_date > today:
        return HttpResponse("아직 오지 않은 날입니다.")  

    # 해당 날짜의 일기 검색
    diary = Diary.objects.filter(date__date=selected_date).first()

    #캘린더 로직 이상함
    if selected_date == today:
        if diary: #오늘이고 다이어리가 존재한다면 -> 상세페이지로 
            return redirect("diaries:diaries_detail", pk=diary.pk)
        else: #오늘인데 다이어리가 존재하지 않는다면 -> 다이어리리 작성 페이지로
            return redirect("diaries:")  
    elif diary:
        return redirect("diaries:diaries_detail", pk=diary.pk)  # 해당 날짜 일기 O -> 상세 페이지
    else:
        return render(request, "diaries/diary_write.html", {"selected_date": selected_date})  # 일기가 없을 경우 diary_view.html 보여줌

def main(request):
    return render(request, 'users/main.html')
