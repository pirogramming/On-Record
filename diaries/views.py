from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from .forms import PetForm, PlantForm, DiaryForm
from .models import User, Personality, Diary, Pet, Plant
from replies.models import Reply
from django.views.decorators.csrf import csrf_exempt
import json

# 캘린더 관련
from datetime import date
import calendar
from replies.views import create_response
# 테스트용 코드
from django.http import HttpResponse

from datetime import datetime

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

            return redirect('diaries:view_calendar')
        else:
            print("폼 에러:", form.errors)  # ✅ 폼 오류 확인
            print("POST 데이터:", request.POST)  # ✅ POST 데이터 확인
            print(form.errors) # 어떤 오류가 발생했는지 출력
            context = {
              'form': form,
            }
            return render(request, 'diaries/view_calendar.html', context) 
    else:
        # GET 요청일 때 작성 form을 출력
        form = PlantForm()

        context = {
          'form': form,
        }

        return render(request, 'diaries/create_plant.html', context)

from collections import defaultdict

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

    user = request.user

    if user.is_authenticated:
        # 반려 동물과 반려 식물 개수를 합산
        total_friends = Pet.objects.filter(user=user).count() + Plant.objects.filter(user=user).count()
        # 로그인한 유저의 Diary만 가져옴
        diaries = Diary.objects.filter(user=user, date__range=(first_date, last_date))
        pets = Pet.objects.filter(user=user)
        plants = Plant.objects.filter(user=user)
        friends = list(pets) + list(plants)
    else:
        total_friends = 0
        diaries = Diary.objects.none()

    # 날짜별 일기 매핑
    diary_map = defaultdict(int)

    for diary in diaries:
        if diary.date: # 날짜가 있는 경우
            diary_map[diary.date.day] += 1 # 해당 날짜에 쓴 일기 개수 증가

    diary_ratios = {}
    if total_friends > 0:
        for day, count in diary_map.items():
            diary_ratios[day] = count / total_friends
    
    friend_total_diary_count = {}

    for friend in friends:
        # 전체 일기 개수 가져오기
        if isinstance(friend, Pet):
            total_count = Diary.objects.filter(user=user, pet=friend).count()
        elif isinstance(friend, Plant):
            total_count = Diary.objects.filter(user=user, plant=friend).count()
        else:
            total_count = 0
        
        friend_total_diary_count[friend.id] = total_count

    context = {
        "year_range": year_range,
        "month_range": month_range,
        "year": year,
        "month": month,
        "today": today,
        "first_day": first_day + 1,
        "days": days,
        "diary_map": diary_map, # 날짜별 작성된 일기 개수
        "total_friends": total_friends, # 반려친구 총 수
        "diary_ratios": diary_ratios, # 날짜별 작성된 일기 비율
        "friends": friends, # 반려친구 목록
        "friend_total_diary_count": friend_total_diary_count, # 반려친구별 전체 일기 개수
    }


    return render(request, "diaries/view_calendar.html", context)

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

from django.shortcuts import render
from .forms import DiaryForm
from datetime import date
from communities.models import Like,Comment


#다이어리 쓰는 화면 렌더링
def render_diaries(request):
    form = DiaryForm(user=request.user)

    # GET 파라미터에서 날짜 정보 가져오기
    day = int(request.GET.get('day'))
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))

    selected_date = date(year, month, day)

    context = {
        'form': form,
        'selected_date': selected_date,
    }
    return render(request, 'diaries/create_diaries.html', context)

# 다이어리 db에 생성하는 함수 즉, 완료버튼 누르면 실행되는 함수
def create_diaries(request): #다이어리를 db에 생성하는 함수. post 요청으로 day,month,year를 넘겨줘야 함, 현재는 생성 시간은 지금 시간으로
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['date'] = datetime(
            year=int(request.GET.get('year')),
            month=int(request.GET.get('month')),
            day=int(request.GET.get('day'))
        ).date()
        form = DiaryForm(post_data, request.FILES, user=request.user)
        if form.is_valid():
            diaries = form.save(commit=False) # Diary 객체 생성(저장 x)

            friends_value = form.cleaned_data['friends']  # 선택한 반려친구 정보 가져오기
            if friends_value.startswith('pet-'):
                diaries.pet = Pet.objects.get(id=int(friends_value.split('-')[1]))
                diaries.plant = None  # Plant 필드는 None으로 설정
            elif friends_value.startswith('plant-'):
                diaries.plant = Plant.objects.get(id=int(friends_value.split('-')[1]))
                diaries.pet = None  # Pet 필드는 None으로 설정

            diaries.user = request.user  # 현재 사용자를 연결

            diaries.save()  # 새로운 Diary 저장
            # 저장된 Diary의 pk로 Reply 생성
            create_response(diaries.pk)

            return redirect('diaries:detail_diaries', pk=diaries.pk)
        else: 
            print(form.errors)
            return redirect('diaries:view_calendar')
        
    else:
        form = DiaryForm(user=request.user)

        # GET 파라미터에서 날짜 정보 가져오기
        day = int(request.GET.get('day'))
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))

        selected_date = date(year, month, day)

        context = {
            'form': form,
            'selected_date': selected_date,
        }
        return render(request, 'diaries/create_diaries.html', context)

