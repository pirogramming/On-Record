from django.shortcuts import render, redirect
from users.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

def main(request):
  return render(request, 'users/main.html')

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
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

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, request.POST)
    if form.is_valid():
      user = form.get_user()
      auth.login(request, user)
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
  return redirect('users:main')