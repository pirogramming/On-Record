from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from users.models import User, EmailVerification
from diaries.models import Pet, Plant
from users.forms import SignupForm, ProfileForm
from django.http import JsonResponse
from .utils import get_kakao_token, get_kakao_user_info, encrypt_password, decrypt_password
from datetime import timedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from django.core.signing import BadSignature
from django.conf import settings
from django.urls import reverse
import requests
import uuid
import environ
env = environ.Env()

def main(request):
  return render(request, 'users/main.html')

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user_email = form.cleaned_data['email']
      nickname = form.cleaned_data['nickname']
      password = form.cleaned_data['password1']

      # 인증 토큰 초기화
      EmailVerification.objects.filter(email=user_email).delete()

      # 이메일 인증 토큰 생성
      token = uuid.uuid4()
      verification = EmailVerification.objects.create(
        email=user_email,
        nickname=nickname,
        token=token,
        expires_at=now() + timedelta(minutes=5)
      )

      # 이메일 인증 링크 생성
      verification_link = request.build_absolute_uri(reverse('users:verify_email', args=[token]))

      # 이메일 전송
      send_mail(
        subject='온기록 회원가입을 위한 이메일 인증 요청',
        message=f'아래 링크를 클릭하여 이메일 인증을 완료하세요:\n{verification_link}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
      )

      encrypted_password = encrypt_password(password)

      response = render(request, 'users/signup_pending.html', {'email': user_email})
      response.set_signed_cookie('password1', encrypted_password, salt='secure_salt', max_age=300, httponly=True)  # 5분 동안 유지
      return response

    return render(request, 'users/signup.html', {'form': form})

  else: # GET 요청
    form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def verify_email(request, token):
  try:
    verification = EmailVerification.objects.get(token=token, expires_at__gte=now())

    try:
      encrypted_password = request.get_signed_cookie('password1', salt='secure_salt')
      password = decrypt_password(encrypted_password) # 복호화
    except (KeyError, BadSignature):
      return render(request, 'users/verification_failed.html', {'error': '비밀번호 정보가 만료되었습니다. 다시 회원가입을 진행해주세요.'})
    
    user = User.objects.create(
      email=verification.email,
      nickname=verification.nickname,
    )

    user.set_password(password)
    user.is_active = True
    user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)
    
    verification.delete() # 인증 완료 후 토큰 삭제
    return redirect('users:main')
  except EmailVerification.DoesNotExist:
    return render(request, 'users/verification_failed.html')

def user_login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      user = form.get_user()
      auth.login(request, user)
    
      has_pet = Pet.objects.filter(user=user).exists()      
      has_plant = Plant.objects.filter(user=user).exists()

      if has_pet or has_plant:
        return redirect('diaries:view_calendar')
      else:
        return redirect('users:main')
      
    else:
      context = {
        'form': form,
      }
      return render(request, template_name='users/login.html', context=context)
  else:
    form = AuthenticationForm()
    context = {
      'form': form,
    }
    return render(request, template_name='users/login.html', context=context)

def logout(request):
  auth.logout(request)

  # 카카오 로그아웃 API 호출
  access_token = request.session.get('kakao_access_token')
  if access_token:
    kakao_logout(access_token)
    request.session.pop('kakao_access_token', None)

  return redirect('users:main')

def kakao_callback(request):
  code = request.GET.get('code') # 카카오에서 리다이렉션 시 전달된 'code' 파라미터
  if code:
    try:
      access_token, refresh_token = get_kakao_token(code)
      user_info = get_kakao_user_info(access_token)

      nickname = user_info.get('properties', {}).get('nickname', 'Unknown')
      email = user_info.get('kakao_account', {}).get('email', None)
      profile_image = user_info.get('properties', {}).get('profile_image', None)

      user, created = User.objects.get_or_create(nickname=nickname)
      user.nickname = nickname
      user.email = email
      user.profile_image = profile_image

      if created:
        user.nickname = nickname
        user.email = email
        user.profile_image = profile_image
        user.save()
      else:
        user.save()

      user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
      auth.login(request, user)
      return redirect('users:main')
    except Exception as e:
      return JsonResponse({'error': str(e)}, status=400)
  else:
    return JsonResponse({'error': 'Invalid code'}, status=400)

def naver_login(request):
  client_id = env('NAVER_CLIENT_ID')
  redirect_uri = env('NAVER_REDIRECT_URI')
  naver_auth_url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state=STATE_STRING"
  return redirect(naver_auth_url)

def kakao_login(request):
  client_id = env('KAKAO_CLIENT_ID')
  redirect_uri = env('KAKAO_REDIRECT_URI')
  kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&prompt=login"
  return redirect(kakao_auth_url)

def kakao_logout(access_token):
  logout_url = "https://kapi.kakao.com/v1/user/logout"
  headers = {
    "Authorization": f"Bearer {access_token}"
  }
  response = requests.post(logout_url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Failed to logout: {response.json()}")
    return None
  
# 프로필 수정 페이지 렌더링 로직(마이페이지 -> 프로필 수정 버튼 클릭 시 실행)
def render_profile(request):
    user = request.user
    form = ProfileForm(instance=user)
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'users/update_profile.html', context) # 프로필 수정 페이지 렌더링(html 경로 수정 필요)

# 프로필 수정 로직(마이페이지 -> 프로필 수정 form에서 '완료' 버튼 클릭 시 실행)
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid(): # 폼 유효성 검사
            form.save()
            return redirect('diaries:mypage', pk=user.pk)
        return redirect('diaries:mypage', pk=user.pk)
    else:
      return redirect('diaries:mypage', pk=user.pk) # 프로필 수정 페이지 렌더링(html 경로 수정 필요)

@login_required
def delete_user(request):
  user = request.user

  if request.method == 'POST':
    user.delete()
    auth.logout(request)

    return redirect('users:main')

  return render(request, 'users/delete_confirm.html')