# 일기 생성 페이지에서 공개여부 버튼 클릭시 공개/비공개 여부를 처리하는 로직
@csrf_exempt  # CSRF 토큰을 검사하지 않도록 설정 (AJAX 요청에서는 필요)
def toggle_disclosure(request, diary_id):
    if request.method == "POST":
        try:
            diary = Diary.objects.get(id=diary_id, user=request.user)  # 현재 로그인한 사용자의 데이터만 변경 가능
            data = json.loads(request.body)
            diary.disclosure = data.get("disclosure", diary.disclosure)
            diary.save()

            return JsonResponse({"success": True, "disclosure": diary.disclosure})
        except Diary.DoesNotExist:
            return JsonResponse({"success": False, "error": "이 일기의 소유자가 아닙니다."}, status=404)
    return JsonResponse({"success": False, "error": "잘못된 요청 방식입니다."}, status=400)

#06 다이어리 상세페이지
from django.db.models import Case, When, BooleanField

def detail_diaries(request, pk):
    diaries = get_object_or_404(Diary, id=pk)
    likes_count = Like.objects.filter(diary=diaries).count()

    # 댓글에 is_author 정보 추가
    comments = Comment.objects.filter(diary=diaries).select_related('comment_user').annotate(
        is_author=Case(
            When(comment_user=request.user, then=True),
            default=False,
            output_field=BooleanField()
        )
    ).values('id', 'content', 'comment_user__nickname', 'is_author')

    is_author = False
    if diaries.user == request.user:
        is_author = True
    request_user_like = Like.objects.filter(
        diary=diaries,
        like_user=request.user
    )
    if request_user_like.exists():
        is_liked = True
    else:
        is_liked = False

    context = {
        'diaries': diaries,
        'reply': diaries.reply,
        'likes_count': likes_count,
        'comments': comments,

        'is_author': is_author,
        'is_liked' : is_liked
    }
    return render(request, 'diaries/detail_diaries.html', context)

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
    context = {
            'diaries': diaries,
            'reply' : diaries.reply
        }
    return render(request, 'diaries/diaries_detail.html', context)

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

#09 다이어리 수정
def update_diaries(request, pk):
    diaries = get_object_or_404(Diary, id=pk)  # 기존 다이어리 가져오기

    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES, instance=diaries, user=request.user)  
        
        if form.is_valid():
            diaries = form.save(commit=False)  # Diary 객체 생성(저장 X)

            # ✅ 선택한 반려친구 정보 가져오기
            friends_value = request.POST.get('friends', None)  # form.cleaned_data 대신 request.POST 사용
            if friends_value:
                if friends_value.startswith('pet-'):
                    diaries.pet = get_object_or_404(Pet, id=int(friends_value.split('-')[1]), user=request.user)
                    diaries.plant = None  # Plant 필드는 None으로 설정
                elif friends_value.startswith('plant-'):
                    diaries.plant = get_object_or_404(Plant, id=int(friends_value.split('-')[1]), user=request.user)
                    diaries.pet = None  # Pet 필드는 None으로 설정

            diaries.user = request.user  # 현재 사용자를 연결

            # ✅ 기존 date 값 유지 or 새로운 값 적용
            date_value = request.POST.get('date', diaries.date)
            if date_value:
                diaries.date = datetime.strptime(date_value, "%Y-%m-%d").date()

            diaries.save()  # 다이어리 저장

            # ✅ 기존 Reply가 있는지 확인하고, 있으면 업데이트
            try:
                existing_reply = diaries.reply  # ✅ 기존 답장 가져오기 (OneToOneField 역참조)
                existing_reply.delete()  # ✅ 기존 답장 삭제
            except Reply.DoesNotExist:
                pass  # ✅ 답장이 없으면 그냥 넘어감

            # ✅ 새로운 답장 생성
            create_response(diaries.pk)

            return redirect('diaries:detail_diaries', pk=diaries.pk)
        else:
            print(form.errors)  # ❗ 폼이 유효하지 않은 경우 에러 출력
    else:
        form = DiaryForm(instance=diaries, user=request.user)

    context = {
        'form': form,
        'diaries': diaries,
    }
    return render(request, 'diaries/update_diaries.html', context)

