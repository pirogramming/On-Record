from django.shortcuts import render

# 테스트용 코드
from django.http import HttpResponse

def test(request):
  return HttpResponse('test')

def friend_create(request):
  return render(request, 'diaries/friend_create.html')