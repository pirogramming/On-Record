from django.shortcuts import render, redirect
from .forms import FriendForm
from .models import Personality

# 테스트용 코드
from django.http import HttpResponse

def test(request):
  return HttpResponse('test')

def main(request):
  return render(request, 'users/main.html')

def mypage(request):
  return render(request, 'diaries/mypage.html')

def community(request):
  return render(request, 'diaries/community.html')

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

      return redirect('users:main')
    else:
      print("Personality 테이블 내용: ", Personality.objects.all()) # 테이블 내용 출력
      print("폼 에러:", form.errors)  # ✅ 폼 오류 확인
      print("POST 데이터:", request.POST)  # ✅ POST 데이터 확인
      print(form.errors) # 어떤 오류가 발생했는지 출력
      context = {
        'form': form,
      }
      return render(request, 'users/main.html', context)
  else:
    # GET 요청일 때 작성 form을 출력
    form = FriendForm()

    context = {
      'form': form,
    }

    return render(request, 'diaries/friend_create.html', context)