def main(request):
    return render(request, 'users/main.html')

#마이페이지    
def mypage(request, pk):
    user = User.objects.get(id=pk)
    diaries = Diary.objects.filter(user=user)
    pets = Pet.objects.filter(user=user)
    plants = Plant.objects.filter(user=user)

    friends = list(pets) + list(plants)

    context = {
        'user': user,
        'diaries': diaries,
        'pets': pets,
        'plants': plants,
        'friends': friends,
    }
    return render(request, 'diaries/mypage.html', context)

#캘린더 날짜 선택시 반려친구 리스트
def friend_list(request):
    # GET 요청에서 날짜 정보 가져오기
    day = request.GET.get("day")
    month = request.GET.get("month")
    year = request.GET.get("year")

    # 날짜가 있을 경우 YYYY-MM-DD로 변환
    if day and month and year:
        selected_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    else:
        selected_date = None  # 날짜 정보가 없으면 None

    user = request.user
    pets = Pet.objects.filter(user=user)
    plants = Plant.objects.filter(user=user)
    friends = list(pets) + list(plants)

    # 전체 일기 개수
    friend_total_diary_count = {}
    # 친구별 작성된 일기 개수
    friend_diary_count ={}
    # 일기 pk 저장용
    friend_diary_pk = {}

    for friend in friends:
        # 전체 일기 개수 가져오기
        if isinstance(friend, Pet):
            total_count = Diary.objects.filter(user=user, pet=friend).count()
        elif isinstance(friend, Plant):
            total_count = Diary.objects.filter(user=user, plant=friend).count()
        else:
            total_count = 0
        
        friend_total_diary_count[friend.id] = total_count

    # 선택한 날짜에 작성된 일기 개수 가져오기
    if selected_date:
        for friend in friends:
            if isinstance(friend, Pet):
                diary = Diary.objects.filter(user=user, pet=friend, date=selected_date).first()
            elif isinstance(friend, Plant):
                diary = Diary.objects.filter(user=user, plant=friend, date=selected_date).first()
            else:
                diary = None
            
            friend_diary_count[friend.id] = Diary.objects.filter(
                user=user,
                pet=friend if isinstance(friend, Pet) else None,
                plant=friend if isinstance(friend, Plant) else None,
                date=selected_date
            ).count()

            if diary:
                friend_diary_pk[friend.id] = diary.pk # 해당 반려친구의 일기 pk 저장
            else:
                friend_diary_pk[friend.id] = None # 일기가 없으면 None

    context = {
        'user': user,
        'friends': friends,
        'selected_date': selected_date,
        'friend_total_diary_count': friend_total_diary_count,
        'friend_diary_count': friend_diary_count,
        'friend_diary_pk': friend_diary_pk,
    }

    return render(request, 'diaries/friend_list.html', context)

