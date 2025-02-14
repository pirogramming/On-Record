from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 회원가입 폼
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': '이메일을 입력하세요'}),
        required=True
    )
    nickname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '닉네임을 입력하세요'}),
        required=True
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력하세요'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 다시 입력하세요'}),
        required=True
    )
    
    class Meta:
        model = User
        
        # 회원가입 시 입력받을 필드
        fields = ['nickname', 'email', 'password1', 'password2']

# 프로필 수정 폼
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'profile_image']