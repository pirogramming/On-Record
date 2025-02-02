from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager # CustomUserManager import

class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(upload_to="profile_images/%Y%m%d", blank=True, null=True)

    # id를 이메일로 사용하기 위한 설정
    username = None # 기존 username 필드 제거
    email = models.EmailField(unique=True) # 이메일을 id로 사용

    USERNAME_FIELD = 'email' # 인증 id를 이메일로 변경
    REQUIRED_FIELDS = ['nickname'] # superuser 생성 시 필수 필드

    objects = CustomUserManager() # CustomUserManager를 사용하도록 설정

    def __str__(self):
        return self.nickname