# 마이페이지 -> 반려친구 수정 시 수정페이지로 연결하는 로직
def update_pet(request, pk):
    pet = get_object_or_404(Pet, id=pk)  # ✅ 해당 ID의 Pet이 없으면 404 반환

    # ✅ GET 요청: 기존 정보가 포함된 폼을 사용자에게 보여줌
    if request.method == 'GET':
        if pet.user != request.user:
            return HttpResponseForbidden("권한이 없습니다.")  # ✅ 403 Forbidden 반환

        form = PetForm(instance=pet)  # 기존 데이터를 포함한 폼 생성

        context = {
            'form': form,
            'pet': pet,
        }
        return render(request, "diaries/update_pet.html", context)

    # ✅ POST 요청: 사용자가 수정한 정보를 저장
    elif request.method == 'POST':
        if pet.user != request.user:
            return HttpResponseForbidden("권한이 없습니다.")  # ✅ 403 Forbidden 반환

        # POST 데이터 복사해서 수정 가능하게 변환
        post_data = request.POST.copy()

        # "1,3,4" → ["1", "3", "4"] 변환
        selected_personalities = post_data.get("personal", "").split(",")
        selected_personalities = [int(pid) for pid in selected_personalities if pid.isdigit()]
        print("🔹 변환된 personal ID 리스트:", selected_personalities)

        # ✅ ManyToMany 필드 수정
        post_data.setlist("personal", selected_personalities) # Django 폼이 올바르게 인식하도록 수정

        # ✅ 기존 pet 객체를 기반으로 폼 생성 (새 객체가 아닌 기존 객체를 수정)
        form = PetForm(post_data, request.FILES, instance=pet)
        if form.is_valid():
            updated_pet = form.save(commit=False)  # ✅ DB 저장 전 수정된 pet 객체 가져오기
            updated_pet.user = request.user  # ✅ 현재 로그인한 사용자 연결
            updated_pet.save()  # ✅ 수정된 내용 저장

            # ✅ ManyToManyField 반영
            updated_pet.personal.set(Personality.objects.filter(id__in=selected_personalities))
            form.save_m2m()  # ✅ ManyToMany 관계 저장

            return redirect("diaries:mypage", request.user.id)  # ✅ 저장 후 캘린더 페이지로 이동
        else:
            print(form.errors)  # 디버깅용 에러 출력
            return render(request, "diaries/update_pet.html", {"form": form, "pet": pet})

    return HttpResponseForbidden("잘못된 요청 방식입니다.")  # ✅ GET, POST 외 다른 요청 방식을 차단

# 마이페이지 -> 반려식물 수정 시 수정페이지로 연결하는 로직    
def update_plant(request, pk):
    plant = Plant.objects.get(id=pk)
    if plant.user == request.user:
        if request.method == 'POST':
            form = PlantForm(request.POST, request.FILES, instance=plant)
            if form.is_valid():
                plant = form.save(commit=False)
                plant.user = request.user
                plant.save()
                return redirect('diaries:mypage', pk=request.user.pk)
            else:
                return HttpResponse('폼이 유효하지 않습니다.')
        else:
            form = PlantForm(instance=plant)
            context = {
                'form': form,
                'plant': plant,
            }
            return render(request, 'diaries/update_plant.html', context)
    
    else:
        return HttpResponse('권한이 없습니다.')

# 마이페이지 -> 반려동물 삭제 시 삭제페이지로 연결하는 로직    
def delete_pet(request, pk):
    if request.method == "DELETE":  # ✅ DELETE 요청만 처리
        pet = get_object_or_404(Pet, id=pk)

        # ✅ 삭제 권한 확인 (본인의 반려동물만 삭제 가능)
        if pet.user != request.user:
            return HttpResponseForbidden("권한이 없습니다.")

        pet.delete()  # ✅ DB에서 삭제
        return JsonResponse({"success": True})  # ✅ 성공 응답

    return JsonResponse({"success": False, "error": "잘못된 요청 방식입니다."}, status=400)

# 마이페이지 -> 식물 삭제 시 삭제페이지로 연결하는 로직
def delete_plant(request, pk):
    if request.method == "DELETE":  # ✅ DELETE 요청만 처리
        plant = get_object_or_404(Plant, id=pk)

        # ✅ 삭제 권한 확인 (본인의 반려동물만 삭제 가능)
        if plant.user != request.user:
            return HttpResponseForbidden("권한이 없습니다.")

        plant.delete()  # ✅ DB에서 삭제
        return JsonResponse({"success": True})  # ✅ 성공 응답

    return JsonResponse({"success": False, "error": "잘못된 요청 방식입니다."}, status=400)

from django.contrib.auth.decorators import login_required

# 반려친구에게 쓴 일기 목록
@login_required
def mydiary_list(request, friend_id):
    friend = Pet.objects.filter(id=friend_id, user=request.user).first() or \
                Plant.objects.filter(id=friend_id, user=request.user).first()

    if not friend:
        return render(request, 'diaries/mydiary_list.html', {'error': '해당 반려친구를 찾을 수 없습니다.'})

    # 반려친구가 Pet인지 Plant인지 확인 후 해당 필드로 필터링 
    if isinstance(friend, Pet):
        diaries = Diary.objects.filter(user=request.user, pet=friend).order_by('-date')
    else:
        diaries = Diary.objects.filter(user=request.user, plant=friend).order_by('-date')

    context = {
        'diaries': diaries,
        'friend_name': friend.name,
    }

    return render(request, 'diaries/mydiary_list.html', context)