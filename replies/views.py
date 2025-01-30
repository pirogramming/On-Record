from django.shortcuts import render

# 테스트용 코드
from django.http import HttpResponse

def test(request):
  return HttpResponse('test')