from django.db import models
from users.models import User

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="diary_images/%Y%m%d", blank=True, null=True)
    disclosure = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Personality(models.Model):
    type = models.CharField(max_length=20, unique=True) # 성격 유형(ex) 상냥한, 다정한)

    def __str__(self): # 반려친구 등록 시 보이기 위해
        return self.type

class Friend(models.Model):
    KIND_CHOICES = [
        ('dog', '강아지'),
        ('cat', '고양이'),
        ('plant', '식물'),
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
    image = models.ImageField(upload_to="friend_images/%Y%m%d", blank=True, null=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    diary_user = models.ForeignKey(User, related_name="diary_user", on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    like_user = models.ForeignKey(User, related_name="like_user", on_delete=models.CASCADE)


class Comment(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    diary_user = models.ForeignKey(User, related_name="comment_diary_user", on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, related_name="comment_user", on_delete=models.CASCADE)
    content = models.TextField()