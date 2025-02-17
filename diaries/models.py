from django.db import models
from users.models import User
import os
import uuid
from django.utils.deconstruct import deconstructible
from django.utils import timezone

# 파일 업로드 시 파일명을 랜덤한 UUID로 변경
@deconstructible
class UploadToUniqueFilename:
    def __init__(self, subdir):
        self.subdir = subdir

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]  # 파일 확장자 가져오기
        filename = f"{uuid.uuid4().hex}.{ext}"  # UUID를 파일명으로 사용
        return os.path.join(self.subdir, filename)


class Personality(models.Model):
    type = models.CharField(max_length=20, unique=True) # 성격 유형(ex) 상냥한, 다정한)

    def __str__(self): # 반려친구 등록 시 보이기 위해
        return self.type


class Pet(models.Model):
    KIND_CHOICES = [
        ('dog', '강아지'),
        ('cat', '고양이'),
        ('bird', '새'),
        ('rabbit', '토끼'),
        ('fish', '물고기'),
        ('hamster', '햄스터'),
        ('turtle', '거북이'),
        ('etc', '기타'),
    ]

    GENDER_CHOICES = [
        ('male', '남'),
        ('female', '여'),
        ('unknown', '없음'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default='dog')
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    personal = models.ManyToManyField(Personality, blank=True) # 여러 개의 성격 선택 가능
    image = models.ImageField(upload_to="pet_images/%Y%m%d", blank=True, null=True)
    pet_fav = models.CharField(max_length=50, blank=False, null=False)
    pet_hate = models.CharField(max_length=50, blank=False, null=False)
    pet_sig = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class Plant(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    image = models.ImageField(upload_to="plant_images/%Y%m%d", blank=True, null=True)
    plant_con = models.CharField(max_length=50, blank=False, null=False)
    plant_sig = models.CharField(max_length=50, blank=False, null=False)
    plant_adv = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

class Diary(models.Model):
    # 날씨
    WEATHER_CHOICES = [
        ( 'sunny', '☀️' ),
        ( 'windy', '💨' ),
        ( 'cloudy', '☁️' ),
        ( 'hot', '🔥' ),
        ( 'cold', '🥶' ),
        ( 'rainy', '🌧' ),
        ( 'snowy', '❄️' ),
    ]

    # 감정
    MOOD_CHOICES = [
        ( 'happy' ,  '🥰' ),
        ( 'funny' ,  '🤣' ),
        ( 'excited', '🤩' ),
        ( 'normal', '😌' ),
        ( 'sad'   ,  '😢' ),
        ( 'angry' ,  '😡' ),
        ( 'tired' ,  '😪' ),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="diary_images/%Y%m%d", blank=True, null=True)
    disclosure = models.BooleanField(default=True) # 공개 여부
    date = models.DateField(blank=True, null=True) # 기본 값을 현재 시간으로 설정
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='happy')
    weather = models.CharField(max_length=10, choices=WEATHER_CHOICES, default='sunny')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # 누구한테 쓴건지
    def __str__(self):
        return self.title


