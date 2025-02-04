from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 회원가입 폼
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        
        # 회원가입 시 입력받을 필드
        fields = ['nickname', 'email', 'password1', 'password2']