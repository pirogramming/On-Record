from django.shortcuts import render, redirect
from users.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from users.models import User
from django.http import JsonResponse
from .utils import get_kakao_token, get_kakao_user_info
import requests
import environ
from diaries.models import Pet, Plant
env = environ.Env()

def main(request):
  return render(request, 'users/main.html')

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.backend = 'django.contrib.auth.backends.ModelBackend'
      auth.login(request, user)
      return redirect('users:main')
    else:
      return render(request, 'users/signup.html', {'form': form}) # 회원가입 에러 메시지 표시
  else:
    form = SignupForm()
    context = {
      'form': form,
    }
    return render(request, template_name='users/signup.html', context=context)

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